from shiny import *
from pathlib import Path
from htmltools import HTMLDependency

sortable_dep = HTMLDependency(
    name = "SortableJS",
    version = "1.15.3",
    source={
            "subdir": "www/sortable/",
        },
    script= {"src": "sortable.js"},
)

def shapes(inputId):
    return ui.tags.div(
        sortable_dep,
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
        id=inputId,
        class_="sortable"
        #class_="js-sortable row",
        #data_hs_sortable_options='{\"animation\": 150, \"ghostClass\": \"sortablejs-custom-chosen-child\"}'
    )

def IsSwitch(input_string):
    one = "1" in input_string
    two = "2" in input_string
    three = "3" in input_string
    four = "4" in input_string
    return (one and two and three and four)

def get_outcome(input_sequence, output_sequence):
    map = {i:n for n,i in enumerate(input_sequence)}
    outcome = [map[o]+1 for o in output_sequence]
    return("".join(str(x) for x in outcome))
    
def compute(formula):
    fml, outcome = formula.split("=")
    fml = fml.split("+")

    #answers = ["".join([str(x) for x in list(a)]) for a in permutations([1, 2, 3, 4])]
    answers = ['1234', '1243', '1324', '1342', '1423', '1432', '2134', '2143', '2314', '2341', 
            '2413', '2431', '3124', '3142', '3214', '3241', '3412', '3421', '4123', '4132', 
            '4213', '4231', '4312', '4321']

    def switch(a, b):
        a = {o:i for o,i in enumerate(a)}
        new = [a[int(n)-1] for n in b]
        return("".join(str(x) for x in new))

    for a in answers:
        # replace x in fmlwith a
        fml_temp = list(map(lambda x: x.replace('x', a), fml))
        out = "1234"
        for i in range(len(fml_temp)):
            out = switch(out, fml_temp[i])
        if out == outcome:
            break
    return(a)

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
    shapes("initial"),
    ui.head_content(ui.include_js("app_py.js")),
    ui.input_text("fml", "Formula:", ""),
    ui.output_text_verbatim("text"),
    shapes("final"),
    #ui.head_content(ui.include_js(Path(__file__).parent / "light-dark.js")),
)

def server(input, output, session):
    initial = reactive.value("")
    final = reactive.value("")
    @output
    @render.text
    def text():
        fml = input.fml().strip()
        type = IsComplete(fml)
        if type=="incomplete": return ''
        if type=="empty":
            if initial()=="" or final()=="": return ''
            else: return get_outcome(initial(), final())
        if type=="short": return compute(fml)
        if type=="long":
            parts, outcome = fml.split("=")
            parts = parts.split("+")
            outcome = get_outcome(parts[0], outcome)
            parts = parts[1:]
            formula = "+".join(parts)
            formula = formula + "=" + outcome
            return compute(formula)
        if type=="shape":
            if initial()=="" or final()=="": return 'Please move the shapes'
            outcome = get_outcome(initial(), final())
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
    def _():
        if input.keyid() == 96:  # clear input when ` or ~ is pressed
            print("clear")
            ui.update_text("fml", value="")


app = App(app_ui, server, debug=True, static_assets= Path(__file__).parent / "www")