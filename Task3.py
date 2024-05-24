# for beginner
import random
import string

def generate_password(length, character_set):
    password = ''
    for _ in range(length):
        password += random.choice(character_set)
    return password

def main():
    print("Random Password Generator")
    print("------------------------")

    length = int(input("Enter password length: "))
    character_set = ''

    print("Choose character set:")
    print("1. Letters (a-z, A-Z)")
    print("2. Numbers (0-9)")
    print("3. Symbols (!, @, #, $, etc.)")
    print("4. All of the above")

    choice = int(input("Enter your choice (1-4): "))

    if choice == 1:
        character_set = string.ascii_letters
    elif choice == 2:
        character_set = string.digits
    elif choice == 3:
        character_set = string.punctuation
    elif choice == 4:
        character_set = string.ascii_letters + string.digits + string.punctuation
    else:
        print("Invalid choice. Exiting.")
        return

    password = generate_password(length, character_set)
    print("Generated password:", password)

if __name__ == "__main__":
    main()