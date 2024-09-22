from itertools import permutations

def compute(formula):
    fml, outcome = formula.split("=")
    fml = fml.split("+")
    #fml.insert(0, "1234")

    answers = ["".join([str(x) for x in list(a)]) for a in permutations([1, 2, 3, 4])]

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

while True:

    formula = input("Formula: ")

    print(compute(formula))
        

    print("----------------------------------------")
