# NOTE: change tables to (db, item, attribute)
import tkinter as tk
from tkinter import ttk
from db import dbsetup, update_tree, add_user, update_item, delete_item, dataset_list, add_dataset, persons_list, add_info, run_db_merge, run_person_merge

root = tk.Tk()
root.title("SQLite Database Viewer")
root.geometry("650x400")

# type and id of last table pressed
selected_type = None
#selected_id = None
# table type displayed and ref id
search_table = False # NOT a table type
table_type = None
table_id = None
# current db person or info selected
db_id = None
person_id = None
# column and id of item selectet from tree
column = None
curr_id = None

# entry state
command = False

dbsetup()
#add_user()

# dropdown click item
def db_combo_action(out):
    global selected_type
    #global selected_id
    global search_table
    global table_type
    global table_id
    global db_id
    global person_id

    selected_type = "Datasets"
    table_type = "Persons"
    search_table = False

    table_id = db_ids[db_combo.current()]
    db_id = table_id
    person_id = None

    entry_var.set(db_combo.get())
    ppl_combo.delete(0, "end")
    info_entry_var.set("")

    label.config(text=f"{db_combo.get()} (id:{db_id})")

    update_tree(tree,table_type,table_id)
    update_combo_options(table_type)

def ppl_combo_action(out):
    global search_table
    global selected_type
    global table_type
    global table_id
    global person_id

    selected_type = "Persons"
    table_type = "Person_Info"
    search_table = False

    table_id = ppl_ids[ppl_combo.current()]
    person_id = table_id

    entry_var.set(ppl_combo.get())
    info_entry_var.set("")

    update_tree(tree,table_type,table_id)

# on text line enter
def entry_enter(event):
    global search_table

    value = event.widget.get()
    merge_val = merge_type.get()

    if(not value):
        return

    if(command == 0):
        entry_update(value)
    elif(command == 1):
        entry_merge(merge_val, value)
    elif(command == 2):
        search_table = True
        entry_search()

def entry_search():
    global table_type
    global table_id

    table_id = None

    value = entry_var.get()
    col = col_combo.get()
    table_type = table_combo.get()
    if(db_id and col and table_type):
        update_tree(tree,table_type,db_id, col, value)

def entry_merge(merge_val, value):
        if(merge_val == 0 and db_id):
            print("running db merge")
            run_db_merge(db_id, value)
        if(merge_val == 1 and db_id):
            print("running person merge")
            run_person_merge(db_id, value)
            update_tree(tree,table_type,table_id)
# updates tree if type is item
# or updates selected combo box
def entry_update(value):
    if(value is None):
        print("N/A")

    if(selected_type == "Item"):
        if(curr_id and column):
            update_item(table_type, curr_id, column, value)
            update_tree(tree,table_type,table_id)
    if(selected_type == "Datasets"):
        update_item(selected_type, db_id, "name", value)
        update_combo_options(selected_type)
    if(selected_type == "Persons"):
        update_item(selected_type, person_id, "name", value)
        update_combo_options(selected_type)

# chart click
def on_tree_click(event):
    global column
    global curr_id
    global selected_type

    row_id = tree.identify_row(event.y)
    col_id = tree.identify_column(event.x)

    data_str = None
    if(table_type == "Persons"):
        data_str = [None, "ind", "name", "note"]
    if(table_type == "Person_Info"):
        data_str = [None, "ind", "text", "date", "tag"]

    if row_id and col_id:
        item = tree.item(row_id, "values")
        ind = int(col_id[1:]) -1
        curr_id = item[2]
        selected_type = "Item"
        
        if(ind == 0):
            item_delete()
        elif(ind > 1):
            column = data_str[ind]
            entry_var.set(item[ind + 2])
# insert/delete new item
def insert_db(event):
    text = event.widget.get().strip()
    if text:
        add_dataset(text)
        update_combo_options("Datasets")
        event.widget.delete(0, "end")

def insert_person(event):
    text = event.widget.get().strip()
    if text and db_id:
        add_user(db_id, text)
        update_combo_options("Persons")
        update_tree(tree,table_type,table_id)
        event.widget.delete(0, "end")

def insert_info(event):
    text = event.widget.get().strip()
    if text and person_id:
        add_info(person_id, text)
        update_tree(tree,table_type,table_id)
        event.widget.delete(0, "end")

def item_delete():
    delete_item(table_type, curr_id)
    if(search_table):
        entry_search()
    else:
        update_tree(tree,table_type, table_id)

