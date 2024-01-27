# float int -> (listof float)
# Produce a list that contains the given float the given number of times
def generate_list_from_number(f: float, i0: int) -> list[float]:
    def inner_f(i: int,acc: list[float]) -> list[float]:
        while True:
            if i == 0:
                return acc
            else:
                temp_list: list[float] = acc
                temp_list.append(f)
                acc = temp_list
                i = i - 1
    return inner_f(i0,[])

# (listof (listof float)) -> (listof (tupleof float))
# Produce a list of tuples to be used as arguments to a single asterick
def generate_arg_list(lolof: list[list[float]]) -> list[tuple]:
    return list(zip(*lolof)) # !!! can I use the zip object directly instead of converting to a list?