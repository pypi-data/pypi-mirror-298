# my_library/__init__.py

# Import the TracingManager class to make it available at the package level
from .tia_otel_observability_tracer import TracingManager

# You can also define __all__ to specify what gets imported with 'from my_library import *'
__all__ = ["TracingManager"]

