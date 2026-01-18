# Resume Parser System

A web-based Resume Parser System that allows you to manage employee resumes efficiently. The system lets you view all employee details, view single employee details, and delete employee records via a simple and intuitive interface. The backend is powered by a RESTful API.

# Features
- Add New Employees: Upload and save employee information including name, email, phone, location, work experience, and more.
- View All Employees: See a list of all employees with their basic details.
- View Single Employee: View detailed information of a specific employee.
- Delete Employee: Remove an employee record from the system.
- Duplicate Email Handling: Prevents duplicate emails during employee creation.
- Responsive UI: Built with Tailwind CSS and Font Awesome for modern styling.

# Technologies Used
- Frontend: HTML, CSS (Tailwind), JavaScript
- Backend: Django, Django REST Framework
- Database: SQLite (default for Django)
- API Testing: Postman



# Installation & Setup

1. Clone the Repository
git clone https://github.com/yourusername/resume-parser-system.git
cd resume-parser-system

2. Create & Activate Virtual Environment
python -m venv venv
   - Windows:   
     &nbsp;  venv\Scripts\activate
   - macOS/Linux:   
      &nbsp; source venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Run Migrations
python manage.py migrate

5. Start Development Server
python manage.py runserver

6. Access the Application
Open your browser at http://127.0.0.1:8000



# API Endpoints
Method	Endpoint	Description  
- GET	/api/employees/	Get all employees
- GET	/api/employees/<id>/	Get details of a single employee
- POST	/api/create-employee/	Add a new employee
- DELETE	/api/employees/<id>/	Delete an employee

You can test all API endpoints using the provided Postman collection.

# Usage
Navigate to the Employees page to view all records.  
Click on an employee to view detailed information.  
Use the Delete button to remove an employee.  
Add new employees via the Add Employee form, ensuring unique email addresses.
