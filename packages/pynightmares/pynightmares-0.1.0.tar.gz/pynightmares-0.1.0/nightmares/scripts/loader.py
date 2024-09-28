import importlib
import os
import sys

def load_all_modules_from_package(package_name):
    package = sys.modules[package_name]
    package_path = package.__path__[0]
    
    for module_name in os.listdir(package_path):
        if module_name.endswith(".py") and module_name != "__init__.py" and module_name != "loader.py":
            module_name = module_name[:-3]
            full_module_name = f"{package_name}.{module_name}"
            importlib.import_module(full_module_name)
