from shiny import *
from htmltools import HTMLDependency

def sortable_dep() -> HTMLDependency:
    sortable_dep = HTMLDependency(
        name = "SortableJS",
        version = "1.15.3",
        source={
                "href": "https://cdnjs.cloudflare.com/ajax/libs/Sortable/1.15.3"
            },
        script= {"src": "Sortable.min.js"},
    )
    return sortable_dep

