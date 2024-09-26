#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
import logging
import subprocess
import time
from datetime import datetime
from datetime import timedelta
from pathlib import Path
from shutil import copy
from shutil import copytree
from tempfile import mkdtemp

import osgeo.ogr as ogr


KEEP_FILENAME = ".tondor_keep"


log = logging.getLogger(__name__)


def has_grassland_polygons(lulc_vector_filepath, gpkg_class_column, grassland_class_str):
    CLASS_ATTRIBUTE = gpkg_class_column
    source = ogr.Open(str(lulc_vector_filepath), update=False)
    layer = source.GetLayer()
    layer_defn = layer.GetLayerDefn()
    field_names = [layer_defn.GetFieldDefn(i).GetName() for i in range(layer_defn.GetFieldCount())]
    if CLASS_ATTRIBUTE not in field_names:
        msg = "File {:s} does not have expected attribute {:s}".format(str(lulc_vector_filepath), CLASS_ATTRIBUTE)
        raise Exception(msg)
    num_matching_polygons = 0
    feature = layer.GetNextFeature()
    while feature is not None:
        # for feature in layer:
        lulc_value = feature.GetField(CLASS_ATTRIBUTE)
        if str(lulc_value) == grassland_class_str:
            num_matching_polygons += 1
        feature = layer.GetNextFeature()
    source = None
    if num_matching_polygons == 0:
        log.warning(f"File {str(lulc_vector_filepath)} does not have any polygons with {CLASS_ATTRIBUTE}={grassland_class_str}.")
        return False
    else:
        return True
