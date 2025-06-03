# DevTick - Developer Todo App

## Table of Contents
1. [Features](#features)
   - [📝 Developer Todo List](#-developer-todo-list)
   - [📚 Contact Book](#-contact-book)
   - [🔑 API Key Management](#-api-key-management)
   - [💡 Project Ideas](#-project-ideas)
   - [🛠️ Project Categories](#-project-categories)
   - [🤖 AI-Powered Features](#-ai-powered-features)
   - [📈 Progress Tracker](#-progress-tracker)
   - [🔄 Sync Across Devices](#-sync-across-devices)
   - [🎨 Theme Customization](#-theme-customization)
   - [🔍 Advanced Search](#-advanced-search)
2. [Future Enhancements](#future-enhancements)
3. [Tech Stack](#tech-stack)
4. [File Structure](#file-structure)
5. [Installation](#installation)
6. [Environment Setup](#environment-setup)
7. [Flask Development Template](#flask-development-template)
8. [Get Involved](#get-involved)
9. [Contact](#contact)

## Features

### 📝 Developer Todo List
- Task management system designed for developers to organize their work and track project progress
- Categories for different coding tasks, from bug fixes to new feature development
- Priority levels and due dates for better task organization
- Search functionality to quickly find specific tasks

### 📚 Contact Book
- A space to store and organize contacts, like collaborators, mentors, or clients
- Ability to store contact details, GitHub profiles, LinkedIn, or other relevant links
- Search functionality to quickly find contacts
- Additional fields for custom contact information

### 🔑 API Key Management
- Secure storage and organization of API keys for the projects you're working on
- Ability to add notes or descriptions for each API key to remind developers of usage, limits, and restrictions
- API key generator with customizable options:
  - Adjustable key length
  - Character type selection (uppercase, lowercase, numbers, special characters)
  - One-click copy functionality
- Search functionality to quickly find specific API keys

### 💡 Project Ideas
- A section for users to add and brainstorm new project ideas
- Categorize ideas based on difficulty, tech stack, or type of application
- AI-powered project enhancement suggestions
- Project status tracking (Planning, Active, Completed, On Hold, Archived)
- Additional custom fields for project details

### 🛠️ Project Categories
- Organize projects based on categories such as:
  - **Web Development**
  - **Mobile Development**
  - **AI/ML Projects**
  - **Open Source Contributions**
  - **DevOps**
  - **Full-Stack Development**
- Custom category support
- Project recovery system for deleted projects

### 🤖 AI-Powered Features
- **AI Chat Assistant:**
  - Real-time coding assistance
  - Code explanation and debugging help
  - Best practices suggestions
  - Code block and file handling
- **Project Enhancement:**
  - AI-generated suggestions for project improvements
  - Technical improvements recommendations
  - Best practices implementation
  - New feature suggestions
  - Documentation recommendations
  - Testing strategy suggestions
- **Smart Search:**
  - Semantic search across projects
  - Context-aware suggestions

### 📈 Progress Tracker
- Track milestones and project completion percentages
- Visual representation of task completion and deadlines
- Project status updates
- Start and end date tracking
- Contributor and role management

### 🔄 Sync Across Devices
- Sync the app across multiple devices to ensure developers can access their tasks, contacts, and ideas wherever they go
- Session management for secure access
- Persistent login state

### 🎨 Theme Customization
- Dark and light mode support
- Persistent theme preference
- Modern, clean UI design
- Responsive layout for all devices
- Customizable color schemes

### 🔍 Advanced Search
- Real-time search across all features
- Filter by categories, status, and dates
- Search in project details, notes, and custom fields
- Search history tracking

## Future Enhancements
- **Collaboration Tools:** Ability to share project ideas and tasks with teams for easier collaboration
- **Code Snippet Library:** A place to store and share reusable code snippets or templates
- **Code Review Integration:** Integrate with GitHub/GitLab to make it easy to manage pull requests or code reviews
- **Project Templates:** Pre-built project templates for common development scenarios
- **Time Tracking:** Built-in time tracking for tasks and projects
- **Export/Import:** Ability to export and import project data
- **API Integration:** Integration with popular development tools and services
- **Mobile App:** Native mobile applications for iOS and Android

## Tech Stack

- **Backend:** Flask (Python)
  - Flask-Session for session management
  - Flask Blueprint for modular routing
  - SQLAlchemy for database operations
  - OpenAI API integration for AI features
  
- **Database:** SQLite3
  - Multiple database files for different features
  - JSON storage for flexible data structures
  - Efficient indexing for quick searches
  
- **Frontend:** 
  - HTML5 and CSS3
  - Vanilla JavaScript
  - Responsive design
  - Modern UI components
  - Real-time updates

## File Structure

```
DevTick/
├── templates/
│   ├── auth/
│   │   ├── loggedin.html
│   │   ├── login.html
│   │   ├── signup.html
│   ├── viewProjects.html
│   ├── project.html
│   ├── homepage.html
│   ├── viewKeys.html
│   ├── key.html
│   ├── viewContacts.html
│   ├── contact.html
│   ├── viewTasks.html
│   ├── task.html
│   ├── sentence.html
│   ├── templates.html
│   ├── index.html
├── utils/
│   ├── chat.py
│   ├── projects.py
│   ├── contacts.py
│   ├── keys.py
│   ├── tasks.py
│   ├── sql.py
│   ├── resetAllDB.py
│   ├── auth.py
│   ├── SarvAuth.py
├── databases/
│   ├── projects.db
│   ├── tasks.db
│   ├── contacts.db
│   ├── chat.db
├── flask_session/
├── .venv/
├── .env
├── .gitignore
├── DevTickIcon.png
├── DevTickLogo.png
├── LICENSE
├── README.md
├── Template_README.md
├── app.py
├── personalNotes.txt
└── requirements.txt
```

**Explanation:**

- `templates/`: Contains all HTML template files for the application's frontend
  - `auth/`: Authentication-related pages (login, signup, logged-in state)
  - `viewProjects.html`, `project.html`: Project management interface
  - `viewKeys.html`, `key.html`: API key management interface
  - `viewContacts.html`, `contact.html`: Contact book interface
  - `viewTasks.html`, `task.html`: Todo list interface
  - `sentence.html`: AI chat interface
  - `templates.html`: Template management interface
  - `homepage.html`: Main dashboard
  - `index.html`: Landing page

- `utils/`: Contains all Python utility modules
  - `chat.py`: AI chat functionality implementation
  - `projects.py`: Project management logic
  - `contacts.py`: Contact book management
  - `keys.py`: API key management
  - `tasks.py`: Todo list functionality
  - `sql.py`: Database operations and queries
  - `resetAllDB.py`: Database reset utility
  - `auth.py`, `SarvAuth.py`: Authentication and authorization

- `databases/`: SQLite database files
  - `projects.db`: Stores project information
  - `tasks.db`: Stores todo items
  - `contacts.db`: Stores contact information
  - `chat.db`: Stores chat history

- `flask_session/`: Flask session storage directory

- `.venv/`: Python virtual environment directory

- Configuration Files:
  - `.env`: Environment variables (API keys, secrets)
  - `.gitignore`: Git ignore rules
  - `requirements.txt`: Python package dependencies

- Assets:
  - `DevTickIcon.png`: Application icon
  - `DevTickLogo.png`: Application logo

- Documentation:
  - `README.md`: Project documentation
  - `Template_README.md`: Template for documentation
  - `LICENSE`: Project license
  - `personalNotes.txt`: Developer notes

- Core Files:
  - `app.py`: Main application entry point
  - `auth.py`: Authentication module
  - `sql.py`: Database operations

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
   python3 -m venv .venv
   ```

4. Activate the virtual environment:
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - Unix/MacOS:
     ```bash
     source .venv/bin/activate
     ```

5. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

6. Run the Flask app:
   ```bash
   python app.py
   ```

7. Visit `http://127.0.0.1:5000/` in your browser to access the app.

## Environment Setup

1. Create a `.env` file in the root directory with the following variables:
   ```
   OPENAI_KEY=your_openai_api_key
   FLASK_SECRET_KEY=your_flask_secret_key
   ```

2. Configure your database settings in `sql.py` if needed.

3. Set up your OpenAI API key for AI features:
   - Sign up for an OpenAI account
   - Generate an API key
   - Add it to your `.env` file

## Flask Development Template
For this project, I used the **[Flask Development Template](https://github.com/SarveshwarSenthilKumar/Flask-Development-Template)** as the base template for building the backend. The template provides a solid foundation for developing Flask applications with best practices, including structure for routing, database handling, and integration with various extensions like Flask-Migrate for database migrations.

## Development Guidelines

### Code Style
- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and single-purpose

### Database Management
- Use SQLite for local development
- Follow the existing database schema
- Use the provided utility functions in `sql.py`
- Reset databases using `resetAllDB.py` if needed

### Frontend Development
- Maintain consistent styling across pages
- Use the existing CSS classes and components
- Ensure responsive design for all screen sizes
- Follow the established template structure

### Testing
- Test all new features thoroughly
- Ensure backward compatibility
- Test across different browsers
- Verify mobile responsiveness

## Contributing

### How to Contribute
1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Submit a pull request

### Pull Request Guidelines
- Provide a clear description of changes
- Include screenshots for UI changes
- Update documentation as needed
- Ensure all tests pass

### Code Review Process
- All pull requests will be reviewed
- Feedback will be provided promptly
- Changes may be requested before merging
- Maintain a positive and constructive discussion

## Get Involved
DevTick is an open-source project aimed at helping developers stay organized and productive. Contributions are welcome! Whether you're interested in adding new features, improving the UI/UX, or helping with documentation, your support will be valuable.

If you'd like to contribute or collaborate, check out the GitHub repository (to be added).

## Contact
For any questions, feedback, or contributions, feel free to reach out:

- **Email:** [sarveshwar313@gmail.com](mailto:sarveshwar313@gmail.com)
- **GitHub Repository:** [DevTick GitHub](https://github.com/SarveshwarSenthilKumar/DevTick)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.