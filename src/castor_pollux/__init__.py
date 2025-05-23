# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from .rest import continuation
from .adapter import encode, decode

__all__ = [
    'continuation',
    'encode',
    'decode'
]