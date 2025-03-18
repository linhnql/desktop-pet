import tkinter as tk
from ..animation import AnimationStates
from .simple_pet import SimplePet
from src import logger
import random
import win32gui


class InteractablePet(SimplePet):
    v_x: float = 0
    v_y: float = 0
    a_x: float = 0
    a_y: float = 0
    tooltip: tk.Toplevel = None
    tooltip_label: tk.Label = None
    tooltip_after_id = None
    is_desktop_active = True  # Track if desktop is active

    def __init__(self, x, y, canvas, animator):
        super().__init__(x, y, canvas, animator)
        self.setup_tooltip()
        self.update_tooltip_content()
        self.canvas.window.wm_attributes("-topmost", True)
        self.canvas.window.bind("<FocusOut>", self.on_focus_out)
        self.keep_on_top()
        
        # Start checking for window focus
        self.check_desktop_active()
        self.app_title = self.canvas.window.title()

    def keep_on_top(self):
        self.canvas.window.wm_attributes("-topmost", True)
        self.canvas.window.after(100, self.keep_on_top)

    def on_focus_out(self, event):
        self.canvas.window.wm_attributes("-topmost", True)
        # When focus is lost, hide tooltip
        self.hide_tooltip()

    def is_on_desktop(self):
        """
        Check if the desktop or the app itself (title containing 'Totoro') is active.
        Returns True if desktop or app is active, False if another application is active.
        """
        foreground_window = win32gui.GetForegroundWindow()
        
        try:
            class_name = win32gui.GetClassName(foreground_window)
            window_title = win32gui.GetWindowText(foreground_window)
            # logger.info(f"Foreground window: handle={foreground_window}, class={class_name}, title={window_title}")
            
            if self.app_title == window_title:
                # logger.info(f"App detected as desktop (title contains '{self.app_title}')")
                return True
            
            desktop_classes = {
                "Progman",                      # Program Manager - Main desktop on older Windows (XP, 7, 10)
                "WorkerW",                      # Wallpaper layer - Often appears when desktop is visible (Windows 7, 10)
                "SysListView32",                # List of icons on desktop (child of Progman)
                "Shell_TrayWnd",                # Main taskbar (Start menu, system tray)
                "Static",                       # Hidden window when all apps are minimized (based on your log)
                "DesktopWindowXamlSource",      # Desktop on Windows 11 (XAML-based)
                "NotifyIconOverflowWindow",     # System tray overflow (when clicking hidden icons in tray)
                "Windows.UI.Core.CoreWindow",   # Core UI window on Windows 10/11 (UWP-related desktop components)
                "Shell_SecondaryTrayWnd",       # Secondary taskbar on multi-monitor setups (Windows 10/11)
                "DV2ControlHost",               # Desktop View control host (related to Start menu on Windows 7/8)
                "Shell_DLL_DefView",            # Default view of desktop (child of Progman on some systems)
                "MultitaskingViewFrame",        # Task View or Alt+Tab interface on Windows 10/11
                "TaskListThumbnailWnd",         # Thumbnail preview when hovering over taskbar
                "TrayNotifyWnd",                # System tray notification area
                "TrayClockWClass",              # Clock in system tray
                "ReBarWindow32",                # Toolbar in taskbar
                "CiceroUIWndFrame",             # Input method editor (IME) window (may appear on desktop)
                "ApplicationManager_DesktopShellWindow",  # Desktop shell on Windows 11 (less common)
                "Start",                        # Start menu on Windows 10/11 when opened
                "ExplorerWClass",               # Explorer window (may relate to desktop on some configurations)
                "CabinetWClass",                # File Explorer window (if Explorer displays desktop)
                "ApplicationFrameWindow",       # UWP app frame (Windows 11 shell components)
            }
            if class_name in desktop_classes:
                # logger.info("Desktop detected (class match)")
                return True
                
        except Exception as e:
            logger.info(f"Foreground window: handle={foreground_window}, error getting info: {str(e)}")
        
        # logger.info("Application detected (no desktop or app match)")
        return False

    def check_desktop_active(self):
        """
        Periodically check if desktop is active and update state
        """
        previous_state = self.is_desktop_active
        self.is_desktop_active = self.is_on_desktop()
        
        # If desktop state changes, update tooltip
        if previous_state != self.is_desktop_active:
            if not self.is_desktop_active and self.tooltip.winfo_viewable():
                self.hide_tooltip()
            elif self.is_desktop_active and not self.tooltip.winfo_viewable():
                self.update_tooltip_content()
        
        self.canvas.window.after(300, self.check_desktop_active)

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
        # Only show tooltip if desktop is active
        if not self.is_desktop_active:
            self.hide_tooltip()
            return
            
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
        display_time = random.randint(1000, 3000)  # Maximum 3 seconds
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
        # Only show random tooltips if desktop is active
        if random.random() < 0.3 and not self.tooltip.winfo_viewable() and self.is_desktop_active:
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
        excluded_states = {AnimationStates.WALK_POSITIVE_MANY, AnimationStates.WALK_NEGATIVE_MANY}
        available_states = [state for state in self.animator.animations.keys() if state not in excluded_states]
        random_state = random.choice(available_states)
        self.set_animation_state(random_state)
        # logger.info(f"Random state after clicked: {random_state}")

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