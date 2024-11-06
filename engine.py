def IsSwitch(input_string: str) -> bool:
    """
    Check if the input string contains the digits '1', '2', '3', and '4' which correspond to the switch positions.

    Args:
        input_string (str): The string to be checked.

    Returns:
        bool: True if all digits '1', '2', '3', and '4' are present in the input string, False otherwise.
    """
    # Check if the string contains the digits '1', '2', '3', and '4'.
    one = "1" in input_string
    two = "2" in input_string
    three = "3" in input_string
    four = "4" in input_string

    # Return True if all digits are present, False otherwise.
    return one and two and three and four


def GetOutcome(input_sequence: str, output_sequence: str) -> str:
    """
    Solves a single switch.

    Args:
        input_sequence (str): The input sequence.
        output_sequence (str): The output sequence.

    Returns:
        str: The single switch.
    """
    # Create a dictionary mapping the characters in the input sequence to their indices
    map = {i: n for n, i in enumerate(input_sequence)}
    # Create a list of characters representing the outcome sequence
    # by using the indices from the map to look up the corresponding
    # characters in the output sequence
    outcome = [map[o] + 1 for o in output_sequence]
    # Join the list into a string and return it
    return "".join(str(x) for x in outcome)


def compute(formula: str) -> str:
    """
    Compute the outcome of the given formula.

    The formula should be a string containing the switch positions and the outcome
    separated by an '=' character.

    Args:
        formula (str): The formula to be computed.

    Returns:
        str: The computed outcome.
    """
    fml, outcome = formula.split("=")
    fml = fml.split("+")
    fml.append(outcome)
    del outcome

    def switch(a: str, b: str) -> str:
        """
        Compute the outcome of a single switch.

        Args:
            a (str): The sequence to be switched.
            b (str): The switch positions.

        Returns:
            str: The computed outcome.
        """
        a = {o: i for o, i in enumerate(a)}
        new = [a[int(n) - 1] for n in b]
        return "".join(str(x) for x in new)

    def ReverseSwitch(b: str, outcome: str) -> str:
        """
        Compute the reverse of a single switch.

        Args:
            b (str): The switch positions.
            outcome (str): The outcome of the switch.

        Returns:
            str: The computed reverse switch.
        """
        # Create a list of characters representing 'a' initialized with empty strings
        a = [""] * len(outcome)
        # Iterate over the outcome string and corresponding indices from 'b'
        for i, char in enumerate(outcome):
            # Convert the character from 'b' into an integer index, and place the corresponding 'outcome' character in 'a'
            a[int(b[i]) - 1] = char
        # Join the list back into a string and return it
        return "".join(a)

    x_index = fml.index("x")
    lhs = fml[:x_index]
    rhs = fml[x_index + 1 :]

    if len(rhs) == 1:
        rhs = rhs[0]
    else:
        b = rhs[-1]
        for i in range(1, len(rhs)):
            b = ReverseSwitch(rhs[-i - 1], b)
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
            return GetOutcome(
                a,
                rhs,
            )


def IsComplete(fml: str) -> str:
    """
    Determines the completeness and type of a formula.
    
    Args:
        fml (str): The formula to be checked.
    
    Returns:
        str: The type of completeness or category of the formula, 
             such as 'empty', 'shape', 'short', 'long', or 'incomplete'.
    """
    if fml == "":
        return "empty"
    if fml == "x":
        return "shape"
    if "=" in fml:
        parts = fml.split("=")
        if len(parts) != 2:
            return "incomplete"
        outcome = parts[1].strip()
        first_part = fml.split("+")[0]
        if len(outcome) == 4:
            if IsSwitch(outcome) and (IsSwitch(first_part) or first_part == "x"):
                return "short"
            elif sum(map(lambda x: x in outcome, first_part)) == 4:
                return "long"
            else:
                return "incomplete"
        else:
            return "incomplete"
    if "+" not in fml:
        return "incomplete"
    parts = fml.split("+")
    if "x" not in parts:
        return "incomplete"
    parts = [p for p in parts if p != "x"]
    if all(map(IsSwitch, parts)):
        return "shape"
    else:
        return "incomplete"


if __name__ == "__main__":
    while True:
        fml = input("Enter the formula: ").strip()
        type = IsComplete(fml)
        match type:
            case "incomplete" | "shape":
                print("The formula is incomplete")
            case "empty":
                import sys

                sys.exit()
            case "short":
                print(compute(fml))
            case "long":
                parts, outcome = fml.split("=")
                parts = parts.split("+")
                outcome = GetOutcome(parts[0], outcome)
                parts = parts[1:]
                formula = "+".join(parts)
                formula = formula + "=" + outcome
                print(compute(formula))
