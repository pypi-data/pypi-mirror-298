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
__date__ = "01/02/2022"


from tomoscan.esrf.identifier.folderidentifier import (
    BaseFolderAndfilePrefixIdentifierMixIn,
)
from tomoscan.identifier import VolumeIdentifier
from tomoscan.utils import docstring


class JP2KVolumeIdentifier(BaseFolderAndfilePrefixIdentifierMixIn, VolumeIdentifier):
    """Identifier specific to JP2K volume"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, tomo_type=VolumeIdentifier.TOMO_TYPE)

    @property
    @docstring(VolumeIdentifier)
    def scheme(self) -> str:
        return "jp2k"

    @staticmethod
    def from_str(identifier):
        from tomoscan.esrf.volume.jp2kvolume import JP2KVolume

        return (
            BaseFolderAndfilePrefixIdentifierMixIn._from_str_to_single_frame_identifier(
                identifier=identifier,
                SingleFrameIdentifierClass=JP2KVolumeIdentifier,
                ObjClass=JP2KVolume,
            )
        )
