# ui_p5.py
# Created by Daniel Hoch at 11.4 18:00

import networkx as nx
import p5
from PySide2.QtCore import *
from PySide2.QtWidgets import QVBoxLayout, QMessageBox

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvas
import matplotlib.pyplot as plt

from datasearch.graphics.shapes_drawer import BaseDrawer, ShapesDrawer
from datasearch.graphics.ui_basic import Ui
from datasearch.networking.client import setup_client, graph_from_server

from random import random

RED    = lambda x: (max(255 - 50*x, 0), 0, 0)
BLUE   = lambda x: (0, min(30*(x+3), 255), min(30*(x+7), 255))
YELLOW = (255, 255, 0)
BLACK  = 0
GRAY   = 221
GRAYSCALE = lambda x: (204 - max(x-50, 0) * 4, ) * 3

C = 600
R = 30

MARGIN = 50

SHELL = 0
BIPARTITE = 1
SPECTRAL = 2
SPRING = 3
CIRCULAR = 4

DATA_MODE = 0
DIAG_IN_MODE = 1
DIAG_OUT_MODE = 2

DIAGRAMS = 'diagrams'

prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']
colors = colors[1:] + colors[:1]
colors_hex = list(colors)
colors = [(c[1:3], c[3:5], c[5:7]) for c in colors]
colors = [(int(x, 16), int(y, 16), int(z, 16)) for x, y, z in colors]
COLORS = lambda x: colors[x % len(colors)]


def printarrow(x, y):
    return lambda: print("%s ==> %s" % (x, y))


def printnode(n):
    return lambda: print("Node no. %s" %n)


def generate_info(key, g):
    # inc_m = random() * 100
    # out_m = random() * inc_m
    basic = {
        'Alias': '', # 'No Alias',
        'Address': str(key),
        'Sent': '', # str(out_m) + ' BTC',
        'Received': '', # str(inc_m - out_m) + ' BTC',
        'Balance': '', # str(inc_m - out_m) + ' BTC',
        'Transactions': '', # str(int(random() * 1000)),
        'Avg. In Transaction': '', # str(random()) + ' BTC',
        'Avg. Out Transaction': '' # str(random() * 2) + ' BTC'
    }
    inp = g.predecessors(key)
    if inp:
        i_dig = {}
        s = 0
        for i in inp:
            if i != key:
                r = random()
                i_dig[i] = r
                s += r
        other = 0
        final_i_dig = {}
        other_il = []
        # m = max(i_dig.values())
        i_thresh = 0.1 # min(0.1, max([x for x in i_dig.values() if x != m]))
        for i in i_dig:
            i_dig[i] /= s
            if i_dig[i] < i_thresh:
                other += i_dig[i]
                other_il.append(i)
            else:
                final_i_dig[i] = i_dig[i]
        if other > 0:
            final_i_dig['other'] = other
    else:
        final_i_dig, other_il = None, None
    out = g.successors(key)
    if out:
        o_dig = {}
        s = 0
        for o in out:
            if o != key:
                r = random()
                o_dig[o] = r
                s += r
        other = 0
        other_ol = []
        final_o_dig = {}
        # m = max(o_dig.values())
        o_thresh = 0.1 # min(0.1, max([x for x in o_dig.values() if x != m]))
        for o in o_dig:
            o_dig[o] /= s
            if o_dig[o] < o_thresh:
                other += o_dig[o]
                other_ol.append(o)
            else:
                final_o_dig[o] = o_dig[o]
        if other > 0:
            final_o_dig['other'] = other
    else:
        final_o_dig, other_ol = None, None
    diagrams = {'incoming money': (final_o_dig, other_ol), 'outgoing money': (final_i_dig, other_il)}
    advanced = {
        'In-Degree': '', # int(random() * 100),
        'Out-Degree': '', # int(random() * 100),
        'Unique In-Degree': '', # int(random() * 10),
        'Unique Out-Degree': '', # int(random() * 10),
        'Stdev. In Transaction': '', # str(random()),
        'Stdev. Out Transaction': '', # str(random()),
        'Local Clustering Coefficient': '' # random()
    }
    anomaly = random() * 100
    return {'basic': basic, DIAGRAMS: diagrams, 'advanced': advanced, 'anomaly': anomaly}


