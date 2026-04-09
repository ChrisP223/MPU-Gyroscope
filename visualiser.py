'''
pip install numpy
pip install PyQt6
pip install pyqtgraph
pip install PyOpenGL
pip install PyOpenGL_accelerate'''


import time
import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph.Qt import QtCore
import os
os.environ["PYQTGRAPH_QT_LIB"] = "PyQt6"
#Το αρχείο που περιέχει τις κινήσεις του αισθητήρα
FILE = "movement.txt"

#Διαβάζουμε όλες τις γραμμές από το αρχείο
with open(FILE, "r") as f:
    lines = f.readlines()

# Αποθηκεύουμε τα δεδομένα κινήσεων σε λίστα
frames = []
for line in lines:
    line = line.strip()
    if "," in line:
        try:
            parts = line.split(",")
            if len(parts) == 3:
                # Κάθε γραμμή έχει 3 τιμές: roll, pitch, yaw
                frames.append((float(parts[0]), float(parts[1]), float(parts[2])))
        except:
            pass

print(f"Φορτώθηκαν {len(frames)} frames")

app = pg.mkQApp("Visualizer")
w = gl.GLViewWidget()
w.setWindowTitle("Movement Replay")
w.setGeometry(0, 0, 800, 600)
w.setCameraPosition(distance=4)
w.show()

# Ορισμός κορυφών κουτιού
verts = np.array([
    [-1, -0.3, -0.1], [ 1, -0.3, -0.1],
    [ 1,  0.3, -0.1], [-1,  0.3, -0.1],
    [-1, -0.3,  0.1], [ 1, -0.3,  0.1],
    [ 1,  0.3,  0.1], [-1,  0.3,  0.1],
], dtype=float)

# Ορισμός των τριγωνικών επιφανειών του κουτιού
faces = np.array([
    [0,1,2], [0,2,3],
    [4,5,6], [4,6,7],
    [0,1,5], [0,5,4],
    [2,3,7], [2,7,6],
    [0,3,7], [0,7,4],
    [1,2,6], [1,6,5],
])

# Χρώματα
colors = np.array([
    [1,0,0,1],[1,0,0,1],#red
    [0,1,0,1],[0,1,0,1],#green
    [0,0,1,1],[0,0,1,1],#blue
    [1,1,0,1],[1,1,0,1],#yellow
    [0,1,1,1],[0,1,1,1],#cyan
    [1,0,1,1],[1,0,1,1],#purple
], dtype=float)

#Mesh creation
mesh = gl.GLMeshItem(vertexes=verts, faces=faces, faceColors=colors,
                     smooth=False, drawEdges=True)
w.addItem(mesh)

#ground reference
g = gl.GLGridItem()
g.scale(2, 2, 1)
w.addItem(g)

# Άξονες αναφοράς(R=X, G=Y, Β=Z)
xaxis = gl.GLLinePlotItem(pos=np.array([[0,0,0],[2,0,0]]), color=(1,0,0,1), width=2)
yaxis = gl.GLLinePlotItem(pos=np.array([[0,0,0],[0,2,0]]), color=(0,1,0,1), width=2)
zaxis = gl.GLLinePlotItem(pos=np.array([[0,0,0],[0,0,2]]), color=(0,0,1,1), width=2)
w.addItem(xaxis)
w.addItem(yaxis)
w.addItem(zaxis)


frame_index = [0]

def update():
    #Επαναφορά στην αρχή όταν τελειώσουν τα frames
    if frame_index[0] >= len(frames):
        frame_index[0] = 0
        return

    #Διαβάζουμε τις γωνίες
    roll, pitch, yaw = frames[frame_index[0]]
    frame_index[0] += 1


    mesh.resetTransform()
    mesh.rotate(yaw,   0, 0, 1) #Z
    mesh.rotate(pitch, 0, 1, 0) #Y
    mesh.rotate(roll,  1, 0, 0) #X

#καλεί update() κάθε 50ms
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)

if __name__ == "__main__":
    pg.exec()
