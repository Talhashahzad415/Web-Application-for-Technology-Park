🏢 Web Application for Software Technology Park

This project is a Django-based web application designed to automate and manage the daily operations of a Software Technology Park. It implements full CRUD (Create, Read, Update, Delete) functionality and provides dedicated portals for Freelancers, Companies, and Administrators.

🚀 Overview

The system streamlines and digitizes several key management tasks within the park. It enables real-time tracking, booking, and communication among stakeholders, helping to maintain an organized, efficient, and collaborative environment.

⚙️ Key Features
🔸 1. Automated Booking System

Room Booking: Companies can book rooms based on availability.

Desk Booking: Freelancers can reserve desks within the co-working space.

Meeting Room Booking: Both companies and freelancers can schedule meeting rooms.

Status Monitoring: The system dynamically displays the availability status of all rooms, desks, and meeting rooms.

🔸 2. Messaging System

Built-in chat functionality allows seamless communication between freelancers and companies.

Messages are stored securely and can be accessed anytime by the users.

🔸 3. Complaint Management

Both freelancers and companies can submit complaints or requests to the admin through their respective portals.

Admins can view, respond to, and resolve complaints efficiently.

🔸 4. Multi-Portal Access

Freelancer Portal: Allows freelancers to book desks, communicate with companies, and send complaints to admin.

Company Portal: Enables companies to book rooms, hold meetings, message freelancers, and manage complaints.

Admin Portal: Provides administrators with full control over bookings, complaints, and user management.

🔸 5. CRUD Functionality

Each module (Rooms, Desks, Meeting Rooms, Users, Messages, and Complaints) supports:

Create – Add new records

Read – View details and availability

Update – Modify existing entries

Delete – Remove records

🧰 Tech Stack

Backend: Django (Python)

Frontend: HTML, CSS, JavaScript

Database: SQLite

Frameworks/Tools: Django

📈 Outcome

This application reduces manual workload by automating bookings, communication, and complaint handling. It improves space utilization, enhances transparency, and supports better coordination among companies, freelancers, and administrators.

🧩 Project Backend

Framework: Django (Python)

Database: SQLite (local database for development)

Virtual Environment: Python venv for dependency isolation

Dependencies: All Python packages are listed in requirements.txt

📁 Project Structure
crudprojrct1/          # Root project folder
├── crudprojrct1/      # Django project settings and config
├── enroll/             # Django app folder (handles main CRUD functionality)
├── db.sqlite3          # SQLite database (ignored in .gitignore for public use)
├── manage.py           # Django management script
├── MyEnv/              # Python virtual environment (ignored in .gitignore)
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation

⚡ Requirements

Before running the project, make sure you have:

Python 3 installed

pip (Python package installer)

Git (to clone the repository)

🛠️ Step-by-Step Setup Instructions

Follow these steps carefully to run this project on your own machine.

1️⃣ Clone the repository

Open a terminal and run:

git clone -b talha https://github.com/Talhashahzad415/Web-Application-for-Technology-Park
cd crudprojrct1


-b talha ensures you clone the correct branch.
If you want the default branch, you can omit -b talha.

2️⃣ Create a virtual environment

A virtual environment keeps your project dependencies separate from system Python.

python3 -m venv MyEnv


This creates a folder called MyEnv inside your project.

3️⃣ Activate the virtual environment
source MyEnv/bin/activate


You will see your terminal prompt change to (MyEnv)

This means you are now using the project’s isolated Python environment.

4️⃣ Install project dependencies

All required Python packages are listed in requirements.txt. Install them with:

pip install -r requirements.txt


If you don’t have requirements.txt, you can install Django manually:

pip install django

5️⃣ Apply database migrations

Django uses migrations to create the database tables. Run:

python manage.py migrate


This will create the SQLite database (db.sqlite3) with all the necessary tables.

6️⃣ Create a superuser (optional)

To access Django admin panel:

python manage.py createsuperuser


Enter a username, email, and password.

This account allows you to manage your data via Django’s admin interface.

7️⃣ Run the development server

Start the server:

python manage.py runserver


Open a web browser and go to:

http://127.0.0.1:8000/


You should see your Django project running locally.

🔧 How Users Can Use This Project

Clone the repository using Git.

Activate the virtual environment.

Install dependencies with pip install -r requirements.txt.

Apply migrations to set up the database.

Run the server with python manage.py runserver.

Access the project in the browser.

All CRUD operations are now available for testing and use.

⚙️ Notes

.gitignore prevents committing unnecessary files like:

Virtual environment (MyEnv/)

Local database (db.sqlite3)

Python cache (__pycache__/)

To stop the server: press Ctrl + C in the terminal.

Any changes can be committed and pushed to GitHub:

git add .
git commit -m "Your message"
git push

🔗 GitHub Repository

https://github.com/Talhashahzad415/Web-Application-for-Technology-Park

