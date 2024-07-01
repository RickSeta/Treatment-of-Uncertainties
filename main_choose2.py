import facade

def ask_until_valid(text):
    codes = [ "ac", "al", "am", "ap", "ba", "ce", "df", "es", "go", "ma", "mg", "ms", "mt", "pa", "pb", "pe", 
    "pi", "pr", "rj", "rn", "ro", "rr", "rs", "sc", "se", "sp", "to" ]
    user_input = input(text)
    while user_input not in codes:
        print("Código de estado inválido!")
        user_input = input(text)
    return user_input

origin = ask_until_valid("Insira o código do estado de origem que deseja analisar\n")
destination = ask_until_valid("Insira o código do estado de destino que deseja analisar\n")

facade.treatment_as_queue(origin, destination, True)