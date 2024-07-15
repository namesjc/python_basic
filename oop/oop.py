import datetime


class Employee:
    # class variable
    raise_amt = 1.04
    num_of_emps = 0

    # constructor
    def __init__(self, first, last, pay):
        # instance variables
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

    # additional constructor
    @classmethod
    def from_string(cls, emp_str):
        first, last, pay = emp_str.split('_')
        return cls(first, last, pay)

    @staticmethod
    def is_workday(day: datetime.date):
        if day.weekday() == 5 or day.weekday() == 6:
            return False
        return True


class Developer(Employee):
    raise_amt = 1.10

    def __init__(self, first, last, pay, prog_lang):
        super().__init__(first, last, pay)
        # equivalent to
        # Employee.__init__(self, first, last, pay)
        self.prog_lang = prog_lang


class Manager(Employee):
    def __init__(self, first, last, pay, employees: list = None):
        super().__init__(first, last, pay)
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
            print("-->", emp.fullname())


# print(Employee.raise_amt)
# emp_1 = Employee('Corey', 'Schafer', 50000)
# print(emp_1.raise_amt)
#
# Employee.set_raise_amt(1.05)
# emp_2 = Employee('Test', 'User', 60000)
# print(emp_2.raise_amt)
#
# emp_str_1 = 'John_Deo_7000'
# Employee.from_string(emp_str_1)
#
# print(Employee.num_of_emps)
#
# my_date = datetime.date(2024, 6, 29)
# print(Employee.is_workday(my_date))

# print(help(Developer))

dev_1 = Developer('Marco', 'Chan', 5000, "Python")
# print(dev_1.email)
# print(dev_1.prog_lang)
dev_2 = Developer('Test', 'Employee', 7000, "Java")
# print(dev_1.pay)
# dev_1.apply_raise()
# print(dev_1.pay)

mgr_1 = Manager('Sue', 'Smith', 90000, [dev_1])

# print(mgr_1.email)
# mgr_1.add_emp(dev_2)
# mgr_1.remove_emp(dev_1)
# print(mgr_1.print_emp())

print(isinstance(mgr_1, Manager))
print(issubclass(Manager, Employee))
