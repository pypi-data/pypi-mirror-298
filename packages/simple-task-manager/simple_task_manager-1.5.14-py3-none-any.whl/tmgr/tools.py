import os
import sys

def file_get_full_path(file_path):
    if file_path:               
        # Check if the path is absolute
        if not os.path.isabs(file_path):
            # If it's not absolute, resolve it relative to the application path
            app_path =sys.path[0] #os.path.dirname(os.path.abspath(__file__))  # Application's base directory
            file_path = os.path.abspath(os.path.join(app_path, file_path))  # Resolve the relative path

