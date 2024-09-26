
import logging
from datetime import datetime
from os.path import exists
import csv
import glob
try:
    import ogr, osr
except:
    from osgeo import ogr, osr
import os

log = logging.getLogger(__name__)

def yearmonth_parse(yearmonth):
    start_final_date = [ym.strip() for ym in yearmonth.split("-")]
    start_date = datetime.strptime(start_final_date[0],"%Y%m%d")
    final_date   = datetime.strptime(start_final_date[1],"%Y%m%d")
    start_date_basename = start_date.strftime("%Y%m%d")
    final_date_basename = final_date.strftime("%Y%m%d")
    return yearmonth, start_date, final_date, start_date_basename, final_date_basename

def satellite_parse(satellites):
    satellite_masterlist = ['sentinel-2', 'landsat-4', 'landsat-5', 'landsat-7', 'landsat-8','landsat-9']
    satellites_list = [sat.strip() for sat in satellites.split(",")]

    if not set(satellites_list) <= set(satellite_masterlist):
       log.error("Satellite not in master list, check naming convention")

    basename_sat = ""
    for satellite in satellites_list:
        basename_sat = basename_sat + satellite[0] + satellite[-1]
    return satellites, satellites_list, basename_sat

def band_parse(bands, satellites, satellite_bandinstance, pixel_size):
    band_masterlist = ["coastal_aerosol", "vis-b", "vis-g", "vis-r", "nir", "swir1", "swir2", "pan", "cirrus", "tir-10900", "tir-12000", "tir-11450", "re-705", "re-740", "re-781"]
    bands_list = [band.strip() for band in bands.split(",")]

    if not set(bands_list) <= set(band_masterlist):
       log.error("Band not in master list, check naming convention")
    basename_band = ""
    for band in band_masterlist:
        if band in bands:
            basename_band = basename_band + "1"
            satellite_bandinstance.satellite_band_check(band, satellites, pixel_size)
        else:
            basename_band = basename_band + "0"
    return bands, bands_list, basename_band

def resampling_parse(resampling):
    resampling_masterlist = ['average', 'near', 'bilinear', 'cubic']
    if resampling not in resampling_masterlist:
       log.error("Resampling not in master list, check naming convention")
    return resampling

def statistic_parse(statistic, targetdates):
    statistic_masterlist = ["wavg", "spline"]
    if not statistic in statistic_masterlist:
       log.error("Statistic not in master list, check naming convention")

    targetdates_list = [tardat.strip() for tardat in targetdates.split(",")]
    return statistic, targetdates_list, targetdates

def pixel_parse(pixel_size):
    pixel_size_str = str(pixel_size)
    pixel_size_int = int(pixel_size)
    pixel_size_basename = 'PI' + pixel_size_str
    return pixel_size_int, pixel_size_str, pixel_size_basename

def maxcloudcover_parse(max_cloud_cover):
    max_cloud_cover_str = str(max_cloud_cover)
    max_cloud_cover_int = int(max_cloud_cover)
    max_cloud_cover_basename = 'MAXCLOUD' + max_cloud_cover_str
    return max_cloud_cover_int, max_cloud_cover_str, max_cloud_cover_basename

def trim_parse(trim_low, trim_high):
    trim_low_str  = str(trim_low)
    trim_high_str = str(trim_high)
    trim_low_int  = int(trim_low)
    trim_high_int = int(trim_high)
    trim_basename = 'TRIM' + trim_low_str.zfill(3) + trim_high_str.zfill(3)
    return trim_low_int, trim_high_int, trim_low_str, trim_high_str, trim_basename

def nodata_parse(nodata_value):
    nodata_value_int = int(nodata_value)
    nodata_value_str = str(nodata_value)
    nodata_value_basename = 'NODATA' + nodata_value_str
    return nodata_value_int, nodata_value_str, nodata_value_basename

