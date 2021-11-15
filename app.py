import numpy as np
from orqviz.geometric import get_coordinates_on_direction
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph.Qt import QtCore, QtGui


def create_landscape_app(parameter_trajectory, losses, pca, scan_pca_result, save_images: bool=False):
    x, y = scan_pca_result._get_coordinates_on_directions(in_units_of_direction=False)
    z = scan_pca_result.values * 2

    ## Create a GL View widget to display data
    app = pg.mkQApp("VQE landscape")

    w = gl.GLViewWidget()
    w.resize(1920, 1200)
    w.show()
    w.setWindowTitle("VQE landscape")
    w.setCameraPosition(distance=40)

    ## Add a grid to the view
    g = gl.GLGridItem(size=QtGui.QVector3D(25, 25, 1))
    g.setDepthValue(10)
    w.addItem(g)

    p1 = gl.GLSurfacePlotItem(
        x=x,
        y=y,
        z=z,
        shader="normalColor",
        color=(0.5, 0.5, 0.5, 0.5),
        glOptions="opaque",
        antialias=True,
    )
    w.addItem(p1)

    direction_x = pca.pca.components_[pca.components_ids[0]]
    direction_y = pca.pca.components_[pca.components_ids[1]]
    shift = pca.pca.mean_

    projected_trajectory_x = get_coordinates_on_direction(
        parameter_trajectory, direction_x, origin=shift
    )
    projected_trajectory_y = get_coordinates_on_direction(
        parameter_trajectory, direction_y, origin=shift
    )

    height = 1.1 * z.max() * np.ones(projected_trajectory_x.shape)
    pos = np.stack((projected_trajectory_y, projected_trajectory_x, height), 1)

    l1 = gl.GLLinePlotItem(
        pos=pos,
        width=6,
        glOptions="additive",
        antialias=True,
        color=(0.8, 0.8, 1.0, 1.0),
    )
    l1.setDepthValue(10)

    w.addItem(l1)

    i = 0
    def update():
        global i
        if save_images:
            w.grabFramebuffer().save(f'img/{i}.png')
            i = i + 1
            w.orbit(0.4, 0)

    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(0)
