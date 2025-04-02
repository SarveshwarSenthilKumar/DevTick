# DevTick - Developer Todo App

## Table of Contents
1. [Features](#features)
   - [📝 Developer Todo List](#-developer-todo-list)
   - [📚 Contact Book](#-contact-book)
   - [🔑 API Key Management](#-api-key-management)
   - [💡 Project Ideas](#-project-ideas)
   - [🛠️ Project Categories](#-project-categories)
   - [🤖 AI-Powered Text Chat](#-ai-powered-text-chat)
   - [📈 Progress Tracker](#-progress-tracker)
   - [🔄 Sync Across Devices](#-sync-across-devices)
2. [Future Enhancements](#future-enhancements)
3. [Tech Stack](#tech-stack)
4. [File Structure](#file-structure)
5. [Installation](#installation)
6. [Flask Development Template](#flask-development-template)
7. [Get Involved](#get-involved)
8. [Contact](#contact)

## Features

### 📝 Developer Todo List
- Task management system designed for developers to organize their work and track project progress.
- Categories for different coding tasks, from bug fixes to new feature development.

### 📚 Contact Book
- A space to store and organize contacts, like collaborators, mentors, or clients.
- Ability to store contact details, GitHub profiles, LinkedIn, or other relevant links.

### 🔑 API Key Management
- Secure storage and organization of API keys for the projects you're working on.
- Ability to add notes or descriptions for each API key to remind developers of usage, limits, and restrictions.

### 💡 Project Ideas
- A section for users to add and brainstorm new project ideas.
- Categorize ideas based on difficulty, tech stack, or type of application (e.g., mobile, web, AI).

### 🛠️ Project Categories
- Organize projects based on categories such as:
  - **Web Development**
  - **Mobile Development**
  - **AI/ML Projects**
  - **Open Source Contributions**
- This will help developers find and focus on relevant types of work.

### 🤖 AI-Powered Text Chat
- An AI-based chat feature that can answer coding questions, provide guidance, or even help debug code.
- Assist with explaining algorithms or suggesting best practices.

### 📈 Progress Tracker
- Track milestones and project completion percentages.
- Visual representation of task completion and deadlines.

### 🔄 Sync Across Devices
- Sync the app across multiple devices to ensure developers can access their tasks, contacts, and ideas wherever they go.

## Future Enhancements
- **Collaboration Tools:** Ability to share project ideas and tasks with teams for easier collaboration.
- **Code Snippet Library:** A place to store and share reusable code snippets or templates.
- **Code Review Integration:** Integrate with GitHub/GitLab to make it easy to manage pull requests or code reviews.

## Tech Stack

- **Backend:** Flask (Python)
  - A lightweight Python web framework that makes it easy to develop APIs and web applications.
  
- **Database:** SQLite3
  - SQLite3 is used for local, lightweight database management. It will store user health data, preferences, and AI-generated recommendations.

- **Frontend:** HTML and CSS
  - Simple, clean HTML and CSS will be used to build the user interface. Future enhancements could include JavaScript and front-end frameworks like React or Vue.js.

## File Structure

```
DevTick/
├── templates/
│   ├── auth/
│   │   ├── loggedin.html
│   │   ├── login.html
│   │   ├── signup.html
│   ├── index.html
├── .gitignore
├── DevTickIcon.png
├── DevTickLogo.png
├── LICENSE
├── README.md
├── SarvAuth.py
├── Template_README.md
├── app.py
├── auth.py
├── createAPIstorage.py
├── createContactbook.py
├── createDatabase.py
├── createProjectsDB.py
├── createTasksDB.py
├── requirements.txt
└── sql.py
```

**Explanation:**

- `templates/`: Directory containing HTML template files for the application's frontend.
  - `auth/`: Contains authentication-related pages like login and registration.
- `.gitignore`: Specifies files and directories that Git should ignore.
- `DevTickIcon.png` and `DevTickLogo.png`: Image assets for the application's icon and logo.
- `LICENSE`: The license under which DevTick is distributed.
- `README.md`: Provides an overview of the project, including features and installation instructions.
- `SarvAuth.py` and `auth.py`: Modules handling authentication functionalities.
- `Template_README.md`: Likely a template for README files, possibly for use in other parts of the project.
- `app.py`: The main application script that initializes and runs the Flask server.
- `createAPIstorage.py`, `createContactbook.py`, `createDatabase.py`, `createProjectsDB.py`, `createTasksDB.py`: Scripts for creating and managing various databases used in the application.
- `requirements.txt`: Lists the Python dependencies required to run the application.
- `sql.py`: Contains SQL-related functions or classes for database interactions.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/SarveshwarSenthilKumar/DevTick.git
   ```

2. Navigate to the project directory:
   ```bash
   cd DevTick
   ```

3. Create a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   ```

4. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up the databases by running each of the following scripts:
   ```bash
   python createAPIstorage.py
   python createContactbook.py
   python createDatabase.py
   python createProjectsDB.py
   python createTasksDB.py
   ```

6. Run the Flask app:
   ```bash
   python app.py
   ```

7. Visit `http://127.0.0.1:5000/` in your browser to access the app.

## Flask Development Template
For this project, I used the **[Flask Development Template](https://github.com/SarveshwarSenthilKumar/Flask-Development-Template)** as the base template for building the backend. The template provides a solid foundation for developing Flask applications with best practices, including structure for routing, database handling, and integration with various extensions like Flask-Migrate for database migrations.

## Get Involved
DevTick is an open-source project aimed at helping developers stay organized and productive. Contributions are welcome! Whether you're interested in adding new features, improving the UI/UX, or helping with documentation, your support will be valuable.

If you'd like to contribute or collaborate, check out the GitHub repository (to be added).

## Contact
For any questions, feedback, or contributions, feel free to reach out:

- **Email:** [sarveshwar313@gmail.com](mailto:sarveshwar313@gmail.com)
- **GitHub Repository:** [DevTick GitHub](https://github.com/SarveshwarSenthilKumar/DevTick)