def unmasksummersnow_parse(unmask_snow, start_date, final_date):
    unmasksummersnow_masterlist = ['Q3','07','08','09']
    unmask_summer_snow_basename = "UNMASKSUMSNOW"

    startdateyear  = start_date.strftime("%Y")
    startdatemonth = start_date.strftime("%m")
    startdateday   = start_date.strftime("%d")

    finaldateyear = final_date.strftime("%Y")
    finaldatemonth = final_date.strftime("%m")
    finaldateday   = final_date.strftime("%d")

    start = datetime(day=int(startdateday), month=int(startdatemonth), year=int(startdateyear))
    end   = datetime(day=int(finaldateday), month=int(finaldatemonth), year=int(finaldateyear))

    startsum = datetime.strptime("01-07-"+startdateyear, "%d-%m-%Y")
    endsum   = datetime.strptime("01-10-"+finaldateyear, "%d-%m-%Y")
    if startsum <= start <= endsum and startsum <= end <= endsum and unmask_snow:
       log.debug("The time period is within summer time and unmask snow is: {}".format(unmask_snow))
       unmask_snow_timeperiod = "yes"
       unmask_summer_snow_basename = unmask_summer_snow_basename + '1'
    else:
       log.debug("The time period is within summer time and unmask snow is: {}".format(unmask_snow))
       unmask_snow_timeperiod = "no"
       unmask_summer_snow_basename = unmask_summer_snow_basename + '0'
    return unmask_snow, unmask_summer_snow_basename

def find_epsg_tilename(sitecode):
    if sitecode[0:3] == "UTM":
       epsg_no = sitecode[3:5]
       EPSG = int('326' + epsg_no)
    else:
       epsg_no = sitecode[0:2]
       EPSG = int('326' + epsg_no)
    return EPSG

def get_sitecode_from_aoiwkt_parse(aoi_wkt, t_srs):
    if aoi_wkt.endswith(".gpkg"):
       log.debug("aoi is specified as an gpkg file")
       aoi_ds = ogr.Open(aoi_wkt)
       aoi_lyr = aoi_ds.GetLayer()
       aoi_feat = aoi_lyr.GetNextFeature()
       aoi_geom = aoi_feat.GetGeometryRef()
       aoi_geom_wkt = aoi_geom.ExportToWkt()
       aoi_srs = aoi_lyr.GetSpatialRef()
       aoi_epsg = aoi_srs.GetAttrValue('AUTHORITY', 1)
       log.debug("Espg of input gpkg file: {}".format(aoi_epsg))

       aoi_geom = get_aoi_geometry(aoi_wkt, int(aoi_epsg))
       if aoi_geom["status"] == "ERROR":
          logger.error(aoi_geom["message"])
       else:
          aoi_geom = aoi_geom["output"]

       log.debug("aoi_geom: {}".format(aoi_geom))
    else:
       aoi_geom = aoi_wkt
    if True:
       compositing_grid = get_grid_file(t_srs)
       if compositing_grid["status"] == "OK":
          log.debug("grid geopackage:{}".format(compositing_grid["output"]))
          compositing_squares = get_composite_squares(aoi_geom, compositing_grid["output"])
    return compositing_squares


def get_composite_squares(aoi_geom, grid_geopackage):
    """
    Return list of dictionaries - compositing squares in target Spatial Reference System.
    :param aoi_geom:
    :param grid_geopackage:
    :return:
    """
    aoi_geom_inner = ogr.CreateGeometryFromWkt(aoi_geom).Buffer(-1)

    # output dictionary
    composite_squares = list()

    # get grid geopackage layer
    grid_ds = ogr.Open(grid_geopackage)
    grid_lyr = grid_ds.GetLayer()
    aoi_geom = ogr.CreateGeometryFromWkt(aoi_geom)
    grid_lyr.SetSpatialFilter(aoi_geom)
    feat = grid_lyr.GetNextFeature()

    while feat is not None:
        feat_geom = feat.GetGeometryRef().Buffer(-1)

        # create little inner buffer to exclude neighbour squares
        if feat_geom.Intersects(aoi_geom_inner):

            # feat = grid_lyr.GetNextFeature()
            composite_square = {"id": feat.GetField("id"),
                                "sitecode":feat.GetField("sitecode"),
                                "xmin": feat.GetField("xmin"),
                                "xmax": feat.GetField("xmax"),
                                "ymin": feat.GetField("ymin"),
                                "ymax": feat.GetField("ymax"),
                                "sen2_tiles": feat.GetField("sen2_tiles").split(","),
                                "ls_tiles": feat.GetField("ls_tiles").split(","),
                                "sen1_orbits": feat.GetField("sen1_orb").split(",")}
            composite_squares.append(composite_square)
        feat = grid_lyr.GetNextFeature()
    # Sort the results by id.
    composite_squares = sorted(composite_squares, key=lambda sq: sq["sitecode"])
    sitecodes = [composite_square["sitecode"] for composite_square in composite_squares]
    return sitecodes, composite_squares

