"""Handle point-and-click element selection in a Reflex app"""

import functools
import inspect
import textwrap
from pathlib import Path
from typing import Any
import reflex as rx

from reflex_ai import paths
from reflex_ai.utils import path_utils, ast_utils

# These components will never be selectable.
ignored_components = [
    rx.accordion.root.__self__,
    rx.accordion.icon.__self__,
    rx.accordion.item.__self__,
    rx.accordion.trigger.__self__,
    rx.alert_dialog.trigger.__self__,
    rx.hover_card.root.__self__,
    rx.hover_card.trigger.__self__,
    rx.hover_card.content.__self__,
    rx.popover.root.__self__,
    rx.popover.trigger.__self__,
    rx.popover.content.__self__,
    rx.recharts.responsive_container.__self__,
    rx.select.content.__self__,
    rx.select.group.__self__,
    rx.select.item.__self__,
    rx.select.root.__self__,
    rx.theme.__self__,
    rx.Fragment,
]
# Radix triggers that fire on_pointer_down events need to be disabled so that on_click works.
neuter_pointer_down = [
    rx.select.trigger.__self__,
]
# For components that do not support on_click at all, wrap these in a box.
box_wrap_components = [
    rx.markdown.__self__,
]
# Preserve a reference to the original create method's function.
og_component_create = rx.Component.create.__func__


class Selection(rx.Base):
    """Capture details of a selected component."""

    # The filename of the component.
    filename: str = ""

    # The function name of the component.
    function_name: str = ""

    # The starting line number of the component.
    start_line: int = 0

    # The ending line number of the component.
    end_line: int = 0

    # The list of modules for the call stack.
    modules: list[dict[str, Any]] = []

    def get_selection_id(self) -> str:
        """Get a unique identifier for the selection.

        Returns:
            A unique identifier for the selection.
        """
        return f"{self.filename}:{self.start_line}-{self.end_line}"

    def get_selection_code(self) -> str:
        """Get the code for the selection.

        Returns:
            The code for the selection.
        """
        return textwrap.dedent(
            "\n".join(
                Path(self.filename)
                .read_text()
                .splitlines()[self.start_line - 1 : self.end_line]
            )
        )

    def get_selection_module(self) -> str:
        """Get the module for the selection.

        Returns:
            The module for the selection.
        """
        if paths.tmp_root_path is None:
            return ""
        module_rel_path = (
            Path(self.filename).relative_to(paths.tmp_root_path).with_suffix("")
        )
        return ".".join(module_rel_path.parts)


class ClickSelectionState(rx.State):
    """Track the currently selected component and the code that created it."""

    # The currently selected component.
    selection: Selection = Selection()

    # The code that created the selected component.
    code: str = ""

    # The id of the currently selected element.
    selected_element: str = ""

    async def handle_click(self, selection: Selection):
        """Handle a click event on a component.

        Args:
            selection: The selected component.
        """
        # Importing here to avoid circular import
        from reflex_ai.playground import SettingsState

        # Open the toolbar
        settings_state = await self.get_state(SettingsState)
        settings_state.is_open = True

        # Set the selection.
        selection = Selection.parse_obj(selection)
        self.selection = selection
        self.selected_element = selection.get_selection_id()
        self.code = selection.get_selection_code()

    async def click_page(self, filename, function):
        """
        Given a file, and the "main component" of the file, handle a click event on the component.

        Args:
            filename: The file to open
            function: The "main component" of the file
        """

        import ast

        with open(filename, "r") as f:
            tree = ast.parse(f.read())

        main_page_node = ast_utils.find_node(tree, "function", function)
        return_statement = ast_utils.find_node(main_page_node, "return", None)

        selection = Selection(
            filename=filename,
            function_name=function,
            start_line=return_statement.lineno,
            end_line=getattr(return_statement, "end_lineno", return_statement.lineno),
            modules=[{"filename": filename, "function": function}],
        )

        await self.handle_click(selection)


