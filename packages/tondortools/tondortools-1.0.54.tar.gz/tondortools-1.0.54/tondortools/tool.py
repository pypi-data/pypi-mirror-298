#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
import subprocess
import time
import glob
import os
import calendar
import shutil
import urllib.request as request
import math

from datetime import datetime
from datetime import timedelta
from pathlib import Path
from shutil import copy
from shutil import copytree
from tempfile import mkdtemp

import rasterio
from rasterio.transform import from_origin
from shapely.geometry import box
import osgeo.gdal as gdal
try:
    import ogr, osr
except:
    from osgeo import ogr, osr
import numpy as np
import pandas as pd

from .geo import BoundingBox, create_extent_wkt
from .input_parser import compile_basename_optcomposite, \
    compile_optcomposite_nodata_basename
from .logging_config import init_logging, get_console_handler

KEEP_FILENAME = ".tondor_keep"

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG) # Add the common handler
log.addHandler(get_console_handler())
log.propagate = False

def log_subprocess(args, work_dir, log_filepath, timeout=None):
    log.debug("Calling subprocess: {:s}, logging to {:s}.".format(repr(args), str(log_filepath)))
    with open(str(log_filepath), "at", encoding="utf-8") as logf:
        logf.write("\n{:s} Calling subprocess: {:s}.\n".format(datetime.utcnow().isoformat()[:23], repr(args)))
        logf.flush()
        pr = subprocess.run(args, cwd=work_dir, stdout=logf, stderr=logf, timeout=timeout, check=False)
        log.info("Subprocess exited with code {:d}, args={:s}.".format(pr.returncode, repr(args)))
        logf.write("\n{:s} Subprocess exited with code {:d}.\n".format(datetime.utcnow().isoformat()[:23], pr.returncode))
    pr.check_returncode()

def run_subprocess(args, work_dir):
    start = time.time()
    log.debug("Calling subprocess, args={:s}.".format(repr(args)))
    pr = subprocess.run(args, cwd=work_dir, check=False)
    pr.check_returncode()
    end = time.time()
    if int(pr.returncode) == 0:
        log.info(f"exit code {pr.returncode} --> {end - start} seconds --> {args}")
        log.info("Subprocess exited with code {:d}, args={:s}.".format(pr.returncode, repr(args)))
    else:
        raise Exception(f"exit code {pr.returncode} --> {end - start} seconds --> {args}")
###########################################

def query_site_selections(year, bioregion, selection_website_url):
    selection_query_url = f"{selection_website_url}?year={year}&bioregion={bioregion}"
    log.info("Querying the site selection infos from {:s}".format(selection_query_url))
    with request.urlopen(selection_query_url) as response:
        if response.getcode() == 200:
            source = response.read()
            return json.loads(source)["sites"]
        else:
            log.error("An error occurred while attempting to retrieve data from the API.")


###########################################

def read_tool_def(tool_def_filepath):
    tool_def = json.loads(tool_def_filepath.read_text())
    return tool_def


def set_input_param(job_step_params, ident, value):
    for input_p in job_step_params["parameters"]:
        if input_p["ident"] == ident:
            input_p["value"] = value

def get_json_item(file_path, key_name):
    with open(file_path, 'r') as file:
        json_content = json.load(file)

    # Retrieve the "database" item
    database_item = json_content.get(key_name)
    return database_item

def get_input_param(job_step_params, ident):
    for input_p in job_step_params["parameters"]:
        if input_p["ident"] == ident:
            return input_p["value"]
    return None

