"""
TODO:
    - [x] Basic drawing functions
    - [x] Fps and ms counter
    - [ ] Add more drawing functions
    - [ ] Support for multiple monitors
    - [ ] Support for multiple targets
    - [ ] Compile using Cython/nuitka for better performance on low end systems
    - [x] Create own font rendering system
    - [ ] Add anchor system for text rendering

FIXME:
    - [ ] Method overloading instead of `_ex` & `with_angle` functions
"""

import math
import OpenGL.GL as gl
import OpenGL.GLUT as glut
import glfw
import glm
from rich.traceback import install
import win32gui
import win32api
import win32con
import time
from .helper import Point, Rect, RGBA, Color
from typing import Literal

install()

class Target:
    def __init__(self, title: str) -> None:
        self._title = title
        self._hwnd = win32gui.FindWindow(None, title)
        self._rect = Rect(*win32gui.GetWindowRect(self._hwnd))
        self._is_valid = win32gui.GetForegroundWindow() == self._hwnd

    @property
    def title(self) -> str:
        return self._title

    @property
    def hwnd(self) -> int:
        return self._hwnd
    
    @property
    def rect(self) -> Rect:
        return self._rect

    @property
    def is_valid(self) -> bool:
        return self._is_valid

    def __bool__(self) -> bool:
        return self.is_valid

    @property
    def exists(self) -> bool:
        return win32gui.IsWindow(self._hwnd) and self.hwnd != 0

    def find(self) -> None:
        if not self._hwnd:
            self._hwnd = win32gui.FindWindow(None, self._title)

    def update(self) -> None:
        self._rect = Rect(*win32gui.GetWindowRect(self._hwnd))
        self._is_valid = win32gui.GetForegroundWindow() == self._hwnd




def get_monitor_dpi():
    """ Return monitor resolution in dot per inch.
        Returns:
            float: monitor dot per inch
    """
    monitor = glfw.get_primary_monitor()[0]
    # Size in mm
    video_physical_size = glm.vec2(glfw.get_monitor_physical_size(monitor))
    #Monitor info
    video_resolution = glm.vec2(glfw.get_video_mode(monitor).size)
    # Calculate screen DPI
    inch_to_mm = 0.393701/10.0
    dpi = (video_resolution/(video_physical_size*inch_to_mm))
    return sum(dpi) / 2.0


