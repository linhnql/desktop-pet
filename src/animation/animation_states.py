from enum import Enum, auto


class AnimationStates(Enum):
    """Represents all the possible animation states for our desktop pet"""

    # Recommended all pets have these first few states
    IDLE = "nhun_nhay"
    IDLE_TO_SLEEP = auto() #nam cong
    SLEEP_TO_IDLE = auto() #nam cong
    SLEEP = auto()
    #LEFT
    WALK_NEGATIVE = auto()
    WALK_NEGATIVE_MANY = auto()
    RUN_NEGATIVE = auto()
    RUN_NEGATIVE_TIRED = auto()
    WALK_NEGATIVE_RAIN = auto()
    #RIGHT
    WALK_POSITIVE = auto()
    WALK_POSITIVE_MANY = auto()
    RUN_POSITIVE = auto()
    RUN_POSITIVE_TIRED = auto()
    WALK_POSITIVE_RAIN = auto()
    #DANCE
    LOVE = auto()
    DRUM = auto()
    IDLE_TO_GRABBED = auto()  # OPTIONAL
    GRABBED = auto()
    GRAB_TO_FALL = auto()  # OPTIONAL
    FALLING = auto()
    LANDED = auto()