'''
pip install numpy
pip install PyQt6
pip install pyqtgraph
pip install PyOpenGL
pip install PyOpenGL_accelerate
'''

import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph.Qt import QtCore, QtWidgets
from collections import deque
import os
os.environ["PYQTGRAPH_QT_LIB"] = "PyQt6"

FILE = "movement.txt"

with open(FILE, "r") as f:
    lines = f.readlines()
frames = []
for line in lines:
    line = line.strip()
    if "," in line:
        try:
            parts = line.split(",")
            if len(parts) == 5:
                roll_raw   = float(parts[0])
                pitch_raw  = float(parts[1])
                roll_filt  = float(parts[2])
                pitch_filt = float(parts[3])
                yaw_filt   = float(parts[4])
                frames.append((roll_raw, pitch_raw, roll_filt, pitch_filt, yaw_filt))
        except:
            pass

print(f"Loaded {len(frames)} frames")

app = pg.mkQApp("Visualizer")

# 3D 2D comparison
main_win = QtWidgets.QWidget()
main_win.setWindowTitle("IMU Sensor Fusion Visualizer")
main_win.setGeometry(0, 0, 1400, 650)
layout = QtWidgets.QHBoxLayout()
main_win.setLayout(layout)

w = gl.GLViewWidget()
w.setMinimumWidth(700)
w.setCameraPosition(distance=4)
layout.addWidget(w)

# Box vertices
verts = np.array([
    [-1, -0.3, -0.1], [ 1, -0.3, -0.1],
    [ 1,  0.3, -0.1], [-1,  0.3, -0.1],
    [-1, -0.3,  0.1], [ 1, -0.3,  0.1],
    [ 1,  0.3,  0.1], [-1,  0.3,  0.1],
], dtype=float)

faces = np.array([
    [0,1,2], [0,2,3],
    [4,5,6], [4,6,7],
    [0,1,5], [0,5,4],
    [2,3,7], [2,7,6],
    [0,3,7], [0,7,4],
    [1,2,6], [1,6,5],
])

colors = np.array([
    [1,0,0,1],[1,0,0,1],
    [0,1,0,1],[0,1,0,1],
    [0,0,1,1],[0,0,1,1],
    [1,1,0,1],[1,1,0,1],
    [0,1,1,1],[0,1,1,1],
    [1,0,1,1],[1,0,1,1],
], dtype=float)

mesh = gl.GLMeshItem(vertexes=verts, faces=faces, faceColors=colors,
                     smooth=False, drawEdges=True)
w.addItem(mesh)

g = gl.GLGridItem()
g.scale(2, 2, 1)
w.addItem(g)

xaxis = gl.GLLinePlotItem(pos=np.array([[0,0,0],[2,0,0]]), color=(1,0,0,1), width=2)
yaxis = gl.GLLinePlotItem(pos=np.array([[0,0,0],[0,2,0]]), color=(0,1,0,1), width=2)
zaxis = gl.GLLinePlotItem(pos=np.array([[0,0,0],[0,0,2]]), color=(0,0,1,1), width=2)
w.addItem(xaxis)
w.addItem(yaxis)
w.addItem(zaxis)

plot_panel = QtWidgets.QWidget()
plot_layout = QtWidgets.QVBoxLayout()
plot_panel.setLayout(plot_layout)
layout.addWidget(plot_panel)

#Roll
roll_plot = pg.PlotWidget(title="Roll: Raw vs Filtered")
roll_plot.setLabel('left', 'Angle', units='°')
roll_plot.setLabel('bottom', 'Frame')
roll_plot.addLegend()
roll_plot.setYRange(-180, 180)
curve_roll_raw  = roll_plot.plot(pen=pg.mkPen('r', width=1), name='Raw Roll')
curve_roll_filt = roll_plot.plot(pen=pg.mkPen('g', width=2), name='Filtered Roll')
plot_layout.addWidget(roll_plot)

# Pitch 
pitch_plot = pg.PlotWidget(title="Pitch: Raw vs Filtered")
pitch_plot.setLabel('left', 'Angle', units='°')
pitch_plot.setLabel('bottom', 'Frame')
pitch_plot.addLegend()
pitch_plot.setYRange(-180, 180)
curve_pitch_raw  = pitch_plot.plot(pen=pg.mkPen('y', width=1), name='Raw Pitch')
curve_pitch_filt = pitch_plot.plot(pen=pg.mkPen('c', width=2), name='Filtered Pitch')
plot_layout.addWidget(pitch_plot)

#Yaw
yaw_plot = pg.PlotWidget(title="Yaw: Filtered Only (no accel reference)")
yaw_plot.setLabel('left', 'Angle', units='°')
yaw_plot.setLabel('bottom', 'Frame')
yaw_plot.addLegend()
curve_yaw = yaw_plot.plot(pen=pg.mkPen('m', width=2), name='Filtered Yaw')
plot_layout.addWidget(yaw_plot)

main_win.show()

HISTORY = 100
SKIP    = 3  #frames consumed per tick


roll_raw_hist   = deque(maxlen=HISTORY)
pitch_raw_hist  = deque(maxlen=HISTORY)
roll_filt_hist  = deque(maxlen=HISTORY)
pitch_filt_hist = deque(maxlen=HISTORY)
yaw_filt_hist   = deque(maxlen=HISTORY)

frame_index = [0]

def update():
    for _ in range(SKIP):
        if frame_index[0] >= len(frames):
            frame_index[0] = 0
            return
        roll_raw, pitch_raw, roll_filt, pitch_filt, yaw_filt = frames[frame_index[0]]
        frame_index[0] += 1

    roll_raw_hist.append(roll_raw)
    pitch_raw_hist.append(pitch_raw)
    roll_filt_hist.append(roll_filt)
    pitch_filt_hist.append(pitch_filt)
    yaw_filt_hist.append(yaw_filt)

    mesh.resetTransform()
    mesh.rotate(yaw_filt,   0, 0, 1) #Z
    mesh.rotate(pitch_filt, 0, 1, 0) #Y
    mesh.rotate(roll_filt,  1, 0, 0) #X

    curve_roll_raw.setData(list(roll_raw_hist))
    curve_roll_filt.setData(list(roll_filt_hist))
    curve_pitch_raw.setData(list(pitch_raw_hist))
    curve_pitch_filt.setData(list(pitch_filt_hist))
    curve_yaw.setData(list(yaw_filt_hist))

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(15)

if __name__ == "__main__":
    pg.exec()
