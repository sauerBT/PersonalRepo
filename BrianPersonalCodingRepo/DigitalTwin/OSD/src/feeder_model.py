import math
from typing import Literal 

# float float float -> float
# Produce the saturated density of a powder (eng units: mass/vol adopted from the material bulk density)
# based the material bulk density (eng units: mass/vol).  
# ASSUME: material bulk density cannot be <= 0
# NOTE: this is a Data-driven model with two coefficients
def sat_density(matBulkDensity: float, c1SatDensity: float = .071875, c2SatDensity: float = 3.07) -> float:
    if matBulkDensity <= 0:
        raise RuntimeError("Material Bulk Density Cannot be less than or equal to zero")
    else: 
        return (c1SatDensity * math.exp(c2SatDensity*matBulkDensity))

# float float float float -> float
# Produce the saturated density of a powder (eng units: mass/vol adopted from the material bulk density)
# based the material bulk density (eng units: mass/vol).  
# ASSUME: screw vol per rev cannot be < 0
def sat_feed_factor(saturated_density: float, feederScrewVPR: float) -> float | Literal[0]:
    if feederScrewVPR < 0:
        return 0
    else:
        return(saturated_density*feederScrewVPR)

# float float float -> float
# Produce the beta value (unitless) for the beta decay curve based on the hausner ratio
# ASSUME: hausnerRatio != 0 
def beta(hausnerRatio: float, c1Beta: float = 42.74, c2Beta: float = 50.02) -> float:
    if hausnerRatio <= 0:
        raise RuntimeError("Hausner Ration cannot be less than or equal to zero")
    else:
        return (c1Beta*hausnerRatio - c2Beta)

# float float float float float float -> float
# Produce the minimum feed factor of the feeder coupled with the materil (eng units: mass/rev) 
def min_feed_factor(sat_feed_factor: float, c1MinFeedFactor: float = 1.76, c2MinFeedFactor: float = .54) -> float:
    return(c1MinFeedFactor*math.log(sat_feed_factor) + c2MinFeedFactor)

# float float float float float float float float float float -> float
# Produce the apparent feed factor (eng units: mass/rev) using the beta decay equation
# ASSUME: feeder weight cannot be less than zero
def apparent_feed_factor(saturated_feed_factor: float, minimum_feed_factor: float, beta: float, feederWeight: float) -> float:
    if feederWeight < 0:
            return(saturated_feed_factor-math.exp(-1*beta*0*(saturated_feed_factor-minimum_feed_factor)))
    else:
        return(saturated_feed_factor-math.exp(-1*beta*feederWeight*(saturated_feed_factor-minimum_feed_factor)))

# float float float float float float float float float float -> float
# Produce the feed rate (eng. units: mass) using the apparent feed factor
def feed_rate(apparent_feed_factor: float,feederScrewSpeed: float) -> float:
    return(apparent_feed_factor*feederScrewSpeed)

def maxVolPerRev(maxScrewSpeed: float,feederScrewVPR: float) -> float:
    return(maxScrewSpeed*feederScrewVPR)

def maxFeedRate(maxScrewSpeed: float,feederScrewVPR: float,matBulkDensity: float) -> float:
    return(maxVolPerRev(maxScrewSpeed,feederScrewVPR)*(sat_density(matBulkDensity)/1000))