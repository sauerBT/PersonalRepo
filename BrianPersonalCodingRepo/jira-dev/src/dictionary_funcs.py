# Dictionary Dictionary -> Dictionary
# Produce a dictionary listing ONLY the key:value pairs thats exist in the first dictionary but not the second
# NOTE: this function is only meant for single depth dictionaries
# TODO add capability for arbitrary depth dictionaries with embedded lists, arrays, and dicts
def dictionary_compare(d1: dict,d2: dict) -> dict:
    if d2 == {}:
        return d1
    else:
        def inner_f(d: dict, acc: dict) -> dict:
            for key in iter(d1):
                temp_dict: dict = dict(**acc)
                if d2.get(key) != None:
                    if d1[key] != d2[key]:
                        temp_dict.update({key:d1[key]})
                else:
                    temp_dict.update({key:d1[key]})
                acc = temp_dict
            return acc
        return inner_f(d1,{})