def tile_aoi(geom_wkt):
    """
    Check if aoi is large enough to split into tiles (larger than 4 compositing tiles).
    :param geom_wkt: aoi geometry wkt
    :return: True in case of large aoi; False in case of small aoi
    """
    geom = ogr.CreateGeometryFromWkt(geom_wkt)
    area = geom.GetArea()
    if area > 9e8:
        return True
    else:
        return False

def get_grid_file(epsg_code):
    """
    Get absolute path to compositing grid file.
    :param epsg_code: EPSG code of target Spatial Reference System.
    :return: absolute path to compositing grid file.
    """
    gridfile = os.path.abspath(os.path.join("/tondor/tiles_gpkgfiles", "{0}_withsitecode.gpkg".format(epsg_code)))
    if os.path.isfile(gridfile):
        return {"status": "OK",
                "output": gridfile}
    else:
        return {"status": "ERROR",
                "message": "Target SRS specified with EPSG code: {0} either does not exist or is not currently supported.".format(epsg_code)}

def get_aoi_geometry(aoi_file, epsg_code):
    """
    Get Union geometry WKT from vector spatial data file.
    :param aoi_file: file path to vector spatial data file (e.g.: .shp, .geojson, .gpkg...)
    :param epsg_code: EPSG code of target SRS (e.g.: 5514 for S-JTSK, 4326 for WGS-84...)
    :return: WKT of union geometry
    """

    if not os.path.isfile(aoi_file):
        return {"status": "ERROR",
                "message": "AOI file does not exist."}

    ds = ogr.Open(aoi_file)
    if ds is None:
        return {"status": "ERROR",
                "message": "AOI file is not in supported format."}
    lyr = ds.GetLayer()
    s_srs = lyr.GetSpatialRef()
    t_srs = osr.SpatialReference()
    t_srs.ImportFromEPSG(epsg_code)
    transform = osr.CoordinateTransformation(s_srs, t_srs)

    if lyr.GetFeatureCount() == 1:

        feat = lyr.GetNextFeature()
        geom = feat.GetGeometryRef()
        geom.Transform(transform)
        return {"status": "OK",
                "output": geom.ExportToWkt()}
    else:
        feat = lyr.GetNextFeature()
        geom = feat.GetGeometryRef()
        geom.Transform(transform)
        geom = geom.Clone()
        feat = lyr.GetNextFeature()

        while feat is not None:
            geom_next = feat.GetGeometryRef()
            geom_next.Transform(transform)
            geom = geom.Union(geom_next)
            feat = lyr.GetNextFeature()
        return {"status": "OK",
                "output": geom.ExportToWkt()}

    '''
       aoi_geom_processing_tiles_srs = ogr.CreateGeometryFromWkt(aoi_geom_wkt)
    elif aoi_wkt.lower().startswith("POLYGON".lower()) or aoi_wkt.lower().startswith("MULTIPOLYGON".lower()):
       log.debug("Extent specified")
       aoi_geom_processing_tiles_srs = ogr.CreateGeometryFromWkt(aoi_wkt)
    else:
       log.error("check aoi wkt parameter")

    processing_tiles_filepaths = glob.glob("/mnt/tondor.nfs/tiles_gpkgfiles/*.gpkg")

    for processing_tiles_filepath in processing_tiles_filepaths:
        # get processing tiles features
        processing_tiles_ds = ogr.Open(processing_tiles_filepath)
        processing_tiles_lyr = processing_tiles_ds.GetLayer()
        processing_tiles_srs = processing_tiles_lyr.GetSpatialRef()
        processing_tiles_epsg = processing_tiles_srs.GetAttrValue('AUTHORITY', 1)

        # transform AOI SRS to processing tiles's SRS if needed
        if aoi_epsg != processing_tiles_epsg:
            transform = osr.CoordinateTransformation(aoi_srs, processing_tiles_srs)
            aoi_geom_processing_tiles_srs.Transform(transform)

        processing_tiles_lyr.SetSpatialFilter(aoi_geom_processing_tiles_srs)
        nr_of_processing_units = processing_tiles_lyr.GetFeatureCount()
        log.debug("No of processing units:{} for tiles filepath {}".format(nr_of_processing_units, processing_tiles_filepath))
        if nr_of_processing_units >0:
                # processing iteratively over processing tiles
                processing_feature = processing_tiles_lyr.GetNextFeature()
                processing_feature_nr = 1
                while processing_feature is not None:
                    processing_feature_id = processing_feature.GetField("TILE_ID")
                    print("Processing feature ID is: {}".format(processing_feature_id))
                    processing_feature = processing_tiles_lyr.GetNextFeature()
    '''

