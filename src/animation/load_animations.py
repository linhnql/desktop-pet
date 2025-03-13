from itertools import repeat
import pathlib
import os
import random
from typing import Tuple, Dict
from .animation_states import AnimationStates
from .animation import Animation


def get_animations(
    pet_name: str, target_resolution: Tuple[int, int], should_run_preprocessing: bool
) -> Dict[AnimationStates, Animation]:
    """Loads all of the animations for a pet and their source files into a dictionary
    Args:
        pet_name (str): name of the pet, ie the name of folder its animations are in
        target_resolution (Tuple[int, int]): target size of the animations
    Returns:
        Dict[AnimationStates, Animation]
    """
    # Load the animation gifs from the sprite folder and make each of the gifs into a list of frames
    # Path to sprites we want to use
    impath = pathlib.Path().resolve()
    impath = os.path.join(impath, "src", "sprites")
    Animation.should_run_preprocessing = should_run_preprocessing
    # **** This can be whatever set of animations you want it to be
    # **** I just like horses so I have set it to that
    animations = get_totoro_animations(impath, target_resolution)

    return animations

def get_totoro_animations(impath: str, target_resolution: Tuple[int, int]):
    """Loads all of the animations for a totoro
    Args:
        impath (str): path to the folder the animations are in
        target_resolution (Tuple[int, int]): target size of the animations
    Returns:
        Dict[AnimationStates, Animation]
    """
    pj = os.path.join
    impath = pj(impath, "totoro")
    standing_actions = [AnimationStates.IDLE_TO_SLEEP]
    standing_actions.extend(repeat(AnimationStates.IDLE, 2))
    standing_actions.extend(repeat(AnimationStates.SLEEP_TO_IDLE, 3))
    standing_actions.extend(repeat(AnimationStates.LANDED, 3))
    standing_actions.extend(repeat(AnimationStates.GRABBED, 3))
    standing_actions.extend(repeat(AnimationStates.DRUM, 2))
    standing_actions.extend(repeat(AnimationStates.FALLING, 3))

    animations: Dict[AnimationStates, Animation] = {
        AnimationStates.IDLE: Animation(
            standing_actions,
            gif_location=pj(impath, "tym.gif"),
            target_resolution=target_resolution,
        ),
        AnimationStates.IDLE_TO_SLEEP: Animation(
            [AnimationStates.SLEEP],
            gif_location=pj(impath, "nam_cong.gif"),
            target_resolution=target_resolution,
        ),
        AnimationStates.SLEEP: Animation(
            [
                AnimationStates.SLEEP,
                AnimationStates.SLEEP_TO_IDLE,
            ],
            gif_location=pj(impath, "ngu.gif"),
            target_resolution=target_resolution,
        ),
        AnimationStates.SLEEP_TO_IDLE: Animation(
            standing_actions,
            gif_location=pj(impath, "nam_cong.gif"),
            target_resolution=target_resolution,
        ),

        # RIGHT
        AnimationStates.WALK_POSITIVE: Animation(
            [
                AnimationStates.WALK_POSITIVE_MANY,
                AnimationStates.RUN_POSITIVE,
            ],
            gif_location=pj(impath, "di_bo_phai.gif"),
            v_x=3,
            target_resolution=target_resolution,
        ),        
        AnimationStates.WALK_POSITIVE_MANY: Animation(
            [
                AnimationStates.RUN_POSITIVE
            ],
            gif_location=pj(impath, "di_bo_phai_nhieu.gif"),
            v_x=3,
            target_resolution=target_resolution,
        ),
        AnimationStates.RUN_POSITIVE: Animation(
            [
                AnimationStates.RUN_POSITIVE_TIRED
            ],
            gif_location=pj(impath, "chay_phai.gif"),
            v_x=6,
            target_resolution=target_resolution,
        ),
        AnimationStates.RUN_POSITIVE_TIRED: Animation(
            [
                AnimationStates.WALK_POSITIVE_RAIN
            ],
            gif_location=pj(impath, "chay_phai_met.gif"),
            v_x=6,
            target_resolution=target_resolution,
        ),
        AnimationStates.WALK_POSITIVE_RAIN: Animation(
            standing_actions,
            gif_location=pj(impath, "di_bo_phai_mua.gif"),
            v_x=3,
            target_resolution=target_resolution,
        ),

        # LEFTTTT
        AnimationStates.WALK_NEGATIVE: Animation(
            [
                AnimationStates.WALK_NEGATIVE_MANY,
                AnimationStates.RUN_NEGATIVE,
            ],
            gif_location=pj(impath, "di_bo_trai.gif"),
            v_x=-3,
            target_resolution=target_resolution,
        ),        
        AnimationStates.WALK_NEGATIVE_MANY: Animation(
            [
                AnimationStates.RUN_NEGATIVE
            ],
            gif_location=pj(impath, "di_bo_trai_nhieu.gif"),
            v_x=-3,
            target_resolution=target_resolution,
        ),
        AnimationStates.RUN_NEGATIVE: Animation(
            [
                AnimationStates.RUN_NEGATIVE_TIRED
            ],
            gif_location=pj(impath, "chay_trai.gif"),
            v_x=-6,
            target_resolution=target_resolution,
        ),
        AnimationStates.RUN_NEGATIVE_TIRED: Animation(
            [
                AnimationStates.WALK_NEGATIVE_RAIN
            ],
            gif_location=pj(impath, "chay_trai_met.gif"),
            v_x=-6,
            target_resolution=target_resolution,
        ),
        AnimationStates.WALK_NEGATIVE_RAIN: Animation(
            standing_actions,
            gif_location=pj(impath, "di_bo_trai_mua.gif"),
            v_x=-3,
            target_resolution=target_resolution,
        ),

        AnimationStates.GRABBED: Animation(
            [AnimationStates.GRABBED],
            gif_location=pj(impath, "quay_lung.gif"),
            target_resolution=target_resolution,
        ),
        AnimationStates.DRUM: Animation(
            [AnimationStates.IDLE_TO_SLEEP],
            gif_location=pj(impath, "go_trong.gif"),
            target_resolution=target_resolution,
        ),
        AnimationStates.FALLING: Animation(
            [AnimationStates.FALLING],
            gif_location=pj(impath, "nhun_nhay.gif"),
            target_resolution=target_resolution,
            a_y=2,
        ),
        AnimationStates.LANDED: Animation(
            [
                AnimationStates.LANDED, 
                AnimationStates.WALK_POSITIVE
            ],
            gif_location=pj(impath, "tym.gif"),
            target_resolution=target_resolution,
        ),
    }
    return animations