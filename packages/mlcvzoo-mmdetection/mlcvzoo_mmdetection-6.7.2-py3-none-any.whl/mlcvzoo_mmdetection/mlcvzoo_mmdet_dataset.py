# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

"""
Module for providing the possibility to train a mmdetection
model on data that is provided by the annotation handler
of the MLCVZoo. This is realized by extending the 'DATASETS'
registry of mmdetection.
"""

import logging
import os
from typing import Any, Dict, List, Optional

from mlcvzoo_base.api.data.annotation import BaseAnnotation
from mlcvzoo_base.configuration.annotation_handler_config import AnnotationHandlerConfig
from mlcvzoo_base.configuration.class_mapping_config import ClassMappingConfig
from mlcvzoo_base.data_preparation.annotation_handler import AnnotationHandler
from mmdet.datasets.base_det_dataset import BaseDetDataset
from mmengine.config import ConfigDict
from related import to_model

logger = logging.getLogger(__name__)


class MLCVZooMMDetDataset(BaseDetDataset):
    """
    Implementation of a custom dataset. It follows the instructions given by:
    https://mmdetection.readthedocs.io/en/dev-3.x/advanced_guides/customize_dataset.html

    We followed an example and created our own dataset class
    which has to be compatible to the class "BaseDataset"
    of the mmdetection framework.
    """

    def __init__(
        self,
        *args: Any,
        annotation_handler_config: Optional[ConfigDict] = None,
        class_mapping_config: Optional[ConfigDict] = None,
        include_segmentation_as_bbox: bool = False,
        **kwargs: Any,
    ) -> None:
        self.annotations: List[BaseAnnotation] = []
        self.CLASSES: List[str] = []

        self._include_segmentation_as_bbox = include_segmentation_as_bbox

        if annotation_handler_config is not None:
            # Set annotation handler configuration from given annotation handler config
            configuration = to_model(AnnotationHandlerConfig, annotation_handler_config)
            # Set class mapping configuration from given class mapping config
            if class_mapping_config is not None:
                configuration.class_mapping = to_model(
                    ClassMappingConfig, class_mapping_config
                )
            # Create annotation handler, if no class mapping config was given,
            # assume it is part of the config file
            annotation_handler = AnnotationHandler(
                configuration=configuration,
            )
            # Load annotations and model classes from annotation handler
            self.annotations = annotation_handler.parse_training_annotations()
            self.CLASSES = annotation_handler.mapper.get_model_class_names()

            self.METAINFO = {
                "classes": self.CLASSES,
            }

        self._with_bbox: bool = False
        self._with_mask: bool = False
        self._box_type: str = "hbox"
        pipeline = kwargs.get("pipeline")
        if pipeline is not None:
            annotation_pipelines = []
            for pipeline_element in pipeline:
                if pipeline_element["type"] in self._get_annotation_pipeline_types():
                    annotation_pipelines.append(pipeline_element)

            # Handle with_seg if we need to train panoptic segmentation models
            # self.with_seg: bool
            if len(annotation_pipelines) > 0:
                self._with_bbox = annotation_pipelines[0].get("with_bbox", False)
                self._with_mask = annotation_pipelines[0].get(
                    "with_mask", False
                ) or annotation_pipelines[0].get("with_polygon", False)
                self._box_type = annotation_pipelines[0].get("box_type", "hbox")

        BaseDetDataset.__init__(self, *args, **kwargs)

    @staticmethod
    def _get_annotation_pipeline_types() -> List[str]:
        """
        List of types which are associated with pipelines that load annotations.
        These are used to gather information which kind of data e.g. bounding boxes or
        segmentations should be parsed in the load_data_list(...).

        Returns:
            List of types as strings
        """
        return ["LoadAnnotations", "mmdet.LoadAnnotations"]

    @staticmethod
    def __generate_summary_message(base_message: str, data_dict: Dict[str, int]) -> str:
        """
        Produce a data summary message

        Args:
            base_message: Header of the message
            data_dict: Dictionary containing the summary information

        Returns:
            The generated message
        """
        message = base_message.format(sum(data_dict.values())) + "\n"

        for key, value in data_dict.items():
            message += f"{str(value).rjust(10)} | {str(key)}\n"

        return message

    def load_data_list(self) -> List[Dict[str, Any]]:
        """
        Transform the mlcvzoo annotations into the format that is required by the data
        loaders of the open-mmlab world.

        For the respective annotation format convention have a look at their documentation

        Returns:
             The loaded data list in the format required by the data loader in the open-mmlab world
        """
        data_list: List[Dict[str, Any]] = []
        bbox_data_dict: Dict[str, int] = {}
        segmentation_data_dict: Dict[str, int] = {}

        # TODO: Handle ignore flag if present in kwargs
        for img_id, annotation in enumerate(self.annotations):
            if not os.path.isfile(annotation.image_path):
                logger.debug(
                    "Skip annotation with path='%s' since image='%s' does not exist",
                    annotation.annotation_path,
                    annotation.image_path,
                )
                continue

            instances: List[Dict[str, Any]] = []
            if self._with_bbox and not self._with_mask:
                for bounding_box in annotation.get_bounding_boxes(
                    include_segmentations=self._include_segmentation_as_bbox
                ):
                    # Check which box type is configured for the dataset pipeline

                    # Object Detection training - only take orthogonal boxes
                    # hbox => xyxy
                    if self._box_type == "hbox":
                        mmdet_bbox = bounding_box.ortho_box().to_list(dst_type=float)

                    # Rotated Object Detection training - every box is supported
                    # qbox => xyxyxyxy
                    elif self._box_type == "qbox":
                        mmdet_bbox = bounding_box.polygon().reshape(-1).tolist()
                    else:
                        raise ValueError(
                            "Currently only 'hbox' and 'qbox' are supported "
                            "for the parameter 'box_type'"
                        )

                    instances.append(
                        {
                            "ignore_flag": 0,
                            "ignore": 0,
                            "bbox_label": bounding_box.class_id,
                            "bbox": mmdet_bbox,
                        }
                    )
                    if bounding_box.class_identifier.class_name not in bbox_data_dict:
                        bbox_data_dict[bounding_box.class_identifier.class_name] = 1
                    else:
                        bbox_data_dict[bounding_box.class_identifier.class_name] += 1
            elif self._with_mask:
                # Segmentation training - train with masks and bounding boxes
                for segmentation in annotation.segmentations:
                    instances.append(
                        {
                            "ignore_flag": 0,
                            "ignore": 0,
                            "bbox_label": segmentation.class_id,
                            "bbox": segmentation.ortho_box().to_list(dst_type=float),
                            # Mask annotations for usage in Instance/Panoptic Segmentation models.
                            # mmdet allows two formats: list[list[float]] or dict,
                            # we use the list format here, where the inner list[float] has to be
                            # in the format [x1, y1, ..., xn, yn] (n≥3)
                            "mask": segmentation.polygon().reshape(1, -1).tolist(),
                            # Polygon annotations for training Text Detection networks in mmocr.
                            # The format is the same as above for the inner list:
                            # [x1, y1, ..., xn, yn] (n≥3)
                            "polygon": segmentation.polygon().reshape(-1).tolist(),
                        }
                    )
                    if (
                        segmentation.class_identifier.class_name
                        not in segmentation_data_dict
                    ):
                        segmentation_data_dict[
                            segmentation.class_identifier.class_name
                        ] = 1
                    else:
                        segmentation_data_dict[
                            segmentation.class_identifier.class_name
                        ] += 1

            data_list.append(
                {
                    "img_path": annotation.image_path,
                    "img_id": img_id,
                    "seg_map_path": None,
                    "height": annotation.get_height(),
                    "width": annotation.get_width(),
                    "instances": instances,
                }
            )

        if len(bbox_data_dict.values()) > 0:
            logger.info(
                MLCVZooMMDetDataset.__generate_summary_message(
                    base_message="MLCVZooMMDetDataset loaded {} BBoxes:",
                    data_dict=bbox_data_dict,
                )
            )

        if len(segmentation_data_dict.values()) > 0:
            logger.info(
                MLCVZooMMDetDataset.__generate_summary_message(
                    base_message="MLCVZooMMDetDataset loaded {} Segmentations: ",
                    data_dict=segmentation_data_dict,
                )
            )

        return data_list
