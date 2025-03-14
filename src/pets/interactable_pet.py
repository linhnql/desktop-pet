import tkinter as tk
from ..animation import AnimationStates
from .simple_pet import SimplePet
from src import logger
import random


class InteractablePet(SimplePet):
    v_x: float = 0
    v_y: float = 0
    a_x: float = 0
    a_y: float = 0
    tooltip: tk.Toplevel = None
    tooltip_label: tk.Label = None
    tooltip_after_id = None

    def __init__(self, x, y, canvas, animator):
        super().__init__(x, y, canvas, animator)
        self.setup_tooltip()
        self.update_tooltip_content()

    def setup_tooltip(self):
        self.tooltip = tk.Toplevel(self.canvas.window)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.geometry("110x25")
        
        # Create a Canvas to draw the rounded rectangle
        self.tooltip_canvas = tk.Canvas(self.tooltip, width=100, height=25, bg="white", highlightthickness=0)
        self.tooltip_canvas.pack(expand=True, fill="both")
        
        # Create a Label inside the Canvas
        self.tooltip_label = tk.Label(
            self.tooltip_canvas, text="", bg="white", fg="black", font=("Arial", 8)
        )
        self.tooltip_label.place(x=10, y=5)
        self.tooltip.withdraw()

    def rounded_rect(self, canvas, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
                  x1+radius, y1,
                  x2-radius, y1,
                  x2-radius, y1,
                  x2, y1,
                  x2, y1+radius,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2, y2-radius,
                  x2, y2,
                  x2-radius, y2,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1+radius, y2,
                  x1, y2,
                  x1, y2-radius,
                  x1, y2-radius,
                  x1, y1+radius,
                  x1, y1+radius,
                  x1, y1]
        return canvas.create_polygon(points, **kwargs, smooth=True)

    def update_tooltip_content(self):
        animation = self.get_current_animation()
        if not animation.show_tooltip or not animation.list_message:
            self.hide_tooltip()
            return
        message = animation.get_random_message()
        self.tooltip_label.configure(text=message)
        
        # Update the tooltip size based on the text width
        self.tooltip.update_idletasks()  # Update the geometry manager
        text_width = self.tooltip_label.winfo_reqwidth() + 20  # Add some padding
        self.tooltip.geometry(f"{text_width}x25")
        self.tooltip_canvas.config(width=text_width)
        self.tooltip_canvas.delete("all")
        self.rounded_rect(self.tooltip_canvas, 0, 0, text_width, 25, 10, fill="white", outline="black")
        
        self.update_tooltip_position()
        self.tooltip.deiconify()
        if self.tooltip_after_id:
            self.canvas.window.after_cancel(self.tooltip_after_id)
        display_time = random.randint(1000, 3000)  # Tối đa 3 giây
        self.tooltip_after_id = self.canvas.window.after(display_time, self.update_tooltip_content)

    def update_tooltip_position(self):
        animation = self.get_current_animation()
        size = animation.target_resolution
        tooltip_x = self.x + 55
        tooltip_y = self.y - 20
        self.tooltip.geometry(f"+{tooltip_x}+{tooltip_y}")

    def hide_tooltip(self):
        self.tooltip.withdraw()
        if self.tooltip_after_id:
            self.canvas.window.after_cancel(self.tooltip_after_id)
            self.tooltip_after_id = None

    def set_animation_state(self, state: AnimationStates) -> bool:
        changed = self.animator.set_animation_state(state)
        if changed:
            self.reset_movement()
            self.update_tooltip_content()
        return changed

    def reset_movement(self):
        animation = self.get_current_animation()
        self.v_x, self.v_y = animation.get_velocity()
        self.a_x, self.a_y = animation.get_acceleration()

    def do_movement(self):
        self.v_x += self.a_x
        self.v_y += self.a_y
        self.x = int(self.x + self.v_x)
        self.y = int(self.y + self.v_y)
        size = self.animator.animations[self.animator.state].target_resolution
        if self.x < 0 or self.x > self.canvas.resolution["width"] - size[0]:
            self.fade_out()
            if self.x < 0:
                self.x = self.canvas.resolution["width"] - size[0]
            else:
                self.x = 0
            self.fade_in()
        if self.y > self.canvas.resolution["height"] - size[1]:
            self.y = self.canvas.resolution["height"] - size[1]
            if self.animator.state == AnimationStates.FALLING:
                if AnimationStates.LANDED in self.animator.animations:
                    self.set_animation_state(AnimationStates.LANDED)
                else:
                    raise Exception("Stuck falling as no AnimationStates.LANDED is defined.")
        if self.tooltip.winfo_viewable():
            self.update_tooltip_position()

    def fade_out(self):
        self.hide_tooltip()
        for alpha in range(100, 0, -10):
            self.canvas.window.attributes("-alpha", alpha / 100)
            self.canvas.window.update()
            self.canvas.window.after(50)

    def fade_in(self):
        for alpha in range(0, 100, 10):
            self.canvas.window.attributes("-alpha", alpha / 100)
            self.canvas.window.update()
            self.canvas.window.after(50)

    def update(self):
        self.do_movement()
        super().update()
        if random.random() < 0.3 and not self.tooltip.winfo_viewable():
            self.update_tooltip_content()

    def on_tick(self):
        self.update()
        frame = super().get_current_animation_frame()
        super().set_geometry()
        self.canvas.label.configure(image=frame)
        self.handle_event()

    def handle_event(self):
        animation = self.get_current_animation()
        frame_duration = animation.get_frame_duration(self.animator.frame_number)
        self.canvas.window.after(frame_duration, self.on_tick)

    def start_move(self, event):
        if AnimationStates.GRABBED in self.animator.animations:
            self.set_animation_state(AnimationStates.GRABBED)

    def stop_move(self, event):
        available_states = list(self.animator.animations.keys())
        random_state = random.choice(available_states)
        self.set_animation_state(random_state)
        logger.info(f"Random state after clicked: {random_state}")

    def do_move(self, event):
        size = self.animator.animations[self.animator.state].target_resolution
        self.x = event.x_root - int(size[0] / 2)
        self.y = event.y_root - int(size[1] / 2)
        self.set_geometry()
        if self.tooltip.winfo_viewable():
            self.update_tooltip_position()

    def __repr__(self):
        size = self.animator.animations[self.animator.state].target_resolution
        return f"<VirtualPet of {size[0]}x{size[1]} at ({self.x}, {self.y}) using {str(self.animator)} and {str(self.canvas)}>"