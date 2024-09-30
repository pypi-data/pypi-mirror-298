from enum import Enum


class GlobalVariable(Enum):
    """
    Enumeration representing different types of GlobalVariable.

    Enumerators:
        FEM_MODEL (str): Identifier for Finite Element Model GlobalVariable.
        FORWARD_PROBLEM (str): Identifier for Forward Problem GlobalVariable.
        GENERAL (str): Identifier for General GlobalVariable.
    """

    FEM_MODEL: str = "FEM_MODEL"
    FORWARD_PROBLEM: str = "FORWARD_PROBLEM"
    GENERAL: str = "GENERAL"
