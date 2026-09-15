import sqlite3

conn = sqlite3.connect('running.db')
cursor = conn.cursor()

def p_format():
    with open("format.txt", "r", encoding="utf-8") as reader, open("classmates/p_out.csv", "w", encoding="utf-8") as writer:
        writer.write("id,name,note\n")
        for index, line in enumerate(reader):
            clean_line = line.rstrip("\n")
            writer.write(f"{index},{clean_line},\n")

def i_format(input, date):
    with open("classmates/p_out.csv", "r", encoding="utf-8") as reader, open("classmates/i_out.csv", "w", encoding="utf-8") as writer:
        writer.write("person_id,text,date,tag\n")
        reader.readline()
        for index, line in enumerate(reader):
            writer.write(f"{index},,{date},{input}\n")

def run_person_merge(db_id, name):
    cursor.execute("""
        SELECT MIN(id)
        FROM Persons
        WHERE dataset_id = ? AND name = ?
    """, (db_id, name))

    first_id = cursor.fetchone()[0]

    cursor.execute("""
        UPDATE Person_Info
        SET person_id = ?
        WHERE person_id IN (
            SELECT id
            FROM Persons
            WHERE dataset_id = ? AND name = ? AND id != ?
        )
    """, (first_id, db_id, name, first_id))

    conn.commit()
    print(f"Successfully updated. Rows affected: {cursor.rowcount}")

def merge_all():
    with open("format.txt", "r", encoding="utf-8") as reader:
        for line in reader:
            clean_line = line.rstrip("\n")
            run_person_merge(1, clean_line)

def remove_duplicates():
    cursor.execute("""
        DELETE FROM Persons 
        WHERE id NOT IN (
            SELECT person_id FROM Person_Info
        )
    """)

    conn.commit()
    print(f"Successfully updated. Rows affected: {cursor.rowcount}")



# p_format()
# i_format("cs135","fall2023")
merge_all()
remove_duplicates()


conn.close()
