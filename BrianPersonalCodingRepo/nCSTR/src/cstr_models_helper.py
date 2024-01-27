import numpy as np
import numerical_methods as nm
import list_funcs as lf

# y(i) is the output concentration of CSTR for each component
# y0(i) is the initial input concentration of CSTR for each component
# m_in is the input mass flow rate of CSTR
# m3n is the output mass flow rate of CSTR n of N
# m4n is the backflow mass flow rate from CSTR n to CSTR n-1 of N
# x is the number of material streams
# N is the number of total CSTRs (and consequently the total number of differential equations)
# n is the current CSTR differential equation (i.e. Differential equation of CSTR n of N)
# Ouput (dydt) is a matrix containing CSTR output concentration change w.r.t. time and is formatted as follows: dydt[component number i][CSTR number n]

# TODO int -> (listof float)
# Produce a list of calculated mass outputs for each cstr in the series whose size is defined by the input number of cstr
def generate_mass_out_list(m_in: float,dMndt: float,backmix: float,number_of_cstr: int) -> list[float]:
    m_out_list: list[float] = []
    for n in range(number_of_cstr):
        if (n + 1) == number_of_cstr: m_out_list.append(m_in - (number_of_cstr*dMndt)) #base case --> # cstr converted to base 0
        else: 
            if (backmix < 0) or (backmix >= 1): raise RuntimeError("Backmixing variable must be between [0, 1)")
            else: m_out_list.append((m_in - ((n+1)*dMndt))/(1-backmix))
    return m_out_list

# float float float float -> float
# Produce the resulting change in y (dydt) for a single CSTR in series: m_in*(y0[x] - y[x])/Mn
def single_cstr(y: float,y_0: float,m_in: float,mass_n: float) -> float:
    if mass_n <= 0: raise RuntimeError("Mass variable cannot be zero or negative")
    else: return (m_in*(y_0 - y))/mass_n

# float float float float float float float -> float
# Produce the resulting change in y (dydt) for the first CSTR in a series of CSTRs: (m_in*(y0[x] - y[x][n]) + q*m[n]*(y[x][n+1] - y[x][n]))/Mn
def multi_1_cstr(y_n: float,y_n_1: float,y_0: float,m_in: float,m_out_n: float,mass_n: float,backmix: float) -> float:
    if mass_n <= 0: raise RuntimeError("Mass variable cannot be zero or negative")
    else: return (m_in*(y_0 - y_n) + backmix*m_out_n*(y_n_1 - y_n))/mass_n

# float float float float float float float -> float
# Produce the resulting change in y (dydt) for the xth CSTR in a series of CSTRs: (m[n-1]*(y[x][n-1] - y[x][n]) + q*m[n]*(y[x][n+1] - y[x][n]))/Mn
def multi_x_cstr(y_n: float,y_n_1: float,y_n_1prev: float,m_out_n: float,m_out_n_1prev: float,mass_n: float,backmix: float) -> float:
    if mass_n <= 0: raise RuntimeError("Mass variable cannot be zero or negative")
    else: return (m_out_n_1prev*(y_n_1prev - y_n) + backmix*m_out_n*(y_n_1 - y_n))/mass_n

# float float float float -> float
# Produce the resulting change in y (dydt) for the last CSTR in a series of CSTRs: (m[n-1]*(y[x][n-1] - y[x][n]))/Mn
def multi_N_cstr(y_n: float,y_n_1prev: float,m_out_n_prev: float,mass_n: float) -> float:
    if mass_n <= 0: raise RuntimeError("Mass variable cannot be zero or negative")
    else: return (m_out_n_prev*(y_n_1prev - y_n))/mass_n


