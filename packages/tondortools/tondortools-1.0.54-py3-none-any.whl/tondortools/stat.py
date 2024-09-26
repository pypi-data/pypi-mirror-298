import math
import os
import logging
import subprocess
import json

from pathlib import Path

import numpy as np
from tondortools.tool import read_raster_info, save_raster, mosaic_tifs
from multiprocessing import Pool

import numpy
from scipy.interpolate import Rbf
from osgeo.gdalconst import GA_ReadOnly, GDT_Float32, GDT_Int16, GDT_Byte
try:
    from osgeo import gdal
except:
    import gdal

from .tool import merge_tiles, setup_tiles, raster_bounds_to_polygon, create_template_raster, read_raster_info
from .geo import BoundingBox

from scipy.interpolate import interp1d, CubicSpline
NODATA_VALUE = -99999
MAX_TILE_SIZE = 3000
CPU_COUNT = 7

log = logging.getLogger(__name__)


def append_to_dict(dictionary, key, value):
    if key in dictionary:
        dictionary[key].append(value)
    else:
        dictionary[key] = [value]


def generate_interpolated_multiband_tile(input_data):
    tile_info = input_data[0]

    tile_multiband_interpolated_composite = Path(tile_info["tile_multiband_interpolated_composite"])
    if not tile_multiband_interpolated_composite.exists():
        (xmin, ymax, xsize, ysize, pixel_width, projection, epsg, data_type, n_bands, _) = read_raster_info(
            str(tile_info['tile_multiband_composite']))
        input_rasters_bands = tile_info['n_band']

        src_ds = gdal.Open(str(tile_info['tile_multiband_composite']))
        src_ds_array = src_ds.ReadAsArray().astype(float)
        src_ds_array_shape = src_ds_array.shape
        nodata_value = src_ds.GetRasterBand(1).GetNoDataValue()

        if tile_info['tile_mask'] is not None and tile_info['tile_mask'] != "None":
            src_mask_ds = gdal.Open(str(tile_info['tile_mask']))
            src_mask_ds_array = src_mask_ds.ReadAsArray().astype(float)
            src_mask_ds_array_1d = src_mask_ds_array.ravel()
            src_mask_ds_array_band_zero_indices = numpy.where(src_mask_ds_array_1d == 0)[0]
            
        if len(src_ds_array_shape) == 3:
            array_bands = src_ds_array_shape[0]
            array_rows = src_ds_array_shape[1]
            array_cols = src_ds_array_shape[2]
        elif len(src_ds_array_shape) == 2:
            array_rows = src_ds_array_shape[0]
            array_cols = src_ds_array_shape[1]

        n_timeperiods = int(n_bands / input_rasters_bands)
        nodata_mask = numpy.zeros((n_timeperiods, ysize, xsize))

        for raster_band in range(int(input_rasters_bands)):
            zero_indices_master_complete = set
            for time_epoch in numpy.arange(n_timeperiods):
                array_band_number = raster_band + (input_rasters_bands * time_epoch)
                src_ds_array_band = src_ds_array[array_band_number, :, :]
                nodata_mask[time_epoch, :, :] += src_ds_array_band == nodata_value
                src_ds_array_1d = src_ds_array_band.ravel()
                src_ds_array_band_zero_indices = numpy.where(src_ds_array_1d == nodata_value)[0]
                zero_indices_master_complete = zero_indices_master_complete.union(set(src_ds_array_band_zero_indices))

            if tile_info['tile_mask'] is not None and tile_info['tile_mask'] != "None":
                zero_indices_master = zero_indices_master_complete.difference(src_mask_ds_array_band_zero_indices)
            else:
                zero_indices_master = zero_indices_master_complete
                

            zero_indices_master_list = list(zero_indices_master)
            if len(zero_indices_master_list) == 0 : continue

            band_allmonth_1darray_list = []

            for time_epoch in numpy.arange(n_timeperiods):
                array_band_number = raster_band + (input_rasters_bands * time_epoch)
                src_ds_array_band = src_ds_array[array_band_number, :, :]
                src_ds_array_1d = src_ds_array_band.ravel()
                band_allmonth_1darray_list.append(src_ds_array_1d[zero_indices_master_list])

            band_allmonth_1darray = numpy.stack(band_allmonth_1darray_list, axis=0)
            band_allmonth_1darray[band_allmonth_1darray == nodata_value] = NODATA_VALUE
            numpy.apply_along_axis(custom_interpolate_data, 0, band_allmonth_1darray)
            band_allmonth_1darray[band_allmonth_1darray == NODATA_VALUE] = nodata_value

            for time_epoch in numpy.arange(n_timeperiods):
                array_band_number = raster_band + (input_rasters_bands * time_epoch)
                src_ds_array_band = src_ds_array[array_band_number, :, :]
                src_ds_array_1d = src_ds_array_band.ravel()
                src_ds_array_1d[zero_indices_master_list] = band_allmonth_1darray[time_epoch, :]
                src_ds_array[array_band_number, :, :] = src_ds_array_1d.reshape(array_rows, array_cols)

        ulx = tile_info["ulx"]
        uly = tile_info["uly"]
        src_ds_array[src_ds_array == NODATA_VALUE] = nodata_value
        #nodata_mask[nodata_mask > 1] = 1
        save_raster(src_ds_array, tile_info["tile_multiband_interpolated_composite"], "GTiff", int(epsg), ulx, uly,
                    pixel_width, data_type,
                    nodata_value=nodata_value)
        save_raster(nodata_mask, tile_info["tile_multiband_mask"], "GTiff", int(epsg), ulx, uly,
                    pixel_width, GDT_Byte,
                    nodata_value=None)
        log.debug(f"- done interpolating {tile_info['row']}, {tile_info['col']} -")

