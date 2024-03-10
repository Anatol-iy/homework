from collections import UserDict
from datetime import datetime

class Field:                     #базовий клас для полів
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)

class Name(Field):            #зберігає імя 
    def __init__(self, value):
        super().__init__(value)
    def __str__(self):
        return "Name:" + super().__str__()

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        
        if not value.isdigit() or len(value) != 10:  # Валідація номера телефону (має бути 10 цифр)
            raise ValueError("Invalid phone number")

class Birthday(Field):
    
    def __init__(self, value):
        if self.is_valid(value):
            super().__init__(value)
    def is_valid(self, value):
        day = ''
        try:
            day = datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            pass #raise ValueError('Invalid day birthday')
        return day 
    

class Record:                        #зберігання інформації про контакт
    def __init__(self, name):
        self.name = Name(name)       #зберігання об'єкта Name в окремому атрибуті.
        self.phones = []             # зберігання списку об'єктів Phone в окремому атрибуті.
        self.birthday = None
    
    def add_phone(self, phone_number):
        phone = Phone(phone_number)  #экземпляр класса Phone c номером телефона
        self.phones.append(phone)    

    def remove_phone(self, phone_number): #удаление
        phone_to_remove = self.find_phone(phone_number)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)


    def edit_phone(self, old_number, new_number): #редагування
        for phone in self.phones:
            if phone.value == old_number:
                phone.value = new_number
                break

    def find_phone(self, phone_number): #найти номер
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None
    
    def add_birthday(self, day_birthday: str):
        self.birthday = Birthday(day_birthday)

    def show_birthday(self):
        if self.birthday:
            return str(self.birthday)
        return 'Birthday not found' 


    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):    #зберігання та управління записами 
   
    def add_record(self, contact):
        self.data[contact.name.value] = contact  # Зберігаємо об'єкт класу Record, а не словник
        print(f"Your contact {contact.name} has been added to AddressBook")

    def find(self, name):
        if name in self.data:
            return self.data[name] 
        else:
            print('This contact is absent in Addressbook')

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            print(f'Contact {name} has been removed in AddressBook')

    def birthdays(self): 
        today = datetime.now()  # Отримуємо поточну дату
        birthdays_by_day = []  
        for name, record in self.data.items():           # Перебираємо користувачів                       
            birthday = datetime.strptime(record.birthday.value, '%d.%m.%Y')  # Конвертуємо до типу date            
            birthday_this_year = birthday.replace(year=today.year) #рік змінюємо на сьогоднішій рік            
            if birthday_this_year < today:  # Перевіряємо, чи вже минув день народження цього року
                birthday_this_year = birthday_this_year.replace(year=today.year + 1) # Розглядаємо дату на наступний рік
            delta_days = (birthday_this_year - today).days # Порівняння з Поточною Датою:
            if delta_days < 7:
                birthdays_by_day.append(name) #Зберігання Результату 
        return birthdays_by_day
book = AddressBook()  
# Створення нової адресної книги
def input_error(error_message=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValueError:
                return error_message
            except TypeError:
                return error_message
            except IndexError:
                return error_message           
            except KeyError:
                return "Contact not found."
        return wrapper
    return decorator
    
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def add_birthdays(args, book):
        name, birthday = args
        if book.find(name):
            book.find(name).add_birthday(birthday)
            print(f"Birthday added for {name}: {birthday}")
        else:
            print(f"Contact {name} not found.")

def show_birthdays(args, book):
    name, = args
    record = book.find(name)
    if record:
        return record.show_birthday()
    else:
        return "Sorry, we don't have a contact with that name"


@input_error("Give me name and phone, please.")
def add_contact(args, book):
    name, phone = args
    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)
    
    

@input_error("Give me name and phone, please.")
def change_contact(args, book): 
    old_name, new_name = args
    record = book.find(old_name)
    if record:
        record.name.value = new_name
        print(f"Контакт {old_name} был изменен на {new_name}")
    else:
        print(f"Контакт {old_name} не найден.")



@input_error("Enter user name, please.")
def show_phone(args, book):
    name, = args
    record = book.find(name)
    if record:
        return '; '.join(phone.value for phone in record.phones)       
    else:
        return "Sorry, we don't have contact with that name"


def show_all(book):
    return '\n'.join(str(record) for record in book.data.values())

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:  #вечный цикл ввода команд пользователя
        user_input = input("Enter a command: ")
        if not user_input:    #Если пользователь ничего не ввел
            print("Please, enter your command.")
            continue 
        else:                 #если ввел, то обращаемся к функции def parse_input(user_input)
            command, *args = parse_input(user_input)

        if command in ["good bye", "close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":            
            print(add_contact(args, book))

        elif command == "change":             
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))
        
        elif command == "add_birthday":
            print(add_birthdays(args, book))

        elif command == "show_birthday":
            print(show_birthdays(args, book))

        elif command == "birthdays":
            print(book.birthdays()) 

        else:
            print("Invalid command.") 

if __name__ == "__main__":   
    main()                   