class Drawer(ShapesDrawer):
    def __init__(self, w, h, win, first_center, view_mode=SHELL):
        ShapesDrawer.__init__(self, w, h)
        self.win = win
        self.g = None
        self.nodeInfo = None
        self.center = None
        self.viewMode = view_mode
        self.draw = False
        self.pos = None
        self.target_pos = None
        self.to_draw = None
        self.history = []
        self.t = 0
        self.displayMode = DATA_MODE
        self.current = None
        self.first_center = first_center

    def setup(self, w, h):
        BaseDrawer.setup(self, w, h)
        p5.background(255)

        # self.onDrawObservers.append(lambda: self.stretch(mouse_x, mouse_y))

        self.g = self.win.g
        max_node = self.first_center
        self.g = self.g.subgraph(list(self.g) + [max_node])
        self.nodeInfo = {}
        for k in self.g.nodes:
            self.nodeInfo[k] = generate_info(k, self.g)

        i = generate_info(max_node, self.g)
        i['basic']['Alias'] = 'Suspect'
        self.nodeInfo[max_node] = i

        self.t = 0
        self.recenter(max_node)
        print('setup done', max_node)

    def draw(self):
        BaseDrawer.draw(self)

        if not self.draw:
            return
        self.draw = False

        draw_properties = {}
        if self.displayMode == DIAG_IN_MODE:
            for k in self.pos:
                draw_properties[k] = (15, GRAYSCALE(0))

            for i, c in enumerate(self.center):
                draw_properties[c] = (25, BLUE(i))

            x = self.current
            for i, k in enumerate(self.nodeInfo[x][DIAGRAMS]['incoming money'][0]):
                if k in draw_properties:
                    draw_properties[k] = (draw_properties[k][0], COLORS(i+1))

            for k in self.nodeInfo[x][DIAGRAMS]['incoming money'][1]:
                if k in draw_properties:
                    draw_properties[k] = (draw_properties[k][0], COLORS(0))
        elif self.displayMode == DIAG_OUT_MODE:
            for k in self.pos:
                draw_properties[k] = (15, GRAYSCALE(0))

            for i, c in enumerate(self.center):
                draw_properties[c] = (25, BLUE(i))

            x = self.current
            for i, k in enumerate(self.nodeInfo[x][DIAGRAMS]['outgoing money'][0]):
                if k in draw_properties:
                    draw_properties[k] = (draw_properties[k][0], COLORS(i+1))

            for k in self.nodeInfo[x][DIAGRAMS]['outgoing money'][1]:
                if k in draw_properties:
                    draw_properties[k] = (draw_properties[k][0], COLORS(0))
        else:
            for k in self.pos:
                draw_properties[k] = (15, GRAYSCALE(self.nodeInfo[k]['anomaly']))

            for i, c in enumerate(self.center):
                draw_properties[c] = (25, BLUE(i))

        draw_properties[self.current] = (25, draw_properties[self.current][1])

        # The actual Drawing
        self.clear()

        for k in self.pos:
            self.addNode(k, draw_properties[k][0], self.nodeInfo[k],
                         color=draw_properties[k][1])
        self.addEdges(draw_properties, self.to_draw)

    def setMode(self, mode):
        if self.displayMode != mode:
            self.displayMode = mode
            self.draw = True

    def stretch(self, x, y):
        for k in self.pos:
            kx, ky = self.target_pos[k]
            if (kx - x) ** 2 + (ky - y) ** 2 <= R ** 2:
                continue
            l = QLineF(x, y, kx, ky)
            len = l.length()
            l.setLength(len + C / len)
            target = l.p2()
            self.pos[k] = (max(0, min(self.width, target.x())), max(0, min(self.height, target.y())))

    def mouse_clicked(self, event):
        print('-' * 50)
        print('Mouse: ', mouse_x, mouse_y)
        print('Event Pos: ', event.position)
        print('Pos: ', self.pos)
        super(Drawer, self).mouse_clicked(event)

    def set_time(self, t):
        print('The time is', t)
        self.t = t
        self.center = list(self.history[t - 1])
        self.win.enable_bf(back=(t != 1), forward=(t != len(self.history)))
        self.show_graph()

    def back(self):
        if self.t > 1:
            self.set_time(self.t - 1)

    def forward(self):
        if self.t < len(self.history):
            self.set_time(self.t + 1)

    def expand(self, center):
        self.center.append(center)
        self.history = self.history[:self.t]
        self.history.append(list(self.center))
        self.set_time(self.t + 1)

    def show_graph(self):
        self.clear_observers()
        self.win.setTitle(r'<font color="white"> Data Search results for <font color="tomato">{}</font>'
                          r' (<font color="tomato">{}<font color="white">)'.
                          format(self.nodeInfo[self.center[-1]]['basic']['Alias'],
                                 self.nodeInfo[self.center[-1]]['basic']['Address']))

        # Draw graph
        succ = list()
        pred = list()
        for c in self.center:
            succ.extend(self.g.successors(c))
            pred.extend(self.g.predecessors(c))
        print(succ, pred)
        nodes_to_draw = set(succ + pred + self.center)
        to_draw = self.g.subgraph(nodes_to_draw)
        if self.viewMode == SHELL:
            pos = nx.drawing.shell_layout(to_draw)
            self.position_centers(pos)
        elif self.viewMode == BIPARTITE:
            pos = nx.drawing.bipartite_layout(to_draw, succ)
        elif self.viewMode == CIRCULAR:
            pos = nx.drawing.circular_layout(to_draw, center=(0, 0))
            self.position_centers(pos)
        elif self.viewMode == SPRING:
            pos = nx.drawing.bipartite_layout(to_draw, succ)
            self.position_centers(pos)
            pos = nx.spring_layout(to_draw, k=50, pos=pos)
        else:
            pos = nx.drawing.spectral_layout(to_draw)

        w = self.canvas.width() - MARGIN
        h = self.canvas.height() - MARGIN

        minx = min([x[0] for x in pos.values()])
        miny = min([x[1] for x in pos.values()])
        maxx = max([x[0] for x in pos.values()])
        maxy = max([x[1] for x in pos.values()])

        for k in pos:
            t, s = pos[k]
            pos[k] = (w * (t - minx) / (maxx - minx) + MARGIN / 2, h * (s - miny) / (maxy - miny) + MARGIN / 2)

        self.pos = dict(pos)
        self.target_pos = dict(pos)
        self.to_draw = to_draw
        self.showData(self.center[-1])
        self.draw = True

    def recenter(self, center):
        # Recomputes pos

        self.center = []
        self.expand(center)

    def position_centers(self, pos):
        for c in self.center:
            pos[c] = (0, 0)

    def showData(self, key):
        self.current = key
        self.draw = True
        self.win.displayDict(self.nodeInfo[key])

    def addNode(self, key, r, data, color):
        x, y = self.pos[key]
        self.addCircle(x, y, r, color=color)

        def doIfInCircle(event):
            x, y = self.pos[key]
            ex, ey = mouse_x, mouse_y
            if (ex - x) ** 2 + (ey - y) ** 2 <= r ** 2:
                print('Yay!', key)
                self.showData(key)
                raise 1

        def dcIfInCircle(event):
            x, y = self.pos[key]
            ex, ey = mouse_x, mouse_y
            if (ex - x) ** 2 + (ey - y) ** 2 <= r ** 2:
                self.expand(key)
                raise 1

        self.clickObservers.append(doIfInCircle)
        self.doubleClickObservers.append(dcIfInCircle)

    def addEdges(self, draw_properties, graph):
        edges = [(u, v) for u in graph for v in graph.adj[u] if u != v]
        edges = sorted(edges, key=lambda x: x[0] in self.center or x[1] in self.center)
        for key, ng in edges:
            self.addEdge(draw_properties, key, ng)

    def addEdge(self, draw_properties, s, t):
        x, y = self.pos[t]
        ngx, ngy = self.pos[s]
        l = QLineF(x, y, ngx, ngy)
        nl = l.normalVector()
        nl = nl.translated(-x, -y)
        nl.setLength(5)

        l.setPoints(l.p2(), l.p1())  # flip
        l.setLength(l.length() - draw_properties[t][0])
        l.setPoints(l.p2(), l.p1())  # flip again
        l.setLength(l.length() - draw_properties[s][0])
        if s == self.center[-1] or t == self.center[-1] or (s in self.center and t in self.center):
            c = BLACK
        else:
            c = GRAY
        self.addArrow((l.x1(), l.y1()), (l.x2(), l.y2()), color=c)


