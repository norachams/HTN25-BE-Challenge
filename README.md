# HTN25-BE-Challenge

## Overview
The Hackathon Badge Scanner API is a backend service designed to track hackathon attendees, their check-ins at various activities, and related event data. This API uses Flask with SQLite for rapid development and easy deployment.

## Technologies Used
- **Flask** (Python web framework)
- **SQLite** (Lightweight database)
- **SQLAlchemy** (ORM for database operations)
- **Python 3.12+**

## Setup and Installation

### Prerequisites
- Python 3.x installed
- (Optional) Git for cloning the repository

### Steps

1. **Clone the Repository**
   ```bash
   git clone (https://github.com/norachams/HTN25-BE-Challenge.git)
   cd HTN25-BE-Challenge 


2. Create and Activate a Virtual Environment
    ```bash
    python -m venv venv
    source venv/bin/activate

3. Install Dependencies
   ```bash
     pip install flask flask_sqlalchemy flask_restful
   
4. Initialize the Database. The application uses SQLite.
Running the app will automatically create a hackathon.db file:
    ```bash
      python app.py

6. Import Initial Data If you have downloaded the JSON file (example_data.json), import it into the database:
    ```bash
       python import_data.py

### API Endpoints

1. Get All Users
- Endpoint: GET /users
- Description: Retrieves a list of all users with their details and associated scan records.







