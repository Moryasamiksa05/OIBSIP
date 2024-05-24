import random
import string
import tkinter as tk

def generate_password(length, has_uppercase, has_numbers, has_symbols):
    characters = string.ascii_lowercase
    if has_uppercase:
        characters += string.ascii_uppercase
    if has_numbers:
        characters += string.digits
    if has_symbols:
        characters += string.punctuation

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def check_password_strength(password):
    strength = 0
    if len(password) >= 8:
        strength += 1
    if any(char.isupper() for char in password):
        strength += 1
    if any(char.isdigit() for char in password):
        strength += 1
    if any(char in string.punctuation for char in password):
        strength += 1

    if strength == 4:
        return "Strong"
    elif strength == 3:
        return "Medium"
    else:
        return "Weak"

def main():
    root = tk.Tk()
    root.title("Password Generator")

    length_var = tk.IntVar()
    has_uppercase_var = tk.BooleanVar()
    has_numbers_var = tk.BooleanVar()
    has_symbols_var = tk.BooleanVar()

    length_label = tk.Label(root, text="Password Length:")
    length_label.pack()
    length_entry = tk.Entry(root, textvariable=length_var)
    length_entry.pack()

    uppercase_check = tk.Checkbutton(root, text="Include Uppercase Letters", variable=has_uppercase_var)
    uppercase_check.pack()
    numbers_check = tk.Checkbutton(root, text="Include Numbers", variable=has_numbers_var)
    numbers_check.pack()
    symbols_check = tk.Checkbutton(root, text="Include Symbols", variable=has_symbols_var)
    symbols_check.pack()

    generate_button = tk.Button(root, text="Generate Password", command=lambda: generate_and_display_password(length_var.get(), has_uppercase_var.get(), has_numbers_var.get(), has_symbols_var.get()))
    generate_button.pack()

    root.mainloop()

def generate_and_display_password(length, has_uppercase, has_numbers, has_symbols):
    password = generate_password(length, has_uppercase, has_numbers, has_symbols)
    strength = check_password_strength(password)
    print("Generated Password:", password)
    print("Password Strength:", strength)

if __name__ == "__main__":
    main()