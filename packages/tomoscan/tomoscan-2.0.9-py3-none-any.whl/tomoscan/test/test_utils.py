# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2022 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "03/05/2022"


import pytest

from tomoscan.utils.geometry import BoundingBox1D, BoundingBox3D, _BoundingBox


def test_bounding_box_base():
    bb = _BoundingBox(0, 1)
    with pytest.raises(NotImplementedError):
        bb.get_overlap(None)


def test_bounding_box_1D():
    """
    check if BoundingBox1D is working properly
    """
    # check overlaping
    bb1 = BoundingBox1D(0.0, 1.0)
    bb2 = BoundingBox1D(0.2, 1.0)
    assert bb1.get_overlap(bb2) == BoundingBox1D(0.2, 1.0)
    assert bb2.get_overlap(bb1) == BoundingBox1D(0.2, 1.0)

    bb1 = BoundingBox1D(0.0, 1.0)
    bb2 = BoundingBox1D(0.2, 0.8)
    assert bb1.get_overlap(bb2) == BoundingBox1D(0.2, 0.8)
    assert bb2.get_overlap(bb1) == BoundingBox1D(0.2, 0.8)

    bb1 = BoundingBox1D(0.0, 1.0)
    bb2 = BoundingBox1D(1.0, 1.2)
    assert bb2.get_overlap(bb1) == BoundingBox1D(1.0, 1.0)

    # check outside
    bb1 = BoundingBox1D(0.0, 1.0)
    bb2 = BoundingBox1D(2.0, 2.2)

    assert bb2.get_overlap(bb1) is None
    assert bb1.get_overlap(bb2) is None

    # check on fully including in the other
    bb1 = BoundingBox1D(0.0, 1.0)
    bb2 = BoundingBox1D(0.1, 0.3)
    assert bb2.get_overlap(bb1) == BoundingBox1D(0.1, 0.3)
    assert bb1.get_overlap(bb2) == BoundingBox1D(0.1, 0.3)

    with pytest.raises(TypeError):
        bb1.get_overlap(None)


def test_bounding_box_3D():
    """
    check if BoundingBox3D is working properly
    """
    # check overlaping
    bb1 = BoundingBox3D((0.0, -0.1, 0.0), [1.0, 0.8, 0.9])
    bb2 = BoundingBox3D([0.2, 0.0, 0.1], (1.0, 2.0, 3.0))
    assert bb1.get_overlap(bb2) == BoundingBox3D((0.2, 0.0, 0.1), (1.0, 0.8, 0.9))
    assert bb2.get_overlap(bb1) == BoundingBox3D((0.2, 0.0, 0.1), (1.0, 0.8, 0.9))

    # check outside
    bb1 = BoundingBox3D((0.0, -0.1, 0.0), [1.0, 0.8, 0.9])
    bb2 = BoundingBox3D([0.2, 0.0, -2.1], (1.0, 2.0, -1.0))

    assert bb2.get_overlap(bb1) is None
    assert bb1.get_overlap(bb2) is None

    # check on fully including in the other
    bb1 = BoundingBox3D((0.0, 0.1, 0.2), (1.0, 1.1, 1.2))
    bb2 = BoundingBox3D((-2.0, -3.0, -4.0), (2.0, 2.0, 2.0))
    assert bb2.get_overlap(bb1) == BoundingBox3D((0.0, 0.1, 0.2), (1.0, 1.1, 1.2))
    assert bb1.get_overlap(bb2) == BoundingBox3D((0.0, 0.1, 0.2), (1.0, 1.1, 1.2))

    with pytest.raises(TypeError):
        bb1.get_overlap(None)
