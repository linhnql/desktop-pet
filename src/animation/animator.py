from typing import Dict
from src import logger
from .animation_states import AnimationStates
from .animation import Animation

class Animator:
    def __init__(self, frame_number: int, state: AnimationStates, animations: Dict[AnimationStates, Animation], repititions=0):
        self.frame_number = frame_number
        self.state = state
        self.animations = animations
        self.repititions = repititions
        self.time_accumulator = 0  # Theo dõi thời gian tích lũy

    def update(self, delta_time: float) -> None:
        """Cập nhật frame dựa trên thời gian thực tế."""
        current_animation = self.animations[self.state]
        self.time_accumulator += delta_time * 1000  # Chuyển sang ms

        # Lấy thời gian của khung hình hiện tại
        frame_duration = current_animation.get_frame_duration(self.frame_number)

        # Nếu thời gian tích lũy vượt quá thời gian khung hình, chuyển sang khung tiếp theo
        while self.time_accumulator >= frame_duration:
            self.time_accumulator -= frame_duration
            self.frame_number += 1

            # Kiểm tra nếu hết chu kỳ hoạt ảnh
            if self.frame_number >= len(current_animation.frames):
                self.frame_number = 0
                self.state = current_animation.next(self)

    def set_animation_state(self, state: AnimationStates) -> bool:
        if state == self.state:
            return False
        self.frame_number = 0
        self.repititions = 0
        self.time_accumulator = 0
        self.state = state
        return True

    def __repr__(self):
        return f"<Animator: {str(self.state)} on frame {self.frame_number}>"