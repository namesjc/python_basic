# Python OOP

## 1.Basic

```python
class Employee:
  
    # initialize or construct
    def __int__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first + '.' + last + '@cpmpany.com'
    
    def fullname(self):
        return f'{self.first} {self.last}'
```

```python
# create instance 
emp_1 = Employee('Marco', 'Chan', 5000)
emp_2 = Employee('Test', 'User', 7000)
```

```python
# print employee's email
print(emp_1.email)

# call fullname method
print(emp_1.fullname())
print(emp_2.fullname())

# the equivalent way to call fullname method, need to pass the instance as argument
Employee.fullname(emp_1)
```

## 2.Class variables

class variables are variables that are shared among all instances of the class. Should be the same for each instance.

```python
class Employee:
  
    # class variables
    raise_amount = 1.04
    num_of_emps = 0
      
      # initialize or construct
    def __int__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first + '.' + last + '@company.com'
        Employee.num_of_emps += 1
    
    def fullname(self):
        return f'{self.first} {self.last}'
    
    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amount)
```

```python
# before we create the instance, the value of num_of_emps is 0
print(Employee.num_of_emps)
# create instance 
emp_1 = Employee('Marco', 'Chan', 5000)
emp_2 = Employee('Test', 'User', 7000)
# after we instantiated two instances, the value of num_of_emps is 2
print(Employee.num_of_emps)
```

When we try to access an attribute on an instance, it will first check if the instance contains that attribute and if it doesn't then it will see if the class or any class it inherits from contains that attribute. 

```python
print(Employee.raise_amount)
print(emp_1.raise_amount)
print(emp_2.raise_amount)
```

To better understand class variables, we can print out the namespace of employee.

```python
# The result should not contains raise_amount attribute
print(emp_1.__dict__)
# When we we print the Employee namespace, you should see the raise_amount
print(Employee.__dict__)
```

We can change the raise_amount for the whole class level or instance level

```python
# change the variable for class level
Employee.raise_amount = 1.05
# change the variable for instance level
emp_1.raise_amount = 1.05
# after assign raise_amount for instance, the result of the namespace is different
print(emp_1.__dict__)
```

## 3.classmethods and staticmethods

```python
class Employee:
  
    # class variables
    raise_amt = 1.04
    num_of_emps = 0
    
    # initialize or construct
    def __int__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first + '.' + last + '@company.com'
        Employee.num_of_emps += 1
    
    # instance method
    def fullname(self):
        return f'{self.first} {self.last}'
    
    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amt)
    
    @classmethod
    def set_raise_amt(cls, amount):
        cls.raise_amt = amount
    
    # Additional constructor
    @classmethod
    def from_string(cls, emp_str):
        first, last, pay = emp_str.split('-')
        return cls(first, last, pay)
    
    # static methods don't take the instance(self) or class(cls) as the first argument
    @staticmethod
    def is_workday(day):
        if day.weekday() == 5 or day.weekday == 6:
            return False
        return True
```

```python
# create instance 
emp_1 = Employee('Marco', 'Chan', 5000)
emp_2 = Employee('Test', 'User', 7000)

emp_str_1 = 'John_Deo_7000'
emp_str_2 = 'Steve_Smith_7000'
emp_str_3 = 'Jane_Deo_7000'
```

```python
Employee.set_raise_amt(1.05)
print(Employee.raise_amt)
print(emp_1.raise_amt)
print(emp_2.raise_amt)
```

```python
# Alternative constructor using classmethod
new_emp_1 = Employee.from_string(emp_str_1)
```

```python
import datetime
my_date = datetime.date(2022, 6, 3)
print(Employee.is_workday(my_date))
```

## 4.Inheritance - Creating subclasses

