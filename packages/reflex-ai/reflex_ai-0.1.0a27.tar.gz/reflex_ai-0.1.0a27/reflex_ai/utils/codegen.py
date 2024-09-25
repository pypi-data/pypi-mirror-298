import ast
import difflib
import astor
from reflex_ai.utils import ast_utils


def get_ast_and_source(module_name: str) -> tuple[ast.Module, str]:
    """Get the AST and source code of a module.

    Args:
        module_name: The name of the module.

    Returns:
        The AST and source code of the module.
    """
    source = ast_utils.get_module_source(module_name)
    tree = ast.parse(source)
    return tree, source


def find_target_node(
    tree: ast.Module, element_type: str, element_name: str, class_name: str = None
) -> ast.AST:
    """Find the target node in the AST.

    Args:
        tree: The AST of the module.
        element_type: The type of element to find (function, class, or variable).
        element_name: The name of the element to find.
        class_name: The name of the class to search within (if applicable).

    Returns:
        The target node in the AST.

    Raises:
        ValueError: If the class or element is not found.
    """
    if class_name:
        class_node = ast_utils.find_node(tree, "class", class_name)
        if not class_node:
            raise ValueError(f"Class {class_name} not found")
        return ast_utils.find_node(class_node, element_type, element_name)
    return ast_utils.find_node(tree, element_type, element_name)


def generate_diff(previous_source: str, new_tree: ast.Module) -> list[str]:
    """Generate the diff between the previous source and the new tree.

    Args:
        previous_source: The previous source code.
        new_tree: The new AST.

    Returns:
        The diff between the previous source and the new tree.
    """
    new_source = astor.to_source(new_tree)
    return list(difflib.ndiff(previous_source, new_source))


def to_unified_diff(ndiff: str) -> str:
    """Convert a list of diff lines to a unified diff string.

    Args:
        ndiff: The list of diff lines.

    Returns:
        The unified diff string.
    """
    previous_source = "".join(difflib.restore(ndiff, 1))
    new_source = "".join(difflib.restore(ndiff, 2))
    return "\n".join(
        difflib.unified_diff(
            previous_source.splitlines(),
            new_source.splitlines(),
        )
    )


def add_python_element(
    module_name: str, content: str, class_name: str = None
) -> list[str]:
    """Add a new element (class, function, or variable) to a Python file after the imports.

    Args:
        module_name: The name of the module.
        content: The content of the new element.
        class_name: The name of the class to add the element to (if applicable).

    Returns:
        The diff between the previous source and the new source.

    Raises:
        ValueError: If the class is not found.
    """
    tree, previous_source = get_ast_and_source(module_name)
    new_element = ast.parse(content).body[0]

    if class_name:
        class_node = ast_utils.find_node(tree, "class", class_name)
        if not class_node:
            raise ValueError(f"Class {class_name} not found")
        target_body = class_node.body
    else:
        target_body = tree.body

    # Find the position after the last import statement
    insert_position = 0
    for i, node in enumerate(target_body):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            insert_position = i + 1
        else:
            break
    target_body.insert(insert_position, new_element)

    return generate_diff(previous_source, tree)


def update_python_element(
    module_name: str,
    element_type: str,
    element_name: str,
    new_content: str,
    class_name: str = None,
) -> list[str]:
    """Update the source code of an element (class, function, or variable) in a module.

    Args:
        module_name: The name of the module.
        element_type: The type of element to update (class, function, or variable).
        element_name: The name of the element to update.
        new_content: The new content of the element.
        class_name: The name of the class containing the element (if applicable).

    Returns:
        The diff between the previous source and the new source.

    Raises:
        ValueError: If the element is not found.
    """
    if element_type not in ["class", "function", "variable"]:
        raise ValueError(
            f"Invalid element type {element_type} - must be one of 'class', 'function', or 'variable'"
        )

    tree, previous_source = get_ast_and_source(module_name)
    target_node = find_target_node(tree, element_type, element_name, class_name)

    if not target_node:
        raise ValueError(f"{element_type.capitalize()} {element_name} not found")

    new_node = ast.parse(new_content).body[0]

    if element_type == "variable":
        target_node.value = new_node.value
    elif element_type == "function":
        # Update the function signature
        target_node.name = new_node.name
        target_node.args = new_node.args
        target_node.returns = new_node.returns
        # Preserve docstring if present
        for item in target_node.body:
            if isinstance(item, ast.Expr) and isinstance(item.value, ast.Str):
                new_node.body.insert(0, item)
                break
        target_node.body = new_node.body
    else:
        target_node.body = new_node.body

    return generate_diff(previous_source, tree)


def delete_python_element(
    module_name: str, element_type: str, element_name: str, class_name: str = None
) -> list[str]:
    """Delete an element (class, function, or variable) from a module.

    Args:
        module_name: The name of the module.
        element_type: The type of element to delete (class, function, or variable).
        element_name: The name of the element to delete.
        class_name: The name of the class containing the element (if applicable).

    Returns:
        The diff between the previous source and the new source.

    Raises:
        ValueError: If the class or element is not found.
    """
    tree, previous_source = get_ast_and_source(module_name)

    if class_name:
        class_node = ast_utils.find_node(tree, "class", class_name)
        if not class_node:
            raise ValueError(f"Class {class_name} not found")
        class_node.body = [
            node
            for node in class_node.body
            if not (
                (
                    isinstance(node, ast.FunctionDef)
                    and element_type == "function"
                    and node.name == element_name
                )
                or (
                    isinstance(node, ast.Assign)
                    and element_type == "variable"
                    and any(
                        t.id == element_name
                        for t in node.targets
                        if isinstance(t, ast.Name)
                    )
                )
            )
        ]
    else:
        tree.body = [
            node
            for node in tree.body
            if not (
                (
                    isinstance(node, ast.FunctionDef)
                    and element_type == "function"
                    and node.name == element_name
                )
                or (
                    isinstance(node, ast.ClassDef)
                    and element_type == "class"
                    and node.name == element_name
                )
                or (
                    isinstance(node, ast.Assign)
                    and element_type == "variable"
                    and any(
                        t.id == element_name
                        for t in node.targets
                        if isinstance(t, ast.Name)
                    )
                )
            )
        ]

    return generate_diff(previous_source, tree)