def db_delete():
    global ppl_options
    global ppl_ids
    global db_id

    if(db_id):
        delete_item("Datasets", db_id)
        tree.delete(*tree.get_children())
        update_combo_options("Datasets")

        label.config(text="None")

        db_combo.delete(0, "end")
        ppl_combo.delete(0, "end")
        info_entry_var.set("")

        ppl_options, ppl_ids = [], []
        ppl_combo["values"] = ppl_options

        db_id = None

# update combobox after adding item
def update_combo_options(combo_type):
    global db_options, db_ids
    global ppl_options, ppl_ids

    if(combo_type == "Datasets"):
        db_options, db_ids = dataset_list()
        db_combo["values"] = db_options
    if(combo_type == "Persons"):
        ppl_options, ppl_ids = persons_list(db_id)
        ppl_combo["values"] = ppl_options
    if(combo_type == "Person_Info"):
        print("update_combo_options N/A")

# entry toggle function
def entry_toggle():
    global command
    command = (command + 1) % 3
    if(command == 0):
        table_combo.pack_forget()
        col_combo.pack_forget()

        command_button.config(activebackground="SeaGreen1",bg="white")
    elif(command == 1):
        db_raido.pack(side=tk.LEFT)
        person_radio.pack(side=tk.LEFT)
        command_button.config(activebackground="white",bg="SeaGreen1")
    elif(command == 2):
        db_raido.pack_forget()
        person_radio.pack_forget()

        table_combo.pack(side=tk.LEFT)
        col_combo.pack(side=tk.LEFT)

        command_button.config(activebackground="white",bg="khaki1")

def search_combo(out):
    table_sel = table_combo.get()
    if(table_sel == "Persons"):
        col_combo["values"] = ["name","note",]
    if(table_sel == "Person_Info"):
        col_combo["values"] = ["tag", "text", "date"]


top = ttk.Frame()
#dbdelete button
db_del = tk.Button(top, text="del", command=db_delete, bg="firebrick1")
# Add a button to trigger the database pull
label = tk.Label(top, text="N/A",anchor="sw")

entry_row = ttk.Frame()
# entry to control data
command_button = tk.Button(entry_row, text="[~]", command=entry_toggle)
command_button.config(activebackground="SeaGreen1",bg="white")

#radio buttons
merge_type = tk.IntVar(value=0)
db_raido = ttk.Radiobutton(entry_row, text="db", variable=merge_type, value=0)
person_radio = ttk.Radiobutton(entry_row, text="person", variable=merge_type, value=1)

# search combo
table_combo = ttk.Combobox(entry_row ,values=["Persons","Person_Info"], state="readonly")
col_combo = ttk.Combobox(entry_row ,values=[""])

table_combo.bind("<<ComboboxSelected>>", search_combo)

entry_var = tk.StringVar()
entry = ttk.Entry(entry_row, textvariable=entry_var)
entry.bind("<Return>", entry_enter)

# dropdown frame
drops = ttk.Frame()
# dropdown1
db_options, db_ids = dataset_list()
db_combo = ttk.Combobox(drops,values=db_options)
db_combo.bind("<<ComboboxSelected>>", db_combo_action)
db_combo.bind('<Return>', insert_db)

# dropdown2
ppl_options, ppl_ids = [], []
ppl_combo = ttk.Combobox(drops, values=ppl_options)
ppl_combo.bind("<<ComboboxSelected>>", ppl_combo_action)
ppl_combo.bind('<Return>', insert_person)

# dropdown3
# TODO: make this into an entry
info_entry_var = tk.StringVar()
info_entry = ttk.Entry(drops, textvariable=info_entry_var)
info_entry.bind('<Return>', insert_info)


# Create the Treeview (The tree)
tree = ttk.Treeview(root, show="headings")

# Add a vertical scrollbar
scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)

# Configure tree
tree.configure(yscrollcommand=scrollbar.set)
tree.bind("<Button-1>", on_tree_click)

# Pack layout
top.pack(fill=tk.X)
db_del.pack(side=tk.LEFT)
label.pack(fill="both", expand=True, anchor="s")

entry_row.pack(fill=tk.X)
command_button.pack(side=tk.LEFT)
entry.pack(fill="both", expand=True, side=tk.RIGHT)

drops.pack(side=tk.LEFT, anchor="n")
db_combo.pack()
ppl_combo.pack()
info_entry.pack(fill=tk.X)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

root.mainloop()