def get_selection_props(selection: Selection) -> dict[str, Any]:
    """Generate on_click handler and outline props for selectable components.

    Args:
        selection: The selected component.

    Returns:
        A dictionary of props that includes the on_click handler and outline props.
    """
    return {
        "on_click": ClickSelectionState.handle_click(
            selection
        ).prevent_default.stop_propagation,
        "position": "relative",
        "::before": rx.cond(
            ClickSelectionState.selected_element == f"{selection.get_selection_id()}",
            {
                "content": "''",
                "position": "absolute",
                "top": "-4px",
                "left": "-4px",
                "width": "calc(100% + 8px)",
                "height": "calc(100% + 8px)",
                "backgroundColor": "var(--select-bg)",
                "outline": "2px dashed var(--select-outline)",
                "borderRadius": "0.35rem",
                "zIndex": "999",
                "pointerEvents": "none",
                "display": "block",
            },
            {},
        ),
    }


def component_create_override(base_paths: list[Path]) -> classmethod:
    """Generate an override for Component.create that is active for the given paths.

    Args:
        base_paths: Components originating from modules prefixed by these paths will be clickable.

    Returns:
        A replacement Component.create function that adds an on_click handler where needed.
    """
    base_paths = base_paths + [path_utils.SCRATCH_DIR_NAME]

    @classmethod
    def _component_create_override(cls, *children, **props):
        if cls not in ignored_components:
            # Walk up the stack to find the first frame that originates from a base path.
            stack = inspect.stack()
            for i, frame in enumerate(stack):
                # Skip the module frame.
                if frame.function == "<module>":
                    continue
                
                if "site-packages" in frame.filename:
                    continue

                # If the frame originates from a base path, create the selection.
                if any(frame.filename.startswith(str(p)) for p in base_paths):
                    # The end index is the frame where the playground component is called.
                    end_idx = [frame.function for frame in stack].index("playground")

                    # Find all the modules in the call stack.
                    modules = [
                        {
                            "filename": frame.filename,
                            "function": frame.function,
                        }
                        for frame in stack[i:end_idx]
                    ]

                    # Create the selection.
                    selection = Selection(
                        filename=frame.filename,
                        function_name=frame.function,
                        start_line=frame.lineno,
                        end_line=frame.positions.end_lineno,
                        modules=modules,
                    )
                    down_props = get_selection_props(selection)

                    # If the component is a box wrap component, wrap it in a box.
                    if cls in box_wrap_components:
                        return rx.box(
                            og_component_create(cls, *children, **props),
                            **down_props,
                        )

                    # Add the selection props to the component.
                    props.update(down_props)

                    # If the component is a trigger that fires on_pointer_down, disable it.
                    if cls in neuter_pointer_down:
                        props.setdefault("special_props", set()).add(
                            rx.Var.create(
                                "onPointerDown={(e) => e.preventDefault()}",
                                _var_is_string=False,
                            ),
                        )
                    break
        return og_component_create(cls, *children, **props)

    return _component_create_override


def clickable(base_paths: list[Path] | None = None):
    """A decorator helper to make all components in a given page clickable to select.

    The active selection (filename and line range) is stored in
    ClickSelectionState.selected_element

    The code for the selection is cached in ClickSelectionState._selected_code

    Args:
        base_paths: Components originating from modules prefixed by these paths will be clickable.

    Returns:
        A decorator that adds an on_click handler to the component.
    """
    if base_paths is None:
        base_paths = [Path(".").resolve()]

    def outer(fn):
        @functools.wraps(fn)
        def inner(*args, **kwargs):
            # Override the component create method.
            rx.Component.create = component_create_override(base_paths=base_paths)
            try:
                # Call the page wrapper
                return fn(*args, **kwargs)
            finally:
                # Restore the original component create method.
                rx.Component.create = classmethod(og_component_create)

        # Preserve the original function name to avoid having to specify route in add_page.
        inner.__name__ = fn.__name__
        return inner

    return outer
