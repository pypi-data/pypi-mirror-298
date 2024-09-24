import numpy as np

from fish_scan._widget import (
    FishAnalysis
)


def test_image_threshold_widget(make_napari_viewer):
    viewer = make_napari_viewer()
    layer = viewer.add_image(np.random.random((100, 100)))
    my_widget = FishAnalysis(viewer)

    # implement test here
