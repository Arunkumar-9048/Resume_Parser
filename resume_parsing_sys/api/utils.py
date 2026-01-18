import re
import PyPDF2
import docx
import spacy
from dateutil import parser as date_parser 

nlp = spacy.load("en_core_web_sm")

def extract_text(file):
    if file.name.endswith('.pdf'):
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"  # Keep line breaks for structure
        return text
    elif file.name.endswith('.docx'):
        doc = docx.Document(file)
        return "\n".join([p.text for p in doc.paragraphs])  # Already preserves paragraphs
    else:
        return ""

def parse_resume(text):
    data = {
        "full_name": "",
        "email": "",
        "phone": "",
        "location": "",
        "experience": "",
        "linkedin": ""
    }

    # Keep original text with line breaks for name extraction
    original_text = text
    # Flatten for other extractions
    flattened_text = original_text.replace("\n", " ").replace("\r", " ")
    flattened_text = re.sub(r'\s+', ' ', flattened_text)

    # -------------------
    # 1. Email
    email = re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', flattened_text)
    data['email'] = email[0] if email else ""

    # 2. Phone
    phone = re.findall(r'\+?\d[\d\s-]{7,}\d', flattened_text)
    data['phone'] = phone[0] if phone else ""

    # 3. LinkedIn
    linkedin = re.search(r'(https?://)?(www\.)?linkedin\.com/in/[A-Za-z0-9_-]+', flattened_text)
    data['linkedin'] = linkedin.group(0) if linkedin else ""

    # 4. SpaCy NER for Location (and later for names)
    doc = nlp(flattened_text)
    locations = [ent.text for ent in doc.ents if ent.label_ == "GPE"]
    data['location'] = locations[0] if locations else ""

    # -------------------
    # 5. Full Name Detection
    # Check first 5 lines of original text (preserves structure)
    lines = original_text.splitlines()
    for line in lines[:5]:
        clean_line = line.strip()
        # Improved heuristic: 1-4 words, no numbers, likely name-like (e.g., allow titles)
        words = clean_line.split()
        if 1 <= len(words) <= 4 and not any(word.isdigit() for word in words):
            # Optional: Strip common titles for cleaner extraction
            title_stripped = re.sub(r'^(Dr\.|Mr\.|Ms\.|Mrs\.)\s*', '', clean_line, flags=re.I)
            data['full_name'] = title_stripped.strip()
            break

    # Fallback to SpaCy PERSON entity if top lines didn't work
    if not data['full_name']:
        names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
        if names:
            data['full_name'] = names[0]

    # Convert all-caps name to title case (only if it's all caps and detected)
    if data['full_name'] and data['full_name'].isupper():
        data['full_name'] = data['full_name'].title()

    # -------------------
    # 6. Experience Extraction (Expanded)
    experience_list = []
    
    # Refined regex for duration patterns (captures full phrases like "6 months of experience")
    duration_regex = re.compile(r'\b(\d+(?:\.\d+)?\s*(?:\+)?\s*(?:years?|yrs?|months?|mos?)\s*(?:of\s*\w+)*\s*(?:in|at|with|of)?\s*\w*\s*\w*)', re.I)
    duration_matches = duration_regex.findall(flattened_text)
    # Filter out very short matches (e.g., avoid "6 months" if it's incomplete)
    duration_matches = [match.strip() for match in duration_matches if len(match.split()) >= 2]
    if duration_matches:
        experience_list.extend(duration_matches)
    
    # Regex for date ranges (unchanged, but integrated)
    date_range_regex = re.compile(r'\b(?:\d{1,2}/\d{1,2}/\d{4}|\w+ \d{4})\s*-\s*(?:present|current|\d{1,2}/\d{1,2}/\d{4}|\w+ \d{4})\b', re.I)
    date_matches = date_range_regex.findall(flattened_text)
    for match in date_matches:
        try:
            # Parse and calculate approximate years
            parts = match.split(' - ')
            start = date_parser.parse(parts[0])
            end = date_parser.parse(parts[1]) if parts[1].lower() not in ['present', 'current'] else None
            if end:
                years = (end - start).days / 365.25
                experience_list.append(f"{years:.1f} years (from {match})")
            else:
                import datetime
                now = datetime.datetime.now()
                years = (now - start).days / 365.25
                experience_list.append(f"{years:.1f} years (from {match})")
        except:
            experience_list.append(f"Date range: {match}")
    
    # Use SpaCy for contextual extraction: Get full sentences with matches
    for sent in doc.sents:
        if any(token.lemma_ in ["work", "experience", "employ", "serve"] for token in sent):
            sent_matches = duration_regex.findall(sent.text) + date_range_regex.findall(sent.text)
            if sent_matches:
                # Add the full sentence for richer context
                experience_list.append(sent.text.strip())
    
    # Deduplicate and join (prioritize full sentences if available)
    unique_experiences = list(set(experience_list))
    # Sort by length to prefer fuller descriptions
    unique_experiences.sort(key=len, reverse=True)
    data['experience'] = "; ".join(unique_experiences[:5]) if unique_experiences else ""  # Limit to top 5 to avoid overload

    return data