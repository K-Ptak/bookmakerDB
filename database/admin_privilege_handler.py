from tkinter import messagebox

from ttkbootstrap import INFO, OUTLINE
from database.database_handler import DatabasePointer
import ttkbootstrap as ttk

database = DatabasePointer()


def privilege_messegebox(root):
    messagebox.showinfo("Zmiana uprawnień", "Zmieniono uprawnienia użytkownika!")
    root.destroy()


def add_privilege(name, root):
    DatabasePointer.mysql_update(table="user", values="user_admin = 1", conditions=f"user_login = '{name}'")
    privilege_messegebox(root)


def del_privilege(name, root):
    DatabasePointer.mysql_update(table="user", values="user_admin = 0", conditions=f"user_login = '{name}'")
    privilege_messegebox(root)


def show_add_privilege_window(root):
    add_privilege_window = ttk.Toplevel(root)
    add_privilege_window.title("Nadawanie uprawnień")
    add_privilege_window.geometry("800x600+700+150")
    add_privilege_window.transient(root)

    registration_label = ttk.Label(add_privilege_window, text="Wybierz użytkownika, któremu chcesz nadać uprawnienia",
                                   font=("Arial", 12))
    registration_label.pack(pady=10)

    text = ttk.Text(add_privilege_window)
    text.pack(side="left", padx=100, pady=(0, 100))
    sb = ttk.Scrollbar(add_privilege_window, command=text.yview)
    sb.pack(side="right")
    text.configure(yscrollcommand=sb.set)

    usernames = database.mysql_select(table="user", column="user_login", conditions="WHERE user_admin = 0")
    usernames.sort()

    for i in usernames:
        button = ttk.Button(text, text=i, bootstyle=(INFO, OUTLINE),
                            command=lambda t=i: add_privilege(t, add_privilege_window))
        button.pack(padx=10, pady=(5, 5), fill=ttk.BOTH, expand=1)
        text.window_create("end", window=button)
        text.insert("end", "\n")
    return


def show_del_privilege_window(root, username):
    del_privilege_window = ttk.Toplevel(root)
    del_privilege_window.title("Usuwanie uprawnień")
    del_privilege_window.geometry("800x600+700+150")
    del_privilege_window.transient(root)

    registration_label = ttk.Label(del_privilege_window, text="Wybierz użytkownika, któremu chcesz usunąć uprawnienia",
                                   font=("Arial", 12))
    registration_label.pack(pady=10)

    text = ttk.Text(del_privilege_window)
    text.pack(side="left", padx=100, pady=(0, 100))
    sb = ttk.Scrollbar(del_privilege_window, command=text.yview)
    sb.pack(side="right")
    text.configure(yscrollcommand=sb.set)

    usernames = database.mysql_select(table="user", column="user_login", conditions=f"WHERE user_admin = 1 AND user_login NOT LIKE '{username}'")
    usernames.sort()

    for i in usernames:
        button = ttk.Button(text, text=i, bootstyle=(INFO, OUTLINE),
                            command=lambda t=i: del_privilege(t, del_privilege_window))
        button.pack(padx=10, pady=(5, 5), fill=ttk.BOTH, expand=1)
        text.window_create("end", window=button)
        text.insert("end", "\n")
    return
