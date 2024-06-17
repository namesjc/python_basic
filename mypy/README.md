# Mypy

## Possible type annotations

- numbers (`int`, `float`, `Decimal` ...)
- strings
- collections (`List[int]`, `Dict[str, int]`, `Set[int]` ...) - notice upper case name
- our own classes (`BusinessReport`, `CheckoutController`...)
- `None`
- `Optional`
- lambdas (`Callable[[int], str]`)
- special types `Any` and `NoReturn`
- generics

## Any

- It can be considered a type that has all values and all methods [link](https://www.python.org/dev/peps/pep-0484/#the-any-type)
- It passes the static check, but fails in runtime
- `Any` turns off type checking

```python
from typing import Any

def function_with_any(argument: Any):
    argument.not_existing_method()
    for a in argument:
        print(a)
    argument + 1
    
 # Success: no issues found in 1 source file
```

## NoReturn

- Shows that given function do not return anything
- Cannot create an instance of `NoReturn`
- Can be very useful, I will show it later

```python
def method_that_returns() -> NoReturn:
    return 1

# error: Return statement in function which does not return
```

## Union types

- good for modeling data with different shapes (user is either Admin or Employee)
- types do not have to have a common root
- types from external libraries can be used here as well

```python
from typing import Union

class Admin: pass

class Employee: pass

User = Union[Admin, Employee]

def handle_login(user: User):
    if isinstance(user, Admin):
        print("Admin login")
    else:
        print("User login")
        
handle_login(Admin())
handle_login(Employee())
```

## Optional

- `Optional[T]` is `Union[T, None]`
- Type safe way to indicate that given type can be nullable

### Problem

```python
def function() -> str:
    return None

function() + "suffix"

# In runtime
# TypeError: unsupported operand type(s) for +: 'NoneType' and 'str'

# With mypy
# error: Incompatible return value type (got "None", expected "str")
```

## Type guards (type narrowing)

```python
from typing import Optional

def add_unsafe(number: Optional[int]) -> int:
    return number + 1
# error: Unsupported operand types for + ("None" and "int")
# note: Left operand is of type "Optional[int]"

def add(number: Optional[int]) -> int:
    if number:
        # mypy knows that number is not None here
        return number + 1
    else:
        return 1
```

## Exhaustiveness checking

### Problem

```python
from typing import Union

class Employee: pass


class Manager: pass

class Administrator: pass

User = Union[Employee, Manager, Administrator]

def function(user: User) -> str:
    if isinstance(user, Employee):
        return "Employee"
    else:
        return "Manager"
    
# Success: no issues found in 1 source file
```

### Solution [link](https://github.com/python/typing/issues/735)

```python
def assert_never(x: NoReturn) -> NoReturn:
    raise AssertionError(f"Invalid value: {x!r}")
    
def function(user: User):
    if isinstance(user, Employee):
        return "Employee"
    elif isinstance(user, Manager):
        return "Manager"
    else:
        assert_never(user)
        
# error: Argument 1 to "assert_never" 
# has incompatible type "Administrator"; expected "NoReturn"
```

## Structural polymorphism

- You can define polymorphic relation basing on the structure
- You don't need to modify the type - you can use classes from libraries
- Great for modeling data and extracting common data pieces from unrelated types
- More explicit than union types
- Big disadvantage is that you cannot track implementations - as opposed to inheritance

### Problem

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Admin:
    email: str
    admin_id: str
    
    
@dataclass(frozen=True)
class Employee:
    email: str
    employee_id: str
    
    
def send_email(with_email: Any):
    print(with_email.email)
    
    
send_email(Admin("email", "admin_id"))
send_email(Employee("email", "employee_id"))
send_email(42)
```

### Solution

```python
from typing import Protocol
from dataclasses import dataclass

class WithEmail(Protocol):
    @property
    def email(self) -> str:
        pass
    
    
@dataclass(frozen=True)
class Admin:
    email: str
    admin_id: str
    
    
@dataclass(frozen=True)
class Employee:
    email: str
    employee_id: str
    
    
def send_email(with_email: WithEmail):
    print(with_email.email)
    
    
send_email(Admin("email", "admin_id"))
send_email(Employee("email", "employee_id"))
```

## Generics

- used when we want to have a class, that does not care about what is inside
- gives guarantees that `T` is always the same - `MyList[int]` always work with `int`
- generic parameter says `fill this hole to have a complete type`
- you cannot use just `MyList`, its not a complete type

```python
from typing import TypeVar, Generic


T = TypeVar('T')

class MyList(Generic[T]):
    def append(self, value: T) -> None:
        pass
    
    def pop(self) -> T:
        pass
    
    
intlist = MyList[int]()
intlist.append(5)
value: int = intlist.pop()

intlist.append("str")

# argument 1 to "append" of "MyList" 
# has incompatible type "str"; expected "int"
```

## New Types

- Add another level of type safety 
- Great for documentation

### Problem

```python
order_id = 123
company_id = 3


def find_company_order(company_id: int, order_id: int) -> str:
    return f"company_id={company_id} order_id={order_id}"
    
print(find_company_order(order_id, company_id))
# => company_id=123 order_id=3
```

### Solution

```python
from typing import NewType

OrderId = NewType('OrderId', int)
CompanyId = NewType('CompanyId', int)

order_id = OrderId(123)
company_id = CompanyId(3)

def find_company_order(company_id: CompanyId, order_id: OrderId) -> str:
    return f"company_id={company_id} order_id={order_id}"

find_company_order(order_id, company_id)

# error: Argument 1 to "find_company_order" has incompatible type 
# "OrderId"; expected "CompanyId"
# error: Argument 2 to "find_company_order" has incompatible type 
# "CompanyId"; expected "OrderId"
```