def sitecode_extent(sitecode,  epsg_code):
    gridfile = os.path.abspath(os.path.join("/tondor/tiles_gpkgfiles", "{0}_withsitecode.gpkg".format(epsg_code)))
    processing_tiles_ds = ogr.Open(gridfile)
    processing_tiles_lyr = processing_tiles_ds.GetLayer()
    processing_tiles_srs = processing_tiles_lyr.GetSpatialRef()
    processing_tiles_epsg = processing_tiles_srs.GetAttrValue('AUTHORITY', 1)

    for feature in processing_tiles_lyr:

        if feature['sitecode'] == sitecode:
           return feature.geometry().ExportToWkt()

def load_included_scenes(csvfile):
    scene_identifiers = []
    with open(csvfile) as cf:
        csv_reader = csv.reader(cf, delimiter=",")
        for row in csv_reader:
            if row == []:
                break
            scene_identifiers.append(row[-1].strip())
    return scene_identifiers

def find_landsat_sentinel_fromincludedscenes(scenes):
    landsatscenes_dict = {}
    landsat9_dict = {}
    landsat8_dict = {}
    landsat7_dict = {}
    landsat5_dict = {}
    sentinelscenes_list = []
    for scene in scenes:
        scene_namepart_list = [sat.strip() for sat in scene.split("_")]
        if scene_namepart_list[0] == 'LC09':
            if scene_namepart_list[2] not in landsat9_dict.keys():
                landsat9_dict[scene_namepart_list[2]] = [scene_namepart_list[3]]
            else:
                landsat9_dict[scene_namepart_list[2]].append(scene_namepart_list[3])
        elif scene_namepart_list[0] == 'LC08':
            if scene_namepart_list[2] not in landsat8_dict.keys():
                landsat8_dict[scene_namepart_list[2]] = [scene_namepart_list[3]]
            else:
                landsat8_dict[scene_namepart_list[2]].append(scene_namepart_list[3])
        elif scene_namepart_list[0] == 'LC07':
            if scene_namepart_list[2] not in landsat7_dict.keys():
                landsat7_dict[scene_namepart_list[2]] = [scene_namepart_list[3]]
            else:
                landsat7_dict[scene_namepart_list[2]].append(scene_namepart_list[3])
        elif scene_namepart_list[0] == 'LC05':
            if scene_namepart_list[2] not in landsat5_dict.keys():
                landsat5_dict[scene_namepart_list[2]] = [scene_namepart_list[3]]
            else:
                landsat5_dict[scene_namepart_list[2]].append(scene_namepart_list[3])

        elif scene.startswith('S2'):
            scene_namepart_list = [sat.strip() for sat in scene.split(".")]
            sentinelscenes_list.append(scene_namepart_list[0])
    landsatscenes_dict[9] = landsat9_dict
    landsatscenes_dict[8] = landsat8_dict
    landsatscenes_dict[7] = landsat7_dict
    landsatscenes_dict[5] = landsat5_dict

    return landsatscenes_dict, sentinelscenes_list