class Overlay:
    def __init__(self, target: str) -> None:
        self._target = Target(target)
        self._on_tick = None
        self._loop_time = time.time()
        self._frames = 0
        self.fps = 0
        self.ms = 0
        self._window = None


    def create(self) -> None:
        # init glfw
        if not glfw.init() or not glut.glutInit():
            self.error("glfw/glut can not be initialized!")
        
        glfw.window_hint(glfw.FLOATING, glfw.TRUE)
        glfw.window_hint(glfw.TRANSPARENT_FRAMEBUFFER, glfw.TRUE)
        glfw.window_hint(glfw.DECORATED, glfw.FALSE)
        glfw.window_hint(glfw.FOCUS_ON_SHOW, glfw.FALSE)
        glfw.window_hint(glfw.RESIZABLE, glfw.FALSE)
        glfw.window_hint(glfw.SAMPLES, 4)

        # create window

        self._window = glfw.create_window(1920, 1079, "", None, None)
        if not self._window:
            self.error("glfw window can not be created!")
        
        glfw.make_context_current(self._window)
        glfw.set_input_mode(self._window, glfw.CURSOR, glfw.CURSOR_DISABLED)
        glfw.swap_interval(0) # disable vsync

        # set opengl attributes
        gl.glPushAttrib(gl.GL_ALL_ATTRIB_BITS)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPushMatrix()
        gl.glLoadIdentity()
        gl.glOrtho(0, 1920, 1079, 0, -1, 1)
        gl.glDisable(gl.GL_DEPTH_TEST)
        gl.glDisable(gl.GL_TEXTURE_2D)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        # gl.glEnable(gl.GL_LINE_SMOOTH)


        # make window transparent
        win32gui.SetWindowLong(self.hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(self.hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT)

        # hide from taskbar 
        win32gui.SetWindowLong(self.hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(self.hwnd, win32con.GWL_EXSTYLE) & ~win32con.WS_EX_APPWINDOW | win32con.WS_EX_TOOLWINDOW)

        glfw.set_window_aspect_ratio(self._window, 4, 3)

    def stop(self) -> None:
        glfw.set_window_should_close(self._window, True)

    def destroy(self) -> None:
        glfw.destroy_window(self._window)
        glfw.terminate()

    def run(self) -> None:
        if not self._on_tick:
            self.error("No render callback set!")
        
        while not self.target.exists:
            self.target.update()
            time.sleep(1)


        while not glfw.window_should_close(self._window):
            # poll events
            glfw.poll_events()

            # update target rect and validity
            self.target.update()

            # increment frame counter
            self._current_loop_time = time.time()
            self._frames += 1

            # calculate fps and ms and call seconds callback
            if self._current_loop_time - self._loop_time >= 1:
                self.ms = int(1000/self._frames)
                self.fps = int(self._frames/(self._current_loop_time - self._loop_time))
                self._loop_time = self._current_loop_time
                self._frames = 0

                # call seconds callback

            # call render callback
            self.on_tick(self)

            # cleaning
            glfw.swap_buffers(self._window)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)
            gl.glClearColor(0, 0, 0, 0)
            

        self.destroy()

    def error(self, error) -> None:
        if not self._on_error:
            self._on_error(self, error)
        
        self._on_error(self, error)

    def _on_error(self, error) -> None:
        raise Exception(error)


    @property
    def hwnd(self) -> int:
        if not self._window:
            self.error("Window not created!")
            return 0
        return glfw.get_win32_window(self._window)

    @property
    def on_tick(self) -> callable:
        return self._on_tick
    
    @on_tick.setter
    def on_tick(self, callback: callable) -> None:
        self._on_tick = callback

    @property
    def on_error(self) -> callable:
        return self._on_error
    
    @on_error.setter
    def on_error(self, callback: callable) -> None:
        self._on_error = callback

    @property
    def target(self) -> Target:
        return self._target

    #  line drawing functions

    @staticmethod
    def draw_line(start: Point | tuple[int, int], end: Point | tuple[int, int], color: RGBA | tuple[int, int, int, float]) -> None:
        gl.glLineWidth(1)
        gl.glBegin(gl.GL_LINES)
        gl.glColor4f(*color)
        gl.glVertex2f(*start)
        gl.glVertex2f(*end)
        gl.glEnd()
    
    @staticmethod
    def draw_line_ex(start: Point | tuple[int, int], end: Point | tuple[int, int], width: int, color: RGBA | tuple[int, int, int, float]) -> None:
        gl.glLineWidth(width)
        gl.glBegin(gl.GL_LINES)
        gl.glColor4f(*color)
        gl.glVertex2f(*start)
        gl.glVertex2f(*end)
        gl.glEnd()

    @staticmethod
    def draw_line_from_angle(start: Point | tuple[int, int], angle: int, length: int, color: RGBA | tuple[int, int, int, float]) -> None:
        gl.glLineWidth(1)
        gl.glBegin(gl.GL_LINES)
        gl.glColor4f(*color)
        gl.glVertex2f(*start)
        gl.glVertex2f(start.x + math.sin(angle) * length, start.y + math.cos(angle) * length)
        gl.glEnd()

    @staticmethod
    def draw_line_from_angle_ex(start: Point | tuple[int, int], angle: int, length: int, width: int, color: RGBA | tuple[int, int, int, float]) -> None:
        gl.glLineWidth(width)
        gl.glBegin(gl.GL_LINES)
        gl.glColor4f(*color)
        gl.glVertex2f(*start)
        gl.glVertex2f(start.x + math.sin(angle) * length, start.y + math.cos(angle) * length)
        gl.glEnd()


    # rect drawing functions

    @staticmethod
    def draw_filled_rect(rect: Rect, color: RGBA | tuple[int, int, int, float]) -> None:
        gl.glBegin(gl.GL_QUADS)
        gl.glColor4f(*color)
        gl.glVertex2f(rect.left, rect.top)
        gl.glVertex2f(rect.right, rect.top)
        gl.glVertex2f(rect.right, rect.bottom)
        gl.glVertex2f(rect.left, rect.bottom)
        gl.glEnd()

    @staticmethod
    def draw_filled_rect_from_angle(rect: Rect, color: RGBA | tuple[int, int, int, float], angle: int) -> None:
        gl.glPushMatrix()
        gl.glTranslatef(rect.center.x, rect.center.y, 0)
        gl.glRotatef(angle, 0, 0, 1)
        gl.glTranslatef(-rect.center.x, -rect.center.y, 0)
        gl.glBegin(gl.GL_QUADS)
        gl.glColor4f(*color)
        gl.glVertex2f(rect.left, rect.top)
        gl.glVertex2f(rect.right, rect.top)
        gl.glVertex2f(rect.right, rect.bottom)
        gl.glVertex2f(rect.left, rect.bottom)
        gl.glEnd()
        gl.glPopMatrix()

    @staticmethod
    def draw_empty_rect(rect: Rect, color: RGBA | tuple[int, int, int, float]) -> None:
        gl.glLineWidth(1)
        gl.glBegin(gl.GL_LINE_LOOP)
        gl.glColor4f(*color)
        gl.glVertex2f(rect.left, rect.top)
        gl.glVertex2f(rect.right, rect.top)
        gl.glVertex2f(rect.right, rect.bottom)
        gl.glVertex2f(rect.left, rect.bottom)
        gl.glEnd()

    @staticmethod
    def draw_empty_rect_ex(rect: Rect, width: int, color: RGBA | tuple[int, int, int, float]) -> None:
        gl.glLineWidth(width)
        gl.glBegin(gl.GL_LINE_LOOP)
        gl.glColor4f(*color)
        gl.glVertex2f(rect.left, rect.top)
        gl.glVertex2f(rect.right, rect.top)
        gl.glVertex2f(rect.right, rect.bottom)
        gl.glVertex2f(rect.left, rect.bottom)
        gl.glEnd()

    @staticmethod
    def draw_empty_rect_from_angle(rect: Rect, color: RGBA | tuple[int, int, int, float], angle: int) -> None:
        gl.glLineWidth(1)
        gl.glPushMatrix()
        gl.glTranslatef(rect.center.x, rect.center.y, 0)
        gl.glRotatef(angle, 0, 0, 1)
        gl.glTranslatef(-rect.center.x, -rect.center.y, 0)
        gl.glBegin(gl.GL_LINE_LOOP)
        gl.glColor4f(*color)
        gl.glVertex2f(rect.left, rect.top)
        gl.glVertex2f(rect.right, rect.top)
        gl.glVertex2f(rect.right, rect.bottom)
        gl.glVertex2f(rect.left, rect.bottom)
        gl.glEnd()
        gl.glPopMatrix()

    @staticmethod
    def draw_empty_rect_from_angle_ex(rect: Rect, width: int, color: RGBA | tuple[int, int, int, float], angle: int) -> None:
        gl.glLineWidth(width)
        gl.glPushMatrix()
        gl.glTranslatef(rect.center.x, rect.center.y, 0)
        gl.glRotatef(angle, 0, 0, 1)
        gl.glTranslatef(-rect.center.x, -rect.center.y, 0)
        gl.glBegin(gl.GL_LINE_LOOP)
        gl.glColor4f(*color)
        gl.glVertex2f(rect.left, rect.top)
        gl.glVertex2f(rect.right, rect.top)
        gl.glVertex2f(rect.right, rect.bottom)
        gl.glVertex2f(rect.left, rect.bottom)
        gl.glEnd()
        gl.glPopMatrix()


    # circle drawing functions

    @staticmethod
    def draw_filled_circle(position: Point | tuple[int, int], radius: int, color: RGBA | tuple[int, int, int, float]) -> None:
        gl.glBegin(gl.GL_TRIANGLE_FAN)
        gl.glColor4f(*color)
        gl.glVertex2f(*position)
        for i in range(360):
            gl.glVertex2f(position.x + math.sin(i) * radius, position.y + math.cos(i) * radius)
        gl.glEnd()

    @staticmethod
    def draw_filled_circle_from_angle(position: Point | tuple[int, int], radius: int, color: RGBA | tuple[int, int, int, float], angle: int) -> None:
        gl.glPushMatrix()
        gl.glTranslatef(position.x, position.y, 0)
        gl.glRotatef(angle, 0, 0, 1)
        gl.glTranslatef(-position.x, -position.y, 0)
        gl.glBegin(gl.GL_TRIANGLE_FAN)
        gl.glColor4f(*color)
        gl.glVertex2f(*position)
        for i in range(360):
            gl.glVertex2f(position.x + math.sin(i) * radius, position.y + math.cos(i) * radius)
        gl.glEnd()
        gl.glPopMatrix()

    @staticmethod
    def draw_empty_circle(position: Point | tuple[int, int], radius: int, color: RGBA | tuple[int, int, int, float]) -> None:
        # draw empty circle
        gl.glColor4f(*color)
        theta = math.pi * 2 / float(500)
        tangetial_factor = math.tan(theta)
        radial_factor = math.cos(theta)
        x = radius
        y = 0
        gl.glLineWidth(1)
        gl.glBegin(gl.GL_LINE_LOOP)
        
        for i in range(500):
            gl.glVertex2f(x + position[0], y + position[1])
            tx = -y
            ty = x

            x += tx * tangetial_factor
            y += ty * tangetial_factor

            x *= radial_factor
            y *= radial_factor
        gl.glEnd()

    @staticmethod
    def draw_empty_circle_ex(position: Point | tuple[int, int], radius: int, width: int, color: RGBA | tuple[int, int, int, float]) -> None:
        # draw empty circle
        gl.glColor4f(*color)
        theta = math.pi * 2 / float(500)
        tangetial_factor = math.tan(theta)
        radial_factor = math.cos(theta)
        x = radius
        y = 0
        gl.glLineWidth(width)
        gl.glBegin(gl.GL_LINE_LOOP)
        
        for i in range(500):
            gl.glVertex2f(x + position[0], y + position[1])
            tx = -y
            ty = x

            x += tx * tangetial_factor
            y += ty * tangetial_factor

            x *= radial_factor
            y *= radial_factor
        gl.glEnd()

    @staticmethod
    def draw_filled_dot(position: Point | tuple[int, int], point_width: float, color: RGBA | tuple[int, int, int, float]) -> None:
        gl.glPointSize(point_width)
        gl.glBegin(gl.GL_POINTS)
        gl.glColor4f(*color)
        gl.glVertex2f(*position)
        gl.glEnd()

    @staticmethod
    def draw_text(text: str, bottom_left: Point, color: RGBA, font=glut.GLUT_BITMAP_9_BY_15) -> None:
        """
        Draws text on the screen.
        TODO: 
            Add anchor system (glutBitmapWidth(font, char) & glutBitmapHeight(font))
            or using much simple calculation with GLUT_BITMAP_9_BY_15 or GLUT_BITMAP_8_BY_13
        """
        center_center = Point(bottom_left.x - int(9*len(text)/2), bottom_left.y)
        gl.glColor4f(0.0, 1.0, 0.0, 1.0)
        gl.glRasterPos2i(*center_center)
        lines = text.split("\n")
        for line in lines:
            for c in line:
                glut.glutBitmapCharacter(font, ord(c))

    def draw_test(self, rect: Rect) -> None:
        self.draw_empty_rect(rect, Color.WHITE)
        self.draw_line(Point(rect.left, rect.top), Point(rect.right, rect.bottom), Color.WHITE)
        self.draw_line(Point(rect.right, rect.top), Point(rect.left, rect.bottom), Color.WHITE)
        self.draw_empty_circle_ex(rect.center, 100, 5, Color.ORANGE)
        
        self.draw_text(f"{str(self.fps)} fps", Point(rect.left, rect.top))
        self.draw_text(f"{str(self.ms)} ms", Point(rect.left, rect.top+30))

    @staticmethod
    def get_input(key: int) -> bool:
        """
        Returns True if the key is pressed, False otherwise.
        """
        return win32api.GetAsyncKeyState(key) & 1

