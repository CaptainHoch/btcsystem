# sc_my.py

from PySide2.QtCore import *
from PySide2.QtGui import QPainterPath
import p5

WHITE = (255,)
BLACK = (0,)

ARROW_CACHE = {}


class BaseDrawer:
    def __init__(self, w, h, frame_rate=60):
        self.width = w
        self.height = h
        self.clickObservers = []
        self.doubleClickObservers = []
        self.onDrawObservers = []
        p5.set_sketch(lambda: self.setup(w, h), self.draw,
                      handlers={'mouse_pressed': self.mouse_clicked,
                                'mouse_double_clicked': self.mouse_double_clicked},
                      frame_rate=frame_rate)

    def setup(self, w, h):
        p5.size(w, h)

    def draw(self):
        for o in self.onDrawObservers:
            o()

    def mouse_clicked(self, event):
        try:
            for o in self.clickObservers:
                o(event)
        except:
            return

    def mouse_double_clicked(self, event):
        try:
            for o in self.doubleClickObservers:
                o(event)
        except:
            return

    def clear_observers(self):
        self.clickObservers.clear()
        self.doubleClickObservers.clear()
        self.onDrawObservers.clear()

    @property
    def canvas(self):
        return p5.get_canvas().native


class ShapesDrawer(BaseDrawer):
    def __init__(self, w, h, frame_rate=60):
        BaseDrawer.__init__(self, w, h, frame_rate=frame_rate)

    def addLine(self, p1, p2):
        p5.line(p1, p2)

    '''
    def addPath(self, path):
        p5.path(path)
    '''

    def addArrow(self, p1, p2, color=BLACK):
        p5.stroke(color)

        self.addLine(p1, p2)

        to_int = (int(p1[0]), int(p1[1]), int(p2[0]), int(p2[1]))
        if to_int in ARROW_CACHE:
            arrow = ARROW_CACHE[to_int]

        else:
            p1 = QPoint(*p1)
            p2 = QPoint(*p2)

            path = QPainterPath()
            path.moveTo(p1)
            path.lineTo(p2)

            line = QLineF(p1, p2)

            end = p2
            pathlen = path.length()
            leng = min(10, pathlen / 4.0)
            arrowbase = path.pointAtPercent(path.percentAtLength(pathlen - leng))
            l1 = QLineF(arrowbase, end)
            l2 = QLineF(arrowbase, end)
            l1.setAngle(line.angle() - 150)
            l2.setAngle(line.angle() + 150)
            l1.setLength(l1.length() / 2.0)
            l2.setLength(l2.length() / 2.0)

            arrow = (arrowbase.toTuple(), l1.p2().toTuple(), end.toTuple(), l2.p2().toTuple())
            ARROW_CACHE[to_int] = arrow

        p5.fill(color)
        p5.quad(*arrow)

    def addCircle(self, x, y, r, color=WHITE):
        with p5.push_style():
            p5.no_stroke()
            p5.fill(*color)
            p5.circle((x, y), 2*r)

    def clear(self):
        p5.background(255)