def included_sceneslist_parse(INCLUDED_SCENES_PATH):

    includedscenes_file_exists = exists(INCLUDED_SCENES_PATH)
    included_scenes = []
    included_landsatscenes_dict ={}
    included_sentinelscenes_list = []
    if includedscenes_file_exists:
        log.debug("Included scenes file exist in :{}".format(INCLUDED_SCENES_PATH))
        included_scenes = load_included_scenes(INCLUDED_SCENES_PATH)
        log.debug("Number of all included scenes are :{}".format(len(included_scenes)))
        included_landsatscenes_dict, included_sentinelscenes_list = find_landsat_sentinel_fromincludedscenes(included_scenes)

    if INCLUDED_SCENES_PATH != "" and len(included_scenes) == 0:
       input("Included scene path is one of the input. But the file is not found. Check whether the link is correct. Exiting")
       raise Exception("Incorrect included scene file")
       exit()

    return included_landsatscenes_dict, included_sentinelscenes_list, includedscenes_file_exists, included_scenes

def ignore_skip_missingL2A_parse(SKIP_MISSING_L2A_PATH):
    skip_missing_l2a_exists = exists(SKIP_MISSING_L2A_PATH)
    missing_l2a_list = []
    if skip_missing_l2a_exists:
       log.debug("Skipped missing l2a scenes file exist in :{}".format(SKIP_MISSING_L2A_PATH))
       missing_l2a_list = load_included_scenes(SKIP_MISSING_L2A)
    if SKIP_MISSING_L2A_PATH != "" and len(missing_l2a_list) == 0:
       input("Skipped missing l2a file list is one of the input. But the file is not found. Check whether the link is correct. Exiting")
       log.error("Incorrect skipping missing l2a file")
       exit()

    return skip_missing_l2a_exists, missing_l2a_list

def compile_basename_optcomposite(optcomposite_pattern_dict):

    optcomposite_basename = 'OPT_STARTDATE_FINALDATE_SITECODE_PIXELSIZE_SATELLITES_BANDS_RESAMPLING_UNMASKSUMMERSNOW_MAXCLOUD_TRIM_DATATYPE_OUTPUTNODATAVALUE_STATISTIC_*'
    optcomposite_master_pattern_list = ['SATELLITES', 'PIXEL_SIZE', 'BANDS', 'DATE_RANGE', 'SITECODE', 'STATISTICS', 'RESAMPLING', 'TARGET_DATES', 'OUTPUT_NODATA_VALUE',
                                   'MAX_CLOUD', 'TRIM_LOW', 'TRIM_HIGH', 'UNMASK_SUMMER_SNOW']

    optcomposite_basename_parts_list = optcomposite_basename.split('_')
    satellite_bandinstance  = satellite_band()

    for item in optcomposite_master_pattern_list:
        if item in optcomposite_pattern_dict.keys():

            if item == 'SATELLITES':
                satellites, satellites_list, basename_sat = satellite_parse(optcomposite_pattern_dict[item])
                optcomposite_basename = optcomposite_basename.replace('SATELLITES', basename_sat)

            elif item == 'PIXEL_SIZE':
                pixel_size, pixel_size_str, pixel_size_basename = pixel_parse(optcomposite_pattern_dict[item])
                optcomposite_basename = optcomposite_basename.replace('PIXELSIZE', pixel_size_basename)

            elif item == 'BANDS':
                all_binary = all(c in '01' for c in optcomposite_pattern_dict[item])
                if all_binary:
                    optcomposite_basename = optcomposite_basename.replace('BANDS', optcomposite_pattern_dict[item])
                    continue
                _, bands, basename_band = band_parse(optcomposite_pattern_dict[item], satellites, satellite_bandinstance, pixel_size)
                optcomposite_basename = optcomposite_basename.replace('BANDS',basename_band)

            elif item == 'STATISTICS':
                statistics = 'wavg'
                optcomposite_basename = optcomposite_basename.replace('STATISTIC',statistics)

            elif item == 'DATE_RANGE':
                yearmonth, start_date, final_date, start_date_basename, final_date_basename = yearmonth_parse(optcomposite_pattern_dict[item])
                optcomposite_basename = optcomposite_basename.replace('STARTDATE',start_date_basename)
                optcomposite_basename = optcomposite_basename.replace('FINALDATE',final_date_basename)

            elif item == 'SITECODE':
                optcomposite_basename = optcomposite_basename.replace('SITECODE', optcomposite_pattern_dict[item])

            elif item == 'RESAMPLING':
                resampling = resampling_parse(optcomposite_pattern_dict[item])
                optcomposite_basename = optcomposite_basename.replace('RESAMPLING', resampling)

            elif item == 'MAX_CLOUD':
                max_cloud_cover, max_cloud_cover_str, max_cloud_cover_basename = maxcloudcover_parse(optcomposite_pattern_dict[item])
                optcomposite_basename = optcomposite_basename.replace('MAXCLOUD', max_cloud_cover_basename)

            elif item == 'UNMASK_SUMMER_SNOW':
                if optcomposite_pattern_dict[item] == 'yes': unmask_snow = True
                else: unmask_snow = False
                unmask_snow, unmask_summer_snow_basename = unmasksummersnow_parse(unmask_snow, start_date, final_date)
                optcomposite_basename = optcomposite_basename.replace('UNMASKSUMMERSNOW', unmask_summer_snow_basename)

    for optcomposite_basename_parts_listitem in optcomposite_basename_parts_list:
        if optcomposite_basename_parts_listitem == 'OPT':
            continue
        optcomposite_basename = optcomposite_basename.replace(optcomposite_basename_parts_listitem, '*')
    log.debug(optcomposite_basename)
    return optcomposite_basename

