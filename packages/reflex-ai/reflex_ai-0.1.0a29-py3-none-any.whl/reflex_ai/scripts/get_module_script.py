"""Script to get the source file of a module in a sandbox."""

import inspect
import sys


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
    module = import_module_from_scratch(module_name, root_dir, scratch_dir)
    module_file = inspect.getsourcefile(module)
    return module_file


if __name__ == "__main__":
    module = get_module(sys.argv[1], sys.argv[2], sys.argv[3])
    print()
    print(module)
