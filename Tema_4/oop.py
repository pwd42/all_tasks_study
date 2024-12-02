# class Person:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#
#     def introduce(self):
#         print(f"Hello, my name is {self.name} and I am {self.age} years old.")
#
#
# person = Person("Alice", 30)
# person.introduce()


# class Animal:
#     def __init__(self, name):
#         self.name = name
#
#     def speak(self):
#         pass

# class Dog(Animal):
#     def speak(self):
#         print(f"{self.name} says woof!")
#
#
# my_dog = Dog("Buddy")
# my_dog.speak()

#
#
# class BankAccount:
#     def __init__(self, balance):
#         self.__balance = balance
#         self.bank_name = "Bank"
#
#     def deposit(self, amount):
#         self.__balance += amount
#
#     def withdraw(self, amount):
#         self.__balance -= amount
#
#     def get_balance(self):
#         return self.__balance
#
#
# account = BankAccount(100)
# print(account.get_balance())
# account.withdraw(50)
# print(account.get_balance())
#
#

# class Animal:
#     def __init__(self, name):
#         self.name = name
#
#     def speak(self):
#         pass


# class Dog(Animal):
#     def speak(self):
#         print(f"{self.name} says woof!")
#
#
# class Cat(Animal):
#     def speak(self):
#         print(f"{self.name} says meow!")
#
#
# animals = [Dog("Buddy"), Cat("Kitty")]
#
# for animal in animals:
#     animal.speak()

#
#
from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def area(self):
        pass


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius ** 2


class Rectangle(Shape):
    def __init__(self, h, w):
        self.h = h
        self.w = w

    def area(self):
        return self.h * self.w


circle = Circle(5)
rectangle = Rectangle(5, 10)
print(circle.area())
print(rectangle.area())
#
#
class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

    def description(self):
        return f"{self.title} by {self.author}, {self.pages} pages"


my_book = Book("1984", "George Orwell", 328)
print(my_book.description())


class EBook(Book):
    def __init__(self, title, author, pages, filesize):
        super().__init__(title, author, pages)
        self.filesize = filesize

    def description(self):
        return f"{self.title} by {self.author}, {self.pages} pages, file size: {self.filesize}MB"


my_ebook = EBook("1984", "George Orwell", 328, 1.5)
print(my_ebook.description())
