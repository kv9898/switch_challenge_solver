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

def input(inputID, dataID="id"):
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

def make(func, ID = "inputID"):
    @wraps(func)
    def wrapper(*args, **kwargs):
        input_id = kwargs.get(ID) if ID in kwargs else (args[0] if len(args) > 0 else None)

        if input_id is None:
            return tags.div(dep(), func(*args, **kwargs))

        # Call the original function
        print(f"input_id:{input_id}")
        return tags.div(dep(), func(*args, **kwargs), input(input_id))
    return wrapper
    

