from typing import List, Dict
from collections import defaultdict
from functools import wraps
# Types of data in python
x = 5 # int
x = "5" # str
x = (5, "5", 5) # tuple (immutable static) (ordered)
x = {5, "5", 5.0} # set (mutatable non-duplicate) (unordered)
x = {"name": "John", "age": 30} # dict (mutatable key-value) (unordered)
x = [5, "5", "5", "5.0"] # list (mutatable duplicate) (ordered)
x: List[Dict] = [{
    "name": "John",
    "age": 30
}] # List of dict
x = defaultdict(object) # default dict
x["name"] = "John"
x["age"] = 30
x = range(10) # range
x = zip((1, 2, 3), ("a", "b", "c")) # zip
x = enumerate((1, 2, 3)) # enumerate (index, value)
x = True 
x = False
x = None

def add(a: int, b: int) -> int:
    return a + b
add = lambda a, b: a +b
add(1, 2)
def yield_func():
    yield 1
    yield 2
    with open("python/file.txt", "r") as f:
        for line in f:
            yield line.strip()
x = yield_func()
print(next(x))  # 1
print(next(x)) # 2  
try:
    print(next(x)) # file.txt line no 1
    print(next(x)) # file.txt line no 2
    print(next(x)) # stop iteration
    print(next(x)) # stop iteration
except StopIteration:
    print("StopIteration caught")
def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Something is happening before the function is called.")
        func(*args, **kwargs)
        print("Something is happening after the function is called.")
    return wrapper
@my_decorator
def say_hello(name):
    print(f"Hello {name}")
say_hello("John")
my_decorator(say_hello)("John")
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def get_name(self):
        return self.name

class Student(Person):
    class_name = "Student" # class variable
    def __init__(self, name, age, student_id):
        super().__init__(name, age)
        self.student_id = student_id # instance variable
    def get_student_id(self):
        return self.student_id # instance method
    # encapsualtion
    def __private_method(self):
        print("This is a private method") # private method
    def public_method(self):
        self.__private_method() # calling private method
    def __str__(self):
        return f"Student(name={self.name}, age={self.age}, student_id={self.student_id})" # string representation
    # polymorphism
    def __add__(self, other):
        return Student(self.name + other.name, self.age + other.age, self.student_id + other.student_id)

x = Person("John", 30)
y = Student("John", 30, 1)
z = Student("John", 30, 2)
print(x.get_name())
print(y.get_student_id())
y.public_method()
print(y + z)

# arithmetic
import math 
x = 10
x = ((x + 0 - 5) / 10 ) % 10
x = math.floor(x)
math.ceil(x)
math.sqrt(x)
math.pow(x, 2)
round(x)

print(x)

# comparison
x = 5
y = 10
x > y
x < y
x >= y
x <= y
x == y
x != y
# x not in y # TypeError: argument of type 'int' is not iterable
# x in y # TypeError
x and y
x or y
not x

# control flow
if x > y:
    print(f"{x} is greater than {y}")
elif x < y:
    print(f"{x} is less than {y}")
else: 
    print(f"{x} is equal to {y}")

match x:
    case 1:
        print("x is 1")
    case 2:
        print("x is 2")
    case _:
        print("x is not 1 or 2")

# loops
for i in range(10):
    print(i)
for i, val in enumerate((1, 2, 3)):
    print(i, val) # 0 1, 1 2, 2 3
for i, j in zip((1, 2, 3), ("a", "b", "c")):
    print(i, j) # 1 a, 2 b, 3 c
for key, val in {"a": 1, "b": 2, "c": 3}.items():
    print(key, val) # a 1, b 2, c 3
for key in {"a": 1, "b": 2, "c": 3}.keys():
    print(key) # a, b, c
for val in {"a": 1, "b": 2, "c": 3}.values():
    print(val) # 1, 2, 3
while x < y:
    print(x)
    x += 1
x_range = range(10)
# map, filter, reduce don't work directly on range objects like methods
list(map(lambda a: a * 2, x_range))
list(filter(lambda a: a % 2 == 0, x_range))
from functools import reduce
reduce(lambda a, b: a + b, x_range)
sorted([3, 1, 2], key=lambda a: a, reverse=True)

# Comprehensions
# List comprehension
squared = [i * i for i in range(10)]
# Dict comprehension
squared_dict = {i: i * i for i in range(5)}
# Set comprehension
squared_set = {i * i for i in range(10)}

# Exception Handling
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    print("Execution complete")

# Context Managers
class MyContext:
    def __enter__(self):
        print("Entering context")
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        print("Exiting context")

with MyContext() as c:
    print("Inside context")

# Type Hinting
def greeting(name: str) -> str:
    return "Hello " + name

from typing import Optional, Union
def process_data(data: Union[int, float]) -> Optional[str]:
    if data > 10:
        return str(data)
    return None

 