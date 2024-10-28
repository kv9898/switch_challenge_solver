from shiny import *
from pathlib import Path
import sortable

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

def IsSwitch(input_string):
    one = "1" in input_string
    two = "2" in input_string
    three = "3" in input_string
    four = "4" in input_string
    return (one and two and three and four)

def GetOutcome(input_sequence, output_sequence):
    map = {i:n for n,i in enumerate(input_sequence)}
    outcome = [map[o]+1 for o in output_sequence]
    return("".join(str(x) for x in outcome))
    
def compute(formula: str) -> str:
    fml, outcome = formula.split("=")
    fml = fml.split("+")
    fml.append(outcome)
    del outcome

    def switch(a: str, b: str) -> str:
        a = {o:i for o,i in enumerate(a)}
        new = [a[int(n)-1] for n in b]
        return("".join(str(x) for x in new))

    def ReverseSwitch(b: str, outcome: str) -> str:
        # Create a list of characters representing 'a' initialized with empty strings
        a = [''] * len(outcome)
        # Iterate over the outcome string and corresponding indices from 'b'
        for i, char in enumerate(outcome):
            # Convert the character from 'b' into an integer index, and place the corresponding 'outcome' character in 'a'
            a[int(b[i])-1] = char
        # Join the list back into a string and return it
        return ''.join(a)
    
    x_index = fml.index('x')
    lhs = fml[:x_index]
    rhs = fml[x_index+1:]

    if len(rhs) == 1:
        rhs = rhs[0]
    else:
        b = rhs[-1]
        for i in range(1, len(rhs)):
            b = ReverseSwitch(rhs[-i-1], b)
        rhs = b
        del b

    match len(lhs):
        case 0:
            return rhs
        case 1:
            return GetOutcome(lhs[0], rhs)
        case _:
            a = lhs[0]
            for l in lhs[1:]:
                a = switch(a, l)
            return GetOutcome(a, rhs,)

def IsComplete(fml):
    if (fml == ""): return "empty"
    if (fml == "x"): return "shape"
    if "=" in fml:
        parts = fml.split("=")
        if len(parts) != 2: return "incomplete"
        outcome = parts[1].strip()
        first_part = fml.split("+")[0]
        if (len(outcome) == 4):
            if (IsSwitch(outcome) and (IsSwitch(first_part) or first_part == "x")):
                return "short"
            elif (sum(map(lambda x: x in outcome, first_part)) == 4):
                return "long"
            else:
                return "incomplete"
        else: return "incomplete"
    if ("+" not in fml): return "incomplete"
    parts = fml.split("+")
    if ("x" not in parts): return "incomplete"
    parts = [p for p in parts if p != "x"]
    if all(map(IsSwitch, parts)):
        return "shape"
    else:
        return "incomplete"

app_ui = ui.page_fluid(
    ui.input_checkbox("shape_hide", "Hide Shapes"),
    ui.panel_conditional("!input.shape_hide",
        shapes("initial")),
    ui.head_content(ui.include_js("app_py.js")),
    ui.input_text("fml", "Formula (press `/~ to clear):", ""),
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
    @reactive.effect
    @reactive.event(input.keyid)
    async def _():
        if input.keyid() == 96:  # clear input when ` or ~ is pressed
            ui.update_text("fml", value="")
            await sortable.update(session, "initial", ["b", "g", "r", "y"])
            await sortable.update(session, "final", ["b", "g", "r", "y"])


app = App(app_ui, server, debug=True, static_assets= Path(__file__).parent / "www")