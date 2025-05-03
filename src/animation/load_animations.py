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
    standing_actions = [AnimationStates.IDLE_TO_SLEEP_L]
    standing_actions.extend(repeat(AnimationStates.IDLE_TO_SLEEP_R, 2))
    standing_actions.extend(repeat(AnimationStates.IDLE, 2))
    standing_actions.extend(repeat(AnimationStates.SLEEP_TO_IDLE_L, 3))
    standing_actions.extend(repeat(AnimationStates.SLEEP_TO_IDLE_R, 3))
    standing_actions.extend(repeat(AnimationStates.LANDED, 3))
    standing_actions.extend(repeat(AnimationStates.DRUM, 2))
    standing_actions.extend(repeat(AnimationStates.HERO, 3))
    standing_actions.extend(repeat(AnimationStates.GUITAR, 2))
    standing_actions.extend(repeat(AnimationStates.FALLING, 3))
    standing_actions.extend(repeat(AnimationStates.DRUM_2, 3))
    standing_actions.extend(repeat(AnimationStates.WORK, 3))
    standing_actions.extend(repeat(AnimationStates.QUAY, 3))
    standing_actions.extend(repeat(AnimationStates.AE_QUAY, 3))
    standing_actions.extend(repeat(AnimationStates.TAP_TA, 3))

    animations: Dict[AnimationStates, Animation] = {
        AnimationStates.IDLE: Animation(
            standing_actions,
            gif_location=pj(impath, "tym.gif"),
            target_resolution=target_resolution,
            repititions=random.randint(3, 6),
            list_message=["Xin chào!", "Tớ là Totoro!", "Chào Lu xinh <3"],  # Danh sách message
        ),
        AnimationStates.IDLE_TO_SLEEP_R: Animation(
            [AnimationStates.SLEEP_R],
            gif_location=pj(impath, "nam_cong_phai.gif"),
            target_resolution=target_resolution,
            list_message=["Đừng có lười", "Tập thể dục i"],  # Danh sách message
        ),
        AnimationStates.IDLE_TO_SLEEP_L: Animation(
            [AnimationStates.SLEEP_L],
            gif_location=pj(impath, "nam_cong_trai.gif"),
            target_resolution=target_resolution,
            list_message=["Đừng có lười", "Tập thể dục i"],  # Danh sách message
        ),
        AnimationStates.SLEEP_R: Animation(
            [
                AnimationStates.SLEEP_R,
                AnimationStates.SLEEP_TO_IDLE_R,
                AnimationStates.SLEEP_TO_IDLE_L,
            ],
            gif_location=pj(impath, "ngu_phai.gif"),
            target_resolution=target_resolution,
            repititions=random.randint(4, 7),
            list_message=["Đừng làm phiền", "Yên ngủ coii"]
        ),
         AnimationStates.SLEEP_L: Animation(
            [
                AnimationStates.SLEEP_L,
                AnimationStates.SLEEP_TO_IDLE_R,
                AnimationStates.SLEEP_TO_IDLE_L,
            ],
            gif_location=pj(impath, "ngu_trai.gif"),
            target_resolution=target_resolution,
            repititions=random.randint(4, 7),
            list_message=["Đừng làm phiền", "Yên ngủ coii"]
        ),
        AnimationStates.SLEEP_TO_IDLE_R: Animation(
            standing_actions,
            gif_location=pj(impath, "nam_cong_phai.gif"),
            target_resolution=target_resolution,
            list_message=["Đừng lười", "Tập thể dục i"],  # Danh sách message
        ),
        AnimationStates.SLEEP_TO_IDLE_L: Animation(
            standing_actions,
            gif_location=pj(impath, "nam_cong_trai.gif"),
            target_resolution=target_resolution,
            list_message=["Đừng lười", "Tập thể dục i"],  # Danh sách message
        ),

        # RIGHT
        AnimationStates.WALK_POSITIVE: Animation(
            [
                AnimationStates.WALK_POSITIVE_CV,
                AnimationStates.WALK_RIGHT,
            ],
            gif_location=pj(impath, "di_bo_phai.gif"),
            v_x=2,
            target_resolution=target_resolution,
            repititions=random.randint(3, 6),
            list_message=["Mệt quóo", "Đi lại i"],  # Danh sách message
        ),      
        AnimationStates.WALK_RIGHT: Animation(
            [
                AnimationStates.RUN_POSITIVE
            ],
            gif_location=pj(impath, "di_bo_nhieu_phai.gif"),
            v_x=1,
            target_resolution=target_resolution,
            repititions=random.randint(3, 7),
            list_message=["Đi lẹ lên"],  # Danh sách message
        ),
        AnimationStates.WALK_POSITIVE_CV: Animation(
            [
                AnimationStates.RUN_POSITIVE
            ],
            gif_location=pj(impath, "di_bo_cavat_phai.gif"),
            v_x=1,
            target_resolution=target_resolution,
            # repititions=random.randint(2000, 3000),
            list_message=["Lịch lãmm"],  # Danh sách message
        ),
        AnimationStates.RUN_POSITIVE: Animation(
            [
                AnimationStates.RUN_POSITIVE_TIRED
            ],
            gif_location=pj(impath, "chay_phai.gif"),
            v_x=4,
            target_resolution=target_resolution,
            repititions=random.randint(3, 6),
            list_message=["Đố deadline bắt được tui"],  # Danh sách message
        ),
        AnimationStates.RUN_POSITIVE_TIRED: Animation(
            [
                AnimationStates.WALK_POSITIVE_RAIN
            ],
            gif_location=pj(impath, "chay_met_phai.gif"),
            v_x=3,
            target_resolution=target_resolution,
            repititions=random.randint(3, 6),
            list_message=["Cíu, mệt", "Mắc gì chạy?"],  # Danh sách message
        ),
        AnimationStates.WALK_POSITIVE_RAIN: Animation(
            [
                AnimationStates.SWIM_RIGHT
            ],
            gif_location=pj(impath, "che_o_phai.gif"),
            v_x=2,
            target_resolution=target_resolution,
            repititions=random.randint(3, 6),
            list_message=["Mưa ời"],  # Danh sách message
        ),
        AnimationStates.SWIM_RIGHT: Animation(
            [
                AnimationStates.PHAO
            ],
            gif_location=pj(impath, "boi_phai.gif"),
            target_resolution=target_resolution,
            repititions=random.randint(2, 4),
            v_x=2,
            list_message=["Không kịp mất", "Deadline tới"],  # Danh sách message
        ),
        AnimationStates.PHAO: Animation(
            standing_actions,
            gif_location=pj(impath, "phao.gif"),
            target_resolution=target_resolution,
            repititions=random.randint(2, 4),
            list_message=["Ngập deadline rồi"],  # Danh sách message
        ),
        
        # LEFTTTT
        AnimationStates.WALK_NEGATIVE: Animation(
            [
                AnimationStates.WALK_NEGATIVE_CV,
                AnimationStates.WALK_LEFT,
            ],
            gif_location=pj(impath, "di_bo_trai.gif"),
            v_x=-2,
            target_resolution=target_resolution,
            repititions=random.randint(3, 6),
            list_message=["Mắc mệt thiệt á", "Đi lại chút i"],  # Danh sách message
        ),     
        AnimationStates.WALK_LEFT: Animation(
            [
                AnimationStates.RUN_NEGATIVE
            ],
            gif_location=pj(impath, "di_bo_nhieu_trai.gif"),
            v_x=-1,
            target_resolution=target_resolution,
            repititions=random.randint(3, 7),
            list_message=["Chậm chạp quó"],  # Danh sách message
        ),   
        AnimationStates.WALK_NEGATIVE_CV: Animation(
            [
                AnimationStates.RUN_NEGATIVE
            ],
            gif_location=pj(impath, "di_bo_cavat_trai.gif"),
            v_x=-1,
            target_resolution=target_resolution,
            # repititions=random.randint(2000, 3000),
            list_message=["Lu xinh Lu xinh"],  # Danh sách message
        ),
        AnimationStates.RUN_NEGATIVE: Animation(
            [
                AnimationStates.RUN_NEGATIVE_TIRED
            ],
            gif_location=pj(impath, "chay_trai.gif"),
            v_x=-4,
            target_resolution=target_resolution,
            repititions=random.randint(3, 6),
            list_message=["Trốn lẹ"],  # Danh sách message
        ),
        AnimationStates.RUN_NEGATIVE_TIRED: Animation(
            [
                AnimationStates.WALK_NEGATIVE_RAIN
            ],
            gif_location=pj(impath, "chay_met_trai.gif"),
            v_x=-3,
            target_resolution=target_resolution,
            repititions=random.randint(3, 6),
            list_message=["Cíu, mệt", "Ai bắt tui chạy?"],  # Danh sách message
        ),
        AnimationStates.WALK_NEGATIVE_RAIN: Animation(
            [
                AnimationStates.SWIM_LEFT
            ],
            gif_location=pj(impath, "che_o_trai.gif"),
            v_x=-2,
            target_resolution=target_resolution,
            repititions=random.randint(3, 6),
            list_message=["Mưa nữa ờiii"],  # Danh sách message
        ),
        AnimationStates.SWIM_LEFT: Animation(
            [
                AnimationStates.PHAO
            ],
            gif_location=pj(impath, "boi_trai.gif"),
            target_resolution=target_resolution,
            repititions=random.randint(2, 4),
            v_x=-2,
            list_message=["Về bờ lẹ", "Sắp đuối rồi"],  
        ),
        AnimationStates.PHAO: Animation(
            standing_actions,
            gif_location=pj(impath, "phao.gif"),
            target_resolution=target_resolution,
            repititions=random.randint(2, 4),
            list_message=["Ngập deadline rồi"],  # Danh sách message
        ),

        AnimationStates.GRABBED: Animation(
            standing_actions,
            gif_location=pj(impath, "hit_xa.gif"),
            target_resolution=target_resolution,
            repititions=random.randint(2, 4),
            list_message=["Ráng lên", "Hự..."],  # Danh sách message
        ),
        AnimationStates.DRUM: Animation(
            [
                AnimationStates.GUITAR
            ],
            gif_location=pj(impath, "go_trong.gif"),
            target_resolution=target_resolution,
            repititions=random.randint(3, 5),
            list_message=["Hết giờ!!!"],  # Danh sách message
        ),
        AnimationStates.FALLING: Animation(
            standing_actions,
            gif_location=pj(impath, "nhun_nhay.gif"),
            target_resolution=target_resolution,
            repititions=random.randint(2, 4),
            list_message=["Vận động tý nào"],  # Danh sách message
        ),
        AnimationStates.DANCE: Animation(
            standing_actions,
            gif_location=pj(impath, "nhay_day.gif"),
            target_resolution=target_resolution,
            repititions=random.randint(2, 4),
        ),
        AnimationStates.GUITAR: Animation(
            standing_actions,
            gif_location=pj(impath, "dien_thoai.gif"),
            target_resolution=target_resolution,
            repititions=random.randint(2, 4),
            list_message=["Call me babie..."],  # Danh sách message
        ),
        AnimationStates.WORK: Animation(
            standing_actions,
            gif_location=pj(impath, "lam_viec.gif"),
            target_resolution=target_resolution,
            repititions=random.randint(3, 6),
            list_message=["Tập trung"],  # Danh sách message
        ),
        AnimationStates.QUAY: Animation(
            [AnimationStates.AE_QUAY],
            gif_location=pj(impath, "vung_tay.gif"),
            target_resolution=target_resolution,
            repititions=random.randint(3, 6),
            list_message=["Vận động i"],  # Danh sách message
        ),
        AnimationStates.AE_QUAY: Animation(
            standing_actions,
            gif_location=pj(impath, "ae_quay.gif"),
            target_resolution=target_resolution,
            repititions=random.randint(3, 6),
            list_message=["Tadaaa..."],  # Danh sách message
        ),
        AnimationStates.TAP_TA: Animation(
            standing_actions,
            gif_location=pj(impath, "hit_xa.gif"),
            target_resolution=target_resolution,
            repititions=random.randint(3, 6),
            list_message=["🏋️Hự… Haa…!"],  # Danh sách message
        ),
        AnimationStates.HERO: Animation(
            standing_actions,
            gif_location=pj(impath, "sieu_nhan.gif"),
            target_resolution=target_resolution,
            repititions=random.randint(3, 6),
            list_message=["Cíu thế giới"],  # Danh sách message
        ),
        AnimationStates.DRUM_2: Animation(
            standing_actions,
            gif_location=pj(impath, "danh_trong.gif"),
            target_resolution=target_resolution,
            repititions=random.randint(3, 6),
            list_message=["Thùng... thình... thùng... 🎶🥁"],  # Danh sách message
        ),
        AnimationStates.LANDED: Animation(
            [
                AnimationStates.LANDED, 
                AnimationStates.WALK_POSITIVE
            ],
            gif_location=pj(impath, "lac_vong.gif"),
            target_resolution=target_resolution,
            repititions=random.randint(3, 5),
            list_message=["Mê chưaaa", "Eo thon liềnn"],  # Danh sách message
        ),
    }
    return animations