def calculate_time(start_time):
    end_time = time.time()
    # Calculate the time taken in seconds
    time_taken = end_time - start_time

    # Convert the time taken to hours, minutes, and seconds
    hours = int(time_taken // 3600)
    minutes = int((time_taken % 3600) // 60)
    seconds = int(time_taken % 60)

    # Print the time taken in hours, minutes, and seconds
    log.info(f"Time taken: {hours} hours, {minutes} minutes, {seconds} seconds")


###########################################
#################################################################################################
#################################################################################################
def yearmonth_parse(yearmonth):
    start_final_date = [ym.strip() for ym in yearmonth.split("-")]
    start_date = datetime.strptime(start_final_date[0],"%Y%m%d")
    final_date   = datetime.strptime(start_final_date[1],"%Y%m%d")
    start_date_basename = start_date.strftime("%Y%m%d")
    final_date_basename = final_date.strftime("%Y%m%d")
    return yearmonth, start_date, final_date, start_date_basename, final_date_basename


def generate_yearmonth_monthly(year, month):
    startmonth = month
    endmonth = month
    enddate = calendar.monthrange(year, endmonth)[1]

    yearmonth_start = "{:d}{:02}01".format(year, startmonth)
    yearmonth_end = "{:d}{:02}{:02}".format(year, month, enddate)
    yearmonth_timeperiod = str(yearmonth_start) + '-' + str(yearmonth_end)

    return yearmonth_timeperiod

def generate_yearmonth_quaterly(year, month):
    startmonth = month
    endmonth = month + 2
    enddate = calendar.monthrange(year, endmonth)[1]

    yearmonth_start = "{:d}{:02}01".format(year, startmonth)
    yearmonth_end = "{:d}{:02}{:02}".format(year, endmonth, enddate)
    yearmonth_timeperiod = str(yearmonth_start) + '-' + str(yearmonth_end)

    return yearmonth_timeperiod

def generate_yearmonth_monthbin(year, month, monthbin):
    startmonth = month
    endmonth = month + monthbin
    enddate = calendar.monthrange(year, endmonth)[1]

    yearmonth_start = "{:d}{:02}01".format(year, startmonth)
    yearmonth_end = "{:d}{:02}{:02}".format(year, endmonth, enddate)
    yearmonth_timeperiod = str(yearmonth_start) + '-' + str(yearmonth_end)

    return yearmonth_timeperiod

def generate_quarters_or_yearmonths(year_from, year_till, monthbins=None):
    q_or_ym = []

    year = int(str(year_from)[:4])
    month = int(str(year_from)[4:6])

    end_year = int(str(year_till)[:4])
    end_month = int(str(year_till)[4:6])

    while True:
        if year <= 2015 and monthbins is None:
            yearmonth = generate_yearmonth_quaterly(year, month)
            month = month + 3
        else:
            if monthbins is None:
                yearmonth = generate_yearmonth_monthly(year, month)
                month = month + 1
            if monthbins is not None:
                q_or_ym_bins = []
                for monthbin in monthbins:
                    yearmonth = generate_yearmonth_monthbin(year, month, abs(monthbin) - 1)
                    if not monthbin <0:
                        q_or_ym_bins.append(yearmonth)
                    month = month + abs(monthbin)

                    if year == end_year and month > end_month:
                        return q_or_ym_bins

                    if month > 12:
                        year += 1
                        month = 1

                return q_or_ym_bins
        q_or_ym.append(yearmonth)

        if year == end_year and month > end_month:
            break

        if month > 12:
            year += 1
            month = 1
    return q_or_ym


def generate_yearmonths(ym_from, ym_till):
    year = int(ym_from[:4])
    month = int(ym_from[4:6])
    yearmonths = []
    while True:
        yearmonth = "{:d}{:02}".format(year, month)
        if yearmonth > ym_till:
            break
        yearmonths.append(yearmonth)
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1
    return yearmonths

def generate_timeperiod_monthly(year, month):
    year = int(year)
    month = int(month)
    startmonth = month
    endmonth = month
    enddate = calendar.monthrange(year, endmonth)[1]

    yearmonth_start = "{:d}{:02}01".format(year, startmonth)
    yearmonth_end = "{:d}{:02}{:02}".format(year, month, enddate)
    yearmonth_timeperiod = str(yearmonth_start) + '-' + str(yearmonth_end)

    return yearmonth_timeperiod

def generate_timeperiod_quaterly(year, month):
    startmonth = month
    endmonth = month + 2
    enddate = calendar.monthrange(year, endmonth)[1]

    yearmonth_start = "{:d}{:02}01".format(year, startmonth)
    yearmonth_end = "{:d}{:02}{:02}".format(year, endmonth, enddate)
    yearmonth_timeperiod = str(yearmonth_start) + '-' + str(yearmonth_end)

    return yearmonth_timeperiod

def generate_quarters(year_from, year_till):
    year = int(year_from)
    quarters = [1, 2, 3, 4]
    yearquarters = []
    while True:
        for quarter in quarters:
            yearquarter = "{:d}Q{:d}".format(year, quarter)
            yearquarters.append(yearquarter)
        if year > year_till:
            break
    return yearquarters


def month_range(yearmonth):
    year = int(yearmonth[0:4])
    month = int(yearmonth[4:6])
    start_date = datetime(year, month, 1)
    if month == 12:
        month = 1
        year += 1
    else:
        month += 1
    final_date = datetime(year, month, 1)
    return (start_date, final_date)


def quarter_range(yearquarter):
    year = int(yearquarter[0:4])
    quarter_index = int(yearquarter[5:6]) - 1
    quarter_start_months = [1, 4, 7, 10]
    start_month = quarter_start_months[quarter_index]
    start_date = datetime(year, start_month, 1)

    quarter_final_months = [3, 6, 9, 12]
    final_month = quarter_final_months[quarter_index]
    if final_month == 12:
        final_month = 1
        year += 1
    else:
        final_month += 1
    final_date = datetime(year, final_month, 1)
    return (start_date, final_date)

def identify_period(pattern):
    """
    Identifies the period (quarter or month) based on the provided pattern.

    The pattern is expected to be in the format <year><startmonth>01-<year><endmonth><end date of the month>.
    If the gap between start and end months is 3 months, it identifies the quarter.
    If the gap is 1 month, it identifies the month.

    Args:
    pattern (str): The string pattern containing the year and month information.

    Returns:
    str: A string representing the quarter or month.
    """
    # Extracting year, start month, and end month from the pattern
    start_year = int(pattern[:4])
    start_month = int(pattern[4:6])
    end_year = int(pattern[9:13])
    end_month = int(pattern[13:15])

    # Check if the years are the same
    if start_year != end_year:
        return "Invalid pattern: Years do not match."

    # Calculate the month gap
    month_gap = end_month - start_month + 1

    # Identify the quarter or month
    if month_gap == 3:
        quarter = (start_month - 1) // 3 + 1
        return f"Q{quarter}"
    elif month_gap == 1:
        return f"M{start_month}"
    else:
        return "Invalid pattern: Month gap is neither 1 nor 3."




###########################################
def archive_results(tmp_dir_tpl, src_dst_pairs):
    # Create temporary directory dedicated for this function call.
    tmp_dir = Path(mkdtemp(prefix="{:s}.".format(tmp_dir_tpl.name), suffix=".d", dir=tmp_dir_tpl.parent))

    # Create all destination directories.
    dst_dirs = [dst_path.parent for (src_path, dst_path) in src_dst_pairs]
    dst_dirs = set(dst_dirs)
    dst_dirs = sorted(dst_dirs, key=str)
    for dst_dir in dst_dirs:
        # Before any move begins, the result directory should have updated timestamp.
        # Such updated timestamp should eliminate a race condition
        # when some other process is just removing empty directories.
        # While mkdir() does not update the timestamp if the directory already exists,
        # we must update the timestamp explicitly.
        keep_filepath = dst_dir.joinpath(KEEP_FILENAME)
        try:
            keep_filepath.touch(exist_ok=True)
            keep_filepath.unlink()
        except FileNotFoundError:
            pass
        dst_dir.mkdir(parents=True, exist_ok=True)

    # Copy all source items into temporary directory.
    #
    # To ensure two items with the same name do not collide,
    # give all the items in temporary directory special suffix.
    tmp_dst_pairs = []
    for (i, (src_path, dst_path)) in enumerate(src_dst_pairs, start=1):
        tmp_path = tmp_dir.joinpath("{:s}.{:d}".format(src_path.name, i))
        if src_path.is_dir():
            copytree(str(src_path), str(tmp_path))
            log.info("Directory tree {:s} has been copied to temporary {:s}."
                     .format(str(src_path), str(tmp_path)))
        else:
            copy(str(src_path), str(tmp_path))
            log.info("File {:s} has been copied to temporary {:s}."
                     .format(str(src_path), str(tmp_path)))
        tmp_dst_pairs.append((tmp_path, dst_path))

    # Move already copied items into final destination.
    for tmp_path, dst_path in tmp_dst_pairs:
        tmp_path.rename(dst_path)
        log.info("Temporary file/dir {:s} has been moved to final {:s}."
                 .format(str(tmp_path), str(dst_path)))

    # Remove the temporary directory.
    tmp_dir.rmdir()
    log.info("Temporary directory {:s} has been removed.".format(str(tmp_dir)))

def copy_files_from_archive(scrfiles_path, dst_folder):
    if type(scrfiles_path) == list:
        copied_path = []
        for scrfile_path_item in scrfiles_path:
            if 's3archive' in str(scrfile_path_item):
                pass
            else:
                copied_path = Path(dst_folder).joinpath(Path(scrfile_path_item).name)
                copy_singlefile_from_archive(scrfile_path_item, copied_path)
        copied_path.append(copied_path)
        
    else:
        copied_path = Path(dst_folder).joinpath(Path(scrfiles_path).name)
        if not Path(copied_path).exists():
            copy_singlefile_from_archive(scrfiles_path, copied_path)

    return copied_path
    
def copy_singlefile_from_archive(scrfile_path, dstfile_path):
    if not Path(dstfile_path).exists():
        log.info(f"{scrfile_path} --> {dstfile_path}")
        shutil.copy(str(scrfile_path), str(dstfile_path))
    
def remove_files(file_list):
    for file_list_item in file_list:
        remove_file(file_list_item)

def remove_file(file_path):
    if Path(file_path).exists():
        Path(file_path).unlink()
###########################################
# Utility functions for detecting missing L2A scenes.
#

def parse_sentinel2_name(name):
    if name.endswith(".SAFE"):
        name = name[:-5]
    name_parts = name.split("_")

    obs_datetime = datetime.strptime(name_parts[2], "%Y%m%dT%H%M%S")
    if obs_datetime >= datetime(2022, 1, 26):
        new_radiomatric_correction = True
    else:
        baseline_number = int(name_parts[3][1:])
        if baseline_number >= 400:
            new_radiomatric_correction = True
        else:
            new_radiomatric_correction = False

    info = {"name": name,
            "mission": name_parts[0][2],
            "level": name_parts[1][3:].upper(),
            "obs_date": datetime.strptime(name_parts[2], "%Y%m%dT%H%M%S"),
            "baseline": name_parts[3][1:],
            "radiometric_correction": new_radiomatric_correction,
            "rel_orbit": name_parts[4][1:],
            "tile": name_parts[5][1:],
            "produced_date": datetime.strptime(name_parts[6], "%Y%m%dT%H%M%S"),
            "satellite": "sentinel-2"}
    return info




def pair_sentinel2_scene_infos(scene_infos):
    # Build table of paired L1C and L2A items.
    scene_idx = {}
    for scene_info in scene_infos:
        scene_key = (scene_info["obs_date"], scene_info["tile"])

        if scene_key not in scene_idx:
            scene_idx[scene_key] = ([], [])

        if scene_info["level"] == "L1C":
            l1c_tuple = scene_idx[scene_key]
            l1c_tuple_firstitem_list = l1c_tuple[0]
            if len(l1c_tuple_firstitem_list) == 0:
                scene_idx[scene_key][0].append(scene_info)
            else:
                l1c_tuple_firstitem_list_itembaseline = int(l1c_tuple_firstitem_list[0]['baseline'])
                scene_info_baseline = int(scene_info['baseline'])
                if scene_info_baseline > l1c_tuple_firstitem_list_itembaseline:
                    l1c_tuple_list = list(l1c_tuple)
                    l1c_tuple_list[0] = [scene_info]
                    l1c_tuple = tuple(l1c_tuple_list)
                    scene_idx[scene_key] = l1c_tuple

        elif scene_info["level"] == "L2A":
            l2a_tuple = scene_idx[scene_key]
            l2a_tuple_seconditem_list = l2a_tuple[1]
            if len(l2a_tuple_seconditem_list) == 0:
                scene_idx[scene_key][1].append(scene_info)
            else:
                l2a_tuple_seconditem_list_itembaseline = int(l2a_tuple_seconditem_list[0]['baseline'])
                scene_info_baseline = int(scene_info['baseline'])
                if scene_info_baseline > l2a_tuple_seconditem_list_itembaseline:
                    l2a_tuple_list = list(l2a_tuple)
                    l2a_tuple_list[1] = [scene_info]
                    l2a_tuple = tuple(l2a_tuple_list)
                    scene_idx[scene_key] = l2a_tuple

        else:
            log.warning("Unknown level {:s} of the scene {:s}.".format(scene_info["level"], scene_info["name"]))

    # Sort the items within a pair by produced_date property.
    for (l1c, l2a) in scene_idx.values():
        l1c.sort(key=lambda info: info["produced_date"])
        l2a.sort(key=lambda info: info["produced_date"])

    return scene_idx



def filter_cloud_cover(scene_idx, max_cloud_cover):
    new_scene_idx = {}
    for (key, (l1c, l2a)) in scene_idx.items():
        item_cloud_cover = max(info["cloud_cover"] for info in [*l1c, *l2a])
        if item_cloud_cover > max_cloud_cover:
            key_date, tile = key
            log.debug("All items of the date {:s} and tile {:s} has been removed,"
                      " while the cloud cover {:f} is above {:f}."
                      .format(key_date.isoformat(), tile, item_cloud_cover, max_cloud_cover))
        else:
            new_scene_idx[key] = (l1c, l2a)
    return new_scene_idx


def compile_sentinel2level2a_glob(l1c_name):
    name_parts = l1c_name.split("_")
    mission = name_parts[0]
    obs_date = name_parts[2]
    tile = name_parts[5]
    year = obs_date[:4]
    month = obs_date[4:6]
    day = obs_date[6:8]
    name_glob = "{:s}_MSIL2A_{:s}_*_*_{:s}_*.SAFE".format(mission, obs_date, tile)
    path = Path("Sentinel2", year, month, day)
    return path, name_glob


def compile_sentinel2level2a_eodata_glob(l1c_name):
    path, name_glob = compile_sentinel2level2a_glob(l1c_name)
    path = Path(str(path).replace("Sentinel2/", "Sentinel-2/MSI/L2A/"))
    return path, name_glob


def compile_monthly_composite_filepath(archive_root, year, sitecode, month):
    countrycode = sitecode[0:2]
    yearmonth = "{:04d}{:02d}".format(int(year), month)
    startdate, enddate = month_range(yearmonth)
    # month_range returns (first day of the month, first day of the next month).
    # OPT composite naming convention uses (first day of the month, last day of the month).
    startdate = startdate.strftime("%Y%m%d")
    enddate = (enddate - timedelta(hours=12)).strftime("%Y%m%d")
    basename = "MTC_{startdate}_{enddate}_{sitecode}_OPT.tif"
    basename = basename.format(startdate=startdate, enddate=enddate, sitecode=sitecode)
    return archive_root.joinpath(str(year), countrycode, sitecode, "MTC", "OPT", basename)


def compile_quarterly_composite_filepath(archive_root, year, sitecode, quarter):
    countrycode = sitecode[0:2]
    yearquarter = "{:04d}{:02d}".format(int(year), quarter)
    log.debug(yearquarter)
    startdate, enddate = quarter_range(yearquarter)
    # month_range returns (first day of the month, first day of the next month).
    # OPT composite naming convention uses (first day of the month, last day of the month).
    startdate = startdate.strftime("%Y%m%d")
    enddate = (enddate - timedelta(hours=12)).strftime("%Y%m%d")
    basename = "MTC_{startdate}_{enddate}_{sitecode}_OPT.tif"
    basename = basename.format(startdate=startdate, enddate=enddate, sitecode=sitecode)
    return archive_root.joinpath(str(year), countrycode, sitecode, "MTC", "OPT", basename)

#################################################################################################
#################################################################################################

def save_list_to_json(data_list, folder_path, file_name):
    # Create the folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)

    # Create the file path
    file_path = os.path.join(folder_path, file_name)

    # Write the list to the JSON file
    with open(file_path, 'w') as file:
        json.dump(data_list, file)

def save_dict_to_json(data_dict, folder_path, file_name):
    # Create the folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)

    # Create the file path
    file_path = os.path.join(folder_path, file_name)

    converted_data = {k: (v.item() if isinstance(v, (np.integer, np.floating)) else v) for k, v in data_dict.items()}

    # Write the list to the JSON file
    with open(file_path, 'w') as file:
        json.dump(converted_data, file)

def read_json_to_list(file_path):
    # Read the JSON file into a list
    with open(file_path, 'r') as file:
        data_list = json.load(file)
    return data_list


def read_conversion_table(conversion_table_filepath, conversion_table_original_column, conversion_table_target_column):

    conversion_table_df = pd.read_csv(conversion_table_filepath, usecols=[conversion_table_original_column,
                                                                          conversion_table_target_column],
                                      index_col=0, encoding_errors='ignore')
    conversion_table_df.index = conversion_table_df.index.map(str)
    return conversion_table_df

def find_file_in_archives(relative_path, archive_roots, error_on_missing=True):
    for archive_root in archive_roots:
        log.debug("Searching for {:s} in {:s}".format(str(relative_path), str(archive_root)))
        filepath = archive_root.joinpath(relative_path)
        if filepath.is_file():
            log.info("Found {:s} at {:s}".format(filepath.name, str(filepath)))
            return filepath
    if error_on_missing:
        # If we got up to here, then nothing is found and we must raise FileNotFoundError.
        msg = "Expected file {:s} was not found in any of the archives.".format(str(relative_path))
        log.error(msg)
        raise FileNotFoundError

def find_files_in_archives_pattern(relative_path, archive_roots):
    filepaths = []
    for archive_root in archive_roots:
        log.debug("Searching for {:s} in {:s}".format(str(relative_path), str(archive_root)))
        path_fullpath = Path(archive_root).joinpath(relative_path)

        filepath = glob.glob(str(path_fullpath))
        if len(filepath)>0:
           log.info("Found {} in {}".format(filepath, archive_root))
           filepaths.extend(filepath)
    log.debug("Found the following opt composite files:{}".format(filepaths))
    return filepaths

def find_files_in_archives(relative_path, archive_roots, error_on_missing=True):
    filepaths = []
    for archive_root in archive_roots:
        log.debug("Searching for {:s} in {:s}".format(str(relative_path), str(archive_root)))
        path_fullpath = archive_root.joinpath(relative_path)

        filepath = glob.glob(str(path_fullpath))
        if len(filepath)>0:
           log.info("Found {} in {}".format(filepath, archive_root))
           filepaths.extend(filepath)
    log.debug("Found the following opt composite files:{}".format(filepaths))
    return filepaths

def return_tilename(tilename):
    if "_" in tilename:
        eodata_tilename = tilename.split("_")[0]
        return eodata_tilename
    else:
        return tilename

def return_eodata_tilename(tilename):
    if "-" in tilename:
        eodata_tilename = tilename.split("-")[0]
        return eodata_tilename
    else:
        return tilename


def compile_relative_dir(year, full_tilename, product_name, region = None):
    eodata_tilename = return_eodata_tilename(full_tilename)
    tilename = return_tilename(full_tilename)
    if "-" in tilename:
        if region is None: raise Exception(f"region is None")
        return Path(str(year)).joinpath(str(eodata_tilename).upper(), str(product_name).upper(), str(region).upper(), str(tilename).upper())
    else:
        return Path(str(year)).joinpath(str(tilename).upper(), str(product_name).upper())

def compile_ouput_archive_dir(output_root, year, tilename, product_name, region = None):
    return Path(output_root).joinpath(compile_relative_dir(year, tilename, product_name, region))

def compile_ouput_archive_filepath(output_root, year, tilename, product_name, file_name, region = None):
    ouput_archive_dir = compile_ouput_archive_dir(output_root, year, tilename, product_name, region)
    return ouput_archive_dir.joinpath(file_name)

#####################
#####################

def save_raster_template(rasterfn, newRasterfn, array, data_type, nodata_value=None):

    raster = gdal.Open(str(rasterfn))
    geotransform = raster.GetGeoTransform()
    originX = geotransform[0]
    originY = geotransform[3]
    pixelWidth = geotransform[1]
    pixelHeight = geotransform[5]
    cols = raster.RasterXSize
    rows = raster.RasterYSize

    if len(array.shape) == 2:
        nband = 1
    elif len(array.shape) == 3:
        nband = array.shape[0]

    driver = gdal.GetDriverByName('GTiff')
    outRaster = driver.Create(str(newRasterfn), cols, rows, nband, data_type,
                              ['COMPRESS=DEFLATE', 'TILED=YES', 'BIGTIFF=IF_NEEDED'])
    outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))
    outRasterSRS = osr.SpatialReference()
    outRasterSRS.ImportFromWkt(raster.GetProjectionRef())
    outRaster.SetProjection(outRasterSRS.ExportToWkt())

    if nband == 1:
        outband = outRaster.GetRasterBand(1)
        outband.WriteArray(array, 0, 0)
        if nodata_value is not None:
            outband.SetNoDataValue(nodata_value)
        outband.FlushCache()

    elif nband >1:
        for band_item in range(nband):
            outband = outRaster.GetRasterBand(band_item + 1)
            outband.WriteArray(array[band_item,:,:], 0, 0)
            if nodata_value is not None:
                outband.SetNoDataValue(nodata_value)
            outband.FlushCache()


