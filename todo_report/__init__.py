# Init all providers
import os
import pkgutil


for loader, module_name, is_pkg in pkgutil.walk_packages([os.path.join(os.path.dirname(__file__), "providers")]):
    loader.find_module(module_name).load_module(module_name)
