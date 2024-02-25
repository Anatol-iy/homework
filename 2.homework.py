class AddressBook:
    def __init__(self):
        self.contacts = {}

    def add_contact(self, name, phone):
        self.contacts[name] = phone    
        return "Contact added."

    def change_contact(self, name, new_phone):
        if name in self.contacts:
            self.contacts[name] = new_phone
            return "Contact updated."
        else:
            return "Contact not found."

    def show_phone(self, name):
        if name in self.contacts:
            return self.contacts[name]
        else:
            return "Contact not found."

    def show_all(self):
        if not self.contacts:
            return "No contacts available."
        else:
            return "\n".join(f"{name}: {phone}" for name, phone in self.contacts.items())


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        if not user_input:
            print("Please, enter your command.")
            continue
        else:
            command, args = parse_input(user_input)

        if command in ["good bye", "close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            name, phone = args
            print(book.add_contact(name, phone))

        elif command == "change":
            name, new_phone = args
            print(book.change_contact(name, new_phone))

        elif command == "phone":
            name = args[0] if args else None
            print(book.show_phone(name))

        elif command == "all":
            print(book.show_all())

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()