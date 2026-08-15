import tkinter as tk
from tkinter import messagebox
import sqlite3

conn = sqlite3.connect('example.db')
cursor = conn.cursor()


def dbsetup():
    cursor.execute("PRAGMA foreign_keys = ON;")

    create_table_query = """
    CREATE TABLE IF NOT EXISTS Datasets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );
    """
    cursor.execute(create_table_query)
    create_table_query = """
    CREATE TABLE IF NOT EXISTS Persons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dataset_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        note TEXT,
        FOREIGN KEY (dataset_id) REFERENCES Datasets (id) ON DELETE CASCADE
    );
    """
    cursor.execute(create_table_query)
    create_table_query = """
    CREATE TABLE IF NOT EXISTS Person_Info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER NOT NULL,
        text TEXT NOT NULL,
        date TEXT NOT NULL,
        tag TEXT,
        FOREIGN KEY (person_id) REFERENCES Persons (id) ON DELETE CASCADE
    );
    """
    cursor.execute(create_table_query)


    conn.commit()
    print("i made a table")

def update_tree(tree,table_type,id):
    # Get column names first to build the table dynamically
    cursor.execute(f"PRAGMA table_info({table_type})")

    columns_info = cursor.fetchall()
    # Extract just the column names (e.g., ['id', 'name', 'email', 'age'])
    column_names = [" ", "ind"] + [col[1] for col in columns_info]

    # Fetch all rows from the table
    if(table_type == "Persons"):
        cursor.execute(f"SELECT * FROM Persons where dataset_id = ?", (id,))
    if(table_type == "Person_Info"):
        cursor.execute(f"SELECT * FROM Person_Info where person_id = ?", (id,))

    rows = cursor.fetchall()

    tree["displaycolumns"] = "#all"
    tree["columns"] =column_names

    # Dynamically set up headings and column widths based on the DB schema
    for col in column_names:
        tree.heading(col, text=col.capitalize(), anchor=tk.W)
        tree.column(col, anchor=tk.W, width=150)
    tree.column("#1", width=20, stretch=tk.NO)
    tree.column("#2", width=35, stretch=tk.NO)

    if(table_type == "Persons"):
        print("persons", tree["columns"])
        tree["displaycolumns"] = (" ", "ind", "name", "note")
    if(table_type == "Person_Info"):
        print("infos", tree["columns"])
        tree["displaycolumns"] = (" ", "ind", "text", "date", "tag")

    tree.delete(*tree.get_children())

    for index, row in enumerate(rows):
        tree.insert("", tk.END, values=("-",index)+row)

def dataset_list():
    cursor.execute("SELECT id, name FROM Datasets;")
    tables = cursor.fetchall()

    print(tables)

    table_ids = [table[0] for table in tables]
    table_names = [table[1] for table in tables]

    print("names in datasets:", table_names)
    return table_names, table_ids

def persons_list(db_id):
    cursor.execute("SELECT id, name FROM Persons WHERE dataset_id = ?;",(db_id,))
    tables = cursor.fetchall()

    print(len(tables))

    table_ids = [table[0] for table in tables]
    table_names = [table[1] for table in tables]

    return table_names, table_ids

def info_list(person_id):
    cursor.execute("SELECT id, tag FROM Person_Info WHERE person_id = ?;",(person_id,))
    tables = cursor.fetchall()

    print(len(tables))

    table_ids = [table[0] for table in tables]
    table_names = [table[1] for table in tables]

    return table_names, table_ids

def add_dataset(name):
    cursor.execute(
        "INSERT INTO Datasets (name) VALUES (?)",
        (name,)
    )
    conn.commit()
    print(f"Successfully updated. Rows affected: {cursor.rowcount}")

def add_user(db_id, name):
    note = None

    # Simple validation: Check if fields are empty
    if not name:
        tk.messagebox.showwarning("Input Error", "All fields are required!")
        return
    
    # Try inserting into the database
    # Secure parameterized query to prevent SQL Injection
    cursor.execute(
        "INSERT INTO Persons (dataset_id, name, note) VALUES (?, ?, ?)",
        (db_id, name, note),
    )

    conn.commit()
    print(f"Successfully updated. Rows affected: {cursor.rowcount}")

def add_info(person_id, text):
    note = None

    # Simple validation: Check if fields are empty
    if not text:
        tk.messagebox.showwarning("Input Error", "All fields are required!")
        return
    
    # Try inserting into the database
    # Secure parameterized query to prevent SQL Injection
    cursor.execute(
        "INSERT INTO Person_Info (person_id, text, date, tag) VALUES (?, ?, ?, ?)",
        (person_id, "None", "date", text),
    )

    conn.commit()
    print(f"Successfully updated. Rows affected: {cursor.rowcount}")

def update_item(table_type, item_id, column, value):
    sql_update_query = f"""
        UPDATE {table_type}
        SET {column} = ? 
        WHERE id = ?
    """
        
    # 4. Execute the query
    cursor.execute(sql_update_query, (value, item_id) )
    
    # 5. CRITICAL: Commit the transaction to save changes
    conn.commit()
    
    print(f"Successfully updated. Rows affected: {cursor.rowcount}")

def delete_item(table_type, item_id):
    sql_query = f"""
        DELETE FROM {table_type} 
        WHERE id = ?
    """
        
    cursor.execute(sql_query, (item_id,) )
    conn.commit()
    
    print(f"deleted. Rows affected: {cursor.rowcount}")

def run_merge(value, type, id):
    sql_query = None     
    if(type == 0):
        sql_query = f"""
                "INSERT INTO Persons (dataset_id, name, note) VALUES (?, ?, ?)",
        """
        
    cursor.execute(sql_query, (item_id,) )
    conn.commit()
