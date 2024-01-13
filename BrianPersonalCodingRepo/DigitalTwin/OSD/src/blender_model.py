# float float -> float
# Produce the residence time (tau) in eng units 1/time, where flowIn must be eng units 
# mass/time and currentMass must be in mass  
def tau(flowIn: float,currentMass: float):
    # Division by zero
    if currentMass == 0:
        currentMass = 0.0001
    return(flowIn/currentMass)

# float float float -> float
# Produce the output flow rate in engineering units mass/time, where holdupMass and currentMass
# must be in eng units mass and flowIn must be in eng units mass/time
# ASSUME: output flow rate cannot be less than zero
def flowOut(holdupMass: float,currentMass: float, flowIn: float):
    fo = flowIn - (holdupMass - currentMass)*tau(flowIn,currentMass)
    if fo < 0: # output flow rate cannot be less than zero
        return 0
    else:
        return(fo)

# float float float -> float
# Produce the difference in mass (in eng units mass/time) at the time specified by the flow eng
# unit of time (i.e. if flow is in g/s, the difference is a second in the future). holdupMass and 
# currentMass must be in eng units mass and flowIn must be in eng units mass/time
def holdup(holdupMass: float, currentMass: float, flowIn: float):
    return(flowIn - flowOut(holdupMass,currentMass,flowIn))

# float float float -> float
# Produce the updated mass in eng units mass where holdupMass and 
# currentMass must be in eng units mass and flowIn must be in eng units mass/time
# ASSUME: mass CANNOT be less than zero (physics constraint)
def updateMass(holdupMass: float, currentMass: float, flowIn: float):
    m_new = currentMass + holdup(holdupMass, currentMass, flowIn)
    if m_new < 0:
        return 0 
    else: 
        return m_new