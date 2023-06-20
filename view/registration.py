import tkinter as tk
from tkinter import messagebox
from security.validation import *
from security.encryption import encrypt_value
from security.decryption import decrypt_value
from database.database_handler import DatabasePointer


def register():
    if login_entry.get() == "" or password_entry.get() == "" or name_entry.get() == "" or surname_entry.get() == "" or email_entry.get() == "" or phone_entry.get() == "":
        messagebox.showerror("Błąd rejestracji", "Wypełnij wszystkie pola")
    else:
        database = DatabasePointer
        usernames = database.mysql_select("user_login", "user")
        if login_entry.get() in usernames:
            messagebox.showerror("Błąd rejestracji", "Login jest już zajęty")
            login_entry.delete(0, tk.END)
        else:
            if not validate_email(email_entry.get()):
                messagebox.showerror("Błąd rejestracji", "Adres email jest niepoprawny")
                email_entry.delete(0, tk.END)

            if not validate_phone_number(phone_entry.get()):
                messagebox.showerror("Błąd rejestracji", "Numer telefonu jest niepoprawny")
                phone_entry.delete(0, tk.END)

            if not validate_password(password_entry.get()):
                messagebox.showerror("Błąd rejestracji",
                                     "Hasło jest niepoprawne\n(Minimum jedna mała i duża litera, symbol i cyfra. Hasło musi mieć długość minimum 8)")
                print(password_entry.get())
                password_entry.delete(0, tk.END)

            if validate_email(email_entry.get()) and validate_phone_number(phone_entry.get()) and validate_password(password_entry.get()):
                password = encrypt_value(password_entry.get().encode('utf-8'), "storage/enckey.key")
                print(password)
                print(len(password))
                database.mysql_insert(table="user",
                                      columns="`user_password`, `user_login`, `user_firstname`, `user_surname`, `user_email`, `user_phone_number`, `user_balance`, `user_admin`",
                                      values="%s, %s, %s, %s, %s, %s, %s, %s", params=(
                    password, login_entry.get(), name_entry.get(), surname_entry.get(), email_entry.get(),
                    phone_entry.get(), '0', '0'))

                messagebox.showinfo("Rejestracja", "Rejestracja przeszła pomyślnie!")
                registration_window.destroy()
                usernames = database.mysql_select("user_login", "user")
                passwords = database.mysql_select("user_password", "user")
                admin_privileges = database.mysql_select("user_admin", "user")

                for p in range(len(passwords)):
                    temp = decrypt_value(passwords[p], "storage/enckey.key")
                    temp = temp.decode()
                    passwords[p] = temp

                credentials = {}

                for i in range(len(usernames)):
                    login = usernames[i]
                    password = passwords[i]
                    is_admin = admin_privileges[i]
                    credentials[login] = {'password': password, 'is_admin': is_admin}
                # messagebox.showerror(decrypt_value(password, "storage/enckey.key"), password) - szyfrowanie dziala


def clear_fields():
    # Funkcja do czyszczenia pól formularza
    login_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    surname_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)


def enforce_max_length(event):
    if len(password_entry.get()) >= 30:
        if event.keysym == "BackSpace":
            password_entry.configure(bg="white")
        else:
            password_entry.configure(bg="red")
            messagebox.showinfo("Ostrzeżenie", "Osiągnięto maksymalną długość hasła")
            return "break"  # Blokuje wpisywanie kolejnych znaków
    else:
        password_entry.configure(bg="white")


def open_registration_window(root):
    global login_entry
    global password_entry
    global name_entry
    global surname_entry
    global email_entry
    global phone_entry
    global registration_window
    registration_window = tk.Toplevel(root)
    registration_window.title("Rejestracja")
    registration_window.geometry("300x400+475+150")
    registration_window.transient(root)

    registration_label = tk.Label(registration_window, text="Formularz rejestracji", font=("Arial", 16))
    registration_label.pack(pady=10)

    # Pole login
    login_label = tk.Label(registration_window, text="Login:")
    login_label.pack()
    login_entry = tk.Entry(registration_window)
    login_entry.pack()

    # Pole hasło
    password_label = tk.Label(registration_window, text="Hasło:")
    password_label.pack()
    password_entry = tk.Entry(registration_window, show='*')
    password_entry.pack()
    password_entry.bind('<Key>',
                        enforce_max_length)  # Wywołuje funkcję enforce_max_length po wciśnięciu każdego klawisza

    # Pole imię
    name_label = tk.Label(registration_window, text="Imię:")
    name_label.pack()
    name_entry = tk.Entry(registration_window)
    name_entry.pack()

    # Pole nazwisko
    surname_label = tk.Label(registration_window, text="Nazwisko:")
    surname_label.pack()
    surname_entry = tk.Entry(registration_window)
    surname_entry.pack()

    # Pole email
    email_label = tk.Label(registration_window, text="Email:")
    email_label.pack()
    email_entry = tk.Entry(registration_window)
    email_entry.pack()

    # Pole numer telefonu
    phone_label = tk.Label(registration_window, text="Numer telefonu:")
    phone_label.pack()
    phone_entry = tk.Entry(registration_window)
    phone_entry.pack()

    registration_window.grab_set()

    # Przycisk rejestracji
    register_button = tk.Button(registration_window, text="Zarejestruj się", command=register)
    register_button.pack(pady=10)

    # Przycisk do czyszczenia pól formularza
    clear_button = tk.Button(registration_window, text="Wyczyść pola", command=clear_fields)
    clear_button.pack(pady=5)