def save_raster(array, destfile, driver, epsg, ulx, uly, pixel_size, data_type,
                colortable=None, nodata_value=None):

    Driver = gdal.GetDriverByName(driver)

    if len(array.shape) ==2:
        xsize = array.shape[1]
        ysize = array.shape[0]
        ds = Driver.Create(str(destfile), xsize, ysize, 1, data_type, options=["COMPRESS=DEFLATE", "TILED=YES"])
        ds.SetGeoTransform((ulx, pixel_size, 0, uly, 0, -pixel_size))
        proj = osr.SpatialReference()
        proj.ImportFromEPSG(epsg)
        ds.SetProjection(proj.ExportToWkt())
        band = ds.GetRasterBand(1)
        band.WriteArray(array, 0, 0)
        # set nodata_value if specified
        if nodata_value is not None:
            band.SetNoDataValue(nodata_value)
        # set Color table if specified
        if colortable is not None:
            clrs = gdal.ColorTable()
            for value, rgb in colortable.items():
                clrs.SetColorEntry(int(value), tuple(rgb))
            band.SetRasterColorTable(clrs)

    elif len(array.shape) == 3:
        xsize = array.shape[2]
        ysize = array.shape[1]
        nband = array.shape[0]
        ds = Driver.Create(str(destfile), xsize, ysize, nband, data_type, options=["COMPRESS=DEFLATE", "TILED=YES"])
        ds.SetGeoTransform((ulx, pixel_size, 0, uly, 0, -pixel_size))
        proj = osr.SpatialReference()
        proj.ImportFromEPSG(epsg)
        ds.SetProjection(proj.ExportToWkt())
        for band_item in range(nband):
            band = ds.GetRasterBand(band_item+1)
            band.WriteArray(array[band_item,:,:], 0, 0)
            # set nodata_value if specified
            if nodata_value is not None:
                band.SetNoDataValue(nodata_value)
            # set Color table if specified
            if colortable is not None:
                clrs = gdal.ColorTable()
                for value, rgb in colortable.items():
                    clrs.SetColorEntry(int(value), tuple(rgb))
                band.SetRasterColorTable(clrs)

    band.FlushCache()
    band, ds = None, None


