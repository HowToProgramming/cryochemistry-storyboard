from enum import Enum
from typing import List, Optional, Type
from typing_extensions import Literal

class Position(Enum):
    BACKGROUND = 0
    FOREGROUND = 1
    OVERLAY = 2


class Action:
    def __init__(self, event_type: str, easing: int, start_time: int, end_time: int, params: list) -> None:
        self.event_type = event_type
        self.easing = easing
        self.start_time = start_time
        self.end_time = end_time if end_time != None else ""
        self.params = params
    
    def __repr__(self):
        param_text = ""
        for param in self.params:
            param_text += ","
            if param != None:
                param_text += param.__repr__()
            else:
                continue
                
        return f"{self.event_type},{self.easing},{self.start_time},{self.end_time}{param_text}"
    
    def render(self):
        return self.__repr__()
    
class Scale(Action):
    def __init__(self, easing: int, start_time: int, end_time:int, start_scale: float, end_scale: float) -> None:
        self.start_scale, self.end_scale = start_scale, end_scale
        super().__init__('S', easing, start_time, end_time, [start_scale, end_scale])

class Move(Action):
    def __init__(self, easing: int, start_time: int, end_time: int, pos_start: tuple, pos_end: tuple) -> None:
        self.x_start, self.y_start = pos_start
        self.x_end, self.y_end = pos_end
        super().__init__('M', easing, start_time, end_time, [self.x_start, self.y_start, self.x_end, self.y_end])

class Fade(Action):
    def __init__(self, easing: int, start_time: int, end_time: int, opacity_start: float, opacity_end: float) -> None:
        self.opacity_start = opacity_start
        self.opacity_end = opacity_end
        super().__init__('F', easing, start_time, end_time, [opacity_start, opacity_end])

class Rotate(Action):
    def __init__(self, easing: int, start_time: int, end_time: int, angle_start: float, angle_end: float) -> None:
        self.angle_start = angle_start
        self.angle_end = angle_end
        super().__init__('R', easing, start_time, end_time, [angle_start, angle_end])

class Color(Action):
    def __init__(self, easing: int, start_time: int, end_time: int, RGB1: tuple, RGB2: tuple):
        self.r1, self.g1, self.b1 = RGB1
        self.r2, self.g2, self.b2 = RGB2
        super().__init__('C', easing, start_time, end_time, [self.r1, self.g1, self.b1, self.r2, self.g2, self.b2])

class VectorScale(Action):
    def __init__(self, easing: int, start_time: int, end_time: int, start_size: tuple, end_size: tuple) -> None:
        self.start_x, self.start_y = start_size
        self.end_x, self.end_y = end_size
        super().__init__('V', easing, start_time, end_time, [self.start_x, self.start_y, self.end_x, self.end_y])

class MoveX(Action):
    def __init__(self, easing: int, start_time: int, end_time: int, x_start: float, x_end: float) -> None:
        self.x_start = x_start; self.x_end = x_end
        super().__init__('MX', easing, start_time, end_time, [x_start, x_end])

class MoveY(Action):
    def __init__(self, easing: int, start_time: int, end_time: int, y_start: float, y_end: float) -> None:
        self.y_start = y_start; self.x_end = y_end
        super().__init__('MY', easing, start_time, end_time, [y_start, y_end])

class Loop():
    def __init__(self, start_time: int, loop_count: int, actions: List[Type[Action]]) -> None:
        self.start_time = start_time
        self.loop_count = loop_count
        self.actions = actions
    
    def __repr__(self):
        loop_text = f"L,{self.start_time},{self.loop_count}\n  "
        loop_text += "\n  ".join([action.__repr__() for action in self.actions])
        return loop_text
    
    def render(self):
        return self.__repr__()

class SBObject:
    def __init__(self, file_name):
        self.filename = file_name
        self.action = []
    
    def add_action(self, action: Type[Action]):
        self.action.append(action)
    
    def add_actions(self, actions: List[Type[Action]]):
        self.action += actions
    
    def render(self, pos: Literal[Position.BACKGROUND, Position.FOREGROUND, Position.OVERLAY]):
        string = {
            Position.BACKGROUND: "Background",
            Position.FOREGROUND: "Foreground",
            Position.OVERLAY: "Overlay"
        }
        text = f'Sprite,{string[pos]},Centre,"{self.filename}",320,240\n ' + "\n ".join([i.render() for i in self.action])
        return text + "\n"

class StoryBoard:
    EVENT_TEXT = "[Events]\n//Background and Video events\n"
    BACKGROUND_TEXT = "//Storyboard Layer 0 (Background)\n"
    FAILPASS_TEXT = "//Storyboard Layer 1 (Fail)\n//Storyboard Layer 2 (Pass)\n"
    FOREGROUND_TEXT = "//Storyboard Layer 3 (Foreground)\n"
    OVERLAY_TEXT = "//Storyboard Layer 4 (Overlay)\n"
    SOUND_SAMPLES = "//Storyboard Sound Samples"
    def __init__(self, background_objects=[], foreground_objects=[], overlay_objects=[]) -> None:
        self.background_object = background_objects
        self.foreground_object = foreground_objects
        self.overlay_object = overlay_objects
    
    def render(self):
        text = self.EVENT_TEXT + \
        self.BACKGROUND_TEXT + "".join([i.render(Position.BACKGROUND) for i in self.background_object]) + \
        self.FAILPASS_TEXT + self.FOREGROUND_TEXT + "".join([i.render(Position.FOREGROUND) for i in self.foreground_object]) + \
        self.OVERLAY_TEXT + "".join([i.render(Position.OVERLAY) for i in self.overlay_object])
        return text + self.SOUND_SAMPLES
    
    def osb(self, osb_fp):
        with open(osb_fp, 'w+') as osb:
            osb.write(self.render())