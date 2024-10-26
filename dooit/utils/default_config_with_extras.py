from rich.text import Text
from rich.style import Style

from dooit.api import Todo, Workspace
from dooit.ui.api import DooitAPI
from dooit.ui.api.events import subscribe
from dooit.ui.api.widgets import TodoWidget, WorkspaceWidget
from dooit.ui.events import Startup
from dooit_extras.bar_widgets import Spacer, Mode, TextBox, Clock


# Todo formatters


def todo_desc_formatter(desc: str, todo: Todo):
    text = desc

    if ts := todo.todos:
        text += f" ({len(ts)})"

    if r := todo.recurrence:
        text += f" !{r.days}d"

    return text


def todo_status_formatter(status: str, _: Todo, api: DooitAPI):
    text = "o"
    color = api.app.current_theme.yellow

    if status == "completed":
        text = "x"
        color = api.app.current_theme.green

    if status == "overdue":
        text = "!"
        color = api.app.current_theme.red

    return Text(text, style=Style(color=color, bold=True))


def todo_due_formatter(due, _):
    if not due or due == "none":
        return ""

    text = due.strftime("%Y-%m-%d")

    if due.hour:
        text += f" ({due.strftime('%H:%M')})"

    return text


def todo_urgency_formatter(urgency, _, api: DooitAPI):
    if urgency == 0:
        return ""

    theme = api.app.current_theme
    colors = {
        1: theme.green,
        2: theme.yellow,
        3: theme.orange,
        4: theme.red,
    }

    return Text(
        f"!{urgency}",
        style="bold " + colors.get(urgency, theme.primary),
    )


# Workspace formatters


def workspace_desc_formatter(desc: str, workspace: Workspace):
    text = desc

    if ws := workspace.workspaces:
        text += f" ({len(ws)})"

    return text


@subscribe(Startup)
def key_setup(api: DooitAPI, _):
    api.keys.set("<tab>", api.switch_focus)
    api.keys.set("j", api.move_down)
    api.keys.set("k", api.move_up)
    api.keys.set("i", api.edit_description)
    api.keys.set("d", api.edit_due)
    api.keys.set("a", api.add_sibling)
    api.keys.set("z", api.toggle_expand)
    api.keys.set("Z", api.toggle_expand_parent)
    api.keys.set("g", api.go_to_top)
    api.keys.set("G", api.go_to_bottom)
    api.keys.set("A", api.add_child_node)
    api.keys.set("J", api.shift_down)
    api.keys.set("K", api.shift_up)
    api.keys.set("xx", api.remove_node)
    api.keys.set("c", api.toggle_complete)
    api.keys.set("=,+", api.increase_urgency)
    api.keys.set("-,_", api.decrease_urgency)
    api.keys.set("/", api.start_search)
    api.keys.set("<ctrl+s>", api.start_sort)


@subscribe(Startup)
def layout_setup(api: DooitAPI, _):
    api.layouts.workspace_layout = [WorkspaceWidget.description]
    api.layouts.todo_layout = [
        TodoWidget.status,
        TodoWidget.description,
        TodoWidget.due,
        TodoWidget.urgency,
    ]


@subscribe(Startup)
def formatter_setup(api: DooitAPI, _):
    api.formatter.workspaces.description.add(workspace_desc_formatter)

    api.formatter.todos.status.add(todo_status_formatter)
    api.formatter.todos.description.add(todo_desc_formatter)
    api.formatter.todos.due.add(todo_due_formatter)
    api.formatter.todos.urgency.add(todo_urgency_formatter)


@subscribe(Startup)
def bar_setup(api: DooitAPI, _):
    theme = api.vars.theme

    mode_styles = {
        "NORMAL": Style(bgcolor=theme.primary, color=theme.background_1),
        "INSERT": Style(bgcolor=theme.secondary, color=theme.background_1),
    }

    bar_widgets = [
        Mode(api, mode_styles=mode_styles),
        Spacer(api, width=0),
        Clock(api),
        Spacer(api, width=1),
        TextBox(api, "Dooit"),
    ]

    api.bar.set(bar_widgets)


@subscribe(Startup)
def dashboard_setup(api: DooitAPI, _):
    api.dashboard.set(
        [
            "Welcome to Dooit!",
            "",
            "If you're stuck, press '?' for help.",
        ]
    )