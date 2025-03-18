import tkinter as tk
from ..animation import Animation, AnimationStates, Animator
from ..window_utils import Canvas
from src import logger


class SimplePet:
    x: int
    y: int
    canvas: Canvas
    animator: Animator

    def __init__(self, x, y, canvas, animator):
        self.x = x
        self.y = y
        self.canvas = canvas
        self.animator = animator

    def update(self):
        """Progress to next frame of animation"""
        self.progress_animation()

    def get_current_animation(self) -> Animation:
        """Returns the current animation of the Pet instance

        Returns:
            Animation
        """
        return self.animator.animations[self.animator.state]

    def get_current_animation_frame(self) -> tk.PhotoImage:
        """Get and return the current animation frame

        Returns:
            tk.PhotoImage: Image of animation to draw
        """
        animation = self.get_current_animation()
        return animation.frames[self.animator.frame_number]

    def set_animation_state(self, state: AnimationStates) -> bool:
        """Sets the animation state for this pet

        Args:
            state (AnimationStates): Animation state to try to set

        Returns:
            bool: Whether or not the state actually changed values
        """
        changed = self.animator.set_animation_state(state)
        if changed:
            self.reset_movement()
        return changed

    def progress_animation(self):
        """Move the animation forward one frame. If the animation has finished (i.e., current frame is
        the last frame), then try to progress to the next animation
        """
        animation = self.get_current_animation()
        if self.animator.frame_number < len(animation.frames) - 1:
            # logger.debug("Frame repeating")
            self.animator.frame_number += 1
        else:
            # logger.debug("Getting next state")
            self.animator.frame_number = 0
            self.set_animation_state(animation.next(self.animator))

        # logger.debug(f"{self.animator.state.__repr__()}, {self.animator.frame_number}")

    def set_geometry(self):
        """Update the window position and scale to match that of the pet instance's location and size"""
        size = self.animator.animations[self.animator.state].target_resolution
        self.canvas.window.geometry(
            f"{size[0]}x{size[1]}+{self.x}+{self.y}"
        )

    def handle_event(self):
        """Part of animation loop, after delay between frames in animation,
        proceed to begin logic of drawing next frame
        """
        animation = self.get_current_animation()
        # Lấy thời gian của khung hình hiện tại từ frame_durations
        frame_duration = animation.get_frame_duration(self.animator.frame_number)
        self.canvas.window.after(frame_duration, self.on_tick)

    def on_tick(self):
        """Handle the logic for drawing the next frame and scheduling the next tick"""
        # Cập nhật khung hình
        self.update()
        # Vẽ khung hình hiện tại lên canvas (giả sử canvas có phương thức vẽ)
        self.canvas.delete("all")  # Xóa nội dung cũ
        self.canvas.create_image(
            0, 0, anchor=tk.NW, image=self.get_current_animation_frame()
        )
        # Đặt lại vị trí cửa sổ
        self.set_geometry()
        # Lên lịch cho lần tick tiếp theo
        self.handle_event()

    def reset_movement(self):
        """Reset any movement-related variables (if applicable)"""
        # Giả sử đây là phương thức để reset vận tốc hoặc gia tốc nếu có
        pass