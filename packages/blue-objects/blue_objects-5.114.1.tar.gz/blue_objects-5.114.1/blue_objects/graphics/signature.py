import math
from typing import List
import numpy as np
from functools import reduce

from blueness import module

from blue_objects import NAME
from blue_objects.graphics.text import render_text

NAME = module.name(__file__, NAME)


def add_signature(
    image: np.ndarray,
    header: List[str],
    footer: List[str] = [],
    word_wrap: bool = True,
    line_width: int = 80,
) -> np.ndarray:
    if image is None or not image.shape:
        return image

    word_wrapper = lambda content: [
        line
        for line in reduce(
            lambda x, y: x + y,
            [
                (
                    [
                        " ".join(part)
                        for part in np.array_split(
                            line.split(" "),
                            int(math.ceil(len(line) / line_width)),
                        )
                    ]
                    if len(line) > 2 * line_width
                    else [line]
                )
                for line in content
            ],
            [],
        )
        if line
    ]

    if word_wrap:
        header = word_wrapper(header)
        footer = word_wrapper(footer)

    adjust_length = lambda line: (
        line if len(line) >= line_width else line + (line_width - len(line)) * " "
    )

    return np.concatenate(
        [
            render_text(
                text=adjust_length(line),
                image_width=image.shape[1],
                color_depth=image.shape[2],
            )
            for line in header
        ]
        + [image]
        + [
            render_text(
                text=adjust_length(line),
                image_width=image.shape[1],
                color_depth=image.shape[2],
            )
            for line in footer
        ],
        axis=0,
    )
