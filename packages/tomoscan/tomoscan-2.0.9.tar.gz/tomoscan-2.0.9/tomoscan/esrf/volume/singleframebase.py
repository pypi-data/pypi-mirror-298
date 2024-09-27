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
"""module defining utils for a jp2k volume"""


__authors__ = ["H. Payno", "P. Paleo"]
__license__ = "MIT"
__date__ = "27/01/2022"


import logging
import os
import re
from typing import Optional

import numpy
from silx.io.dictdump import dicttoini
from silx.io.dictdump import load as load_ini
from silx.io.url import DataUrl

from tomoscan.scanbase import TomoScanBase
from tomoscan.utils import docstring
from tomoscan.volumebase import VolumeBase

_logger = logging.getLogger(__name__)


class VolumeSingleFrameBase(VolumeBase):
    """
    Base class for Volume where each slice is saved in a separate file like edf, jp2k or tiff.

    :param int start_index: users can provide a shift on fill name when saving the file. This is interesting if you want to create
                        create a volume from several writer.
    """

    DEFAULT_DATA_SCHEME = None

    DEFAULT_DATA_PATH_PATTERN = "{volume_basename}_{index_zfill6}.{data_extension}"

    DEFAULT_METADATA_EXTENSION = "txt"

    # information regarding metadata
    DEFAULT_METADATA_SCHEME = "ini"

    DEFAULT_METADATA_PATH_PATTERN = "{volume_basename}_infos.{metadata_extension}"

    def __init__(
        self,
        url: Optional[DataUrl] = None,
        data: Optional[numpy.ndarray] = None,
        source_scan: Optional[TomoScanBase] = None,
        metadata: Optional[dict] = None,
        data_url: Optional[DataUrl] = None,
        metadata_url: Optional[DataUrl] = None,
        overwrite: bool = False,
        start_index: int = 0,
        volume_basename: Optional[str] = None,
        data_extension=None,
        metadata_extension="txt",
    ) -> None:
        self._volume_basename = volume_basename
        super().__init__(
            url,
            data,
            source_scan,
            metadata,
            data_url,
            metadata_url,
            overwrite,
            data_extension,
            metadata_extension,
        )

        self._start_index = start_index

    @property
    def start_index(self) -> int:
        return self._start_index

    def get_volume_basename(self, url=None):
        if self._volume_basename is not None:
            return self._volume_basename
        else:
            url = url or self.data_url
            return os.path.basename(url.file_path())

    @docstring(VolumeBase)
    def deduce_data_and_metadata_urls(self, url: Optional[DataUrl]) -> tuple:
        """
        Deduce automatically data and metadata url.
        Default data will be saved as single frame edf.
        Default metadata will be saved as a text file
        """
        if url is None:
            return None, None
        else:
            metadata_keywords = {
                "volume_basename": self.get_volume_basename(url),
                "metadata_extension": self.metadata_extension,
            }
            metadata_data_path = self.DEFAULT_METADATA_PATH_PATTERN.format(
                **metadata_keywords
            )

            return (
                # data url
                DataUrl(
                    file_path=url.file_path(),
                    data_path=self.DEFAULT_DATA_PATH_PATTERN,
                    scheme=url.scheme() or self.DEFAULT_DATA_SCHEME,
                    data_slice=url.data_slice(),
                ),
                # medata url
                DataUrl(
                    file_path=url.file_path(),
                    data_path=metadata_data_path,
                    scheme=url.scheme() or self.DEFAULT_METADATA_SCHEME,
                ),
            )

    @docstring(VolumeBase)
    def load_metadata(self, url: Optional[DataUrl] = None, store: bool = True) -> dict:
        url = url or self.metadata_url
        if url is None:
            raise ValueError(
                "Cannot get metadata_url. An url should be provided. Don't know where to save this."
            )
        if url.scheme() == "ini":
            metadata_file = url.file_path()
            if url.data_path() is not None:
                metadata_file = os.path.join(metadata_file, url.data_path())
                _logger.info(f"load data to {metadata_file}")
            try:
                metadata = load_ini(metadata_file, "ini")
            except FileNotFoundError:
                _logger.warning(
                    f"unable to load metadata from {metadata_file} - File not found"
                )
                metadata = {}
            except Exception as e:
                _logger.error(
                    f"Failed to load metadata from {metadata_file}. Error is {e}"
                )
                metadata = {}
        else:
            raise ValueError(f"scheme {url.scheme()} is not handled")

        if store:
            self.metadata = metadata
        return metadata

    @docstring(VolumeBase)
    def save_metadata(self, url: Optional[DataUrl] = None) -> None:
        if self.metadata is None:
            raise ValueError("No data to be saved")
        url = url or self.metadata_url
        if url is None:
            raise ValueError(
                "Cannot get metadata_url. An url should be provided. Don't know where to save this."
            )
        else:
            if url.scheme() == "ini":
                metadata_file = url.file_path()
                if url.data_path() is not None:
                    metadata_file = os.path.join(metadata_file, url.data_path())
                    _logger.info(f"save data to {metadata_file}")
                    if len(self.metadata) > 0:
                        dicttoini(self.metadata, metadata_file)
            else:
                raise ValueError(f"scheme {url.scheme()} is not handled")

    # utils to format file path

    def format_data_path_for_data(
        self, data_path: str, index: int, volume_basename: str
    ) -> str:
        """
        Return file path to save the frame at `index` of the current volume
        """
        keywords = {
            "index_zfill4": str(index + self.start_index).zfill(4),
            "index_zfill6": str(index + self.start_index).zfill(6),
            "volume_basename": volume_basename,
            "data_extension": self.data_extension,
        }
        return data_path.format(**keywords)

    def get_data_path_pattern_for_data(
        self, data_path: str, volume_basename: str
    ) -> str:
        """
        Return file path **pattern** (and not full path) to  load data.
        For example in edf it can return 'myacquisition_*.edf' in order to be handled by
        """
        keywords = {
            "index_zfill4": "[0-9]{3,4}",
            "index_zfill6": "[0-9]{3,6}",
            "volume_basename": volume_basename,
            "data_extension": self.data_extension,
        }
        return data_path.format(**keywords)

    @docstring(VolumeBase)
    def save_data(self, url: Optional[DataUrl] = None) -> None:
        if self.data is None:
            raise ValueError("No data to be saved")
        url = url or self.data_url
        if url is None:
            raise ValueError(
                "Cannot get data_url. An url should be provided. Don't know where to save this."
            )
        else:
            _logger.info(f"save data to {url.path()}")
            # if necessary create output directory (some third part writer does not do it for us)
            try:
                os.makedirs(url.file_path(), exist_ok=True)
            except FileNotFoundError:
                # can raise FileNotFoundError if file path is '.' for example
                pass

            assert self.data.ndim == 3
            for frame, frame_dumper in zip(
                self.data,
                self.data_file_saver_generator(
                    n_frames=self.data.shape[0], data_url=url, overwrite=self.overwrite
                ),
            ):
                frame_dumper[:] = frame

    def data_file_name_generator(self, n_frames, data_url):
        """
        browse output files for n_frames
        """
        for i_frame in range(n_frames):
            file_name = self.format_data_path_for_data(
                data_url.data_path(),
                index=i_frame,
                volume_basename=self.get_volume_basename(data_url),
            )
            file_name = os.path.join(data_url.file_path(), file_name)
            yield file_name

    @docstring(VolumeBase)
    def data_file_saver_generator(self, n_frames, data_url: DataUrl, overwrite: bool):
        class _FrameDumper:
            def __init__(self, url_scheme, file_name, callback) -> None:
                self.url_scheme = url_scheme
                self.file_name = file_name
                self.overwrite = overwrite
                self.__callback = callback

            def __setitem__(self, key, value):
                if not self.overwrite and os.path.exists(self.file_name):
                    raise OSError(
                        f"{self.file_name} already exists. If you want you can ask for the volume to overwriting existing files."
                    )
                if key != slice(None, None, None):
                    raise ValueError("item setting only handle ':' for now")
                self.__callback(
                    frame=value, file_name=self.file_name, scheme=self.url_scheme
                )

        os.makedirs(data_url.file_path(), exist_ok=True)
        for file_name in self.data_file_name_generator(
            n_frames=n_frames, data_url=data_url
        ):
            yield _FrameDumper(
                file_name=file_name,
                url_scheme=data_url.scheme(),
                callback=self.save_frame,
            )

    def get_volume_shape(self, url=None):
        if self.data is not None:
            return self.data.shape
        else:
            first_slice = next(self.browse_slices(url=url))
            n_slices = len(tuple(self.browse_data_urls()))
            return n_slices, first_slice.shape[0], first_slice.shape[1]

    @docstring(VolumeBase)
    def load_data(
        self, url: Optional[DataUrl] = None, store: bool = True
    ) -> numpy.ndarray:
        url = url or self.data_url
        if url is None:
            raise ValueError(
                "Cannot get data_url. An url should be provided. Don't know where to save this."
            )
        data = list(self.browse_slices(url=url))

        if data == []:
            data = None
            _logger.warning(
                f"Failed to load any data for {self.get_identifier().short_description}"
            )
        else:
            data = numpy.asarray(data)
            if data.ndim != 3:
                raise ValueError(f"data is expected to be 3D not {data.ndim}.")

        if store:
            self.data = data

        return data

    def save_frame(self, frame: numpy.ndarray, file_name: str, scheme: str):
        """
        Function dedicated for volune saving each frame on a single file

        :param numpy.ndarray frame: frame to be save
        :param str file_name: path to store the data
        :param str scheme: scheme to save the data
        """
        raise NotImplementedError("Base class")

    def load_frame(self, file_name: str, scheme: str) -> numpy.ndarray:
        """
        Function dedicated for volune saving each frame on a single file

        :param str file_name: path to store the data
        :param str scheme: scheme to save the data
        """
        raise NotImplementedError("Base class")

    @docstring(VolumeBase)
    def browse_metadata_files(self, url=None):
        url = url or self.metadata_url
        if url is None:
            return
        elif url.file_path() is not None:
            if url.scheme() == "ini":
                metadata_file = url.file_path()
                if url.data_path() is not None:
                    metadata_file = os.path.join(metadata_file, url.data_path())
                    if os.path.exists(metadata_file):
                        yield metadata_file
            else:
                raise ValueError(f"scheme {url.scheme()} is not handled")

    @docstring(VolumeBase)
    def browse_data_files(self, url=None):
        url = url or self.data_url
        if url is None:
            return
        research_pattern = self.get_data_path_pattern_for_data(
            url.data_path(), volume_basename=self.get_volume_basename(url)
        )
        try:
            research_pattern = re.compile(research_pattern)
        except Exception:
            _logger.error(
                f"Fail to compute regular expresion for {research_pattern}. Unable to load data"
            )
            return None

        # use case of a single file
        if not os.path.exists(url.file_path()):
            return
        elif os.path.isfile(url.file_path()):
            yield url.file_path()
        else:
            for file_ in sorted(os.listdir(url.file_path())):
                if research_pattern.match(file_):
                    full_file_path = os.path.join(url.file_path(), file_)
                    yield full_file_path

    @docstring(VolumeBase)
    def browse_data_urls(self, url=None):
        url = url or self.data_url
        for data_file in self.browse_data_files(url=url):
            yield DataUrl(
                file_path=data_file,
                scheme=url.scheme(),
            )

    @docstring(VolumeBase)
    def browse_slices(self, url=None):
        if url is None and self.data is not None:
            for data_slice in self.data:
                yield data_slice
        else:
            url = url or self.data_url
            if url is None:
                raise ValueError(
                    "No data and data_url know and no url provided. Uanble to browse slices"
                )

            for file_path in self.browse_data_files(url=url):
                yield self.load_frame(file_name=file_path, scheme=url.scheme())
