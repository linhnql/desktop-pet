import tkinter as tk
import random
from itertools import repeat
from os import listdir
from os.path import isfile, join
from typing import Tuple, List
from PIL import Image
from src import logger
from .animation_states import AnimationStates


class Animation:
    """Defines the event numbers for this animation and the ways this animation can transfer to the next animation"""

    next_animation_states: List[AnimationStates]
    """possible animations for after this animation"""
    frames: List[tk.PhotoImage]
    """List of frames in the animation"""
    frame_durations: List[int]
    """List of durations (in ms) for each frame, replacing frame_timer to preserve GIF timing"""
    v_x: float
    v_y: float
    a_x: float
    a_y: float
    repititions: int
    """How many times to repeat given animation before moving onto the next animation"""
    target_resolution: Tuple[int, int]
    list_message: List[str]  # Thêm danh sách message cho mỗi animation
    """List of messages to display in tooltip"""
    show_tooltip: bool  # Thêm biến để bật/tắt tooltip

    should_run_preprocessing = False
    """Whether or not to run preprocessing, overwrites saved images. Defaults to False"""

    def __init__(
        self,
        next_animation_states,
        name: str = None,
        frames: List[tk.PhotoImage] = None,
        gif_location: str = None,
        images_location: str = None,
        v_x: float = 0,
        v_y: float = 0,
        a_x: float = 0,
        a_y: float = 0,
        repititions: int = 0,
        frame_multiplier: int = 1,
        target_resolution: Tuple[int, int] = (100, 100),
        reverse: bool = False,
        list_message: List[str] = ["Hi Lu Xinh!", "Tớ là Totoro!", "Love you 3000"],  # Thêm tham số list_message
        show_tooltip: bool = True,       # Thêm tham số để bật/tắt tooltip
    ):
        """
        Args:
            next_animation_states (List[AnimationStates]): Possible animations for this animation to transition to.
            name (str, optional): The verbose name of this animation.
            frames (List[tk.PhotoImage], optional): Frames of images that can be rendered by tkinter.
            gif_location (str, optional): Absolute path to the gif to convert into frames.
            images_location (str, optional): Absolute path to the images folder to load into frames list.
            target_resolution (Tuple[int, int], optional): Resolution of the frames of the animation.
            v_x (float, optional): Change in x for every frame of the animation.
            v_y (float, optional): Change in y for every frame of the animation.
            a_x (float, optional): Change in v_x for every frame of the animation.
            a_y (float, optional): Change in v_y for every frame of the animation.
            repititions (int, optional): How many times this animation should repeat.
            frame_multiplier (int, optional): How many times to duplicate frames (for non-GIF sources).
            reverse (bool, optional): Whether or not to reverse the loaded frames.
            list_message (List[str], optional): List of messages for tooltip display.
            show_tooltip (bool, optional): Whether to show tooltip or not. Defaults to True.
        """
        self.next_animation_states = next_animation_states
        self.v_x = v_x
        self.v_y = v_y
        self.a_x = a_x
        self.a_y = a_y
        self.repititions = repititions
        self.list_message = list_message if list_message is not None else []  # Khởi tạo list_message
        self.show_tooltip = show_tooltip  # Khởi tạo biến bật/tắt tooltip

        # Get and set the frames and their durations
        if name is None:
            name = gif_location.split("src").pop() if gif_location is not None else name
            name = images_location.split("src").pop() if images_location is not None else name
        self.name = name
        # logger.info(f"Loading Animation: {self.name}")

        if frames is None:
            if gif_location is not None:
                frames, durations = Animation.load_gif_to_frames(gif_location)
                self.frame_durations = durations  # Lưu thời gian gốc của GIF
            else:
                raise Exception("Received neither frames nor locations to load the frames.")
        else:
            self.frame_durations = [100] * len(frames)

        if len(frames) == 0:
            raise Exception("There must be at least one frame in the frames list")

        self.target_resolution = target_resolution
        frames = Animation.apply_target_resolution(frames, target_resolution)

        if reverse:
            frames.reverse()
            self.frame_durations.reverse()

        if gif_location is None and frame_multiplier > 1:
            self.frames = [x for item in frames for x in repeat(item, frame_multiplier)]
            self.frame_durations = [d for d in self.frame_durations for _ in range(frame_multiplier)]
        else:
            self.frames = frames

    @staticmethod
    def load_gif_to_frames(path: str) -> Tuple[List[tk.PhotoImage], List[int]]:
        """Load frames and their durations from a GIF file."""
        file = Image.open(path)
        number_of_frames = file.n_frames
        frames = []
        durations = []

        for i in range(number_of_frames):
            file.seek(i)
            duration = file.info.get('duration', 100)
            frame = tk.PhotoImage(file=path, format="gif -index %i" % i)
            frames.append(frame)
            durations.append(int(duration))

        file.close()
        return frames, durations

    @staticmethod
    def apply_target_resolution(frames: List[tk.PhotoImage], target_resolution: Tuple[int, int]) -> List[tk.PhotoImage]:
        """Scale frames to a target resolution."""
        for i in range(len(frames)):
            image = frames[i]
            scale_w = target_resolution[0] / image.width()
            scale_h = target_resolution[1] / image.height()
            if scale_w < 1:
                image = image.subsample(int(1 / scale_w), 1)
            elif scale_w > 1:
                image = image.zoom(int(scale_w), 1)
            if scale_h < 1:
                image = image.subsample(1, int(1 / scale_h))
            elif scale_h > 1:
                image = image.zoom(1, int(scale_h))
            frames[i] = image
        return frames

    @staticmethod
    def remove_partial_transparency_png(path: str) -> Image:
        """Force PNG transparency to fully opaque or fully transparent."""
        # logger.info("START:remove_partial_transparency_png -> " + path)
        png = Image.open(path)
        if path.split(".").pop().lower() != "png":
            return png

        png = png.convert("RGBA")
        datas = png.getdata()
        new_data = [
            (item[0], item[1], item[2], round(item[3] / 255) * 255) if item[3] != 255 else item
            for item in datas
        ]
        png.putdata(new_data)
        png.save(path, path.split(".").pop())
        return png

    def next(self, animator) -> AnimationStates:
        """Determine the next animation state."""
        if animator.repititions < self.repititions:
            animator.repititions += 1
            return animator.state
        else:
            animator.repititions = 0
        return random.choice(self.next_animation_states)

    def get_velocity(self) -> Tuple[float, float]:
        """Return the change in position for this animation."""
        return (self.v_x, self.v_y)

    def get_acceleration(self) -> Tuple[float, float]:
        """Return the change in velocity for this animation."""
        return (self.a_x, self.a_y)

    def get_frame_duration(self, frame_index: int) -> int:
        """Return the duration of the frame at the given index."""
        return self.frame_durations[frame_index % len(self.frame_durations)]

    def get_random_message(self) -> str:
        """Return a random message from the list_message."""
        if self.list_message:
            return random.choice(self.list_message)
        return ""

    def __repr__(self):
        return f"<Animation: {len(self.frames)} frames with variable durations>"