def memoize(func):
    cache = {}

    def memoized_func(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    return memoized_func

# (listof float) float (listof float) (listof float) float float float -> (listof float)
# Produce a list of concentration differentials(dydt) for all cstrs in series
def calculate_stream_concentration(y: list[float],y_0: float,m_out: list[float],mass_n: float,backmix: float,m_in: float) -> list[float]:
    N: int = len(y)
    if not(y): return []
    elif N == 1: return single_cstr(y[0],y_0,m_in,mass_n)
    else: 
        acc: list[float] = []
        for n in range(N):
            if n == 0: acc.append(multi_1_cstr(y[n],y[n + 1],y_0,m_in,m_out[n],mass_n,backmix))
            elif n < (N - 1): acc.append(multi_x_cstr(y[n],y[n + 1],y[n - 1],m_out[n],m_out[n - 1],mass_n,backmix))
            else: acc.append(multi_N_cstr(y[n],y[n - 1],m_out[n - 1],mass_n))
        return acc

# (listof float) -> (listof float)
# Produce a list of the difference between each mass
def change_in_mass(mass0: list[float]) -> list[float]:
    if not(mass0): return []
    else:
        def inner_f(mass: list[float],acc1: list[float],acc2: float) -> list[float]:
            for i in iter(mass):
                temp_list: list = acc2
                temp_list.append(i - acc1)
                acc1 = i
                acc2 = temp_list
            return acc2
        return inner_f(mass0,mass0[0],[])

# (listof (listof float)) (listof float) (listof float) float float float int int -> (listof (listof float))
# Produce a series of ODEs for an undefined (n) number of CSTRs in series with X input componenets (called streams). 
# NOTE:The resulting list should contain an outer list with size = X (# of streams) and inner list with size N (# of CSTRs in series)
def n_cstr_ode(y: list[list[float]],y_0: list[float],m_out: list[float],mass_n: float,backmix: float,m_in: float) -> list[list[float]]:
    if not(y): return []
    else: return [calculate_stream_concentration(stream,y_0x,m_out,mass_n,backmix,m_in) for (stream, y_0x) in zip(y,y_0)]
    

# (listof (listof float)) (listof float) (listof float) float (listof float) -> (listof (listof (listof float)))
# Produce a list of numerical solver outputs (per second) for a given functions
# NOTE: [x_n,y_rk4_n] = rk4_2d(cstrN, x0 = 0, y0 = yCstr, xn = 1, n=10, args=(yIn[t,::], massReal[t], dMdt[t], q, mIn[t]))
    #def replay_ode_funcs(y: list[list[float]],y_input: list[list[float]],mass: list[float],backmix: float,mass_in: list[float]) -> list[list[list[float]]]:
def replay_ode_funcs(func: callable,y: list[list[float]],loargs0: list[tuple]) -> list[list[list[float]]]:
    def inner_f(loargs: list[tuple],acc1: list[list[float]],acc2: list[list[list[float]]]) -> list[list[list[float]]]:
        for tu in iter(loargs):
            [x_n,temp_list] = nm.rk4_2d(func,x0 = 0,y0 = acc1,xn = 1,n=10,args=(tu))
            acc2.append(temp_list.tolist())
            acc1 = temp_list[9,::]
        return acc2
    return inner_f(loargs0,y,[])

# (listof float) int -> (listof (listof float))
# Produce a set of initial conditions to be used by the ODE solver for CSTR ordinary differential equations
def generate_initial_conditions(y_0_0: list[float],number_of_cstr: int) -> list[list[float]]:
    def inner_f(y_0: list[float], acc: list[list[float]]) -> list[list[float]]: 
        for value in iter(y_0):
            temp_list: list[list[float]] = acc
            temp_list.append(lf.generate_list_from_number(value,number_of_cstr))
            acc = temp_list
        return acc
    return inner_f(y_0_0,[])

# (listof (listof float)) (listof float) (listof float) float float float int int -> (listof (listof float))
# Produce a series of ODEs for an undefined (n) number of CSTRs in series with X input componenets (called streams). 
# NOTE:The resulting list should contain an outer list with size = X (# of streams) and inner list with size N (# of CSTRs in series)
def calculate_n_cstr(y: list[list[float]], t, y_0: list[float], mass: float, dMdt: float, backmix: float, m_in: float,number_of_cstr: int = 1):
    if isinstance(y_0, np.ndarray):
        y_0_temp = y_0.tolist()
        y_0 = y_0_temp
    if isinstance(y, np.ndarray):
        y_temp = y.tolist()
        y = y_temp
    if not(y_0):
        return np.array([])
    elif not(y):
        n_cstr: int = number_of_cstr
        y = generate_initial_conditions(y_0,n_cstr)
    else:
        n_cstr = len(y[0])   
    mass_n = mass/n_cstr # Mass term for the current CSTR differential equation (i.e. mass for CSTR n of N)
    dMndt = (dMdt/n_cstr) # Mass accumulation term for the current CSTR differential equation (i.e. mass accumulation for CSTR n of N)

    return np.array([calculate_stream_concentration(stream,y_0x,generate_mass_out_list(m_in,dMndt,backmix,n_cstr),mass_n,backmix,m_in) for (stream, y_0x) in zip(y,y_0)])
    #return np.array(n_cstr_ode(y if type(y) == list else y.tolist(),y0,generate_mass_out_list(m_in,dMndt,backmix,n_cstr),mass_n,backmix,m_in))
