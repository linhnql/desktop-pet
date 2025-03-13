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
    standing_actions.extend(repeat(AnimationStates.HERO, 3))
    standing_actions.extend(repeat(AnimationStates.GUITAR, 2))
    standing_actions.extend(repeat(AnimationStates.FALLING, 3))

    animations: Dict[AnimationStates, Animation] = {
        AnimationStates.IDLE: Animation(
            standing_actions,
            gif_location=pj(impath, "tym_new.gif"),
            target_resolution=target_resolution,
            repititions=random.randint(3, 6),
        ),
        AnimationStates.IDLE_TO_SLEEP: Animation(
            [AnimationStates.SLEEP],
            gif_location=pj(impath, "nam_cong_new.gif"),
            target_resolution=target_resolution,
        ),
        AnimationStates.SLEEP: Animation(
            [
                AnimationStates.SLEEP,
                AnimationStates.SLEEP_TO_IDLE,
            ],
            gif_location=pj(impath, "ngu_new.gif"),
            target_resolution=target_resolution,
            repititions=random.randint(4, 7),
        ),
        AnimationStates.SLEEP_TO_IDLE: Animation(
            standing_actions,
            gif_location=pj(impath, "nam_cong_new.gif"),
            target_resolution=target_resolution,
        ),

        # RIGHT
        AnimationStates.WALK_POSITIVE: Animation(
            [
                AnimationStates.WALK_POSITIVE_MANY,
                AnimationStates.RUN_POSITIVE,
            ],
            gif_location=pj(impath, "di_bo_phai_new.gif"),
            v_x=2,
            target_resolution=target_resolution,
            repititions=random.randint(3, 6),
        ),        
        AnimationStates.WALK_POSITIVE_MANY: Animation(
            [
                AnimationStates.RUN_POSITIVE
            ],
            gif_location=pj(impath, "di_bo_phai_nhieu_new.gif"),
            v_x=1,
            target_resolution=target_resolution,
            repititions=random.randint(50, 100),
        ),
        AnimationStates.RUN_POSITIVE: Animation(
            [
                AnimationStates.RUN_POSITIVE_TIRED
            ],
            gif_location=pj(impath, "chay_phai_new.gif"),
            v_x=4,
            target_resolution=target_resolution,
            repititions=random.randint(3, 6),
        ),
        AnimationStates.RUN_POSITIVE_TIRED: Animation(
            [
                AnimationStates.WALK_POSITIVE_RAIN
            ],
            gif_location=pj(impath, "chay_phai_met_new.gif"),
            v_x=3,
            target_resolution=target_resolution,
            repititions=random.randint(3, 6),
        ),
        AnimationStates.WALK_POSITIVE_RAIN: Animation(
            [
                AnimationStates.SWIM_RIGHT
            ],
            gif_location=pj(impath, "che_o_phai_new.gif"),
            v_x=2,
            target_resolution=target_resolution,
            repititions=random.randint(3, 6),
        ),
        AnimationStates.SWIM_RIGHT: Animation(
            standing_actions,
            gif_location=pj(impath, "boi_phai_new.gif"),
            target_resolution=target_resolution,
            repititions=random.randint(2, 4),
            v_x=2
        ),
        
        # LEFTTTT
        AnimationStates.WALK_NEGATIVE: Animation(
            [
                AnimationStates.WALK_NEGATIVE_MANY,
                AnimationStates.RUN_NEGATIVE,
            ],
            gif_location=pj(impath, "di_bo_trai_new.gif"),
            v_x=-2,
            target_resolution=target_resolution,
            repititions=random.randint(3, 6),
        ),        
        AnimationStates.WALK_NEGATIVE_MANY: Animation(
            [
                AnimationStates.RUN_NEGATIVE
            ],
            gif_location=pj(impath, "di_bo_trai_nhieu_new.gif"),
            v_x=-1,
            target_resolution=target_resolution,
            repititions=random.randint(50, 100),
        ),
        AnimationStates.RUN_NEGATIVE: Animation(
            [
                AnimationStates.RUN_NEGATIVE_TIRED
            ],
            gif_location=pj(impath, "chay_trai_new.gif"),
            v_x=-4,
            target_resolution=target_resolution,
            repititions=random.randint(3, 6),
        ),
        AnimationStates.RUN_NEGATIVE_TIRED: Animation(
            [
                AnimationStates.WALK_NEGATIVE_RAIN
            ],
            gif_location=pj(impath, "chay_trai_met_new.gif"),
            v_x=-3,
            target_resolution=target_resolution,
            repititions=random.randint(3, 6),
        ),
        AnimationStates.WALK_NEGATIVE_RAIN: Animation(
            [
                AnimationStates.SWIM_LEFT
            ],
            gif_location=pj(impath, "che_o_trai_new.gif"),
            v_x=-2,
            target_resolution=target_resolution,
            repititions=random.randint(3, 6),
        ),
        AnimationStates.SWIM_LEFT: Animation(
            standing_actions,
            gif_location=pj(impath, "boi_trai_new.gif"),
            target_resolution=target_resolution,
            repititions=random.randint(2, 4),
            v_x=-2
        ),

        AnimationStates.GRABBED: Animation(
            standing_actions,
            gif_location=pj(impath, "quay_lung_new.gif"),
            target_resolution=target_resolution,
            repititions=random.randint(2, 4),
        ),
        AnimationStates.DRUM: Animation(
            [
                AnimationStates.GUITAR
            ],
            gif_location=pj(impath, "go_trong_new.gif"),
            target_resolution=target_resolution,
            repititions=random.randint(3, 5),
        ),
        AnimationStates.FALLING: Animation(
            standing_actions,
            gif_location=pj(impath, "nhun_nhay_new.gif"),
            target_resolution=target_resolution,
            repititions=random.randint(2, 4),
        ),
        AnimationStates.DANCE: Animation(
            standing_actions,
            gif_location=pj(impath, "nhun_nhay_fail.gif"),
            target_resolution=target_resolution,
            repititions=random.randint(2, 4),
        ),
        AnimationStates.GUITAR: Animation(
            standing_actions,
            gif_location=pj(impath, "danh_dan_new.gif"),
            target_resolution=target_resolution,
            repititions=random.randint(2, 4),
        ),
        AnimationStates.HERO: Animation(
            standing_actions,
            gif_location=pj(impath, "sieu_nhan_new.gif"),
            target_resolution=target_resolution,
            repititions=random.randint(2, 4),
        ),
        AnimationStates.LANDED: Animation(
            [
                AnimationStates.LANDED, 
                AnimationStates.WALK_POSITIVE
            ],
            gif_location=pj(impath, "lac_vong_new.gif"),
            target_resolution=target_resolution,
            repititions=random.randint(3, 5),
        ),
    }
    return animations