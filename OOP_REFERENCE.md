# Object-Oriented Programming (OOP) Reference

## 4IPO3 Course Curriculum Analysis

This document contains all topics, patterns, and concepts covered in the Object-Oriented Programming course, based on the analysis of projects in `/Users/gianlucatiengo/Documents/Progetti/POO/4IPO3`.

---

## Table of Contents

1. [Fundamental OOP Concepts](#1-fundamental-oop-concepts)
2. [Architectural Patterns](#2-architectural-patterns)
3. [Design Patterns](#3-design-patterns)
4. [Structure and Best Practices](#4-structure-and-best-practices)
5. [Reference Projects](#5-reference-projects)

---

## 1. Fundamental OOP Concepts

### 1.1 Encapsulation

**Definition**: Hide implementation details and protect the internal state of objects.

#### Private Attributes with Name Mangling
```python
class Light:
    def __init__(self):
        self.__color = 1  # Private attribute (double underscore)

    def change(self):
        self.__color += 1
        if self.__color > 3:
            self.__color = 1
```

**Reference file**: `11-POO-basic/work/light.py`

#### Property Decorator (Getter/Setter)
```python
class Car:
    def __init__(self, name):
        self.__name = name
        self.__speed = 0

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, val):
        if val < 0:
            val = 0
        if val > 70:  # Maximum limit
            val = 70
        self.__speed = val
```

**Reference file**: `11-POO-basic/work/car_getset.py`

**Advantages**:
- Automatic validation in setters
- Natural syntax: `car.speed = 100`
- Access control

---

### 1.2 Inheritance

**Definition**: Mechanism that allows a class to inherit attributes and methods from another class.

#### Simple Inheritance
```python
class Compte:
    def __init__(self, owner):
        self.owner = owner
        self.balance = 0

    def deposer(self, somme):
        self.balance += somme

    def retirer(self, somme):
        self.balance -= somme

class CompteCourant(Compte):  # Inherits from Compte
    def transferer(self, compteDest, somme):
        self.retirer(somme)
        compteDest.deposer(somme)
```

**Reference file**: `13-POO-advanced/exo/13-51-02_current_account.py`

#### Using super()
```python
class CompteCourant(CompteRenaissance):
    def __init__(self, owner):
        super().__init__(owner)  # Calls parent constructor
```

**Reference file**: `13-POO-advanced/work/bank/current_account.py`

#### Multiple Inheritance
```python
class Fauna(ABC, JungleElement):  # Inherits from two classes
    def __init__(self, position, water):
        super().__init__(position)  # MRO (Method Resolution Order)
        self._water = water
```

**Reference file**: `13-POO-advanced/work/jungle/fauna.py`

**Key concepts**:
- `super()` calls methods from the parent class
- MRO (Method Resolution Order) determines the method lookup order
- Enables code reuse

---

### 1.3 Polymorphism

**Definition**: Ability of objects from different classes to respond to the same message in different ways.

#### Duck Typing (without inheritance)
```python
class Cat:
    def make_sound(self):
        print("Meow")

class Dog:
    def make_sound(self):
        print("Bark")

# Polymorphism: same method, different behaviors
animal_l = [Cat("Kitty", 2.5), Dog("Fluffy", 4)]
for animal in animal_l:
    animal.make_sound()  # Dynamic binding
```

**Reference file**: `13-POO-advanced/exo/13-55-07_polymorphism_sample.py`

#### Polymorphism with Abstract Base Class
```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def make_sound(self):
        pass

class Cat(Animal):
    def make_sound(self):
        print("Meow")

class Dog(Animal):
    def make_sound(self):
        print("Bark")
```

**Reference file**: `13-POO-advanced/exo/13-55-08_polymorphism_inheritance_sample.py`

#### Operator Overloading
```python
class Fauna:
    def __sub__(self, other):  # Overload - operator
        return self.position - other.position
```

**Principle**: "If it walks like a duck and quacks like a duck, then it is a duck"

---

### 1.4 Abstraction

**Definition**: Hide complexity and show only essential functionalities.

#### Abstract Base Classes (ABC)
```python
from abc import ABC, abstractmethod

class Polygon(ABC):
    @property
    @abstractmethod
    def name(self):
        return "polygon"

    @abstractmethod
    def number_of_sides(self):
        pass

class Triangle(Polygon):
    @property
    def name(self):
        return "triangle"

    def number_of_sides(self):
        print("triangle: I have 3 sides")
```

**Reference file**: `13-POO-advanced/exo/13-55-02_abstract_class_sample.py`

**Characteristics**:
- Abstract classes cannot be instantiated directly
- Subclasses MUST implement all abstract methods
- Defines a contract/interface

---

## 2. Architectural Patterns

### 2.1 Model-View-Concept (MVC-like)

**School System**: Separation between data (Model), logic, and presentation.

```
School (Coordinator)
  ├── Bachelor (Degree Program)
  │    └── Course (Courses)
  └── Student (Students with Registrations)
```

**Reference file**: `13-POO-advanced/work/school/`

#### Structure
```python
class School:
    def __init__(self):
        self.bach_d = {}     # Dictionary of Bachelors
        self.stud_d = {}     # Dictionary of Students

    def subscribe_student(self, stud_name, bach_name, course_l):
        for c in course_l:
            c_ref = self.bach_d[bach_name].get_course(c)
            self.stud_d[stud_name].append_course(c_ref)
```

**Principles**:
- Each class has a specific responsibility (Single Responsibility)
- Classes collaborate through references
- Separation between data management and logic

---

### 2.2 Layered Architecture

**Banking System**: Layering in abstract and concrete levels.

```
CompteRenaissance (Abstract Base)
  ├── CompteCourant (Current Account)
  └── CompteEpargne (Savings Account)
```

**Reference file**: `13-POO-advanced/work/bank/`

```python
class CompteRenaissance(ABC):
    _type = "Compte Renaissance"

    def __init__(self, owner):
        self._owner = owner
        self.balance = 0

    @abstractmethod
    def retirer(self, somme):
        pass

class CompteCourant(CompteRenaissance):
    _type = "Compte Courant"
    __frais_retrait = 0.05

    def retirer(self, somme):
        if not self.__check_balance(somme):
            return
        super().retirer(somme)
        self.balance -= self.__frais_retrait
```

---

## 3. Design Patterns

### 3.1 Singleton Pattern

**Purpose**: Ensure a class has only one instance and provide a global access point.

```python
class Storage:
    __instance = None  # Private single instance

    @classmethod
    def singleton(cls):
        """Lazy initialization"""
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def __init__(self):
        if self.__instance is not None:
            raise Exception("This class is a singleton!")
        self.__data = {}

# Usage:
s = Storage.singleton()
t = Storage.singleton()
print(s is t)  # True - same instance
```

**Reference file**: `17-POO-design-pattern/exo/17-19-06_one_dict_singleton.py`

**Characteristics**:
- Single instance in the application
- Lazy initialization (created only when needed)
- Access through class method

---

### 3.2 Observer Pattern

**Purpose**: Define a one-to-many dependency between objects so that when one object changes state, all its dependents are notified.

```python
class Observable(ABC):
    @abstractmethod
    def attach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def notifyObservers(self) -> None:
        pass

class ConcreteSubject(Observable):
    _observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def notifyObservers(self) -> None:
        for observer in self._observers:
            observer.notify(self._state)

class Observer(ABC):
    @abstractmethod
    def notify(self, subject) -> None:
        pass

class ConcreteObserverA(Observer):
    def notify(self, state) -> None:
        print(f"Observer A reacted: state {state}")
```

**Reference file**: `17-POO-design-pattern/exo/17-16-05_observer.py`

#### Practical Example: Traffic Light and Car
```python
class Light:  # Subject/Observable
    def __init__(self, car):
        self.observer = car
        self.color = 1

    def change(self):
        self.color += 1
        self.notify_observers()

    def notify_observers(self):
        self.observer.notify(self.color)

class Car:  # Observer
    def __init__(self, brand):
        self.brand = brand
        self.running = False

    def notify(self, color):
        if color == 2:  # Green
            self.start()
        elif color == 1:  # Red
            self.stop()
```

**Reference file**: `17-POO-design-pattern/exo/17-16-12_trafic_one2one.py`

---

### 3.3 Strategy Pattern

**Purpose**: Define a family of algorithms, encapsulate them, and make them interchangeable.

```python
class SortStrategy(ABC):
    @classmethod
    @abstractmethod
    def trier(cls, data):
        pass

class TriAlphaDirect(SortStrategy):
    @classmethod
    def trier(cls, data):
        return sorted(data)

class TriAlphaInverse(SortStrategy):
    @classmethod
    def trier(cls, data):
        return sorted(data, reverse=True)

class SortContext:
    __tri_d = {
        "alpha-direct": TriAlphaDirect,
        "alpha-inverse": TriAlphaInverse,
    }

    def __init__(self):
        self.__strategy = None

    def set_strategy(self, strategy_name):
        self.__strategy = self.__tri_d[strategy_name]

    def sort(self, data):
        return self.__strategy.trier(data)

# Usage:
context = SortContext()
context.set_strategy("alpha-direct")
print(context.sort([5, 2, 8, 1]))  # [1, 2, 5, 8]
context.set_strategy("alpha-inverse")
print(context.sort([5, 2, 8, 1]))  # [8, 5, 2, 1]
```

**Reference file**: `17-POO-design-pattern/exo/17-20-02_sort.py`

**Advantages**:
- Algorithms interchangeable at runtime
- Easy to add new strategies
- Eliminates complex if/else conditionals

---

### 3.4 Factory Pattern

**Purpose**: Centralize object creation, hiding instantiation logic.

```python
class Shape(ABC):
    @abc.abstractmethod
    def calculate_area(self):
        pass

    @classmethod
    def factory(cls, name):
        if name == 'circle':
            radius = input("Enter the radius: ")
            return Circle(float(radius))
        elif name == 'rectangle':
            height = input("Enter the height: ")
            width = input("Enter the width: ")
            return Rectangle(int(height), int(width))
        elif name == 'square':
            width = input("Enter the width: ")
            return Square(int(width))

# Usage:
shape = Shape.factory('circle')
print(shape.calculate_area())
```

**Reference file**: `17-POO-design-pattern/exo/17-02-14_shapes_solution.py`

**Advantages**:
- Centralized creation
- Hides complexity
- Easy extension with new types

---

### 3.5 Decorator Pattern

**Purpose**: Add functionality to objects/functions dynamically.

#### Function Decorator
```python
def my_decorator(my_function):
    def inner_function():
        print("function decorator ... ", end='')
        my_function()
        print('How are you?')
    return inner_function

@my_decorator
def greet():
    print('Hello! ', end='')

greet()  # Output: "function decorator ... Hello! How are you?"
```

**Reference file**: `17-POO-design-pattern/exo/17-01-05_decorator.py`

#### Property Decorator
```python
@property
def value_celsius(self):
    return self.__value_celsius

@value_celsius.setter
def value_celsius(self, val):
    if val < -273.15:
        val = -273.15
    self.__value_celsius = val
```

**Reference file**: `11-POO-basic/exo/11-03-05_getset_decorator.py`

#### Class Method Decorator
```python
class Employee:
    __min_age = 25

    @staticmethod
    def isAdult(age):
        return age > 18

    @classmethod
    def factory(cls, name, year):
        current_age = date.today().year - year
        if cls.isAdult(current_age) and current_age >= cls.__min_age:
            return cls(name, current_age)
```

**Reference file**: `17-POO-design-pattern/exo/17-01-07_decorator_classmethod.py`

---

### 3.6 Iterator Pattern

**Purpose**: Provide a way to access elements of a collection sequentially.

```python
class CountDown:
    def __init__(self, start):
        self.__counter = start

    def __iter__(self):
        """Returns the iterator"""
        self.__target = 0
        return self

    def __next__(self):
        """Returns the next element"""
        self.__counter -= 1
        if self.__counter <= self.__target:
            raise StopIteration
        return self.__counter

# Usage:
my_iter = iter(CountDown(5))
while True:
    try:
        print(next(my_iter))
    except StopIteration:
        print("Go!")
        break
```

**Reference file**: `17-POO-design-pattern/exo/17-13-06_iter_next_class.py`

**Required methods**:
- `__iter__()` - Returns self
- `__next__()` - Returns next element or raises StopIteration

---

### 3.7 Builder/Composite Pattern

**Purpose**: Build complex objects step by step.

```python
class HtmlObject(ABC):
    def __init__(self, contents=""):
        self.contents = contents
        self.body = []

    def make_body(self):
        body_s = ""
        for o in self.body:
            body_s += str(o)
        return body_s

    def appendElement(self, o):
        self.body.append(o)

class HtmlPageBuilder(HtmlObject):
    def __str__(self):
        body_s = self.make_body()
        return f"""
        <html>
        <head></head>
        <body>
            {body_s}
        </body>
        </html>
        """

# Usage:
builder = HtmlPageBuilder()
section = HtmlSection()
builder.appendElement(section)
div1 = HtmlDiv("Hello World")
section.appendElement(div1)
print(builder)
```

**Reference file**: `13-POO-advanced/work/page_builder/`

---

## 4. Structure and Best Practices

### 4.1 Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Class | PascalCase | `Car`, `Stock`, `CompteRenaissance` |
| Method | snake_case | `get_course()`, `retirer()` |
| Public attribute | snake_case | `self.speed`, `self.balance` |
| Private attribute | `__snake_case` | `self.__color`, `self.__stock` |
| Protected attribute | `_snake_case` | `self._position`, `self._water` |
| Class constant | UPPER_CASE | `MAX_SPEED`, `MIN_AGE` |

### 4.2 Standard Class Structure

```python
class ClassName:
    """Class docstring"""

    # Class attributes
    _class_attribute = value

    def __init__(self, param1, param2):
        """Constructor"""
        self._protected = param1
        self.__private = param2

    def __str__(self):
        """String representation"""
        return f"ClassName: {self._protected}"

    @property
    def public_property(self):
        """Getter"""
        return self.__private

    @public_property.setter
    def public_property(self, value):
        """Setter with validation"""
        if value < 0:
            value = 0
        self.__private = value

    def public_method(self):
        """Public method"""
        self.__private_method()

    def __private_method(self):
        """Private method"""
        pass

    @classmethod
    def class_method(cls):
        """Class method"""
        pass

    @staticmethod
    def static_method():
        """Static method"""
        pass
```

### 4.3 Applied SOLID Principles

#### Single Responsibility Principle
Each class has a single responsibility:
```python
class School:          # Manages the school
class Bachelor:        # Manages a degree program
class Course:          # Manages a course
class Student:         # Manages a student
```

#### DRY (Don't Repeat Yourself)
```python
class CompteCourant(CompteRenaissance):
    def retirer(self, somme):
        if not self.__check_balance(somme):
            return
        super().retirer(somme)  # Reuses parent logic
```

#### Open/Closed Principle
Open for extension, closed for modification:
```python
# New strategies can be added without modifying SortContext
class TriNumericDirect(SortStrategy):
    @classmethod
    def trier(cls, data):
        return sorted(data, key=lambda x: int(x))
```

---

## 5. Reference Projects

### Banking System
**Path**: `13-POO-advanced/work/bank/`

**Concepts**: Inheritance, abstract classes, validation, encapsulation

**Classes**:
- `CompteRenaissance` - Abstract base class
- `CompteCourant` - Current account with fees
- `CompteEpargne` - Savings account with interest

---

### School System
**Path**: `13-POO-advanced/work/school/`

**Concepts**: MVC, many-to-many relationships, composition

**Classes**:
- `School` - Central coordinator
- `Bachelor` - Degree management
- `Course` - Course management
- `Student` - Student management

---

### Traffic Light System
**Path**: `17-POO-design-pattern/exo/17-16-12_trafic_one2one.py`

**Concepts**: Observer pattern, one-to-one relationship

**Classes**:
- `Light` - Subject/Observable (traffic light)
- `Car` - Observer (car reacting to traffic light)

---

### Jungle Simulation
**Path**: `13-POO-advanced/work/jungle/`

**Concepts**: Multiple inheritance, composition, simulation

**Classes**:
- `JungleElement` - Base class with position
- `Fauna` - Abstract class for animals
- `Prey` - Prey that eats plants
- `Plant` - Plants in the jungle

---

### Page Builder
**Path**: `13-POO-advanced/work/page_builder/`

**Concepts**: Builder/Composite pattern, nesting

**Classes**:
- `HtmlObject` - Abstract base class
- `HtmlPageBuilder` - Page builder
- `HtmlSection`, `HtmlDiv`, `HtmlP` - HTML elements

---

## Summary Statistics

```
Total Python files analyzed: 194
├── Python Base: 4 files
├── OOP Basic: 45 files (23%)
├── OOP Advanced: 68 files (35%)
└── Design Patterns: 38 files (20%)

Language: Python 3.x
Modules used: abc, datetime, random, types
```

---

## Topics Covered Checklist

- [x] Classes and Objects
- [x] Constructors (`__init__`)
- [x] Instance methods
- [x] Attributes (public, private, protected)
- [x] Encapsulation
- [x] Property decorators (`@property`, `@setter`)
- [x] Inheritance (simple, multiple)
- [x] Polymorphism (duck typing, ABC)
- [x] Abstract classes (ABC, `@abstractmethod`)
- [x] Special methods (`__str__`, `__sub__`, `__iter__`, `__next__`)
- [x] Class methods (`@classmethod`)
- [x] Static methods (`@staticmethod`)
- [x] Singleton Pattern
- [x] Observer Pattern
- [x] Strategy Pattern
- [x] Factory Pattern
- [x] Decorator Pattern
- [x] Iterator Pattern
- [x] Builder/Composite Pattern
- [x] MVC Architecture
- [x] Layered Architecture
- [x] SOLID Principles
- [x] DRY Principle

---

**Note**: This document is based on the complete analysis of 194 Python files in the folder `/Users/gianlucatiengo/Documents/Progetti/POO/4IPO3`. For each concept, reference files are indicated for further study and examples.
