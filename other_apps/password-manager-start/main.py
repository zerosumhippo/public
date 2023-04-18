from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
           'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
           'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
SYMBOLS = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    password_list_letters = [choice(LETTERS) for letter in range(randint(8, 10))]
    password_list_symbols = [choice(SYMBOLS) for symbol in range(randint(2, 4))]
    password_list_numbers = [choice(NUMBERS) for number in range(randint(2, 4))]

    password_list = password_list_letters + password_list_symbols + password_list_numbers
    shuffle(password_list)

    password = "".join(password_list)
    pw_input.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_input.get()
    username = username_input.get()
    pw = pw_input.get()
    new_data = {
        website: {
            "email": username,
            "password": pw,
        }
    }

    if len(website) == 0 or len(username) == 0 or len(pw) == 0:
        messagebox.showerror(title="Empty Fields", message="Please don't leave any fields empty!")
    else:
        # is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \n\nEmail: {username} "
        #                                                       f"\nPassword: {pw} \n\nIs it ok to save?")
        # if is_ok:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
                # Updating old data with new data
                data.update(new_data)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(new_data, data_file, indent=4)
        except json.decoder.JSONDecodeError:
            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(new_data, data_file, indent=4)
        else:
            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_input.delete(0, 'end')
            username_input.delete(0, 'end')
            username_input.insert(0, "breimer1@hotmail.com")
            pw_input.delete(0, 'end')

# ---------------------------- FIND PASSWORD ------------------------------- #


def find_password():
    website = website_input.get()
    username = username_input.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
            try:
                password = data[website]["password"]
            except KeyError:
                messagebox.showinfo(title="Not Found", message="No details for the website exist.")
            else:
                for key in data:
                    if key.lower() == website.lower() and username == data[website]["email"]:
                        messagebox.showinfo(title=website, message=f"Email/Username: {username}\nPassword: {password}")
    except FileNotFoundError:
        messagebox.showerror(title=f"FileNotFoundError", message="No Data File Found")


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

website_input = Entry(width=33)
website_input.grid(column=1, row=1)
website_input.focus()

username_label = Label(text="Email/Username:")
username_label.grid(column=0, row=2)

username_input = Entry(width=51)
username_input.grid(column=1, row=2, columnspan=2)
username_input.insert(0, "breimer1@hotmail.com")

pw_label = Label(text="Password:")
pw_label.grid(column=0, row=3)

pw_input = Entry(width=33)
pw_input.grid(column=1, row=3)

gen_pw_button = Button(text="Generate Password", width=14, command=generate_password)
gen_pw_button.grid(column=2, row=3)

add_button = Button(text="Add", width=43, command=save)
add_button.grid(column=1, row=4, columnspan=2)

search_button = Button(text="Search", width=14, command=find_password)
search_button.grid(column=2, row=1)


window.mainloop()