```python
class Employee:
  
    # class variables
    raise_amt = 1.04
    
    # initialize or construct
    def __int__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first + '.' + last + '@cpmpany.com'
    
    # instance method
    def fullname(self):
        return f'{self.first} {self.last}'
    
    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amt)

class Developer(Employee):
    raise_amt = 1.10
    
    # subclass init method
    def __init__(self, first, last, pay, prog_lang):
        # inherit from class
        super.__init__(first, last, pay)
        # add its own init method
        self.prog_lang = prog_lang

class Manager(Employee):
  
    def __init__(self, first, last, pay, employees: list = None):
        super().__init__(first, last, pay)
    # both ways are working
    # Employee.__init__(self, first, last, pay)
        if employees is None:
            self.employees = []
        else:
            self.employees = employees

    def add_emp(self, emp):
        if emp not in self.employees:
            self.employees.append(emp)
    
    def remove_emp(self, emp):
        if emp in self.employees:
            self.employees.remove(emp)
    
    def print_emp(self):
        for emp in self.employees:
            print('-->', emp.fullname())
```

```python
dev_1 = Developer('Marco', 'Chan', 5000)
dev_2 = Developer('Test', 'Employee', 7000)
```

```python
# Developer class inherit the method and attribute from Employee, so we can print out the email
print(dev_1.email)
print(dev_2.email)
# access subclass init value
print(dev_1.prog_lang)
```

The better way to understand inheritance, we can use `help()` function to see the details

```python
print(help(Developer))

class Developer(Employee)
 |  Developer(first, last, pay)
 |  
 |  Method resolution order:
 |      Developer
 |      Employee
 |      builtins.object
 |  
 |  Methods inherited from Employee:
 |  
 |  __init__(self, first, last, pay)
 |      Initialize self.  See help(type(self)) for accurate signature.
 |  
 |  apply_raise(self)
 |  
 |  fullname(self)
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors inherited from Employee:
 |  
 |  __dict__
 |      dictionary for instance variables (if defined)
 |  
 |  __weakref__
 |      list of weak references to the object (if defined)
 |  
 |  ----------------------------------------------------------------------
 |  Data and other attributes inherited from Employee:
 |  
 |  rasie_amt = 1.04
```

Change attribute in subclass won't change the original class

```python
print(dev_1.pay)
dev_1.apply_raise()
print(dev_1.pay)
```

Manager class

```python
mgr_1 = Manager('', '', 90000, [dev_1])
mgr_1.add_emp(dev_2)
mgr_1.remove_emp(dev_1)
```

```python
# print out mgr_1 email
print(mgr_1.email)
# print out the employees that mgr_1 supervisor
mgr_1.print_emps()
```

Check the class relationship

```python
# the result is true
print(isinstance(mgr_1, Manager))
# the result is false
print(isinstance(mgr_1, Developer))
# the result is true
print(isinstance(mgr_1, Employee))

# the result is true
print(issubclass(Developer, Employee))
# the result is true
print(issubclass(Manager, Employee))
# the result is false
print(issubclass(Developer, Manager))
```

## 5.Special(Magic/Dunder) methods

`__repr__` is meant to be an unambiguous representation of an object and should be used for debugging and logging and things like that. It's really meant to be seen by **another developers**

`__str__` is meant to be more of a readable representation of an object and is meant to be used as a display to the **end user**