def generate_multiband_tile(input_data):

    src_raster_filepaths = input_data[0]
    tile_info = input_data[1]


    multiband_raster_filepath = Path(tile_info['tile_multiband_composite'])
    first_raster = src_raster_filepaths[0]
    raster_ds = gdal.Open(str(first_raster))
    nodata_value = raster_ds.GetRasterBand(1).GetNoDataValue()

    tile_composite_filepaths = []
    for composite_filepath in src_raster_filepaths:
        tile_composite_filepaths.append(Path(tile_info['tile_folder']).joinpath(Path(composite_filepath).name))

    if not Path(multiband_raster_filepath).exists():
        args = ["gdal_merge.py",
                "-separate",
                "-o", str(multiband_raster_filepath),
                "-of", "GTiff",
                "-co", "compress=DEFLATE",
                "-a_nodata", f"{nodata_value}",
                "-ul_lr", str(tile_info["ulx"]), str(tile_info["uly"]), str(tile_info["lrx"]), str(tile_info["lry"])]
        args = args + [str(filepath) for filepath in tile_composite_filepaths]
        cmd_output = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        log.debug("exit code {} --> {}".format(cmd_output.returncode, args))

def mosaic_tile_tifs(tile_infos, mosaic_filepath, work_dir, method='average'):
    raster_list = []
    for tile_info in tile_infos:
        if Path(tile_info["tile_multiband_interpolated_composite"]).exists():
            raster_list.append(tile_info["tile_multiband_interpolated_composite"])


    src_ds = gdal.Open(str(raster_list[0]))
    nodata_value = src_ds.GetRasterBand(1).GetNoDataValue()

    mosaic_filename = Path(mosaic_filepath).name
    merge_tiles(raster_list, mosaic_filename, work_dir, method)

def generate_subtile_parallel(input_data):
    first_file = input_data[0]
    second_file = input_data[1]
    mosaic_filepath = input_data[2]
    no_data_value = int(input_data[3])
    mosaic_tifs([first_file, second_file], mosaic_filepath, no_data_value)

