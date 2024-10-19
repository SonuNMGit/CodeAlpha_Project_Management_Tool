# CodeAlpha_Project_Management_Tool
Overview-
TaskFlow is a robust project management tool designed to streamline collaboration and enhance productivity. With features for task assignment, progress tracking, and team communication, TaskFlow empowers teams to manage their projects efficiently and effectively.


Features-

User Registration and Authentication: Secure user sign-up and login.

User Profiles: Create and manage user profiles.

Project Creation: Easily create new projects and invite team members to collaborate.

Task Management: Create, assign, edit, and delete tasks within projects.

Progress Tracking: Visual indicators to track the progress of tasks and projects.

Comments and Feedback: Comment on tasks to facilitate discussions and feedback.


Technologies Used-

Backend: Django

Frontend: HTML, CSS, JavaScript 

Database: SQLite 

Authentication: Django built in


Installation-

Clone the repository:

git clone https://github.com/SonuNMGit/CodeAlpha_Project_Management_Tool.git

Navigate to the project directory:

cd CodeAlpha_Project_Management_Tool-TaskFlow

Create a virtual environment:

python -m venv venv

Activate the virtual environment:

On Windows:

venv\Scripts\activate

On macOS/Linux:

source venv/bin/activate

Install the required packages:

pip install -r requirements.txt

Apply migrations:

python manage.py migrate

Create a superuser:

python manage.py createsuperuser

Run the development server:

python manage.py runserver

Access the application at http://127.0.0.1:8000.


Usage-

Users can sign up and create profiles.

Create projects and invite team members.

Assign tasks to team members and track progress.

Comment on tasks for discussions and feedback.

Receive notifications for task updates and project changes.
