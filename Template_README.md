# Flask Development Template

Welcome to the Flask Development Template! This repository serves as a foundational template to kickstart your Flask web application projects. It provides a structured setup, essential configurations, and examples to streamline your development process.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [Database Setup](#database-setup)
- [Configuration Settings](#configuration-settings)
- [Famous Websites Using Flask](#famous-websites-using-flask)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Flask Framework**: Lightweight and flexible web framework.
- **Structured Project Layout**: Organized directories and modules for scalability.
- **SQLite Integration**: Ready-to-use SQLite database setup.
- **Template Rendering**: Example HTML templates using Jinja2.
- **Dependency Management**: `requirements.txt` for easy package installations.
- **Customizable Configuration**: Easy-to-modify settings for encryption, authentication, and server behavior.

## Project Structure

The project follows a standard Flask application structure:

```
Flask-Development-Template/
├── templates/
│   ├── auth/
│   │   └── loggedIn.html
│   │   └── login.html
│   │   └── signup.html
│   └── index.html
├── app.py
├── auth.py
├── createDatabase.py
├── .env
├── .gitignore
├── requirements.txt
└── ToDo.txt
```

- `templates/`: Contains HTML templates rendered by Flask views.
- `templates/auth`: Contains HTML templates rendered by Flask views specifically for authentication purposes.
- `app.py`: Main application file where the Flask app is initialized and routes are defined.
- `auth.py`: Manages authentication routes via Flask Blueprint.
- `createDatabase.py`: Script to initialize and populate the SQLite database.
- `.env`: Stores sensitive environment variables like encryption keys.
- `.gitignore`: Ensures that sensitive files (e.g., `.env`) are not committed to version control.
- `requirements.txt`: Lists Python dependencies required for the project.
- `ToDo.txt`: A placeholder for tracking tasks and future enhancements.

### Additional Files

- `SarvAuth.py`: Python functions useful for authentication.
    - `CheckEmail(email)`: Returns `True` (Valid Email) or `False` (Invalid Email) using a regular expressions check.
    - `VerifyName(name)`: Returns `[True, name]` or `[False, error]` by checking for special characters and capitalizing the first letter of each name.
    - `CheckUserPassword(username, password)`: Returns `[True]` or `[False, error]` by validating both username and password.
    - `hash(password)`: Returns a password hashed using the SHA-256 module.

- `sql.py`: Python package for SQLite Database Management created by Harvard (Updated for 2025). [CS50 Reference](https://cs50.harvard.edu/x/2025/)

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Python 3.8 or higher
- `pip` (Python package installer)

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/SarveshwarSenthilKumar/Flask-Development-Template.git
   cd Flask-Development-Template
   ```

2. **Create a Virtual Environment**:

   It's recommended to use a virtual environment to manage dependencies.

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Set the Flask Application Environment**:

   ```bash
   export FLASK_APP=app.py
   export FLASK_ENV=development  # Enables debug mode
   ```

   On Windows:

   ```bash
   set FLASK_APP=app.py
   set FLASK_ENV=development
   ```

2. **Initialize the Database**:

   ```bash
   python createDatabase.py
   ```

3. **Run the Application**:

   ```bash
   flask run
   ```

   Access the application at `http://127.0.0.1:5000/`.

## Database Setup

The template uses SQLite for database management. The `createDatabase.py` script initializes the database and populates it with initial data. Modify this script to customize your database schema and seed data.

## Configuration Settings

### Changing the Encryption Key

1. Open the `.env` file.
2. Set your encryption key:

   ```
   ENCRYPTION_KEY=your_secret_key_here
   ```

3. Ensure `.env` is added to `.gitignore` to prevent it from being committed:

   ```
   echo .env >> .gitignore
   ```

### Enabling or Disabling AutoRun

In `app.py`, modify the `autoRun` variable:

```python
autoRun = True  # Change to False to disable auto-run on script execution
```

### Changing the Port Number

Modify the `port` variable in `app.py`:

```python
port = 5000  # Change this to your preferred port number
```

Run Flask on the specified port:

```bash
flask run --port=5000
```

### Enabling or Disabling Authentication

Modify the `authentication` variable in `app.py`:

```python
authentication = True  # Set to False to disable authentication
```

### Customizing Database Fields

Modify `createDatabase.py` to change the fields in the database schema.

## Famous Websites Using Flask

Several well-known websites and platforms are built using Flask:

- **Pinterest**: Uses Flask for its web services.
- **LinkedIn**: Parts of LinkedIn’s backend are powered by Flask.
- **Reddit**: Some of Reddit’s microservices use Flask.
- **Netflix**: Flask is used for internal tools and APIs.
- **Lyft**: Utilizes Flask for various services.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -am 'Add new feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Submit a pull request detailing your changes.

For any questions or suggestions, email Sarveshwar Senthil Kumar at Sarveshwar313@gmail.com.
Feel free to add on to `ToDo.txt`.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.

---

*Note: This template is inspired by best practices in Flask application development. For more advanced configurations and features, consider exploring other Flask templates and boilerplates.*

