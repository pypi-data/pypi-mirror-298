import builtins
from importlib.util import find_spec
import sys
import types


def noop(*args):
    """A no-op function.

    Args:
        *args: The arguments to ignore
    """
    pass


original_import = builtins.__import__


def get_custom_import(modified_file, new_source_code_file):
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
        if len(name) >= 3:
            assert(name[:3] != "tmp")

        try:
            print(f"finding spec for {name}")
            spec = find_spec(name)
        except Exception:
            spec = None
        if spec is not None and spec.origin == modified_file:
            new_module = types.ModuleType(name)
            with open(new_source_code_file, "r") as f:
                new_source = f.read()
            exec(new_source, new_module.__dict__)
            return new_module

        module = original_import(name, globals, locals, fromlist, level)

        # Disable reflex_ai.enable
        if name == "reflex_ai" and fromlist and "enable" in fromlist:
            module.enable = noop
        return module

    return custom_import


def validate_source(
    new_source_code_file: str,
    modified_file: str,
    validation_function: str,
    validation_file: str,
):
    """Validate the source code by running the validation function.

    Args:
        new_source_code_file: The new source code file where the changes are made.
        modified_file: The name of the modified file.
        validation_function: The validation function to run.
        validation_file: The file containing the validation function.
    """
    builtins.__import__ = get_custom_import(modified_file, new_source_code_file)
    try:
        # Read the source code
        file_with_source_to_exec = (
            new_source_code_file
            if modified_file == validation_file
            else validation_file
        )

        with open(file_with_source_to_exec) as f:
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
    validate_source(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
