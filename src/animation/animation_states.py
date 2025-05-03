from enum import Enum, auto


class AnimationStates(Enum):
    """Represents all the possible animation states for our desktop pet"""

    # Recommended all pets have these first few states
    IDLE = "nhun_nhay"
    IDLE_TO_SLEEP_R = auto() #nam cong
    SLEEP_TO_IDLE_R = auto() #nam cong
    SLEEP_R = auto()
    IDLE_TO_SLEEP_L = auto() #nam cong
    SLEEP_TO_IDLE_L = auto() #nam cong
    SLEEP_L = auto()
    #LEFT
    WALK_NEGATIVE = auto()
    WALK_NEGATIVE_CV = auto()
    RUN_NEGATIVE = auto()
    RUN_NEGATIVE_TIRED = auto()
    WALK_NEGATIVE_RAIN = auto()
    #RIGHT
    WALK_POSITIVE = auto()
    WALK_POSITIVE_CV = auto()
    RUN_POSITIVE = auto()
    RUN_POSITIVE_TIRED = auto()
    WALK_POSITIVE_RAIN = auto()
    #RANDOM
    LOVE = auto()
    DANCE = auto()
    DRUM = auto()
    HERO = auto()
    GUITAR = auto()
    SWIM_RIGHT = auto()
    SWIM_LEFT = auto()
    PHAO = auto()
    IDLE_TO_GRABBED = auto()  # OPTIONAL
    GRABBED = auto()
    GRAB_TO_FALL = auto()  # OPTIONAL
    FALLING = auto()
    LANDED = auto()

    #new
    DRUM_2 = auto()
    WORK = auto()
    QUAY = auto()
    WALK_RIGHT = auto()
    WALK_LEFT = auto()
    AE_QUAY = auto()
    TAP_TA = auto()