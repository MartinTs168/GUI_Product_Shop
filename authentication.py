from tkinter import Button, Entry

from buying_page import display_products
from canvas import root, frame
from helpers import clean_screen, get_password_hash
from json import dump, loads


def get_users_data():
    info_data = []

    with open("db/users_information.txt", "r") as users_file:
        for line in users_file:
            info_data.append(loads(line))

    return info_data


def render_entry():
    register_button = Button(
        root,
        text="Register",
        bg="blue",
        fg="white",  # font color
        font=('Arial', 11),
        bd=0,
        width=9,
        height=2,
        command=register
    )

    login_button = Button(
        text="Login",
        bg="lightblue",
        fg="white",  # font color
        font=('Arial', 11),
        bd=0,
        width=9,
        height=2,
        command=login
    )

    frame.create_window(350, 260, window=register_button)
    frame.create_window(350, 310, window=login_button)


def register():
    clean_screen()

    frame.create_text(100, 50, text="First Name: ", font=('Arial', 11))
    frame.create_text(100, 100, text="Last Name: ", font=('Arial', 11))
    frame.create_text(100, 150, text="Username: ", font=('Arial', 11))
    frame.create_text(100, 200, text="Password: ", font=('Arial', 11))

    frame.create_window(205, 50, window=first_name_box)
    frame.create_window(205, 100, window=last_name_box)
    frame.create_window(205, 150, window=username_box)
    frame.create_window(205, 200, window=password_box)

    register_button = Button(
        root,
        text="Register",
        bg="blue",
        fg="white",
        font=('Arial', 11),
        bd=0,
        width=22,
        height=2,
        command=registration
    )

    frame.create_window(165, 250, window=register_button)


def registration():
    info_dict = {
        "First name": first_name_box.get(),
        "Last name": last_name_box.get(),
        "Username": username_box.get(),
        "Password": password_box.get(),
    }
    if check_registration(info_dict):
        with open("db/users_information.txt", "a") as users_file:
            info_dict["Password"] = get_password_hash(info_dict["Password"])
            dump(info_dict, users_file)
            users_file.write("\n")

            display_products()


def check_registration(info_dict):
    frame.delete('error')

    for key, value in info_dict.items():

        if not value.strip():
            frame.create_text(170, 320, text=f"{key} cannot be empty!", fill='red', tags='error', font=('Arial', 11), )
            return False

    users_data = get_users_data()

    for user in users_data:
        if user["Username"] == info_dict["Username"]:
            frame.create_text(170, 320, text="Username is already taken!", fill='red', tags='error', font=('Arial', 11))
            return False

    return True


def login():
    clean_screen()
    root.bind("<KeyRelease>", change_login_button_status)

    frame.create_text(100, 150, text="Username: ", font=('Arial', 11))
    frame.create_text(100, 200, text="Password: ", font=('Arial', 11))

    frame.create_window(205, 150, window=username_box)
    frame.create_window(205, 200, window=password_box)

    frame.create_window(165, 280, window=login_button)


def logging():
    if check_login():
        display_products()
        pass
    else:
        frame.create_text(300, 340, text='Invalid username or password!', fill='red', font=('Arial', 11))


def check_login():
    users_data = get_users_data()

    user_username = username_box.get()
    user_password = get_password_hash(password_box.get())

    for user in users_data:
        cur_user_username = user["Username"]
        curr_user_password = user["Password"]

        if cur_user_username == user_username and curr_user_password == user_password:
            return True

    return False


def change_login_button_status(event):
    info = [
        username_box.get(),
        password_box.get(),
    ]

    for el in info:
        if not el.strip():
            login_button['state'] = "disabled"
            break
    else:
        login_button['state'] = "normal"


first_name_box = Entry(root, bd=0)
last_name_box = Entry(root, bd=0)
username_box = Entry(root, bd=0)
password_box = Entry(root, bd=0, show='*')

login_button = Button(
    root,
    text="Login",
    bg="blue",
    fg="white",
    font=('Arial', 11),
    bd=0,
    width=22,
    height=2,
    command=logging
)

login_button['state'] = 'disabled'


