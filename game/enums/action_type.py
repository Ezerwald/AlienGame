from enum import Enum

class ActionType(Enum):
    MOVE = "Move"
    FIX = "Fix"
    ATTACK = "Attack"
    HOLD_ANGLE = "HoldAngle"
    GATHER = "Gather"
    PEEK = "Peek"
    NONE = "None"