def raster2array(rasterfn, band_no=1):
    raster = gdal.Open(str(rasterfn))
    band = raster.GetRasterBand(band_no).ReadAsArray().astype(np.float32)
    band_nodata = raster.GetRasterBand(band_no).GetNoDataValue()
    band[band == band_nodata] = np.nan
    raster = None
    return band

def read_raster_info(raster_filepath):
    ds = gdal.Open(str(raster_filepath))

    RasterXSize = ds.RasterXSize
    RasterYSize = ds.RasterYSize
    gt = ds.GetGeoTransform()
    ulx_raster = gt[0]
    uly_raster = gt[3]
    lrx_raster = gt[0] + gt[1] * ds.RasterXSize + gt[2] * ds.RasterYSize
    lry_raster = gt[3] + gt[4] * ds.RasterXSize + gt[5] * ds.RasterYSize
    imagery_extent_box = box(lrx_raster, uly_raster, ulx_raster, lry_raster)

    xmin = gt[0]
    ymax = gt[3]
    pixel_width = gt[1]
    yres = gt[5]

    projection = ds.GetProjection()
    srs = osr.SpatialReference()
    srs.ImportFromWkt(projection)
    epsg = int(srs.GetAttrValue('AUTHORITY', 1))

    datatype = ds.GetRasterBand(1).DataType
    n_bands = ds.RasterCount
    ds = None
    return (xmin, ymax, RasterXSize, RasterYSize, pixel_width, projection, epsg, datatype, n_bands, imagery_extent_box)

