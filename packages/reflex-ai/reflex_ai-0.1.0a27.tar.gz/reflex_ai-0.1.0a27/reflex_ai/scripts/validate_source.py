import builtins
import sys


def noop(*args):
    """A no-op function.

    Args:
        *args: The arguments to ignore
    """
    pass


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
    module = original_import(name, globals, locals, fromlist, level)

    # Disable reflex_ai.enable
    if name == "reflex_ai" and fromlist and "enable" in fromlist:
        module.enable = noop
    return module


def validate_source(source_file: str, validation_function: str):
    """Validate the source code by running the validation function.

    Args:
        source_file: The source code to validate.
        validation_function: The name of the validation function.
    """
    builtins.__import__ = custom_import
    try:
        # Read the source code
        with open(source_file) as f:
            source_to_exec = f.read()

        # Execute the source code.
        env = {}
        exec(source_to_exec, env, env)

        # Run the validation function.
        component_fn = env[validation_function]
        eval(f"{component_fn.__name__}()", env, env)
    finally:
        builtins.__import__ = original_import


if __name__ == "__main__":
    validate_source(sys.argv[1], sys.argv[2])
