# Smart Error Handler

Smart Error Handler is a packge that helps with fixing errror easier on a python script

Installation:
```
pip install smart-error-handler
```

Usage:
```
from smart_error_handler.smart_error_handler import SmartErrorHandler

handler = SmartErrorHandler()

@handler.handle_error 
def divide_numbers(a, b):
    return a / b


result1 = divide_numbers(10, 2) 
print("Result:", result1)

result2 = divide_numbers(10, 0)  # Should trigger ZeroDivisionError
print("Result:", result2)

result3 = divide_numbers(10, "two")  # Should trigger TypeError
print("Result:", result3)


```