def clip_raster_to_extent(src_filepath, dst_filepath, xmin, xmax, ymin, ymax):
    cmd_gdal = ["gdal_translate",
                "-projwin",
                "{}".format(xmin), "{}".format(ymax),
                "{}".format(xmax), "{}".format(ymin),
                "{}".format(str(src_filepath)),
                "{}".format(str(dst_filepath))]
    cmd_output = subprocess.run(cmd_gdal, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    log.debug("exit code {} --> {}".format(cmd_output.returncode, cmd_gdal))


def clip_project_multibandraster_toextent(composite_filepath, warped_filepath, target_epsg, xmin, xmax, ymin, ymax, work_dir= None, method ='near'):
    cmd_gdal = ["gdalwarp",
           "-t_srs", "EPSG:{}".format(target_epsg),
           "-te",str(xmin),str(ymin),str(xmax),str(ymax),
           "-r", method,
           "-co", "COMPRESS=DEFLATE",
           str(composite_filepath),
           str(warped_filepath)
           ]
    cmd_output = subprocess.run(cmd_gdal, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    log.debug("exit code {} --> {}".format(cmd_output.returncode, cmd_gdal))

def reproject_multibandraster_toextent(composite_filepath, warped_filepath, target_epsg, pixel_size, xmin, xmax, ymin, ymax, work_dir= None, method ='near'):

    cmd_gdal = ["gdalwarp",
           "-t_srs", "EPSG:{}".format(target_epsg),
           "-tr", str(pixel_size), str(pixel_size),
           "-te",str(xmin),str(ymin),str(xmax),str(ymax),
           "-r", method,
           "-co", "COMPRESS=DEFLATE",
           str(composite_filepath),
           str(warped_filepath)
           ]
    cmd_output = subprocess.run(cmd_gdal, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    log.debug("exit code {} --> {}".format(cmd_output.returncode, cmd_gdal))


def reproject_multibandraster(composite_filepath, warped_filepath, target_epsg, pixel_size, work_dir, method ='bilinear'):

    cmd = ["gdalwarp",
           "-t_srs", "EPSG:{}".format(target_epsg),
           "-tr", str(pixel_size), str(pixel_size),
           "-r", method,
           "-co", "COMPRESS=DEFLATE",
           str(composite_filepath),
           str(warped_filepath)
           ]
    run_subprocess(cmd, work_dir)

def reproject_multibandraster_toextent_withnodata(composite_filepath, warped_filepath, target_epsg, pixel_size, xmin, xmax, ymin, ymax, work_dir, nodata_value, method ='bilinear'):

    cmd = ["gdalwarp",
           "-t_srs", "EPSG:{}".format(target_epsg),
           "-tr", str(pixel_size), str(pixel_size),
           "-te",str(xmin),str(ymin),str(xmax),str(ymax),
           "-r", method,
           "-ot", "Float32",
           "-dstnodata", nodata_value,
           "-co", "COMPRESS=DEFLATE",
           str(composite_filepath),
           str(warped_filepath)
           ]
    run_subprocess(cmd, work_dir)

def mosaic_tifs(tile_filepaths, mosaic_filepath, no_data = 0):
    if mosaic_filepath.is_file():
        mosaic_filepath.unlink()
    args = ["gdal_merge.py",
            "-co", "TILED=YES",
            "-co", "COMPRESS=DEFLATE",
            "-n", str(no_data),
            "-a_nodata", str(no_data),
            "-o", str(mosaic_filepath),
            "-pct"] + [str(fp) for fp in tile_filepaths]

    cmd_output = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    log.debug(f"exit code {cmd_output.returncode} --> {args}")

def stack_tifs(tile_filepaths, mosaic_filepath, no_data = 0):
    if mosaic_filepath.is_file():
        mosaic_filepath.unlink()
    args = ["gdal_merge.py",
            "-separate",
            "-o", str(mosaic_filepath),
            "-of", "GTiff",
            "-co", "compress=DEFLATE",
            "-a_nodata", f"{no_data}"]
    args = args + [str(filepath) for filepath in tile_filepaths]
    cmd_output = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    log.debug("exit code {} --> {}".format(cmd_output.returncode, args))

def merge_tiles(tile_filepaths, result_basename, work_dir, method='average'):
    log.debug("Creating merged composite from {:d} tiles for {:s}.".format(len(tile_filepaths), result_basename))
    merged_vrt_filepath = work_dir.joinpath(result_basename.replace(".tif", ".vrt"))
    log.debug("merged vrt filepath:{}".format(merged_vrt_filepath))

    # First create a vrt with the files that should be merged.
    args = ["gdalbuildvrt", merged_vrt_filepath]
    args = args + tile_filepaths
    log.debug("agrs:{}".format(args))
    subprocess.check_output(args)

    # Then convert the vrt to a merged GeoTiff file with compression.
    merged_result_filepath = work_dir.joinpath(result_basename)
    args = ["gdal_translate",
            "-of", "GTiff",
            "-r", f"{method}",
            "-co", "TILED=YES",
            "-co", "COMPRESS=DEFLATE",
            "-co", "BIGTIFF=YES",
           str(merged_vrt_filepath),
           str(merged_result_filepath)]
    subprocess.check_output(args)
    log.info("Final merged composite has been saved to {:s}.".format(str(merged_result_filepath)))
    return merged_result_filepath


def create_mosaic_filepath(raster_filepaths, output_path, NODATA_VALUE, method='average', data_type='Float32'):
    # mosaic_rasters(gdalfile=tiles,
    #                dst_dataset=file.path(Out_folder, paste0(IPCC_class, '_Product_ISB'), "ISB_AOImasked.tif"),
    #                of="GTiff", gdalwarp_params=list(r="average", ot="Float32"),
    #                co=c("COMPRESS=DEFLATE", "PREDICTOR=2", "ZLEVEL=9"), overwrite=TRUE, VERBOSE=TRUE)
    # GDAL Warp parameters
    raster_filepaths_str_list = [str(raster_item) for raster_item in raster_filepaths]
    gdalwarp_cmd = ['gdalwarp',
                    '-of', "GTiff",
                    "-r", method,
                    "-ot", data_type,
                    "-dstnodata", f"{NODATA_VALUE}",
                    "-co", "BIGTIFF=IF_NEEDED",
                    "-co", "TILED=YES",
                    "-co", "COMPRESS=LZW",
                    "-co", "ZLEVEL=9",
                    "-overwrite"] + raster_filepaths_str_list + [str(output_path)]
    cmd_output = subprocess.run(gdalwarp_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    log.debug("exit code {} --> {}".format(cmd_output.returncode, gdalwarp_cmd))

def create_maskedraster(output_gpkg, output_tiff, touch_status= "all_in", column_name='ID', empty_pixel_value=0):
    if touch_status == "all_in":
        CMD_mask = ['gdal_rasterize',
                    '-a',
                    '{}'.format(column_name),
                    '-at',
                    '{}'.format(output_gpkg),
                    '{}'.format(output_tiff)]
        cmd_output = subprocess.run(CMD_mask, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #log.debug("exit code {} --> {}".format(cmd_output.returncode, CMD_mask))

        CMD_mask = ['gdal_rasterize',
                    '-i', '-burn',
                    '{}'.format(str(empty_pixel_value)),
                    '-at',
                    '{}'.format(output_gpkg),
                    '{}'.format(output_tiff)]
        cmd_output = subprocess.run(CMD_mask, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #log.debug("exit code {} --> {}".format(cmd_output.returncode, CMD_mask))

    if touch_status == "all_touch":
        CMD_mask = ['gdal_rasterize',
                    '-a',
                    '{}'.format(column_name),
                    '-at',
                    '{}'.format(output_gpkg),
                    '{}'.format(output_tiff)]
        cmd_output = subprocess.run(CMD_mask, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #log.debug("exit code {} --> {}".format(cmd_output.returncode, CMD_mask))

    if touch_status == "all_on":
        CMD_mask = ['gdal_rasterize',
                    '-a',
                    '{}'.format(column_name),
                    '{}'.format(output_gpkg),
                    '{}'.format(output_tiff)]
        cmd_output = subprocess.run(CMD_mask, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #log.debug("exit code {} --> {}".format(cmd_output.returncode, CMD_mask))


#################################################################################################
#################################################################################################
def has_subset_in_string(string, subset_list):
    string = string.lower()  # Convert the input string to lowercase for case-insensitive matching
    for subset in subset_list:
        if subset.lower() in string:  # Check if the lowercased subset is a substring of the lowercased string
            return True
    return False

def locate_files(input_archive_roots, profile, years_list, sitecode, satellites_list,
                      start_yearmonth_analysis ,end_yearmonth_analysis):
    # Search ndvi tif files.
    all_profile_names = []
    all_profile_filepaths = []
    for input_archive_root in input_archive_roots:
        for year_item in years_list:
            profile_dir = input_archive_root.joinpath(str(year_item), sitecode, str(profile).upper())
            log.debug(f"Searching {profile} tif files in directory {profile_dir}.")
            profile_filepaths = list(profile_dir.glob(f"*_{str(profile.lower())}.tif"))
            for profile_filepath in profile_filepaths:

                has_sat_name = has_subset_in_string(profile_filepath.name, satellites_list)

                profile_date_str = profile_filepath.name.split('_')[1]
                profile_date = datetime.strptime(profile_date_str, '%Y-%m-%d')
                profile_in_timeperiod = (profile_date >= start_yearmonth_analysis) and (profile_date <= end_yearmonth_analysis)

                if str(year_item) in profile_filepath.name and has_sat_name and profile_filepath.is_file() and profile_in_timeperiod:
                    if profile_filepath.name not in all_profile_names:
                        all_profile_filepaths.append(profile_filepath)
                        all_profile_names.append(profile_filepath.name)
                        log.info("Found {:s}".format(str(profile_filepath)))
                    else:
                        log.debug("{:s} was already added from {:s}".format(str(profile_filepath.name), str(input_archive_root)))
        if len(all_profile_filepaths) == 0:
            raise Exception("No {:s} .tif files were found in the archives {:s}."
                            .format(profile,",".join([str(fp) for fp in input_archive_roots])))
        log.info(f"List of all input {profile} files:")
        all_profile_filepaths = sorted(sorted(all_profile_filepaths, key=lambda x: x.name))
        for profile_filepath in all_profile_filepaths:
            log.debug(profile_filepath)
    return all_profile_filepaths


def locate_profile_file(input_archive_roots, profile, time_period, sitecode_name, pixel_size=10, error_on_missing=True):
    sitecode = return_eodata_tilename(sitecode_name)
    yearmonth_list_item = time_period.replace('-', '_')
    year = yearmonth_list_item[0:4]

    # look for ndvi tif
    NDVI_tifname = f"{str(profile).upper()}_{yearmonth_list_item}_{sitecode}_PI{pixel_size}.tif"
    NDVI_relpath = Path(str(year)).joinpath(sitecode, str(profile).upper(), NDVI_tifname)
    NDVI_file = find_file_in_archives(NDVI_relpath, input_archive_roots, error_on_missing=False)


    NDVI_nodata_filename = f"{str(profile).upper()}_{yearmonth_list_item}_{sitecode}_PI{pixel_size}_NODATA.txt"
    NDVI_relpath = Path(str(year)).joinpath(sitecode, str(profile).upper(), NDVI_nodata_filename)
    NDVI_nodata_file = find_file_in_archives(NDVI_relpath, input_archive_roots, error_on_missing=False)

    if NDVI_file is not None:
        return NDVI_file
    elif NDVI_nodata_file is not None:
        return NDVI_nodata_file
    elif not error_on_missing:
        return None
    else:    
        raise Exception(f"{NDVI_file} and {NDVI_nodata_file} not found")

def locate_profile_interpolated_file(input_archive_roots, profile, time_period, sitecode, pixel_size=10, error_on_missing = False):
    yearmonth_list_item = time_period.replace('-', '_')
    year = yearmonth_list_item[0:4]


    interpolated_profile_folder = Path(str(year)).joinpath(sitecode, f"interpolated_{str(profile).upper()}")
    if error_on_missing:
        if not interpolated_profile_folder.exists(): raise Exception(f"{interpolated_profile_folder} doesnt exists")

    # look for ndvi tif
    NDVI_tifname = f"{str(profile).upper()}_{yearmonth_list_item}_{sitecode}_PI{pixel_size}.tif"
    NDVI_relpath = interpolated_profile_folder.joinpath(NDVI_tifname)
    NDVI_file = find_file_in_archives(NDVI_relpath, input_archive_roots, error_on_missing=False)
    if NDVI_file is not None:
        return NDVI_file
    else:
        NDVI_file = locate_profile_file(input_archive_roots, profile, time_period, sitecode, pixel_size=10)
        return NDVI_file

def locate_ndvi_stat(input_archive_roots, profile, year, sitecode, error_on_missing = False):
    # / mnt / hddarchive.nfs / output / 2017 / 42
    # RUS / OPT / MTC_20170101_20171231_42RUS_NDVI.tif
    stat_tifname = f"MTC_{year}0101_{year}1231_{sitecode}_{str('NDVI').upper()}.tif"
    stat_relpath = Path(str(year)).joinpath(sitecode, "OPT", stat_tifname)
    stat_file = find_file_in_archives(stat_relpath, input_archive_roots, error_on_missing=True)
    if stat_file is not None:
        return stat_file

def locate_optcomposites(archive_roots, year, sitecode, training_selection, site_selection):
    # training_selection: indices of months that should be used for the training, typically 111111111111.
    # site_selection: indices of months with suitable composites for the given site, e.g.  001111111110.
    # site_selection can have four digits or 12 digits
    # Constructs expected paths to OPT composites for a given year, site and selection.
    # Months with unsuitable composite are given the value of path=None.
    log.debug("Searching for OPT composites from site={}, year={}, training_selection={}, site_selection={}"
              .format(sitecode, year, training_selection, site_selection))
    countrycode = sitecode[0:2]
    num_timesteps = len(training_selection)
    if len(site_selection) != num_timesteps:
        raise Exception("training_selection and site_selection length must have equal number of timesteps.")

    log.info("Training selection is {:s}".format(repr(training_selection)))
    log.info("Site selection is {:s}".format(repr(site_selection)))

    # Check length of the site selection depending on the year.
    if int(year) >= 2016 and num_timesteps != 12:
        raise Exception("Number of selection items for sitecode {:s} is {:d}, but it should be 12.".format(sitecode, len(site_selection)))
    if int(year) <= 2015 and num_timesteps != 4:
        raise Exception("Number of selection items for sitecode {:s} is {:d}, but it should be 12.".format(sitecode,len(site_selection)))

    optcomposite_filepaths = []
    training_timesteps = []
    site_timesteps = []

    # The site selection is a 12-character or 4-character string of ones and zeros, e.g. 011111100100.
    # The character '1' means that the month is selected.
    # The character '0' means that the month is not selected.
    for ts_index, ts_status in enumerate(training_selection):
        if int(ts_status) == 1:
            training_timesteps.append(ts_index + 1)
    log.info("training_months or quarters: {}.".format(repr(training_timesteps)))

    # Here the indexes of the timesteps from which values should be taken are used.
    for timestep_index, timestep_status in enumerate(site_selection):
        if int(timestep_status) == 1:
            site_timesteps.append(timestep_index + 1)
    log.info("site_months or quarters: {}.".format(repr(site_timesteps)))

    for timestep in training_timesteps:
        if timestep in site_timesteps:
            composite_filepath = None
            for archive_root in archive_roots:
                if num_timesteps == 12:
                    composite_filepath = compile_monthly_composite_filepath(archive_root, year, sitecode, timestep)
                else:
                    composite_filepath = compile_quarterly_composite_filepath(archive_root, year, sitecode, timestep)
                log.info("Searching for composite at {:s}.".format(str(composite_filepath)))
                if composite_filepath.is_file():
                    # If composite is found, then add it to list.
                    log.info("Found composite for site {:s}, timestep {:d} at {:s}"
                             .format(sitecode, timestep, str(composite_filepath)))
                    optcomposite_filepaths.append(composite_filepath)
                    break
            if composite_filepath is None:
                log.error("No composite was found for site {:s}, selected timestep {:d}".format(sitecode, timestep))
                raise FileNotFoundError
        else:
            # If an OPTCOMPOSITE is not in selection then it is set to NONE.
            log.info("Set optcomposite for site {:s}, timestep {:d} to None.".format(sitecode, timestep))
            optcomposite_filepaths.append(None)

    log.info("selected OPT composites for site={}, year={}, training_selection={}, site_selection={} are:"
             .format(sitecode, year, training_selection, site_selection))
    for timestep, fp in enumerate(optcomposite_filepaths):
        log.info("timestep: {:d}, composite: {:s}".format(timestep, str(fp)))
    return training_timesteps, optcomposite_filepaths


def get_cloud_free_scenes(sentinel_tiles_list, start_time, end_time, input_archive_roots, work_dir, pixel_size=10,
                          band_list="011111100000000"):
    yearmonth_list = generate_quarters_or_yearmonths(start_time, end_time)

    # Initialize the dictionary
    result_dict = {}
    for sentinel_tiles_list_item in sentinel_tiles_list:
        result_dict[sentinel_tiles_list_item] = {}
        
        for yearmonth_list_item in yearmonth_list:
            year = yearmonth_list_item[0:4]

            optcomposite_pattern = {'PIXEL_SIZE': pixel_size,
                                    'DATE_RANGE': yearmonth_list_item,
                                    'SITECODE': sentinel_tiles_list_item}
            optcomposite_located = local_tile_yearmonth_optcomposite(optcomposite_pattern, year, sentinel_tiles_list_item,
                                                                     input_archive_roots)
            optcomposite_json_located = Path(optcomposite_located).with_suffix('.json')
            
            with open(optcomposite_json_located, 'r') as file:
                data = json.load(file)
            # Find the number of items that have the content variable 'sitecode' and 's2'
            included_scenes = data.get('included_scenes', [])
            count = sum(1 for item in included_scenes if sentinel_tiles_list_item in item)

            result_dict[sentinel_tiles_list_item][yearmonth_list_item] = count
            
    return  result_dict



def local_tile_yearmonth_optcomposite(optcomposite_pattern, year, sitecode, input_archive_roots):
    optcomposite_basename = compile_basename_optcomposite(optcomposite_pattern)
    optcomposite_tif = f"{optcomposite_basename}.tif"
    opt_composite_site_relpath = Path(str(year)).joinpath(sitecode, 'OPT', optcomposite_tif)
    opt_composite_site_files = find_files_in_archives_pattern(opt_composite_site_relpath,
                                                              input_archive_roots)
    if len(opt_composite_site_files) == 1:
        opt_composite_site_file_archive = opt_composite_site_files[0]
        return  opt_composite_site_file_archive
    elif len(opt_composite_site_files) >1:
        raise Exception(f"opt composite greater than 1")
    elif len(opt_composite_site_files) ==0:
        composite_nodata_filename = compile_optcomposite_nodata_basename(optcomposite_pattern, look_for_pattern=True)
        opt_composite_site_relpath = Path(str(year)).joinpath(sitecode, 'OPT',
                                                              composite_nodata_filename)
        opt_composite_site_files = find_files_in_archives_pattern(opt_composite_site_relpath, input_archive_roots)
        if len(opt_composite_site_files) == 1:
            input_list.append(None)
            return None
        else:
            raise Exception(f"opt composite and nodata txt not found ")

def locate_tile_optcomposites(sitecode, year, input_archive_roots):
    if int(year) < 2016:
        expected_composites = 4
        yearmonth_list = generate_quarters_or_yearmonths(int(f"{year}01"), int(f"{year}12"), [3,3,3,3])
    else:
        expected_composites = 12
        yearmonth_list = generate_quarters_or_yearmonths(int(f"{year}01"), int(f"{year}12"))

    input_list = []
    template_optfile = None

    for yearmonth_list_item in yearmonth_list:
        optcomposite_pattern = {'DATE_RANGE': yearmonth_list_item,
                                'SITECODE': sitecode}
        optcomposite_located = local_tile_yearmonth_optcomposite(optcomposite_pattern, year, sitecode, input_archive_roots)
        input_list.append(optcomposite_located)

    return input_list

def locate_yearmonth_sarcomposite(input_archive_roots, time_period, sitecode_name, pixel_size =20):
    sitecode = return_eodata_tilename(sitecode_name)
    yearmonth_list_item = time_period.replace('-', '_')
    year = yearmonth_list_item[0:4]
    #MTC_20230101_20230131_33UXQ_20_SAR
    # look for ndvi tif
    SAR_tifname = f"MTC_{yearmonth_list_item}_{sitecode}_{pixel_size}_SAR.tif"
    SAR_relpath = Path(str(year)).joinpath(sitecode, "MTC", "BAC", SAR_tifname)
    SAR_file = find_file_in_archives(SAR_relpath, input_archive_roots, error_on_missing=True)
    return SAR_file

def locate_sarcomposites(archive_roots, year, sitecode):
    # Constructs expected paths to SAR composites for a given year and site.
    countrycode = sitecode[0:2]
    composite_filepaths = []
    months = [m for m in range(1, 13)]
    for month in months:
        # Get the start date and end date of a given yearmonth.
        yearmonth = "{:04d}{:02d}".format(int(year), month)
        startdate, enddate = month_range(yearmonth)
        startdate = startdate.strftime("%Y%m%d")
        enddate = enddate.strftime("%Y%m%d")
        composite_basename = "MTC_{startdate}_{enddate}_{sitecode}_SAR.tif"
        composite_basename = composite_basename.format(startdate=startdate, enddate=enddate, sitecode=sitecode)
        composite_path = None
        for archive_root in archive_roots:
            base_dir = archive_root.joinpath(str(year), countrycode, sitecode, "MTC", "SAR")
            log.debug("Searching for {:s} at {:s}".format(composite_basename, str(base_dir)))
            composite_path = base_dir.joinpath(composite_basename)
            if composite_path.is_file():
                log.debug("Found {:s}".format(str(composite_path)))
                break
        if composite_path is None:
            log.warning("No SAR composite for sitecode={:s}, yearmonth={:s} found.".format(sitecode, yearmonth))
        composite_filepaths.append(composite_path)
    if len(composite_filepaths) != 12:
        raise Exception("Some SAR composites are missing for sitecode={:s} and year={:s}. Expected count is 12, number of found composites is {:d}."
                        .format(sitecode, str(year), len(composite_filepaths)))
    return composite_filepaths


def copy_file_from_s3(s3path, dstpath, retries, timeout, sleep_time):
    # FIXME use better mapping of object name from the mapped S3 path.
    object_name = str(s3path).replace("/s3archive/", "")
    if not object_name.startswith("output"):
        object_name = "output/" + object_name

    cmd = ["swift", "download",
           "--output", str(dstpath),
           "cop4n2k-archive", str(object_name)]
    downloaded = False
    try:
        log.debug(" ".join(cmd))
        subprocess.run(cmd, timeout=timeout, check=True)
        downloaded = True
        log.info("Downloaded cop4n2k-archive:{} to {}".format(object_name, dstpath))
    except Exception as ex:
        log.warning(str(ex))
        for retry in range(retries):
            log.warning("retrying download after {}s ..".format(sleep_time))
            time.sleep(sleep_time)
            try:
                log.debug(" ".join(cmd))
                subprocess.run(cmd, timeout=timeout, check=True)
                log.info("Downloaded cop4n2k-archive:{} to {}".format(object_name, dstpath))
                downloaded = True
                break
            except Exception as ex:
                log.warning(str(ex))
                continue
    if downloaded:
        return dstpath
    else:
        log.warning("Object cop4n2k-archive:{} could not be downloaded.".format(object_name))
        return None


def locate_project_lulc_geopackage(archive_roots, year, sitecode, project_code, postfix):
    gpkg_file = None

    # Input GeoPackage can be with or without an _orig.gpkg postfix.
    if postfix is None:
        gpkg_name = "LULC_{:d}_{:s}_{:s}.gpkg".format(year, project_code, sitecode)
    else:
        gpkg_name = "LULC_{:d}_{:s}_{:s}_{:s}.gpkg".format(year, project_code, sitecode, postfix)

    site_relpath = Path(str(year)).joinpath(sitecode, "LULC")
    for archive_root in archive_roots:
        site_dirpath = Path(archive_root).joinpath(site_relpath)
        log.debug("Searching for LULC GeoPackage at {:s}".format(str(site_dirpath)))
        gpkg_file = site_dirpath.joinpath(gpkg_name)
        if gpkg_file.is_file():
            log.info("Found LULC GeoPackage at {:s}".format(str(gpkg_file)))
            break
        gpkg_file = None
    if gpkg_file is None:
        msg = "There is no LULC geopackage for the year {} and sitecode {}. Expected file {} does not exist."
        msg = msg.format(year, sitecode, gpkg_name)
        log.error(msg)
        raise FileNotFoundError(msg)
    return gpkg_file

def check_geopackage_column(gpkg_filepath, column_name):
    CLASS_ATTRIBUTE = column_name
    source = ogr.Open(str(gpkg_filepath), update=False)
    layer = source.GetLayer()
    layer_defn = layer.GetLayerDefn()
    field_names = [layer_defn.GetFieldDefn(i).GetName() for i in range(layer_defn.GetFieldCount())]
    if CLASS_ATTRIBUTE not in field_names:
        msg = "File {:s} does not have expected attribute {:s}".format(str(gpkg_filepath), CLASS_ATTRIBUTE)
        raise Exception(msg)
    else:
        return True

def locate_lulc_geopackage(archive_roots, year, sitecode, postfix):
    if year < 2012:
        reference_geometry = "N2K2006"
    elif year < 2019:
        reference_geometry = "N2K2012"
    else:
        reference_geometry = "N2K2018"
    countrycode = sitecode[0:2]
    gpkg_file = None

    # Input GeoPackage can be with or without an _orig.gpkg postfix.
    if postfix is None:
        gpkg_name = "LULC_{:d}_{:s}_{:s}.gpkg".format(year, reference_geometry, sitecode)
    else:
        gpkg_name = "LULC_{:d}_{:s}_{:s}_{:s}.gpkg".format(year, reference_geometry, sitecode, postfix)

    site_relpath = Path(str(year)).joinpath(countrycode, sitecode, "LULC")
    for archive_root in archive_roots:
        site_dirpath = Path(archive_root).joinpath(site_relpath)
        log.debug("Searching for LULC GeoPackage at {:s}".format(str(site_dirpath)))
        gpkg_file = site_dirpath.joinpath(gpkg_name)
        if gpkg_file.is_file():
            log.info("Found LULC GeoPackage at {:s}".format(str(gpkg_file)))
            break
        gpkg_file = None
    if gpkg_file is None:
        msg = "There is no LULC geopackage for the year {} and sitecode {}. Expected file {} does not exist."
        msg = msg.format(year, sitecode, gpkg_name)
        log.error(msg)
        raise FileNotFoundError(msg)
    return gpkg_file


def locate_lulc_raster(archive_roots, year, sitecode):
    if year < 2015:
        raster_suffix = "OPT_CLASS_POST"
    else:
        raster_suffix = "INT_CLASS_POST"
    countrycode = sitecode[0:2]
    lulc_raster_name = "LULC_{:d}_{:s}_{:s}.tif".format(int(year), sitecode, raster_suffix)
    site_relpath = Path(str(year)).joinpath(countrycode, sitecode, "LULC")
    lulc_raster_file = None
    for archive_root in archive_roots:
        site_dirpath = Path(archive_root).joinpath(site_relpath)
        log.debug("Searching for LULC *CLASS_POST raster at {:s}".format(str(site_dirpath)))
        lulc_raster_file = site_dirpath.joinpath(lulc_raster_name)
        if lulc_raster_file.is_file():
            log.info("Found LULC raster at {:s}".format(str(lulc_raster_file)))
            break
        lulc_raster_file = None
    if lulc_raster_file is None:
        msg = "There is no LULC raster for the year {} and sitecode {}. Expected file {} does not exist."
        msg = msg.format(year, sitecode, lulc_raster_name)
        log.error(msg)
        raise FileNotFoundError(msg)
    return lulc_raster_file


def locate_swf_raster(archive_roots, year, sitecode):
    if int(year) < 2020:
        swf_year = 2015
    else:
        swf_year = 2020
    # determine year_dirpath from the current year
    if 1990 <= int(year) < 2000:
        year_dirpath = "1990_1999"
    elif 2000 <= int(year) < 2006:
        year_dirpath = "2000_2005"
    elif 2006 <= int(year) < 2012:
        year_dirpath = "2006_2011"
    elif 2012 <= int(year) <= 2018:
        year_dirpath = "2012_2018"
    else:
        year_dirpath = "2018_2023"
    swf_name = "{sitecode}_swf_{swf_year}_005m_FULL_3035_v012.tif".format(
        sitecode=sitecode, swf_year=swf_year)
    countrycode = sitecode[0:2]
    swf_relpath =Path("Support").joinpath(year_dirpath, countrycode, "swf")
    for archive_root in archive_roots:
        swf_dirpath = Path(archive_root).joinpath(swf_relpath)
        log.debug("Searching for SWF raster at {:s}".format(str(swf_dirpath)))
        swf_file = swf_dirpath.joinpath(swf_name)
        if swf_file.is_file():
            log.info("Found SWF raster at {:s}".format(str(swf_file)))
            break
        swf_file = None
    if swf_file is None:
        raise FileNotFoundError(
            "There is no SWF raster for the year {} and sitecode {}. Expected file {} does not exist."
                .format(year, sitecode, swf_name))
    return swf_file

def get_sitecode_aoiwkt(geom_info, aoi_epsg, support_data = "/support_data", region=None):

    if region is None:
        ## FIX ME ## make me better
        #################### geometry extent and pixel ###############################
        log.debug("Aoi wkt kwargs {}".format(geom_info))
        if type(geom_info) == str:
            if "-" in geom_info and region is None: raise Exception(f"- given in tilename")
            sitecodes = [geom_info]
        elif type(geom_info) == list:
            sitecodes = geom_info
            log.debug("tiles given as list: {}".format(sitecodes))
        elif str(geom_info).endswith('.gpkg'):
            log.debug("Geo package file given as input. Finding tiles from processing gpkg files to process")
            sitecodes, composite_sitecodes = get_sitecode_from_aoiwkt_parse(geom_info, aoi_epsg, gpkg_folder_path)
            log.debug("tiles: {}".format(sitecodes))
        elif "polygon" in geom_info.lower():
            log.debug("Extent given. Finding tiles from processing gpkg files to process")
            sitecodes, composite_sitecodes = get_sitecode_from_aoiwkt_parse(geom_info, aoi_epsg, gpkg_folder_path)
            log.debug("tiles: {}".format(sitecodes))

        gpkg_folder_path = Path(support_data).joinpath("tiles_csvfiles")
        sitecode_geom_dict = {}
        for sitecode in sitecodes:
            sitecode_geom = sitecode_extent(sitecode, aoi_epsg, gpkg_folder_path)
            sitecode_geom_dict[sitecode] = sitecode_geom

        log.debug("aoi: {}".format(sitecode_geom_dict))
        return sitecode_geom_dict
    else:
        if type(geom_info) == str:
            if "-" in geom_info and region is None: raise Exception(f"- given in tilename")
            sitecodes = [geom_info]
        elif type(geom_info) == list:
            sitecodes = geom_info

        region_geom_csv = Path(support_data).joinpath("tiles", region, f"{region}_tiles.csv")

        sitecode_geom_dict = {}
        for sitecode in sitecodes:
            extent_dict = extract_extent_from_csv(region_geom_csv, sitecode, aoi_epsg)
            extent_wkt = create_extent_wkt(extent_dict, aoi_epsg)
            sitecode_geom_dict[sitecode] = extent_wkt
        log.debug("aoi: {}".format(sitecode_geom_dict))
        return sitecode_geom_dict

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
          log.error(aoi_geom["message"])
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
    '''
    Return list of dictionaries - compositing squares in target Spatial Reference System.
    :param aoi_geom:
    :param grid_geopackage:
    :return:
    '''
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

def extract_extent_from_csv(extent_csv_path, sitecode, epsg_code, tile_column = "tile_name"):

    df = pd.read_csv(extent_csv_path)
    log.debug(f"reading {extent_csv_path} for {sitecode}")

    # Check for 'sentinel2_name' or 'sitecode' and filter

    filtered_df = df[df[tile_column] == sitecode]
    if not filtered_df.empty:
        row_epsg_value = int(filtered_df["epsg"].values[0])
        if row_epsg_value == int(epsg_code):
            log.debug(f"Found in {extent_csv_path} in {tile_column}")
            return {"xmin": filtered_df["xmin"].values[0],
                     "ymin": filtered_df["ymin"].values[0],
                     "xmax": filtered_df["xmax"].values[0],
                     "ymax": filtered_df["ymax"].values[0]}
    else:
        return None

def sitecode_extent(sitecode,  epsg_code, gpkg_folder_path = "/support_data/tiles_csvfiles"):

    found_tiles_list = []
    extent_csv_files = os.listdir(gpkg_folder_path)
    for extent_csv_file_item in extent_csv_files:
        if not str(extent_csv_file_item).endswith(f"{epsg_code}_withsitecode.csv"): continue
        extent_csv_path = Path(gpkg_folder_path).joinpath(extent_csv_file_item)
        extent_dict = extract_extent_from_csv(extent_csv_path, sitecode, epsg_code)
        if extent_dict is not None:
            found_tiles_list.append({"xmin": extent_dict["xmin"],
                                     "ymin": extent_dict["ymin"],
                                     "xmax": extent_dict["xmax"],
                                     "ymax": extent_dict["ymax"]})

    if not len(found_tiles_list) == 1: log.warning(f"More than one tile row found: {found_tiles_list}")
    # If there are more than one item in the list, assert whether the items have the same xmin, ymin, xmax, and ymax values
    if len(found_tiles_list) > 1:
        first_item = found_tiles_list[0]
        for item in found_tiles_list[1:]:
            assert item["xmin"] == first_item["xmin"], "Different xmin values"
            assert item["ymin"] == first_item["ymin"], "Different ymin values"
            assert item["xmax"] == first_item["xmax"], "Different xmax values"
            assert item["ymax"] == first_item["ymax"], "Different ymax values"

    extent_dict = found_tiles_list[0]

    extent_wkt = create_extent_wkt(extent_dict, epsg_code)
    return extent_wkt



###########################################################
def create_template_raster(bbox, tile_epsg, pixel_width, output_path, input_value=1, num_bands = 1, nodata_value = None):
    xmin, ymin, xmax, ymax = bbox.xmin, bbox.ymin, bbox.xmax, bbox.ymax
    width = int((xmax - xmin) / pixel_width)
    height = int((ymax - ymin) / pixel_width)
    transform = (xmin, pixel_width, 0, ymax, 0, -pixel_width)
    tile_crs = f'EPSG:{tile_epsg}'

    data = np.full((num_bands, height, width), input_value, dtype=np.uint8)

    driver = gdal.GetDriverByName('GTiff')
    dst_ds = driver.Create(str(output_path), width, height, num_bands, gdal.GDT_UInt16,
                           options=['COMPRESS=DEFLATE', 'BIGTIFF=YES', 'TILED=YES'])

    # Set the CRS
    srs = osr.SpatialReference()
    srs.SetFromUserInput(str(tile_crs))
    dst_ds.SetProjection(srs.ExportToWkt())

    # Set the transform
    dst_ds.SetGeoTransform(transform)

    # Write data to each band
    for band in range(1, num_bands + 1):
        dst_ds.GetRasterBand(band).WriteArray(data[band - 1])
        if nodata_value is not None:
            dst_ds.GetRasterBand(band).SetNoDataValue(nodata_value)

    # Close the dataset
    dst_ds = None
    return output_path


def raster_bounds_to_polygon(raster_path):
    """
    Convert the bounding box of a raster into a Shapely polygon.

    Parameters:
    - raster_path: The file path of the raster.

    Returns:
    - A Shapely polygon representing the bounding box of the raster.
    """
    with rasterio.open(raster_path) as dataset:
        # Extract the bounding box of the raster
        bounds = dataset.bounds

        # Create a Shapely polygon from the bounding box
        polygon = box(*bounds)

        return polygon

def setup_tiles(aoi_xmin, aoi_ymax, aoi_width_pixels, aoi_height_pixels, pixel_size, n_band, max_tile_size, tiles_parentdir, mask_path = None):

    if not Path(tiles_parentdir).exists():
        os.makedirs(tiles_parentdir)

    n_tile_cols = int(math.ceil(aoi_width_pixels / max_tile_size))
    n_tile_rows = int(math.ceil(aoi_height_pixels / max_tile_size))
    last_col = n_tile_cols - 1
    last_row = n_tile_rows - 1
    tile_infos = []
    log.debug(f"ntiles: {n_tile_rows}, {n_tile_cols}")
    for tile_row in range(n_tile_rows):
        tile_height = max_tile_size
        y_offset = tile_row * tile_height
        # Last row is a special case - tile height must be adjusted.
        if tile_row == last_row:
            tile_height = aoi_height_pixels - (max_tile_size * tile_row)

        for tile_col in range(n_tile_cols):
            tile_width = max_tile_size
            x_offset = tile_col * tile_width
            # Last column is a special case - tile width must be adjusted.
            if tile_col == last_col:
                tile_width = aoi_width_pixels - (max_tile_size * tile_col)

            # tile_ulx and tile_uly are the absolute coordinates of the upper left corner of the tile.
            tile_ulx = aoi_xmin + x_offset * pixel_size
            tile_uly = aoi_ymax - y_offset * pixel_size
            tile_lrx = tile_ulx + tile_width * pixel_size
            tile_lry = tile_uly - tile_height * pixel_size

            tile_work_dir = Path(tiles_parentdir).joinpath("tile_{:03d}_{:03d}".format(
                tile_row + 1, tile_col + 1))
            tile_work_dir.mkdir(parents=True, exist_ok=True)

            tile_multiband_composite = tile_work_dir.joinpath("tile_{:03d}_{:03d}.tif".format(tile_row + 1, tile_col + 1))
            tile_multiband_interpolated_composite = tile_work_dir.joinpath(
                "tile_{:03d}_{:03d}_interpolated.tif".format(tile_row + 1, tile_col + 1))
            tile_multiband_mask = tile_work_dir.joinpath(
                "tile_{:03d}_{:03d}_interpolation_mask.tif".format(tile_row + 1, tile_col + 1))
            tile_mask = None
            if mask_path is not None:
                tile_mask = tile_work_dir.joinpath(Path(mask_path).name)

            tile_info = {
                "row": tile_row,
                "col": tile_col,
                "width": tile_width,
                "height": tile_height,
                "x_offset": x_offset,
                "y_offset": y_offset,
                "ulx": tile_ulx,
                "uly": tile_uly,
                "lrx": tile_lrx,
                "lry": tile_lry,
                "pixel_size": pixel_size,
                "n_band": n_band,
                "tile_folder": str(tile_work_dir),
                "tile_multiband_composite": str(tile_multiband_composite),
                "tile_multiband_interpolated_composite": str(tile_multiband_interpolated_composite),
                "tile_multiband_mask": str(tile_multiband_mask),
                "tile_mask": str(tile_mask)
            }
            tile_infos.append(tile_info)
    return tile_infos




