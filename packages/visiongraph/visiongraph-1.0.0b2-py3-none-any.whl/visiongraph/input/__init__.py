import argparse
import logging
from argparse import _ArgumentGroup
from typing import Union

from visiongraph.input.ImageInput import ImageInput
from visiongraph.input.VideoCaptureInput import VideoCaptureInput
from visiongraph.util.ArgUtils import add_step_choice_argument

InputProviders = {
    "video-capture": VideoCaptureInput,
    "image": ImageInput,
}

# setup dependency input providers
try:
    from visiongraph.input.RealSenseInput import RealSenseInput

    InputProviders["realsense"] = RealSenseInput
except ImportError as ex:
    logging.info(f"RealSense not installed: {ex}")

try:
    from visiongraph.input.AzureKinectInput import AzureKinectInput

    InputProviders["azure"] = AzureKinectInput
except ImportError as ex:
    logging.info(f"Azure not installed: {ex}")

try:
    from visiongraph.input.CamGearInput import CamGearInput

    InputProviders["camgear"] = CamGearInput
except ImportError as ex:
    logging.info(f"VidGear not installed: {ex}")

try:
    from visiongraph.input.Oak1Input import Oak1Input
    from visiongraph.input.OakDInput import OakDInput

    InputProviders["oak1"] = Oak1Input
    InputProviders["oakd"] = OakDInput
except ImportError as ex:
    logging.info(f"DepthAI not installed: {ex}")

try:
    from visiongraph.input.ZEDInput import ZEDInput

    InputProviders["zed"] = ZEDInput
except ImportError as ex:
    logging.info(f"ZED SDK not installed: {ex}")


def add_input_step_choices(parser: Union[argparse.ArgumentParser, _ArgumentGroup], default: Union[int, str] = 0,
                           add_params: bool = True):
    add_step_choice_argument(parser, InputProviders, "--input", help="Image input provider",
                             default=default, add_params=add_params)
