def compute(formula):
    fml, outcome = formula.split("=")
    fml = fml.split("+")

    def IsColor(input_string):
        r = "r" in input_string
        g = "g" in input_string
        b = "b" in input_string
        y = "y" in input_string
        return (r or g or b or y)

    def get_outcome(input_sequence, output_sequence):
        map = {i:n for n,i in enumerate(input_sequence)}
        outcome = [map[o]+1 for o in output_sequence]
        return("".join(str(x) for x in outcome))

    # if outcome and the first element of fml contains any of "y", "b", "g", "red",
    # then we need to execute get_outcome()
    if IsColor(outcome) and IsColor(fml[0]):
        outcome = get_outcome(fml[0], outcome)
        fml = fml[1:]

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

while True:

    formula = input("Formula: ")

    print(compute(formula))
        

    print("----------------------------------------")
