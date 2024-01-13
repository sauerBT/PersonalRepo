import requests
from requests.auth import HTTPBasicAuth

FILTER_PARAMETERS = ["customfield_10016","statuscategorychangedate","key","name"]
# Produce Jira API endpoint for getting issues in a project
def generate_jira_url(jira_base_url: str, type: str="ISSUES") -> str:
    return f"{jira_base_url}/rest/api/2/search"

def get_jira_project_issues(username: str, password_or_api_token: str, jql: str, issues_endpoint: str) -> dict:
    auth = HTTPBasicAuth(username, password_or_api_token)
    params = {
        "jql": jql,
        "maxResults": 500,  # Adjust as needed
    }
    try:
        response = requests.get(issues_endpoint, auth=auth, params=params)
        issues = response.json()
        return issues
    except requests.exceptions.RequestException as e:
        return (f"Error: {e}")
    
# Dictionary -> Dictionary
# Produce a flattened version of the given dictionary of depth n with keys at each depth separated by "/" and values applied when there is no further depth to the dictionar
# TODO #if key_filter(FILTER_PARAMETERS, key):  
def iter_dict(d0: dict) -> dict:
    def f(d: dict,acc1: str,acc2: dict) -> dict:
        if d == {}: return {}
        else:
            for key in iter(d):
                temp_dict: dict = dict(**acc2)
                if type(d) != dict:
                    print(d)
                elif type(d[key]) == list:
                    temp_dict.update(prepend_key(key + "/" + acc1,iter_list(d[key])))
                elif type(d[key]) == dict:
                    temp_dict.update(f(d[key],key if acc1 == "" else acc1 + "/" + key,acc2))
                else:
                    if d.get(key) != None:
                        temp_dict.update({key if acc1 == "" else acc1 + "/" + key: d[key]})
                acc2 = temp_dict
        return acc2
    return f(d0,"",{})
                        
# (listof 'a) -> dictionay
# Produce a dictionary with key names equal to the position in the given list
def iter_list(lox0: list)-> dict:
    def inner_f(lox: list, acc1: int, acc2: dict):
        for value in iter(lox):
            temp_dict: dict = dict(**acc2)
            if type(value) == list:
                temp_dict.update(inner_f(value,acc1,acc2)) #TODO
            elif type(value)== dict:
                temp_dict.update(prepend_key(str(acc1) + "/",iter_dict(value))) #TODO
            else:
                if value != None:
                    temp_dict.update({str(acc1): value})
            acc1 = acc1 + 1
            acc2 = temp_dict
        return acc2
    return inner_f(lox0,0,{})

# dictionary -> dictionary
# Produce a dictionary with each key prepended with the give string
# ASSUME: single depth dictionary
def prepend_key(s: str,d0: dict) -> dict:
    def inner_f(d: dict,acc: list) -> dict:
        for key in iter(d):
            temp_dict: dict = dict(**acc)
            temp_dict.update({s + key: d[key]})
            acc = temp_dict
        return acc
    return inner_f(d0,{})

def key_filter(los: list[str], s) -> bool:
    if not los: return False
    else:
        if los[0] == s: return True
        else: return key_filter(los[1:], s)