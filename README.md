CRUD Project 1 (crudprojrct1)

This is a simple Django CRUD project. “CRUD” stands for Create, Read, Update, Delete, which are the four basic operations of persistent storage.

This project allows users to perform these operations on a database (like adding or updating records).

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

git clone -b talha https://github.com/mohsinprof/crudprojrct1.git
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

https://github.com/mohsinprof/crudprojrct1