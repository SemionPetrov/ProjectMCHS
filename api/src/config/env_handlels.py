from os import getenv

"""
Simple way to get env vars.
With related exception.
"""

class EnvVarNotFound(Exception): 
    def __init__(self, variable):
        self.variable = variable

    def __str__(self) -> str:
        return f"Could not find {self.variable} in env!\nCheck local.env!"


def getenvvar(var_name: str):
    var = getenv(var_name)
    if var == None:
        raise EnvVarNotFound(var_name)
    return var