def recursive_mosaic(file_list, output_file, work_dir, nodata_value, process_cpu_count = CPU_COUNT):

    work_dir_interpolation = work_dir.joinpath('submosaic')
    os.makedirs(work_dir_interpolation, exist_ok=True)

    """Mosaic files recursively two at a time."""
    if len(file_list) == 1:
        os.rename(file_list[0], output_file)
        return

    temp_outputs = []

    subtasks = []
    # Pair up files and mosaic each pair
    for i in range(0, len(file_list), 2):
        if i + 1 < len(file_list):  # Ensure there's a pair
            temp_output = Path(work_dir_interpolation).joinpath(f"temp_mosaic_{i}.tif")
            if not temp_output.exists():
                args = [file_list[i], file_list[i+1], temp_output, nodata_value]
                subtasks.append(args)
            temp_outputs.append(temp_output)
        else:
            temp_outputs.append(file_list[i])
    if len(subtasks) > 0:
        p = Pool(process_cpu_count)
        p.map(generate_subtile_parallel, tuple(subtasks))

    # Recursively mosaic the temp outputs
    recursive_mosaic(temp_outputs, output_file, work_dir_interpolation, nodata_value, process_cpu_count)

    # Cleanup temporary files
    for temp in temp_outputs:
        os.remove(temp)


def do_recursive_tile_mosaic(tile_infos, mosaic_filepath, work_dir):
    raster_list = []
    for tile_info in tile_infos:
        if Path(tile_info["tile_multiband_interpolated_composite"]).exists():
            raster_list.append(tile_info["tile_multiband_interpolated_composite"])

    src_ds = gdal.Open(str(raster_list[0]))
    nodata_value = src_ds.GetRasterBand(1).GetNoDataValue()

    recursive_mosaic(raster_list, mosaic_filepath, work_dir, nodata_value)


def create_multiband_after_tiling(composite_filepaths, tile_infos, process_cpu_count = CPU_COUNT):

    composite_filepaths = [str(composite_filepath) for composite_filepath in composite_filepaths]

    subtasks = []
    for tile_info in tile_infos:
        tile_multiband_path = Path(tile_info["tile_folder"]).joinpath(tile_info["tile_multiband_composite"])
        if tile_multiband_path.exists(): continue
        args = [composite_filepaths, tile_info]
        subtasks.append(args)

    if len(subtasks) > 0:
        p = Pool(process_cpu_count)
        p.map(generate_multiband_tile, tuple(subtasks))
        p.close()  # Close the pool
        p.join()

