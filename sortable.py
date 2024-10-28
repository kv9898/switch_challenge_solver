from functools import wraps
from shiny.ui import tags
from htmltools import HTMLDependency

# __all__ = ["sortable_dep", "sortable_input"]

def dep() -> HTMLDependency:
    sortable_dep = HTMLDependency(
        name = "SortableJS",
        version = "1.15.3",
        source={
                "href": "https://cdnjs.cloudflare.com/ajax/libs/Sortable/1.15.3"
            },
        script= {"src": "Sortable.min.js"},
    )
    return sortable_dep

def input(inputID, dataID="data-id"):
    script =  f"""
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

def output(outputID):
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

def make(ID = "inputID", updatable = False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            div = [dep(), func(*args, **kwargs)]
            input_id = kwargs.get(ID) if ID in kwargs else (args[0] if len(args) > 0 else None)
            if input_id is None:
                if updatable:
                    print("No input ID provided. Cannot update order.")
                return tags.div(*div)

            # Call the original function
            div.append(input(input_id))#.append(output(input_id))
            if updatable:
                div.append(output(input_id))
            return tags.div(*div)
        return wrapper
    return decorator

async def update(session, ID, order):
    type = f"sortable_update_{ID}"
    message = {"order": order}
    await session.send_custom_message(type, message)

    

