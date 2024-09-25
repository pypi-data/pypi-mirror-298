# stripper/__init__.py

# __init__.py
from .text_utils import strip  # Import the strip function directly

# If you want to provide the Stripper class, you can keep it, but this isn't necessary for basic use.
class Stripper:
    def __call__(self, text):
        return strip(text)

# Create an instance of Stripper (if needed)
stripper_instance = Stripper()

# Allow importing the instance directly as 'strip'
__all__ = ['strip', 'stripper_instance']