def tiled_stats(composite_filepaths, work_dir, stat_list=['min', 'mean', 'max', 'range','std_dev'], tile_size = None):
    if tile_size is None:
        max_size_tile = MAX_TILE_SIZE
    else:
        max_size_tile = tile_size
    (xmin, ymax, xsize, ysize, pixel_width, projection, epsg, data_type, n_bands, _) = read_raster_info(
        composite_filepaths[0])
    tile_infos = setup_tiles(xmin, ymax, xsize, ysize, pixel_width, n_bands, max_size_tile, work_dir)

    stat_tiled_dir = work_dir.joinpath('stat')
    stat_tiled_dir.mkdir(parents=True, exist_ok=True)
    create_tilecomposites(composite_filepaths, tile_infos, process_cpu_count=CPU_COUNT)

    create_multiband_after_tiling(composite_filepaths, tile_infos)

    stat_tiled_dict = {}
    for stat_list_item in stat_list:
        stat_tiled_dict[stat_list_item] = []

    for tile_info in tile_infos:
        log.debug(f"-- tile {tile_info['row']} {tile_info['col']} --")
        tile_workdir = Path(tile_info["tile_folder"])
        tile_multiband_raster = tile_info["tile_multiband_composite"]
        ulx = tile_info["ulx"]
        uly = tile_info["uly"]

        src_ds = gdal.Open(str(tile_multiband_raster), GA_ReadOnly)
        imagery = numpy.zeros((src_ds.RasterCount, tile_info["height"], tile_info["width"]), dtype="float")
        for band_index in range(src_ds.RasterCount):
            band_data = src_ds.GetRasterBand(band_index + 1).ReadAsArray().astype("float")
            nodata_value = src_ds.GetRasterBand(1).GetNoDataValue()
            band_data[band_data == nodata_value] = numpy.nan
            imagery[band_index,:, : ] = band_data

        log.debug(f"collecting stats for {tile_info['row']}_{tile_info['col']}")
        for stat_list_item in stat_list:
            
            if stat_list_item == 'min': 
                ndvi_min_filepath  = tile_workdir.joinpath(f"min_{tile_info['row']}_{tile_info['col']}.tif")
                ndvi_min = numpy.nanmin(imagery, axis=0)
                ndvi_min[ndvi_min == numpy.nan] == NODATA_VALUE
                save_raster(ndvi_min, ndvi_min_filepath, "GTiff", int(epsg), ulx, uly, pixel_width, GDT_Float32,
                            nodata_value=NODATA_VALUE)
                del ndvi_min
                stat_tiled_dict['min'].append(ndvi_min_filepath)
    
            if stat_list_item == 'mean': 
                ndvi_mean_filepath  = tile_workdir.joinpath(f"mean_{tile_info['row']}_{tile_info['col']}.tif")
                ndvi_mean = numpy.nanmean(imagery, axis=0)
                ndvi_mean[ndvi_mean == numpy.nan] == NODATA_VALUE
                save_raster(ndvi_mean, ndvi_mean_filepath, "GTiff", int(epsg), ulx, uly, pixel_width, GDT_Float32,
                            nodata_value=NODATA_VALUE)
                del ndvi_mean
                stat_tiled_dict['mean'].append(ndvi_mean_filepath)
    
            if stat_list_item == 'max':
                ndvi_max_filepath  = tile_workdir.joinpath(f"max_{tile_info['row']}_{tile_info['col']}.tif")
                ndvi_max = numpy.nanmax(imagery, axis=0)
                ndvi_max[ndvi_max == numpy.nan] == NODATA_VALUE
                save_raster(ndvi_max, ndvi_max_filepath, "GTiff", int(epsg), ulx, uly, pixel_width, GDT_Float32,
                            nodata_value=NODATA_VALUE)
                del ndvi_max
                stat_tiled_dict['max'].append(ndvi_max_filepath)
    
            if stat_list_item == 'range':
                ndvi_range_filepath = tile_workdir.joinpath(f"range_{tile_info['row']}_{tile_info['col']}.tif")
                ndvi_max = numpy.nanmax(imagery, axis=0)
                ndvi_min = numpy.nanmin(imagery, axis=0)
                ndvi_range = ndvi_max - ndvi_min
                ndvi_range[ndvi_range == numpy.nan] == NODATA_VALUE
                save_raster(ndvi_range, ndvi_range_filepath, "GTiff", int(epsg), ulx, uly, pixel_width, GDT_Float32,
                            nodata_value=NODATA_VALUE)
                del ndvi_range
                stat_tiled_dict['range'].append(ndvi_range_filepath)
    
            if stat_list_item == 'std_dev':
                ndvi_std_filepath = tile_workdir.joinpath(f"std_{tile_info['row']}_{tile_info['col']}.tif")
                ndvi_stddev = numpy.nanstd(imagery, axis=0)
                ndvi_stddev[ndvi_stddev == numpy.nan] == NODATA_VALUE
                save_raster(ndvi_stddev, ndvi_std_filepath, "GTiff", int(epsg), ulx, uly, pixel_width, GDT_Float32,
                            nodata_value=NODATA_VALUE)
                del ndvi_stddev
                stat_tiled_dict['std_dev'].append(ndvi_std_filepath)

        del imagery

    log.debug(f"mosaicing stat rasters")
    stat_composite_list = []
    for dict_key, raster_list in stat_tiled_dict.items():
        mosaic_path = work_dir.joinpath(f"{dict_key}.tif")
        mosaic_tifs(raster_list, mosaic_path, no_data=NODATA_VALUE)
        stat_composite_list.append(mosaic_path)
    return stat_composite_list

