import tkinter as tk
from tkinter import ttk
from db import dbsetup, update_tree, add_user, update_item, delete_item, dataset_list, add_dataset, persons_list, info_list, add_info

root = tk.Tk()
root.title("SQLite Database Viewer")
root.geometry("650x400")

# type and id of last table pressed
selected_type = None
#selected_id = None
# table and id of dropdown item selected/active table
table_type = None
table_id = None
# current db person or info selected
db_id = None
person_id = None
info_id = None
# column and id of item selected
column = None
curr_id = None

dbsetup()
#add_user()

# set the chart to item children
def db_combo_action(out):
    global selected_type
    #global selected_id
    global table_type
    global table_id
    global db_id

    selected_type = "Datasets"
    table_type = "Persons"

    table_id = db_ids[db_combo.current()]
    db_id = table_id
    #selected_id = db_id
    entry_var.set(db_combo.get())
    ppl_combo.delete(0, "end")
    info_combo.delete(0, "end")

    label.config(text=f"{db_combo.get()}")

    update_tree(tree,table_type,table_id)
    update_combo_options(table_type)

def ppl_combo_action(out):
    global selected_type
    global table_type
    global table_id
    global person_id

    selected_type = "Persons"
    table_type = "Person_Info"

    table_id = ppl_ids[ppl_combo.current()]
    person_id = table_id

    entry_var.set(ppl_combo.get())
    info_combo.delete(0, "end")

    update_tree(tree,table_type,table_id)
    update_combo_options(table_type)

def info_combo_action(out):
    global selected_type
    global table_type
    global table_id
    global info_id

    selected_type = "Person_Info"

    entry_var.set(info_combo.get())
    table_id = info_ids[info_combo.current()]
    info_id = table_id
# on text line enter
def entry_enter(event):
    value = event.widget.get()
    if(not value):
        return
    
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
    if(selected_type == "Person_Info"):
        update_item(selected_type, info_id, "tag", value)
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
        update_combo_options("Person_Info")
        update_tree(tree,table_type,table_id)
        event.widget.delete(0, "end")

def item_delete():
    delete_item(table_type, curr_id)
    update_tree(tree,table_type, table_id)
    update_combo_options(table_type)

def db_delete():
    if(db_id):
        delete_item("Datasets", db_id)
        tree.delete(*tree.get_children())
        update_combo_options("Datasets")
        db_combo.delete(0, "end")
        ppl_combo.delete(0, "end")
        info_combo.delete(0, "end")
        label.config(text="None")
        
# update combobox after adding item
def update_combo_options(combo_type):
    global db_options, db_ids
    global ppl_options, ppl_ids
    global info_options, info_ids

    if(combo_type == "Datasets"):
        db_options, db_ids = dataset_list()
        db_combo["values"] = db_options
    if(combo_type == "Persons"):
        ppl_options, ppl_ids = persons_list(db_id)
        ppl_combo["values"] = ppl_options
    if(combo_type == "Person_Info"):
        info_options, info_ids = info_list(person_id)
        info_combo["values"] = info_options

top = ttk.Frame()
#dbdelete button
db_del = ttk.Button(top, text="Del", command=db_delete)
# Add a button to trigger the database pull
label = tk.Label(top, text="hello",anchor="w")

# entry to control data
entry_var = tk.StringVar()
entry = ttk.Entry(root, textvariable=entry_var,width=30)
entry.bind("<Return>", entry_enter)

# dropdown frame
drops = ttk.Frame()
# dropdown1
db_options, db_ids = dataset_list()
db_combo = ttk.Combobox(drops,values=db_options)
db_combo.bind("<<ComboboxSelected>>", db_combo_action)
db_combo.bind('<Return>', insert_db)

# dropdown2
ppl_options, ppl_ids = None, None
ppl_combo = ttk.Combobox(drops, values=ppl_options)
ppl_combo.bind("<<ComboboxSelected>>", ppl_combo_action)
ppl_combo.bind('<Return>', insert_person)

# dropdown2
info_options, info_ids = None, None
info_combo = ttk.Combobox(drops, values=info_options)
info_combo.bind("<<ComboboxSelected>>", info_combo_action)
info_combo.bind('<Return>', insert_info)


# Create the Treeview (The tree)
tree = ttk.Treeview(root, show="headings")

# Add a vertical scrollbar
scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)

# Configure tree
tree.configure(yscrollcommand=scrollbar.set)
tree.bind("<Button-1>", on_tree_click)

# Pack layout
top.pack(fill=tk.X, anchor="w")
db_del.pack(side=tk.LEFT)
label.pack(side=tk.LEFT)
entry.pack(fill=tk.X)
drops.pack(side=tk.LEFT, anchor="n")
db_combo.pack()
ppl_combo.pack()
info_combo.pack()
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

root.mainloop()
