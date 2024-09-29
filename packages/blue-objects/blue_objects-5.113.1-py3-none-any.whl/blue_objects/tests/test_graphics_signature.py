import numpy as np

from blue_objects.env import DUMMY_TEXT
from blue_objects.graphics.signature import add_signature
from blue_objects.tests.test_graphics import test_image


def test_graphics_signature_add_signature(test_image):
    assert isinstance(
        add_signature(
            test_image,
            header=[DUMMY_TEXT],
            footer=[DUMMY_TEXT, DUMMY_TEXT],
        ),
        np.ndarray,
    )