def custom_interpolate_data(data_array):
    try:
        """
        Interpolates the given data using scipy's interp1d and CubicSpline.
        If the missing data is at the first or last position, interp1d is used.
        If the missing data is in between, CubicSpline/RBF interpolation is used.
        """
        data_array[data_array == NODATA_VALUE] = numpy.nan
        # Indices for valid and missing data points
        valid_indices = numpy.where(~numpy.isnan(data_array))[0]
        missing_indices = numpy.where(numpy.isnan(data_array))[0]

        if len(valid_indices) == 1:
            # Finding the non-NaN value
            non_nan_value = data_array[~np.isnan(data_array)][0]
            # Replicating this value across the entire array
            data_array[:] = non_nan_value
        elif len(valid_indices) == 0:
            data_array
        else:
            # Create a copy of the data array for interpolation
            interpolated_data = numpy.copy(data_array)

            # Handle missing data at the beginning or end
            if 0 in missing_indices or (len(data_array) - 1) in missing_indices:
                # Interpolate using linear interpolation
                linear_interp = interp1d(valid_indices, data_array[valid_indices],
                                        kind='linear', fill_value="extrapolate")
                for index in missing_indices:
                    interpolated_data[index] = linear_interp(index)

            if 0 in missing_indices:
                data_array[0] = interpolated_data[0]
            if (len(data_array) - 1) in missing_indices:
                data_array[(len(data_array) - 1)] = interpolated_data[(len(data_array) - 1)]

            # Handle missing data in the middle
            # Create an array of x-coordinates for non-NaN values

            x = numpy.arange(len(data_array))
            y = data_array

            # Remove NaN values for interpolation
            valid_indices_rbf = ~numpy.isnan(y)
            nonvalid_indices_rbf = numpy.isnan(y)
            x_valid = x[valid_indices_rbf]
            y_valid = y[valid_indices_rbf]

            # Perform cubic interpolation
            #cubic_spline = CubicSpline(x_valid, y_valid, bc_type='natural')
            sm = 0.2
            rbf = Rbf(x_valid, y_valid, smooth=sm)

            # Evaluate the interpolated values for all x-coordinates
            #data_pred = cubic_spline(x)
            data_pred = rbf(x)
            data_array[nonvalid_indices_rbf] = data_pred[nonvalid_indices_rbf]
    except Exception as e:
            raise  Exception(f"An error occurred: {e} {data_array} {valid_indices}")

def FitSplineRBF_array(row_array):

    if numpy.sum(row_array != NODATA_VALUE) < 3:
        return

    w = numpy.asarray(row_array == NODATA_VALUE)
    heights = numpy.linspace(1, len(row_array), len(row_array))

    x_col = heights[~w]
    y_col = row_array[~w]
    sm = 0.25
    rbf = Rbf(x_col, y_col, smooth=sm)

    x_excluded = heights[w]
    y_pred = rbf(x_excluded)

    row_array[w] = y_pred


