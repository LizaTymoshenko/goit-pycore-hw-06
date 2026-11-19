from collections import UserDict
from functools import wraps

def verify_fields(conditions: list, error_message: str = 'Wrong format.'):
    def decorator(func):
        @wraps(func)
        def inner(cls, value):
            conditions_apply = [cond(value) for cond in conditions]
            if all(conditions_apply):
                return func(cls, value)
            else:
                print(error_message)
                return None

        return inner 
    
    return decorator

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    

class Name(Field):
    pass

class Phone(Field):
    @verify_fields(conditions=[lambda val: len(val) == 10, lambda val: val.isdigit()], 
                   error_message='Wrong phone format. Expected 10 digits.')
    def __new__(cls, number):
        return super().__new__(cls)

class Record:
    @verify_fields(conditions=[lambda val: len(val) > 1, lambda val: val.istitle()], 
                error_message='Wrong name format. Name should start from capital letter and contain more thatn 1 letter.')
    def __new__(cls, name):
        return super().__new__(cls)

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, number):
        if number not in [p.value for p in self.phones]:
            new_record = Phone(number)
            if new_record:
                self.phones.append(new_record)
                return 'Phone added.'
            else:
                return 'Phone not added.'
        else:
              return 'Phone already exists.'
              

    def remove_phone(self, number):
        phone = [p for p in self.phones if p.value == number]
        if phone:
            self.phones.remove(phone)
            return 'Phone removed.'
        else:
            return 'Phone does not exist.'


    def find_phone(self, number):
        phone = [p for p in self.phones if p.value == number]
        if phone:
            return phone[0].value
        else:
            return 'Phone not found.'

    def edit_phone(self, old_number, new_number):
        ind = [ind for ind, p in enumerate(self.phones) if p.value == old_number]
        if ind:
            self.phones[ind[0]] = Phone(new_number)
            return 'Phone edited.'
        else:
             return 'Phone not found.'



class AddressBook(UserDict):
    def add_record(self, record: Record):
        if record is None:
            return 'Record object is None. Please provide correct record.'
        elif self.data.get(record.name.value):
            return 'Record with this name already exists.'
        else:
             self.data[record.name.value] = record

    def find(self, name: str):
        return self.data.get(name)
        
    def delete(self, name: str):
        if self.data.get(name):
            self.data.pop(name)
            return 'Record deleted.'
        else:
            return 'Record with this name does not exist. Nothing to delete.'


if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    print(john_record.add_phone("777"))
    print(john_record.add_phone("p10"))

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення запису для jane
    wrong_jane_record = Record("jane")
    book.add_record(wrong_jane_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону в записі John
    found_phone = john.find_phone("5555555555")

    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    print(book.delete("Jane"))

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

