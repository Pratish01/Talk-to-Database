import sqlite3
import pandas as pd
from src.config import DATABASE_PATH

def create_sample_db():
    """Creates a sample SQLite database with employees, departments, and salaries."""
    print(f"Creating sample database at {DATABASE_PATH}...")
    
    conn = sqlite3.connect(DATABASE_PATH)
    
    # Departments
    departments_df = pd.DataFrame([
        {"id": 1, "name": "Engineering", "manager_id": 1},
        {"id": 2, "name": "Sales", "manager_id": 4},
        {"id": 3, "name": "Marketing", "manager_id": 6},
    ])
    departments_df.to_sql("departments", conn, if_exists="replace", index=False)
    
    # Employees
    employees_df = pd.DataFrame([
        {"id": 1, "name": "Alice Johnson", "dept_id": 1, "role": "Senior Engineer"},
        {"id": 2, "name": "Bob Smith", "dept_id": 1, "role": "Junior Engineer"},
        {"id": 3, "name": "Charlie Brown", "dept_id": 1, "role": "Tech Lead"},
        {"id": 4, "name": "David Wilson", "dept_id": 2, "role": "Sales Manager"},
        {"id": 5, "name": "Eve Davis", "dept_id": 2, "role": "Account Executive"},
        {"id": 6, "name": "Frank Miller", "dept_id": 3, "role": "Marketing Director"},
    ])
    employees_df.to_sql("employees", conn, if_exists="replace", index=False)
    
    # Salaries (Yearly)
    salaries_df = pd.DataFrame([
        {"employee_id": 1, "amount": 120000, "currency": "USD"},
        {"employee_id": 2, "amount": 80000, "currency": "USD"},
        {"employee_id": 3, "amount": 140000, "currency": "USD"},
        {"employee_id": 4, "amount": 110000, "currency": "USD"},
        {"employee_id": 5, "amount": 95000, "currency": "USD"},
        {"employee_id": 6, "amount": 130000, "currency": "USD"},
    ])
    salaries_df.to_sql("salaries", conn, if_exists="replace", index=False)
    
    # Projects
    projects_df = pd.DataFrame([
        {"id": 101, "name": "Project Alpha", "dept_id": 1, "budget": 50000},
        {"id": 102, "name": "Project Beta", "dept_id": 1, "budget": 30000},
        {"id": 103, "name": "Global Outreach", "dept_id": 3, "budget": 75000},
    ])
    projects_df.to_sql("projects", conn, if_exists="replace", index=False)

    conn.close()
    print("Database created successfully.")

if __name__ == "__main__":
    create_sample_db()