def compile_optcomposite_nodata_basename(optcomposite_pattern_dict, look_for_pattern=False):

    optcomposite_basename = 'OPT_STARTDATE_FINALDATE_SITECODE_PIXELSIZE_SATELLITES_BANDS_NODATA.txt'
    optcomposite_master_pattern_list = ['SATELLITES', 'PIXEL_SIZE', 'BANDS', 'DATE_RANGE', 'SITECODE']


    optcomposite_basename_parts_list = optcomposite_basename.split('_')
    satellite_bandinstance  = satellite_band()

    for item in optcomposite_master_pattern_list:
        if item in optcomposite_pattern_dict.keys():

            if item == 'SATELLITES':
                satellites, satellites_list, basename_sat = satellite_parse(optcomposite_pattern_dict[item])
                optcomposite_basename = optcomposite_basename.replace('SATELLITES', basename_sat)

            elif item == 'PIXEL_SIZE':
                pixel_size, pixel_size_str, pixel_size_basename = pixel_parse(optcomposite_pattern_dict[item])
                optcomposite_basename = optcomposite_basename.replace('PIXELSIZE', pixel_size_basename)

            elif item == 'BANDS':
                all_binary = all(c in '01' for c in optcomposite_pattern_dict[item])
                if all_binary:
                    optcomposite_basename = optcomposite_basename.replace('BANDS', optcomposite_pattern_dict[item])
                    continue
                _, bands, basename_band = band_parse(optcomposite_pattern_dict[item], satellites, satellite_bandinstance, pixel_size)
                optcomposite_basename = optcomposite_basename.replace('BANDS',basename_band)

            elif item == 'STATISTICS':
                statistics = 'wavg'
                optcomposite_basename = optcomposite_basename.replace('STATISTIC',statistics)

            elif item == 'DATE_RANGE':
                yearmonth, start_date, final_date, start_date_basename, final_date_basename = yearmonth_parse(optcomposite_pattern_dict[item])
                optcomposite_basename = optcomposite_basename.replace('STARTDATE',start_date_basename)
                optcomposite_basename = optcomposite_basename.replace('FINALDATE',final_date_basename)

            elif item == 'SITECODE':
                optcomposite_basename = optcomposite_basename.replace('SITECODE', optcomposite_pattern_dict[item])

            elif item == 'RESAMPLING':
                resampling = resampling_parse(optcomposite_pattern_dict[item])
                optcomposite_basename = optcomposite_basename.replace('RESAMPLING', resampling)

            elif item == 'MAX_CLOUD':
                max_cloud_cover, max_cloud_cover_str, max_cloud_cover_basename = maxcloudcover_parse(optcomposite_pattern_dict[item])
                optcomposite_basename = optcomposite_basename.replace('MAXCLOUD', max_cloud_cover_basename)

            elif item == 'UNMASK_SUMMER_SNOW':
                if optcomposite_pattern_dict[item] == 'yes': unmask_snow = True
                else: unmask_snow = False
                unmask_snow, unmask_summer_snow_basename = unmasksummersnow_parse(unmask_snow, start_date, final_date)
                optcomposite_basename = optcomposite_basename.replace('UNMASKSUMMERSNOW', unmask_summer_snow_basename)

    for optcomposite_basename_parts_listitem in optcomposite_basename_parts_list:
        if optcomposite_basename_parts_listitem == "OPT" or optcomposite_basename_parts_listitem == "NODATA.txt":
            continue
        optcomposite_basename = optcomposite_basename.replace(optcomposite_basename_parts_listitem, '*')
    log.debug(optcomposite_basename)
    if not look_for_pattern:
        if '*' in optcomposite_basename:
            raise Exception("provide correct dict to create nodata txt filename")
    return optcomposite_basename




