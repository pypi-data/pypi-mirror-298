import traceback
from .suggestions import get_suggestions
from .logger import Logger

class SmartErrorHandler:
    def __init__(self):
        self.logger = Logger()

    def handler_error(self, func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.log_error(e)
                return None
        return wrapper
    
    def log_error(self, error):
        tb = traceback.format_exc()
        self.logger.log(tb)
        suggestions = get_suggestions(type(error).__name__)
        print(f"Error: {str(error)}")
        print("Suggestions:")
        for suggestion in suggestions:
            print(f"- {suggestion}")
            