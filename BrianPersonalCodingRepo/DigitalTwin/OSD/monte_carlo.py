from typing import Callable

# (listof (listof float)) -> (listof (tupleof float))
# Produce a list of tuples to be used as arguments to a single asterick

def mc_arg(lolof: list[list[float]]) -> list[tuple]:
    return list(zip(*lolof)) # !!! can I use the zip object directly instead of converting to a list?

def sample_profile(distribution_type: str) -> list[list[float]]:
    return [[0.0]]

# (tupleof float) -> float) (listof (tupleof float)) -> (listof float)
def monte_carlo(func: Callable, loargs: list[tuple]) -> list[float]:
    mon: list[float]= []
    while True:
        if not loargs:
            return mon
        mon.append(func(*loargs[0]))
        loargs = loargs[1:]

# (listof (listof float)) (listof (float*float)) -> (listof (listof float))
# Produce the probability that a given set of random numbers occurs within a defined range
def rv_prob(lolof: list[list[float]], lobin: list[tuple]) -> list[list[float]]:
    return [[0.0]]
    # while True:
    #     n = 0
    #     prop_matrix = create_prob_matrix(lobin)
    #     if not lolof:
    #         return ...(lolof[0])
    #     lolof = lolof[1:]