class satellite_band():
    def __init__(self):
        self.landsat_band_lookup_table = {
            "landsat-9": {
                "coastal_aerosol": "SR_B1",
                "vis-b": "SR_B2",
                "vis-g": "SR_B3",
                "vis-r": "SR_B4",
                "nir": "SR_B5",
                "swir1": "SR_B6",
                "swir2": "SR_B7",
                "pan": "SR_B8",
                "cirrus": "SR_B9",
                "tir-10900": "SR_B10",
                "tir-12000": "SR_B11"
            },
            "landsat-8": {
                "coastal_aerosol": "SR_B1",
                "vis-b": "SR_B2",
                "vis-g": "SR_B3",
                "vis-r": "SR_B4",
                "nir": "SR_B5",
                "swir1": "SR_B6",
                "swir2": "SR_B7",
                "pan": "SR_B8",
                "cirrus": "SR_B9",
                "tir-10900": "SR_B10",
                "tir-12000": "SR_B11"
            },
            "landsat-7": {
                "vis-b": "SR_B1",
                "vis-g": "SR_B2",
                "vis-r": "SR_B3",
                "nir": "SR_B4",
                "swir1": "SR_B5",
                "swir2": "SR_B7",
                "tir-11450": "SR_B6"
            },
            "landsat-5": {
                "vis-b": "SR_B1",
                "vis-g": "SR_B2",
                "vis-r": "SR_B3",
                "nir": "SR_B4",
                "swir1": "SR_B5",
                "swir2": "SR_B7",
                "tir_11450": "SR_B6"
            },
            "landsat-4": {
                "vis_b": "SR_B1",
                "vis_g": "SR_B2",
                "vis_r": "SR_B3",
                "nir": "SR_B4",
                "swir1": "SR_B5",
                "swir2": "SR_B7",
                "tir_11450": "SR_B6"
            }
        }
        self.sentinel2_band_lookup_10m_table = {"vis-b": "B02_10m",
                                 "vis-g": "B03_10m",
                                 "vis-r": "B04_10m",
                                 "nir": "B08_10m"}

        self.sentinel2_band_lookup_20m_table = {"vis-b": "B02_20m",
                                 "vis-g": "B03_20m",
                                 "vis-r": "B04_20m",
                                 "re-705": "B05_20m",
                                 "re-740": "B06_20m",
                                 "re-781": "B07_20m",
                                 "nir": "B8A_20m",
                                 "swir1": "B11_20m",
                                 "swir2": "B12_20m"
                                 }

    def landsat_band_lookup(self, sat_label, band_label):
        return self.landsat_band_lookup_table[sat_label][band_label]

    def sentinel2_band_lookup(self, band_label, resolution):
        if resolution >= 20:
            band_expr = self.sentinel2_band_lookup_20m_table[band_label]
        else:
            try:
                band_expr = self.sentinel2_band_lookup_10m_table[band_label]
            except KeyError:
                band_expr = self.sentinel2_band_lookup_20m_table[band_label]

        return band_expr

    def satellite_band_check(self, band_label, satellites, resolution=20):
        for sat in satellites:
            if sat.startswith("landsat"):
                 if not band_label in self.landsat_band_lookup_table[sat].keys():
                    raise Exception("{} doesnot have data for band {}".format(sat, band_label))
            elif sat.startswith("sentinel"):
                 if band_label in self.sentinel2_band_lookup_10m_table.keys() or self.sentinel2_band_lookup_20m_table.keys():
                    log.debug("{} has data for band {}".format(sat, band_label))
                 else:
                    raise Exception("{} doesnot have data for band {}".format(sat, band_label))

    def satellite_bandlist_check(self, bandlist, satellites, resolution = 20):
        for band_label in bandlist:
            self.satellite_band_check(band_label, satellites, resolution)
