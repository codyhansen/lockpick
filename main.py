import string
import random
import JSONFileManager as fm
from tkinter import *
from tkinter import filedialog

PROGRAM_NAME = "Lockpick"
VERSION = "0.0.1"


def generate_password(chars, length=15):
    password = ""

    for i in range(length):
        char_index = random.randint(0, len(chars)-1)
        password += chars[char_index]

    return password


def generate_pick():
    pick = ""

    for i in range(8):
        pick += str(random.randint(1, 9))

    pick += str(random.randint(2, 4))

    return pick


def encrypt(password, pick, chars):
    encrypted_pass = ""
    shift_interval = int(pick[-1])
    shift_increment = pick[:len(pick)-1]

    for i in range(len(password)):

        shift_amount = int(shift_increment[i & len(shift_increment) - 1])
        char_index = chars.index(password[i])

        if not i % shift_interval:
            new_char = chars[char_index - shift_amount]
        else:
            new_char = chars[(char_index + shift_amount) % len(chars)]

        encrypted_pass += new_char

    return encrypted_pass


def decrypt(password, pick, chars):
    decrypted_pass = ""
    shift_interval = int(pick[-1])
    shift_increment = pick[:len(pick) - 1]

    for i in range(len(password)):

        shift_amount = int(shift_increment[i & len(shift_increment) - 1])
        char_index = chars.index(password[i])

        if not i % shift_interval:
            new_char = chars[(char_index + shift_amount) % len(chars)]
        else:
            new_char = chars[char_index - shift_amount]

        decrypted_pass += new_char

    return decrypted_pass


def run_gui(chars):
    window = Tk()
    window.geometry('300x300')

    window.title(PROGRAM_NAME + " " + VERSION)

    filepath = ""

    def create_file():
        path = filedialog.askdirectory() + "/index.lp"
        file_start = {"passwords": []}
        fm.write_file(path, file_start)
        global filepath
        filepath = path

    def select_file():
        path = filedialog.askopenfilename(filetypes=(('Lock files', '*.lp'), ('All files', '*.*')))
        global filepath
        filepath = path

    def save_password():
        encrypted_pass = encrypt(pass_create_text.get(), pick_text.get(), chars)

        global filepath
        pass_result = fm.read_file(filepath)
        new_pass = {"website": web_create_text.get().lower(), "password": encrypted_pass}
        pass_result["passwords"].append(new_pass)
        fm.write_file(filepath, pass_result)

    def recover_password():
        global filepath
        pass_result = fm.read_file(filepath)
        for lock in pass_result["passwords"]:
            if lock["website"] == web_recover_text.get().lower():
                pass_recover_text.delete(0, END)
                decrypted_pass = decrypt(lock["password"], pick_text.get(), chars)
                pass_recover_text.insert(0, decrypted_pass)

    def populate_pick():
        pick_text.delete(0, END)
        pick_text.insert(0, generate_pick())

    def populate_pass():
        pass_create_text.delete(0, END)
        pass_create_text.insert(0, generate_password(chars))

    create_file_button = Button(window, text="Create File", command=create_file)
    select_file_button = Button(window, text="Select File", command=select_file)

    pick_label = Label(window, text="Enter or generate pick:")
    pick_text = Entry(window)
    generate_pick_button = Button(window, text="Generate", command=populate_pick)

    create_label = Label(window, text="Store new password:")
    web_create_label = Label(window, text="Website:")
    pass_create_label = Label(window, text="Password:")
    web_create_text = Entry(window)
    pass_create_text = Entry(window)

    generate_pass_button = Button(window, text="Generate", command=populate_pass)
    save_button = Button(window, text="Save Password", command=save_password)

    recover_label = Label(window, text="Recover password:")
    web_recover_label = Label(window, text="Website:")
    pass_recover_label = Label(window, text="Password:")
    web_recover_text = Entry(window)
    pass_recover_text = Entry(window)
    recover_pass_button = Button(window, text="Recover Password", command=recover_password)

    create_file_button.grid(row=0, column=0)
    select_file_button.grid(row=0, column=1)

    pick_label.grid(row=1, column=0)
    pick_text.grid(row=2, column=0)
    generate_pick_button.grid(row=2, column=1)

    create_label.grid(row=3, column=0)
    web_create_label.grid(row=4, column=0)
    pass_create_label.grid(row=4, column=1)
    web_create_text.grid(row=5, column=0)
    pass_create_text.grid(row=5, column=1)

    generate_pass_button.grid(row=6, column=1)
    save_button.grid(row=7, column=0)

    recover_label.grid(row=8, column=0)
    web_recover_label.grid(row=9, column=0)
    pass_recover_label.grid(row=9, column=1)
    web_recover_text.grid(row=10, column=0)
    pass_recover_text.grid(row=10, column=1)
    recover_pass_button.grid(row=11, column=0)

    window.mainloop()


if __name__ == "__main__":

    char_list = string.ascii_letters + string.digits + string.punctuation

    run_gui(char_list)