For more dunder method, refer to [link](https://docs.python.org/3/reference/datamodel.html)

```python
class Employee:
  
    # class variables
    raise_amt = 1.04
    
    # initialize or construct
    def __int__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first + '.' + last + '@cpmpany.com'
    
    # instance method
    def fullname(self):
        return f'{self.first} {self.last}'
    
    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amt)
    
    def __repr__(self):
        return f'Employee('{self.first}', '{self.last}', 'self.pay')'
    
    def __str__(self):
        return f"{self.fullname} - {self.email}"
    
    def __add__(self, other):
        return self.pay + other.pay
    
    def __len__(self):
        return len(self.fullname())
```

```python
emp_1 = Employee('Jun', 'Chen', 5000)
emp_2 = Employee('Test', 'User', 6000)
```

when we try to print out `emp_1`

```python
print(emp_1)

#the __repr__ will help to print out:
Employee('Jun', 'Chen', '5000')
```

After we add `__str__` method, when we try to print out `emp_1`

```python
print(emp_1)

#the __str__ will help to print out:
Jun Chen - Jun.Chen@company.com
```

We can still access `__repr__`, `__str__` sepcifically

```python
print(repr(emp_1))
print(str(emp_1))
or
print(emp_1.__repr__())
print(emp_1.__str__())
```

Before we have a better understanding of another dunder method, let's have a look at **int** and **str** `__add__` method

```python
print(1+3)
$ 4
print(int.__add__(1, 3))
$ 4

print('a' + 'b')
$ 'ab'
print(str.__add__('a', 'b')
$ 'ab'
```

Another example is `len()`

```python
print(len('test'))
print('test'.__len__())
```

Create `__add__` method for **Employee**

```python
print(emp_1 + emp_2)
$ 11000
```

Create `__len__` method for **Employee**

```python
print(len(emp_1))
```

## 6.Property Decorators - Getter, Setters and Deleters

```python
class Employee:

    def __init__(self, first, last):
        self.first = first
        self.last = last
    
    @property
    def email(self):
        return f"{self.first}.{self.last}@email.com"
    
    @property
    def fullname(self):
        return f'{self.first} {self.last}'
    
    @fullname.setter
    def fullname(self, name):
        first, last = name.split(' ')
        self.first = first
        self.last = last
    
    @fullname.deleter
    def fullname(self):
        print('Delete name!')
        self.first = None
        self.last = None
```

```python
emp_1 = Employee('Jun', 'Chen')
```

`@property` decorator allows us to access class function as a attribute 

```python
print(emp_1.first)
# with @property decorator we can access email as a attribute, although it's a function
print(emp_1.email)
# without @property, when we print the fullname of a instance, we need to call the function fullname(), with with @property decorator just access fullname directly
print(emp_1.fullname)
```

We can use setter and deleter

```python
# change the fullname with decorator @fullname.setter, setter is using the name of a property
emp_1.fullname = 'Marco Chan'
```

## 7.Dataclass

在Python中，`dataclass`是一个用于简化类定义的装饰器，它会自动添加一些特殊方法，如`__init__`、`__repr__`和`__eq__`，从而减少了编写样板代码的需要。这个装饰器是在Python 3.7中引入的，并且位于`dataclasses`模块中。

使用`dataclass`装饰器可以更方便地创建数据类，这些类主要用于存储数据，并且通常具有一些自动生成的方法。

### 基本用法

```python
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int
    city: str

# 创建一个Person对象
p = Person("Alice", 30, "New York")
print(p)  # 输出：Person(name='Alice', age=30, city='New York')
```

在上面的例子中，我们定义了一个名为`Person`的简单数据类，它有三个属性：`name`、`age`和`city`。通过使用`@dataclass`装饰器，我们自动获得了`__init__`、`__repr__`和`__eq__`等方法，而无需手动编写它们。

### 特性

1. **自动生成的`__init__`方法**：根据类变量自动生成构造函数，使得创建对象时能够方便地设置属性。
2. **自动生成的`__repr__`方法**：返回一个表示对象的字符串，便于调试和日志记录。
3. **自动生成的`__eq__`方法**：用于比较两个对象是否相等，基于它们的属性值。
4. **可配置性**：`dataclass`装饰器还提供了一些参数，如`init`、`repr`、`eq`、`order`和`unsafe_hash`，用于控制自动生成哪些方法。
5. **冻结实例**：通过设置`frozen=True`，可以创建不可变的实例，类似于元组。
6. **继承支持**：`dataclass`也支持继承，子类可以继承父类的属性和方法。
7. **类型注解**：与`dataclasses`模块一起使用的类型注解不仅提高了代码的可读性，还有助于静态类型检查工具（如mypy）进行类型检查。

### 示例：使用`frozen=True`创建不可变对象

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class ImmutablePoint:
    x: int
    y: int

p = ImmutablePoint(10, 20)
# p.x = 30  # 这将引发AttributeError，因为对象是不可变的
```

### 总结

`dataclass`装饰器是Python中用于简化数据类定义的一个强大工具。它减少了编写样板代码的工作量，同时提供了丰富的配置选项来满足不同的需求。通过使用类型注解，它还能提高代码的可读性和可维护性。
