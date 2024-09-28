"""Script to get the source file of a module in a sandbox."""

import builtins
import inspect
import sys

original_import = builtins.__import__

def custom_import(name, globals=None, locals=None, fromlist=(), level=0) -> object:
    """A custom import to disable reflex_ai.enable.

    Args:
        name: The name of the module to import.
        globals: The global namespace.
        locals: The local namespace.
        fromlist: The list of names to import.
        level: The level in the package hierarchy.

    Returns:
        The imported module.
    """
    if len(name) >= 3 and name[:3] == "tmp":
        name = name[3:]

    return original_import(name, globals, locals, fromlist, level)


def get_module(module_name: str, root_dir: str, scratch_dir: str):
    """Import the module from the scratchpad.

    Args:
        module_name: The name of the module to import.
        root_dir: The root directory of the module.
        scratch_dir: The scratch directory of the module.

    Returns:
        The imported module.
    """
    # Import here to avoid circular imports.
    from reflex_ai.utils.ast_utils import import_module_from_scratch

    # Import the module from the scratchpad.
    if module_name[:3] == "tmp":
        module_name = module_name[3:]
    module = import_module_from_scratch(module_name, root_dir, scratch_dir)
    module_file = inspect.getsourcefile(module)
    return module_file


if __name__ == "__main__":
    builtins.__import__ = custom_import
    module = get_module(sys.argv[1], sys.argv[2], sys.argv[3])
    builtins.__import__ = original_import
    print()
    print(module)
