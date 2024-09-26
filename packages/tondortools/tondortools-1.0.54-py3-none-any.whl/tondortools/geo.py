#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from math import ceil
from math import floor

try:
    import ogr, osr
except:
    from osgeo import ogr, osr

CATALOG_EPSG = 4326

def count_features(src_filepath):
    src_ds = ogr.Open(str(src_filepath))
    lyr = src_ds.GetLayer()
    return lyr.GetFeatureCount()

def prepare_query_boundingbox(aoi_wkt, aoi_epsg):
    # Prepare bounding box for the query.
    aoi_geom = ogr.CreateGeometryFromWkt(aoi_wkt)
    trans_to_catalog = create_transformation(aoi_epsg, CATALOG_EPSG)
    catalog_aoi_geom = aoi_geom.Clone()
    catalog_aoi_geom.Transform(trans_to_catalog)
    catalog_bbox = BoundingBox.from_geom(catalog_aoi_geom, CATALOG_EPSG)
    return catalog_bbox, catalog_aoi_geom


def create_transformation(src_epsg, dest_epsg):
    src_srs = osr.SpatialReference()
    src_srs.ImportFromEPSG(src_epsg)
    try:
        src_srs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
    except Exception:
        pass
    dest_srs = osr.SpatialReference()
    dest_srs.ImportFromEPSG(dest_epsg)
    try:
        dest_srs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
    except Exception:
        pass
    transformation = osr.CoordinateTransformation(src_srs, dest_srs)
    return transformation


def transform_geom(geom, src_epsg, dest_epsg):
    if src_epsg == dest_epsg:
        dest_geom = geom.Clone()
    else:
        transformation = create_transformation(src_epsg, dest_epsg)
        dest_geom = geom.Clone()
        dest_geom.Transform(transformation)
    return dest_geom


def compile_catalog_geom(aoi_wkt, aoi_epsg, aoi_buffer, catalog_epsg):
    aoi_geom = ogr.CreateGeometryFromWkt(aoi_wkt)
    aoi_geom = aoi_geom.Buffer(aoi_buffer)
    catalog_geom = transform_geom(aoi_geom, aoi_epsg, catalog_epsg)
    (xmin, xmax, ymin, ymax) = catalog_geom.GetEnvelope()
    catalog_bbox_tuple = (xmin, ymin, xmax, ymax)
    return catalog_geom, catalog_bbox_tuple

def create_extent_wkt(extent_dict, epsg_code):
    b_box_instance = BoundingBox(int(extent_dict["xmin"]), int(extent_dict["ymin"]), int(extent_dict["xmax"]), int(extent_dict["ymax"]), int(epsg_code))
    b_box_instance_geom = b_box_instance.to_geom()
    return b_box_instance_geom.ExportToWkt()

class BoundingBox():
    """Utility class for various bounding box handling."""

    def __init__(self, xmin, ymin, xmax, ymax, epsg):
        # Ensure min is always less than max.
        if xmin > xmax:
            xmin, xmax = xmax, xmin
        if ymin > ymax:
            ymin, ymax = ymax, ymin

        # Set up members.
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.epsg = epsg

    def pixel_count(self, size):
        width = int((self.xmax - self.xmin) / size)
        height = int((self.ymax - self.ymin) / size)
        return width * height

    def enlarge(self, size):
        xmin = self.xmin - size
        ymin = self.ymin - size
        xmax = self.xmax + size
        ymax = self.ymax + size
        bbox = type(self)(xmin, ymin, xmax, ymax, self.epsg)
        return bbox

    def enlarge_to_grid(self, size):
        xmin = floor(self.xmin / size) * size
        ymin = floor(self.ymin / size) * size
        xmax = ceil(self.xmax / size) * size
        ymax = ceil(self.ymax / size) * size
        bbox = type(self)(xmin, ymin, xmax, ymax, self.epsg)
        return bbox

    @classmethod
    def from_geom(cls, geom, epsg):
        (xmin, xmax, ymin, ymax) = geom.GetEnvelope()
        bbox = cls(xmin, ymin, xmax, ymax, epsg)
        return bbox

    def to_geom(self):
        ring_geom = ogr.Geometry(ogr.wkbLinearRing)
        ring_geom.AddPoint(self.xmin, self.ymin)
        ring_geom.AddPoint(self.xmax, self.ymin)
        ring_geom.AddPoint(self.xmax, self.ymax)
        ring_geom.AddPoint(self.xmin, self.ymax)
        ring_geom.AddPoint(self.xmin, self.ymin)
        geom = ogr.Geometry(ogr.wkbPolygon)
        geom.AddGeometry(ring_geom)
        geom.FlattenTo2D()
        return geom

    def transform(self, dest_epsg):
        """Transform the instance to dest_epsg coordinate system."""
        if self.epsg == dest_epsg:
            return self

        # Create a new instance with destination epsg.
        dest_geom = transform_geom(self.to_geom(), self.epsg, dest_epsg)
        (xmin, xmax, ymin, ymax) = dest_geom.GetEnvelope()
        dest_bbox = type(self)(xmin, ymin, xmax, ymax, dest_epsg)
        return dest_bbox

    def __repr__(self):
        return "{:s}({:f}, {:f}, {:f}, {:f}, epsg={:d})".format(type(self).__name__,
                                                                self.xmin, self.ymin, self.xmax, self.ymax,
                                                                self.epsg)
