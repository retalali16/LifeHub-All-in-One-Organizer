# LifeHub – Your All-in-One Life Organizer

## Overview
LifeHub is a web application designed to help users manage their lives efficiently by combining task management, habit tracking, and budgeting in one platform.

## Features
- **Task Management**: Create, edit, delete, and set priorities for tasks.
- **Habit Tracking**: Track and manage daily/weekly habits with streaks.
- **Budget Management**: Manage expenses, set financial goals, and view summaries.
- **Notifications and Plan B Suggestions**: Get alerts and alternative options for incomplete tasks.

## Technologies Used
- **Frontend**: Flask Templates and Jinja2 for dynamic rendering.
- **Backend**: Flask for handling API requests and user data.
- **Database**: MongoDB for flexible data storage.
- **Notifications**: Firebase or OneSignal for real-time updates.
- **Form Handling**: Flask-WTF for form processing and validation.

## Project Structure
LIFEHUB/
│
├── application/
│   ├── templates/      # HTML files (Jinja2 templates)
│   ├── __init__.py     # Initialize Flask app and MongoDB connection
│   ├── forms.py        # Form definitions
│   ├── routes.py       # Routing logic for views
│
├── run.py              # Main entry point to run the app
└── requirements.txt    # Python dependencies

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Mostafa-Hisham0/LifeHub-All-in-One-Organizer
    cd LifeHub-All-in-One-Organizer
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up your MongoDB database by updating the `MONGO_URI` in `application/__init__.py` with your own connection string.

4. Run the application:
    ```bash
    python application/run.py
    ```

5. Access the application in your browser at `http://127.0.0.1:5000/`.

## Application Flow
1. **Home Page**: View all tasks with options to add, update, or delete tasks.
2. **Add Task**: Add a new task by filling in details such as task name, description, and completion status.
3. **Update Task**: Update existing tasks and mark them as completed or not completed.
4. **Delete Task**: Delete tasks that are no longer needed.
