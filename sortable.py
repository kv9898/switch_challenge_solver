from functools import wraps
from shiny.ui import tags
from htmltools import HTMLDependency

# Define a function to create a HTMLDependency for SortableJS
def dep() -> HTMLDependency:
    """Creates and returns a SortableJS HTML dependency."""
    sortable_dep = HTMLDependency(
        name="SortableJS",
        version="1.15.3",
        source={
            "href": "https://cdnjs.cloudflare.com/ajax/libs/Sortable/1.15.3"
        },
        script={"src": "Sortable.min.js"},
    )
    return sortable_dep

# Define a function to generate a JavaScript script for making an element sortable
def input(inputID, dataID="data-id"):
    """
    Returns a script tag for initializing a Sortable instance on an element.

    Args:
        inputID (str): The ID of the HTML element to apply Sortable to.
        dataID (str): The attribute used to store data-id on sortable items.
    """
    script = f"""
    var el_{inputID} = document.getElementById('{inputID}');
    if (el_{inputID}) {{
        var sortable_{inputID} = new Sortable(el_{inputID}, {{
            dataIdAttr: '{dataID}',
            animation: 150,
            ghostClass: 'sortable-ghost',
            chosenClass: 'sortable-chosen',
            onSort: function (evt) {{
                var order = sortable_{inputID}.toArray();
                Shiny.setInputValue("{inputID}", order);
            }}
        }});
    }} else {{
        console.error("Element with id '{inputID}' not found");
    }}
    """
    return tags.script(script)

# Define a function to handle sorting updates
def output(outputID):
    """
    Returns a script tag for handling updates to the Sortable instance order.

    Args:
        outputID (str): The ID used to identify the sortable instance.
    """
    script = f"""
    Shiny.addCustomMessageHandler("sortable_update_{outputID}", function(message) {{
        if (typeof sortable_{outputID} !== 'undefined') {{
            sortable_{outputID}.sort(message.order);
            Shiny.setInputValue("{outputID}", message.order);
        }} else {{
            console.error("sortable_{outputID} is not defined. Cannot update order.");
        }}
    }});
    """
    return tags.script(script)

# Define a decorator to wrap functions and make their output sortable
def make(ID="inputID", updatable=False):
    """
    Decorator to make a UI component sortable.

    Args:
        ID (str): The keyword argument name to extract the input ID from, defaults to 'inputID', if not found, defaults to the first argument.
        updatable (bool): Whether the sortable order is updatable via Shiny.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            div = [dep(), func(*args, **kwargs)]
            input_id = kwargs.get(ID) if ID in kwargs else (args[0] if len(args) > 0 else None)
            if input_id is None:
                if updatable:
                    print("No input ID provided. Cannot update order.")
                return tags.div(*div)

            # Append input and output scripts if applicable
            div.append(input(input_id))
            if updatable:
                div.append(output(input_id))
            return tags.div(*div)
        return wrapper
    return decorator

# Define a function to update the order of a sortable element
async def update(session, ID, order):
    """
    Sends a custom message to update the order of a sortable element.

    Args:
        session: The Shiny server session object to send the message to.
        ID (str): The ID of the sortable instance to update.
        order (list): The new order of the sortable items.
    """
    type = f"sortable_update_{ID}"
    message = {"order": order}
    await session.send_custom_message(type, message)

