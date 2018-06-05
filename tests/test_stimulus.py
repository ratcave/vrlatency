from vrlatency import Stimulus
import numpy as np

def test_color():
    for color in [(1., 0., 0.), (1., 1., 0.)]:
        mystim = Stimulus(color=color)
        assert np.isclose(mystim.color, color).all()
        assert np.isclose(mystim.mesh.uniforms['diffuse'], color).all()


def test_point_size():
    for size in [3, 2.2]:
        mystim = Stimulus(size=size)
        assert mystim.size == int(size)