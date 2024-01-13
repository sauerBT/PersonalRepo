from functools import reduce

## (listof String) -> (listof Float)
## Produce a list of floating point values from a list of strings
def listStrToFloat(lox: list[str]):
        return list(map(float,lox))


## String -> (listof String)
## Produce a parsed MQTT topic 
def parseMqttTopic(s: str):
        return s.split("/")

## Bytes String -> (listof String)
## Produce a list of strings built from a byte array 
def parseMqttPayload(payload: bytes,s: str =","):
        return payload.decode('UTF-8').split(s)
    
## (listof String) String String -> String
## Produce an MQTT topic with the input topi keywork replaced with the output topic keyword
## ASSUME: the input keyword DOES NOT occur in the list more than once 
## [to do] remove the above assumption
def createOuputTopic(los: list[str],s1: str ="",s2: str =""):
    replacedList = list(map(lambda s: s2 if (s == s1) else s, los))
    if not replacedList: return""
    else:
        return reduce(lambda a,b: a + "/" + b, replacedList[1:], replacedList[0])
    

## (listof String) String -> String
## Produce the location of a string within a list, otherwise produce False
def topic_loc(los0: list[str], s: str):
    def f(los, acc):
        if not los: return False
        else:
            if los[0] == s: return acc
            else: return (f(los[1:], acc + 1))
    return f(los0,0)
