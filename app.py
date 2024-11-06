from shiny import *
from pathlib import Path
import shiny_sortable as sortable
from engine import *

@sortable.make(updatable = True)
def shapes(inputID):
    return ui.tags.div(
        ui.tags.img(src="img/blue.png", 
            class_="item",
            style="width:50px; height:50px; margin: 5px;",
            **{'data-id': 'b'}),
        ui.tags.img(src="img/yellow.png", 
            class_="item",
            style="width:50px; height:50px; margin: 5px;",
            **{'data-id': 'y'}),
        ui.tags.img(src="img/green.png", 
            class_="item",
            style="width:50px; height:50px; margin: 5px;",
            **{'data-id': 'g'}),
        ui.tags.img(src="img/red.png",
            class_="item", 
            style="width:50px; height:50px; margin: 5px;",
            **{'data-id': 'r'}),
        id=inputID,
        class_="sortable")
        # sortable.input(inputID),

app_ui = ui.page_fluid(
    ui.head_content(ui.include_js("app_py.js")),
    ui.tags.head(
        ui.tags.style(
            ".container-fluid {  max-width: 300px;}",
            type="text/css"
        )
    ),
    ui.input_checkbox("shape_hide", "Hide Shapes"),
    ui.panel_conditional("!input.shape_hide",
        shapes("initial")),
    "Formula (press `/~ to ",
    ui.input_action_link("clear", "Clear"),
    "):",
    ui.input_text("fml", "", ""),
    ui.output_text_verbatim("text"),
    ui.panel_conditional("!input.shape_hide",
    shapes("final")),
)

def server(input, output, session):
    initial = reactive.value("")
    final = reactive.value("")
    @output
    @render.text
    def text():
        fml = input.fml().strip()
        type = IsComplete(fml)
        match type:
            case "incomplete": return ""
            case "empty":
                if initial()=="" or final()=="": return ''
                else: return GetOutcome(initial(), final())
            case "short": return compute(fml)
            case "long":
                parts, outcome = fml.split("=")
                parts = parts.split("+")
                outcome = GetOutcome(parts[0], outcome)
                parts = parts[1:]
                formula = "+".join(parts)
                formula = formula + "=" + outcome
                return compute(formula)
            case "shape":
                if initial()=="" or final()=="": return 'Please move the shapes'
                outcome = GetOutcome(initial(), final())
                formula = fml + "=" + outcome
                return compute(formula)

    @reactive.effect
    @reactive.event(input.initial)
    def _():
        # This block of code will be triggered whenever input.initial() changes
        initial.set(''.join(input.initial()))
    @reactive.effect
    @reactive.event(input.final)
    def _():
        # This block of code will be triggered whenever input.initial() changes
        final.set(''.join(input.final()))
    
    async def clear():
        ui.update_text("fml", value="")
        await sortable.update(session, "initial", ["b", "g", "r", "y"])
        await sortable.update(session, "final", ["b", "g", "r", "y"])
    @reactive.effect
    @reactive.event(input.key)
    async def _():
        if input.key() == "`":  # clear input when ` or ~ is pressed
            await clear()
    @reactive.effect
    @reactive.event(input.clear)
    async def _():
        await clear()

app = App(app_ui, server, static_assets= Path(__file__).parent / "www")