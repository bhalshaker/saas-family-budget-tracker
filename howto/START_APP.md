# How to Start the Family Budget Tracker Application

## Prerequisites

- Python 3.11 installed on your machine.
- Admin access to a PostgreSQL database (local or cloud).
- Network access from your machine to the PostgreSQL database.

## Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/bhalshaker/saas-family-budget-tracker.git
   cd saas-family-budget-tracker
   ```

2. **Create a Virtual Environment and Install Dependencies**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Create a `.env` File**
Copy the example from `config/example.env` or use the following template:
     ```
     db_url=postgresql+asyncpg://postgres:postgres@localhost:5432/familybudget
     db_host=localhost
     db_port=5432
     db_user=postgres
     db_password=postgres
     db_name=familybudget
     token_secret=your-secret-token
     ```
   - Adjust the values to match your PostgreSQL setup.

4. **Create the Database in PostgreSQL**
Connect to your PostgreSQL server and run:
     ```sql
     CREATE DATABASE familybudget;
     ```

5. **Initialize the Database**
   ```bash
   python seed.py
   ```

6. **Run the Application**
   ```bash
   uvicorn main:app
   ```

The application should now be running. If you encounter errors, check your `.env` configuration and database connectivity.