def not_work():

    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)

    msg.setText("This is a message box")
    msg.setInformativeText("This is additional information")
    msg.setWindowTitle("MessageBox demo")
    msg.setDetailedText("The details are as follows:")
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msg.buttonClicked.connect(lambda: msg.close())


class Ui_MainWaindow(Ui):
    def __init__(self, first_center, graph):
        Ui.__init__(self, "mainwindow2.ui")

        self.g = graph
        # self.g = nx.read_adjlist(path="datasearch\\graphics\\grid.edgelist", delimiter=":", create_using=nx.DiGraph).to_directed()

        self.d = Drawer(self.win.graphView.width(), self.win.graphView.height(), self, first_center,
                        view_mode=SPRING)
        self.d.setMode(DATA_MODE)

        self.canvas = self.d.canvas
        self.win.graphView.setLayout(QVBoxLayout())
        self.win.graphView.layout().addWidget(self.canvas)
        self.win.incoming_btn.clicked.connect(lambda: self.d.setMode(DIAG_IN_MODE))
        self.win.outgoing_btn.clicked.connect(lambda: self.d.setMode(DIAG_OUT_MODE))

        self.win.logo.setText("<img src='ui/logo.png' "
                              "height='42' width='42'/>")

        layout = QVBoxLayout()
        diagrams_canvas = FigureCanvas(Figure())
        diagrams_canvas.setStyleSheet("background-color:transparent;")
        self.axs = diagrams_canvas.figure.subplots(1, 2)
        layout.addWidget(diagrams_canvas)
        self.win.diagrams_frame.setLayout(layout)

        self.win.back_button.clicked.connect(self.d.back)
        self.win.fd_button.clicked.connect(self.d.forward)
        self.win.tab_widget.currentChanged.connect(self.change_view_mode)

    def change_view_mode(self):
        print('Changed tab!')
        if self.win.tab_widget.currentIndex() in [0, 2]:
            self.d.setMode(DATA_MODE)
        elif self.win.tab_widget.currentIndex() == 1:
            if self.win.incoming_btn.isChecked():
                self.d.setMode(DIAG_IN_MODE)
            if self.win.outgoing_btn.isChecked():
                self.d.setMode(DIAG_OUT_MODE)

    def setTitle(self, text):
        self.win.title.setText(text)

    def enable_bf(self, back=True, forward=True):
        self.win.back_button.setVisible(back)
        self.win.fd_button.setVisible(forward)

    def displayDict(self, data):
        basic = data['basic']
        diagrams = data[DIAGRAMS]
        advanced = data['advanced']
        anomaly = data['anomaly']

        # BASIC
        result1 = ''
        result2 = ''
        for i, k in enumerate(basic):
            if i % 2 == 0:
                result1 += '<b><font color="tomato">%s</font></b><font color="White">: %s<br>' % (k, basic[k])
            else:
                result2 += '<b><font color="tomato">%s</font></b><font color="White">: %s<br>' % (k, basic[k])

        self.win.label_2.setText(result1)
        self.win.label_3.setText(result2)
        print('done basic!')

        # DIAGRAMS
        for i, k in enumerate(diagrams):
            d = diagrams[k][0]
            self.axs[i].cla()
            self.axs[i].set_title(k)
            if d is None:
                d = {}
            print(d.values())
            labels = list([self.d.nodeInfo[x]['basic']['Address'] for x in d.keys() if x != 'other'])
            if 'other' in d.keys():
                labels = ['other'] + labels
                cols = colors_hex
            else:
                cols = colors_hex[1:]
            self.axs[i].pie(x=list(d.values()),
                            labels=labels,
                            colors=cols)
            print(i)
            self.axs[i].figure.canvas.draw()
        print('done diagrams!')

        # ADVANCED
        result1 = ''
        result2 = ''
        for i, k in enumerate(advanced):
            if i % 2 == 0:
                result1 += '<b><font color="tomato">%s</font></b><font color="White">: %s<br>' % (k, advanced[k])
            else:
                result2 += '<b><font color="tomato">%s</font></b><font color="White">: %s<br>' % (k, advanced[k])

        self.win.label_4.setText(result1)
        self.win.label_5.setText(result2)
        print('done advanced!')

        # ANONALY
        self.win.lbl_anomaly.setText('<font color="white">%.2f%%</font>' % anomaly)
