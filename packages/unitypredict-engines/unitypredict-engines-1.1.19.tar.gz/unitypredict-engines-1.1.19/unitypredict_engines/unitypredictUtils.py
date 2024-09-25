from enum import Enum

class ReturnValues(Enum):
    """
    Enum representing possible return values from functions.
    """
    SUCCESS = 0
    ERROR = 1
    CRED_CREATE_SUCCESS = 2
    CRED_CREATE_ERROR = 3
    CRED_FOUND = 4 
    CRED_NOT_FOUND = 5
    ENGINE_FOUND = 6
    ENGINE_NOT_FOUND = 7
    ENGINE_CREATE_SUCCESS = 8
    ENGINE_CREATE_ERROR = 9
    ENGINE_REMOVE_SUCCESS = 10
    ENGINE_REMOVE_ERROR = 11
    