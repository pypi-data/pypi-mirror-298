import copy
from typing import List, TypeVar, Tuple, Optional

import cv2
import numpy as np
import vector

from visiongraph.model.geometry.Size2D import Size2D
from visiongraph.model.geometry.BoundingBox2D import BoundingBox2D
from visiongraph.result.spatial.ObjectDetectionResult import ObjectDetectionResult
from visiongraph.util import ImageUtils

ODR = TypeVar("ODR", bound=ObjectDetectionResult)


def non_maximum_suppression(results: List[ODR], min_score: float, iou_threshold: float,
                            eta: Optional[float] = None, top_k: Optional[int] = None) -> List[ODR]:
    boxes = [list(result.bounding_box) for result in results]
    confidences = [result.score for result in results]
    indices = cv2.dnn.NMSBoxes(boxes, confidences, min_score, iou_threshold, eta, top_k)
    return [results[int(i)] for i in list(indices)]


def extract_object_detection_roi(image: np.ndarray,
                                 detection: ODR) -> Tuple[np.ndarray, ODR]:
    box: BoundingBox2D = detection.bounding_box.scale_with(Size2D.from_image(image))
    roi = ImageUtils.roi(image, box)

    result = copy.deepcopy(detection)
    result.map_coordinates(Size2D.from_image(image), Size2D.from_image(roi), src_roi=box)
    return roi, result


def bbox_from_landmarks(landmarks: vector.VectorNumpy4D) -> BoundingBox2D:
    xs = np.ma.masked_equal(landmarks["x"], 0.0, copy=False)
    ys = np.ma.masked_equal(landmarks["y"], 0.0, copy=False)

    x_min = xs.min()
    y_min = ys.min()
    x_max = xs.max()
    y_max = ys.max()

    return BoundingBox2D(x_min, y_min, x_max - x_min, y_max - y_min)
