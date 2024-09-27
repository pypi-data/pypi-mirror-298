import enum
import math
from typing import Any

import PIL.Image
import numpy as np
import pydicom
from pydicom.pixel_data_handlers import util
from textual import events
from textual.app import RenderResult
from textual.widget import Widget
from textual_imageview.img import ImageView
from xnat.mixin import ImageScanData
from xnat.prearchive import PrearchiveScan


class ImageViewer(Widget):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.image: ImageView | None = None
        self.dicom_data: pydicom.Dataset | None = None
        self.mouse_down = False

    def set_xnat_data(self, data: ImageScanData | PrearchiveScan) -> None:

        try:
            # try:
            #     dicom_resource = self.xnat_data.resources.get('DICOM', self.xnat_data.resources.get('secondary'))
            #     dicom_files = sorted(dicom_resource.files.values(), key=lambda x: x.path)
            # except AttributeError:
            #     dicom_files = sorted(self.xnat_data.files, key=lambda x: x.name)
            # self.dicom_data = self.xnat_data.read_dicom(file=dicom_files[len(dicom_files) // 2], read_pixel_data=True)
            self.dicom_data = data.read_dicom(read_pixel_data=True)
            assert self.dicom_data

            self.set_image(_create_image(
                self.dicom_data,
                ImageProcessing.LUT if self.dicom_data.Modality == 'US' else ImageProcessing.WINDOW_LEVEL)
            )
        except AttributeError as e:
            self.app.notify(str(e))

    def set_image(self, _image: PIL.Image.Image | None) -> None:
        if _image is None:
            self.image = None
            self.refresh()
            return

        self.image = ImageView(_image)

    def on_show(self) -> None:
        if not self.image:
            return

        width, height = self.size.width, self.size.height
        img_w, img_h = self.image.size

        # Compute zoom such that image fits in container
        zoom_w = math.log(max(width, 1) / img_w, self.image.ZOOM_RATE)
        zoom_h = math.log((max(height, 1) * 2) / img_h, self.image.ZOOM_RATE)
        zoom = max(0, math.ceil(max(zoom_w, zoom_h)))
        self.image.set_zoom(zoom)

        # Position image in center of container
        img_w, img_h = self.image.zoomed_size
        self.image.origin_position = (-round((width - img_w) / 2), -round(height - img_h / 2))
        self.image.set_container_size(width, height, maintain_center=True)

        self.refresh()

    def on_mouse_scroll_down(self, event: events.MouseScrollDown) -> None:
        if not self.image:
            return

        offset = self.region.offset
        zoom_position = self.image.rowcol_to_xy(event.screen_y, event.screen_x, (offset.y, offset.x))
        self.image.zoom(1, zoom_position)
        self.refresh()
        event.stop()

    def on_mouse_scroll_up(self, event: events.MouseScrollDown) -> None:
        if not self.image:
            return

        offset = self.region.offset
        zoom_position = self.image.rowcol_to_xy(event.screen_y, event.screen_x, (offset.y, offset.x))
        self.image.zoom(-1, zoom_position)
        self.refresh()
        event.stop()

    def on_mouse_down(self, _: events.MouseDown) -> None:
        self.mouse_down = True
        self.capture_mouse(capture=True)

    def on_mouse_up(self, _: events.MouseDown) -> None:
        self.mouse_down = False
        self.capture_mouse(capture=False)

    def on_mouse_move(self, event: events.MouseMove) -> None:
        if not self.image:
            return

        if self.mouse_down and (event.delta_x != 0 or event.delta_y != 0):
            self.image.move(event.delta_x, event.delta_y * 2)
            self.refresh()

    def on_resize(self, event: events.Resize) -> None:
        if not self.image:
            return

        self.image.set_container_size(event.size.width, event.size.height)
        self.refresh()

    def render(self) -> RenderResult:
        if not self.image:
            return ''

        return self.image  # type: ignore


SUPPORTED_PHOTOMETRIC_INTERPRETATIONS = {'MONOCHROME1', 'MONOCHROME2', 'RGB', 'YBR_FULL_422'}


class ImageProcessing(enum.Enum):
    NONE = enum.auto()
    LUT = enum.auto()
    WINDOW_LEVEL = enum.auto()


def _create_image(dataset: pydicom.Dataset, processing: ImageProcessing = ImageProcessing.LUT) -> PIL.Image.Image | None:
    if dataset.PhotometricInterpretation not in SUPPORTED_PHOTOMETRIC_INTERPRETATIONS:
        raise ValueError(f'Unsupported image type: {dataset.PhotometricInterpretation}')

    match len(dataset.pixel_array.shape), dataset.PhotometricInterpretation:
        case 4, 'YBR_FULL_422' | 'RGB':
            np_array = dataset.pixel_array[0]
        case 3, _:
            np_array = dataset.pixel_array[0]
        case _:
            np_array = dataset.pixel_array

    match dataset.PhotometricInterpretation:
        case 'MONOCHROME1':
            # minimum is white, maximum is black
            # (https://dicom.innolitics.com/ciods/ct-image/image-pixel/00280004)
            if processing == ImageProcessing.LUT:
                np_array = pydicom.pixel_data_handlers.apply_voi_lut(dataset.pixel_array, dataset)
            if processing == ImageProcessing.WINDOW_LEVEL:
                slope = dataset.RescaleSlope if 'RescaleSlope' in dataset else 1.0
                intercept = dataset.RescaleIntercept if 'RescaleIntercept' in dataset else 0.0
                center = dataset.WindowCenter
                width = dataset.WindowWidth
                np_array = dataset.pixel_array * slope + intercept
                np_array = np.clip(np_array, center - width / 2, center + width / 2)
            minimum, maximum = np.amin(np_array), np.amax(np_array)
            np_array = (maximum - np_array) * 256.0 / (maximum - minimum)

        case 'MONOCHROME2':
            if processing == ImageProcessing.LUT:
                np_array = pydicom.pixel_data_handlers.apply_voi_lut(dataset.pixel_array, dataset)
            if processing == ImageProcessing.WINDOW_LEVEL:
                slope = dataset.RescaleSlope if 'RescaleSlope' in dataset else 1.0
                intercept = dataset.RescaleIntercept if 'RescaleIntercept' in dataset else 0.0
                center = dataset.WindowCenter
                width = dataset.WindowWidth
                np_array = dataset.pixel_array * slope + intercept
                np_array = np.clip(np_array, center - width / 2, center + width / 2)
            minimum, maximum = np.amin(np_array), np.amax(np_array)
            np_array = (np_array - minimum) * 256.0 / (maximum - minimum)

        case 'YBR_FULL_422':
            np_array = util.convert_color_space(np_array, 'YBR_FULL', 'RGB')

        case _:
            pass

    return PIL.Image.fromarray(np_array).convert('RGB')  # type: ignore