def cut_composite_totile_function(input_data):
    src_filepath = input_data[0]
    tile_extent_path_dict_json = input_data[1]

    tile_infos = json.loads(tile_extent_path_dict_json)

    for tile_name, tile_info in tile_infos.items():
        tile_composite_filepath = Path(tile_info['tile_folder']).joinpath(Path(src_filepath).name)
        if tile_composite_filepath.exists(): continue
        cmd_gdal = ["gdal_translate",
                    "-of", "GTiff",
                    "-co", "COMPRESS=DEFLATE",
                    "-co", "BIGTIFF=YES",
                    "-co", "TILED=YES",
                    "-eco", "-projwin",
                    "{}".format(tile_info['ulx']), "{}".format(tile_info['uly']),
                    "{}".format(tile_info['lrx']), "{}".format(tile_info['lry']),
                    str(src_filepath), str(tile_composite_filepath)]
        cmd_output = subprocess.run(cmd_gdal, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        log.debug(f"exit code {cmd_output.returncode} --> {cmd_gdal}")

        if int(cmd_output.returncode) != 0:
            log.error(f"{cmd_output}")
            if "falls completely outside raster extent" in str(cmd_output.stderr):
                shapely_bbox = raster_bounds_to_polygon(src_filepath)
                (xmin, ymax, RasterXSize, RasterYSize, pixel_width, projection, epsg, datatype, n_bands, imagery_extent_box) = read_raster_info(src_filepath)
                bbox = BoundingBox(tile_info['ulx'], tile_info['uly'], tile_info['lrx'], tile_info['lry'], epsg)
                create_template_raster(bbox, epsg, pixel_width, tile_composite_filepath, input_value=0, num_bands = n_bands)

def create_tilecomposites(raster_list, tile_infos, process_cpu_count = CPU_COUNT, mask_path = None):
    tile_extent_path_dict = {}
    for tile_info in tile_infos:
        if not Path(tile_info["tile_multiband_interpolated_composite"]).exists():
            tile_extent_path_dict[Path(tile_info['tile_folder']).name] = {'ulx': tile_info['ulx'],
                                                                 'uly': tile_info['uly'],
                                                                 'lrx': tile_info['lrx'],
                                                                 'lry': tile_info['lry'],
                                                                 'tile_folder': str(tile_info['tile_folder'])}

    if not len(tile_extent_path_dict.items()) == 0:
        tile_extent_path_dict_json = json.dumps(tile_extent_path_dict)

        subtasks = []
        for raster_list_item in raster_list:
            args = [str(raster_list_item), tile_extent_path_dict_json]
            subtasks.append(args)
        if mask_path is not None:
            arg = [str(mask_path), tile_extent_path_dict_json]
            subtasks.append(arg)

        p = Pool(process_cpu_count)
        p.map(cut_composite_totile_function, tuple(subtasks))
        p.close()  # Close the pool
        p.join()

def  create_interpolated_multiband(tile_infos, process_cpu_count = CPU_COUNT):
    subtasks = []
    for tile_info in tile_infos:
        if Path(tile_info["tile_multiband_interpolated_composite"]).exists(): continue
        args = [tile_info]
        log.debug(f"Adding task - {tile_info['row']} ,  {tile_info['col']}")
        subtasks.append(args)

    if len(subtasks) > 0:
        log.debug(f"Doing interpolating for {len(subtasks)}")
        p = Pool(process_cpu_count)
        p.map(generate_interpolated_multiband_tile, tuple(subtasks))
        p.close()  # Close the pool
        p.join()

def create_tiled_multiband(raster_list, work_dir, process_cpu_count = CPU_COUNT, mask_path = None):

    (xmin, ymax, xsize, ysize, pixel_width, projection, epsg, data_type, n_bands, _) = read_raster_info(raster_list[0])
    tile_infos = setup_tiles(xmin, ymax, xsize, ysize, pixel_width, n_bands,MAX_TILE_SIZE, work_dir, mask_path= mask_path)

    create_tilecomposites(raster_list, tile_infos, process_cpu_count=process_cpu_count, mask_path=mask_path)
    create_multiband_after_tiling(raster_list, tile_infos)
    return tile_infos

def interpolate_rasters(raster_list, work_dir, process_cpu_count = CPU_COUNT, do_recursive_mosaic = False, keep_multiband = True,
                        interpolated_filename = None, mask_path = None):

    tile_infos = create_tiled_multiband(raster_list, work_dir, process_cpu_count, mask_path = mask_path)

    create_interpolated_multiband(tile_infos, process_cpu_count=process_cpu_count)

    if interpolated_filename is not None:
        mosaic_filepath = work_dir.joinpath(interpolated_filename)
    else:
        mosaic_filepath = work_dir.joinpath('interpolate.tif')

    if keep_multiband:
        log.debug(f"Keeping multiband")
        if not mosaic_filepath.exists():
            if not do_recursive_mosaic:
                log.debug("Doing non recursive mosaic")
                mosaic_tile_tifs(tile_infos, mosaic_filepath, work_dir)
            else:
                do_recursive_tile_mosaic(tile_infos, mosaic_filepath, work_dir)
        log.debug(f"--X-- Done creating interpolated multiband tif --X--")
        return [mosaic_filepath]
    else:
        interpolated_list = []

        for raster_index, raster_list_item in enumerate(raster_list):
            merged_result_filepath = work_dir.joinpath(Path(raster_list_item).name)
            merged_vrt_filepath = work_dir.joinpath(Path(raster_list_item).name.replace(".tif", ".vrt"))

            merged_mask_result_filepath = work_dir.joinpath(f"mask_{Path(raster_list_item).name}")
            merged_mask_vrt_filepath = work_dir.joinpath(f"mask_{Path(raster_list_item).name.replace('.tif', '.vrt')}")


            if not merged_result_filepath.exists():
                log.debug("merged vrt filepath:{}".format(merged_vrt_filepath))
                args = ["gdalbuildvrt", "-b", f"{raster_index + 1}", f"{str(merged_vrt_filepath)}"]
                for tile_info in tile_infos:
                    tile_multiband_interpolated_path = tile_info["tile_multiband_interpolated_composite"]
                    args.append(str(tile_multiband_interpolated_path))

                log.debug("agrs:{}".format(args))
                subprocess.check_output(args)

                # Then convert the vrt to a merged GeoTiff file with compression.
                args = ["gdal_translate",
                            "-of", "GTiff",
                            "-co", "TILED=YES",
                            "-co", "COMPRESS=DEFLATE",
                            "-co", "BIGTIFF=YES",
                            str(merged_vrt_filepath),
                            str(merged_result_filepath)]
                subprocess.check_output(args)

            if not merged_mask_result_filepath.exists():
                log.debug("merged mask vrt filepath:{}".format(merged_mask_vrt_filepath))
                args = ["gdalbuildvrt", "-b", f"{raster_index + 1}", f"{str(merged_mask_vrt_filepath)}"]
                for tile_info in tile_infos:
                    tile_multiband_mask = tile_info["tile_multiband_mask"]
                    args.append(str(tile_multiband_mask))

                log.debug("agrs:{}".format(args))
                subprocess.check_output(args)

                # Then convert the vrt to a merged GeoTiff file with compression.
                args = ["gdal_translate",
                            "-of", "GTiff",
                            "-co", "TILED=YES",
                            "-co", "COMPRESS=DEFLATE",
                            "-co", "BIGTIFF=YES",
                            str(merged_mask_vrt_filepath),
                            str(merged_mask_result_filepath)]
                subprocess.check_output(args)

            interpolated_list.append((merged_result_filepath, merged_mask_result_filepath))
        return interpolated_list


def find_min_max(raster_filepath, master_mask=None, tile_size = 2000):

    if master_mask is not None:
        raster1 = gdal.Open(str(raster_filepath), gdal.GA_ReadOnly)
        raster2 = gdal.Open(str(master_mask), gdal.GA_ReadOnly)

        # Check if raster dimensions match
        if raster1.RasterXSize != raster2.RasterXSize or raster1.RasterYSize != raster2.RasterYSize:
            raise ValueError("Rasters have different dimensions.")

    mini = 0
    maxi = 0
    raster_ds = gdal.Open(str(raster_filepath), gdal.GA_ReadOnly)
    # Get the raster band
    raster_band = raster_ds.GetRasterBand(1)
    # Get the NoData value
    nodata_value = raster_band.GetNoDataValue()

    for x in range(0, raster_ds.RasterXSize, tile_size):
        for y in range(0, raster_ds.RasterYSize, tile_size):
            width = min(tile_size, raster_ds.RasterXSize - x)
            height = min(tile_size, raster_ds.RasterYSize - y)

            arr_r1 = raster_ds.GetRasterBand(1).ReadAsArray(x, y, width, height)
            if nodata_value is not None:
                arr_r1 = np.where(arr_r1 == nodata_value, np.nan, arr_r1)

            if master_mask is not None:
                master_chunk = raster2.GetRasterBand(1).ReadAsArray(x, y, width, height)
                arr_r1 = arr_r1[master_chunk==1]

            if numpy.nanmin(arr_r1) < mini:
                mini = numpy.nanmin(arr_r1)
            if numpy.nanmax(arr_r1) > maxi:
                maxi = numpy.nanmax(arr_r1)
    return mini, maxi




