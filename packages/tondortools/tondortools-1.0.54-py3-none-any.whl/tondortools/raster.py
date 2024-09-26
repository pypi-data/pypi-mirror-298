import numpy
import shutil
from pathlib import Path
import subprocess
import logging
import numpy as np
import os

from .tool import read_raster_info, save_raster, mosaic_tifs, run_subprocess
import osgeo.gdalconst as gdalconst

from .tool import setup_tiles, save_raster_template, find_file_in_archives, clip_raster_to_extent, reproject_multibandraster_toextent, read_raster_info, raster2array
from .tool import merge_tiles
from .geo import BoundingBox
from .logging_config import init_logging, get_console_handler

from osgeo import gdal
from osgeo.gdalconst import GA_ReadOnly, GDT_Float32, GDT_Byte, GDT_Int16
from scipy.ndimage import binary_erosion

MAX_TILE_SIZE = 4000

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.addHandler(get_console_handler()) 
log.propagate = False

def reclassify_subtiles(master_lc_mask, tile_infos, epsg, nodata_value):
    dataset = gdal.Open(str(master_lc_mask), GA_ReadOnly)
    for tile_info in tile_infos:
        start_x = tile_info["x_offset"]
        start_y = tile_info["y_offset"]
        read_width = tile_info["width"]
        read_height = tile_info["height"]
        ulx = tile_info["ulx"]
        uly = tile_info["uly"]

        # Read the chunk from the raster
        chunk = dataset.ReadAsArray(start_x, start_y, read_width, read_height)
        chunk_mask = numpy.ones_like(chunk)
        chunk_mask[chunk==nodata_value] = 0

        save_raster(chunk_mask, tile_info["tile_multiband_interpolated_composite"], "GTiff", int(epsg),
                    ulx, uly,
                    tile_info["pixel_size"], data_type=GDT_Int16)




def reclassify_raster(master_lc_mask, relcassified_path, work_dir):

    raster_ds = gdal.Open(str(master_lc_mask))
    raster_nodata = raster_ds.GetRasterBand(1).GetNoDataValue()

    (xmin, ymax, xsize, ysize, pixel_width, projection, epsg, data_type, n_bands, _) = read_raster_info(master_lc_mask)
    tile_infos = setup_tiles(xmin, ymax, xsize, ysize, pixel_width, n_bands,MAX_TILE_SIZE, work_dir)

    reclassify_subtiles(master_lc_mask, tile_infos, epsg, raster_nodata)
    raster_list = []
    for tile_info in tile_infos:
        raster_list.append(tile_info["tile_multiband_interpolated_composite"])

    print(f"Mosaic patches for {relcassified_path}")
    mosaic_tifs(raster_list, Path(relcassified_path))

def create_sieved_raster(input_raster, output_raster, sieve=8, diagonal_flag = True):
    (xmin, ymax, xsize, ysize, pixel_width, projection, epsg, data_type, n_bands, _) = read_raster_info(input_raster)

    if diagonal_flag: diag_num = "-8"
    else: diag_num = "-4"
    sieve_args = ["gdal_sieve.py", #"-mask", str(mask_tif),
                  diag_num, "-nomask",
                  "-st", str(sieve),
                  str(input_raster), str(output_raster)]
    cmd_output = subprocess.run(sieve_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    log.debug("exit code {} --> {}".format(cmd_output.returncode, sieve_args))

def perform_binary_erosion(input_raster, output_raster,dilate_iterations=3, invert=False):
    (xmin, ymax, xsize, ysize, pixel_width, projection, epsg, data_type, n_bands, _) = read_raster_info(input_raster)

    ds_raster = gdal.Open(str(input_raster))
    raster_array = ds_raster.GetRasterBand(1).ReadAsArray()
    if invert:
        raster_array = numpy.logical_not(raster_array).astype(int)

    raster_nodata = ds_raster.GetRasterBand(1).GetNoDataValue()
    dilated_array = binary_erosion(raster_array, iterations=dilate_iterations, border_value=1).astype(
        raster_array.dtype)
    if invert:
        dilated_array = numpy.logical_not(dilated_array).astype(int)

    save_raster_template(input_raster, output_raster, dilated_array, GDT_Byte, raster_nodata)



def do_bioregion_mosaic(mosaic_path, bioregion_tiles, year, archive_roots, work_dir, pca_dimension=12):

    if not mosaic_path.exists():
        mosaic_input_list = []
        for bioregion_tilename, site_selection in bioregion_tiles.items():

            tile_stacked_filename = f"OPT_{bioregion_tilename}_{year}_{pca_dimension}.tif"
            opt_composite_site_relpath = Path(str(year)).joinpath(bioregion_tilename, 'interpolated_optcomposite', tile_stacked_filename)
            interpolated_raster = find_file_in_archives(opt_composite_site_relpath, archive_roots, error_on_missing=False)

            work_dir_tile = work_dir.joinpath(tile_stacked_filename)
            if not work_dir_tile.exists():
                if interpolated_raster is None:

                    # first look for dim 12 month
                    tile_fullstacked_filename = f"OPT_{bioregion_tilename}_{year}_12.tif"
                    opt_composite_site_relpath = Path(str(year)).joinpath(bioregion_tilename, 'interpolated_optcomposite',
                                                                          tile_fullstacked_filename)
                    interpolated_fulldim_raster = find_file_in_archives(opt_composite_site_relpath, archive_roots,
                                                                error_on_missing=False)
                    # if dim 12 month then do interpolation of stacked 4 month
                    if interpolated_fulldim_raster is None:
                        interpolated_raster_input_list = []
                        opt_raster_list = locate_tile_optcomposites(bioregion_tilename, year, archive_roots)
                        for opt_raster_list_index, opt_raster_list_item in enumerate(opt_raster_list):
                            if site_selection['selection'][opt_raster_list_index] == '1':
                                interpolated_raster_input_list.append(opt_raster_list_item)
                        log.debug(f"creating interpolated stack from {interpolated_raster_input_list}")
                        interpolate_rasters(interpolated_raster_input_list, work_dir_tile.parent,
                                                                                5, False, True, interpolated_filename=tile_stacked_filename)
                    else:
                        band_selection_list = []
                        site_selection_string = site_selection['selection']
                        interpolated_fulldim_raster_ds = gdal.Open(str(interpolated_fulldim_raster))
                        interpolated_fulldim_raster_bandcount = interpolated_fulldim_raster_ds.RasterCount
                        n_band = interpolated_fulldim_raster_bandcount/len(site_selection_string)
                        for site_selection_string_index, site_selection_string_item in enumerate(site_selection_string):
                            band_1stindex_array = np.arange(6)
                            if site_selection_string_item == '1':
                                band_nthindex_array = band_1stindex_array + (site_selection_string_index*n_band) + 1
                                band_selection_list.extend(list(band_nthindex_array))
                                log.debug(f"adding stack list {band_nthindex_array}")
                        log.debug(f"Calculated stacked raster with {band_selection_list}")

                        tile_vrt_filepath = work_dir.joinpath(tile_stacked_filename.replace('.tif', '.vrt'))

                        vrt_stack = []
                        for band_selection_list_item in band_selection_list:
                            tile_vrt_band_filepath = work_dir.joinpath(tile_stacked_filename.replace('.tif', f'band{band_selection_list_item}.vrt'))
                            gdalbuildvrt_cmd = ["gdalbuildvrt",
                                                "-b", str(band_selection_list_item),
                                                str(tile_vrt_band_filepath), str(interpolated_fulldim_raster)]
                            cmd_output = subprocess.run(gdalbuildvrt_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                            vrt_stack.append(tile_vrt_band_filepath)

                        args = ["gdalbuildvrt", "-separate", str(tile_vrt_filepath)]
                        for vrt_stack_item in vrt_stack:
                            args.append(vrt_stack_item)
                        subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                        cmd_output = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        log.debug(f"exit code {cmd_output.returncode} --> {args}")

                        args = ["gdal_translate",
                                "-of", "GTiff",
                                "-co", "TILED=YES",
                                "-co", "COMPRESS=DEFLATE",
                                "-co", "BIGTIFF=YES",
                                str(tile_vrt_filepath),
                                str(work_dir_tile)]
                        cmd_output = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        log.debug(f"exit code {cmd_output.returncode} --> {args}")

                else:
                    shutil.copy(interpolated_raster, work_dir_tile)
                    log.debug(f"{interpolated_raster} --> {work_dir_tile}")

            interpolated_raster_filepath_list = [work_dir_tile]
            mosaic_input_list.extend([str(interpolated_raster_item) for interpolated_raster_item in interpolated_raster_filepath_list])

        merge_tiles(mosaic_input_list, mosaic_path.name, mosaic_path.parent, method='average')
    return mosaic_path


def normalize_stacked_raster(stacked_raster, normalized_raster, number_of_bands):
    pass

def compress_lzw(input_file, output_file):
    args = [
        'gdal_translate',
        "-co", "TILED=YES",
        "-co", "COMPRESS=LZW",
        "-co", "BIGTIFF=YES",
        str(input_file),
        str(output_file)
    ]
    cmd_output = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    log.debug(f"exit code {cmd_output.returncode} --> {args}")


class Raster_tiling():
    def __init__(self):
        self.bbox = None
        self.rasterxsize = None
        
    def set_clip_extent(self, xmin, xmax, ymin, ymax, epsg):
        self.bbox = BoundingBox(xmin, ymin, xmax, ymax, epsg)
        return self.bbox
    
    def set_bbox(self, bbox):
        self.bbox = bbox
    
    def check_clipped_raster(self, dst_filepath):
        (xmin, ymax, RasterXSize, RasterYSize, pixel_width, projection, epsg, datatype, n_bands, imagery_extent_box) = read_raster_info(dst_filepath)
        if self.rasterxsize is None:
            self.rasterxsize = RasterXSize
            self.rasterysize = RasterYSize
            self.xmin = xmin
            self.ymax = ymax
            self.pixel_width = pixel_width
            self.epsg = epsg
        else:

            assert self.xmin == xmin
            assert self.ymax == ymax
            assert self.epsg == epsg
            
            pixel_factor = np.divide(self.pixel_width, pixel_width)
            assert self.rasterxsize*pixel_factor == RasterXSize
            assert self.rasterysize*pixel_factor == RasterYSize
            
    def clip_sen_tif_to_extent(self, src_filepath, dst_filepath, create_new = False):
        if not dst_filepath.exists() or create_new:
            clip_raster_to_extent(src_filepath, dst_filepath, self.bbox.xmin, self.bbox.xmax, self.bbox.ymin, self.bbox.ymax)
        self.check_clipped_raster(dst_filepath)

    def warp_sen_tif_to_extent(self, src_filepath, dst_filepath, pixel_width, method='near', create_new = False):
        if not dst_filepath.exists() or create_new:
            reproject_multibandraster_toextent(src_filepath, dst_filepath, self.bbox.epsg, pixel_width, self.bbox.xmin, self.bbox.xmax, self.bbox.ymin, self.bbox.ymax, method=method)
        self.check_clipped_raster(dst_filepath)

    def set_raster_params(self, raster_path):
        (xmin, ymax, RasterXSize, RasterYSize, pixel_width, projection, epsg, datatype, n_bands, imagery_extent_box) = read_raster_info(dst_filepath)
        if self.rasterxsize is None:
            self.rasterxsize = RasterXSize
            self.rasterysize = RasterYSize
            self.xmin = xmin
            self.ymax = ymax
            self.pixel_width = pixel_width
            self.epsg = epsg
            
    def rasterize_gpkg(self):
        pass
        
            
def create_individule_tifs_from_bands(tif_path, band_list, work_dir):
    band_tifpath_dict = {}
    for band in band_list:
        
        band_tif_filename = f'{Path(tif_path).stem}_band_{band}.tif'
        band_tif_filepath = Path(work_dir).joinpath(band_tif_filename)
        if not band_tif_filepath.exists():
            
            vrt_file_basename = f'{Path(tif_path).stem}_band_{band}.vrt'
            vrt_filepath = Path(work_dir).joinpath(vrt_file_basename)
            gdalbuildvrt_cmd = ["gdalbuildvrt",
                                "-b", str(band),
                                str(vrt_filepath), tif_path]
            run_subprocess(gdalbuildvrt_cmd, work_dir)
    
    
    
            translate_to_tif = ["gdal_translate",
                                "-of", "GTiff", str(vrt_filepath), str(band_tif_filepath)]
            run_subprocess(translate_to_tif, work_dir)

        band_tifpath_dict[int(band)] = band_tif_filepath
    return band_tifpath_dict   


def set_nodata_value(raster_path, nodata_value):
    """
    Set the NoData value for a given raster.

    Parameters:
    raster_path (str): The file path to the raster.
    nodata_value (numeric): The value to set as NoData.
    """
    # Open the raster file in update mode
    dataset = gdal.Open(str(raster_path), gdal.GA_Update)

    if dataset is None:
        raise FileNotFoundError(f"Raster file not found: {raster_path}")

    try:
        # Loop through all bands in the raster and set the NoData value
        for i in range(1, dataset.RasterCount + 1):
            band = dataset.GetRasterBand(i)
            band.SetNoDataValue(nodata_value)
            band.FlushCache()  # Write changes to disk
    finally:
        # Properly close the dataset to flush all data and avoid data corruption
        dataset = None

    log.debug(f"NoData value set to {nodata_value} for all bands in {raster_path}")
    
def read_raster_to_table(input_raster):
    dataset = gdal.Open(str(input_raster))
    bands = [dataset.GetRasterBand(i + 1).ReadAsArray() for i in range(dataset.RasterCount)]
    rows, cols = bands[0].shape
    data = np.array([band.flatten() for band in bands]).T
    return data, rows, cols


def extract_band(input_raster_path, band_number, output_raster_path = None):
    dataset = gdal.Open(str(input_raster_path))
    band = dataset.GetRasterBand(band_number)
    band_data = band.ReadAsArray()

    driver = gdal.GetDriverByName('GTiff')

    # Temporary output path
    temp_output_path = str(input_raster_path) + '.temp.tif'

    output_dataset = driver.Create(temp_output_path, band.XSize, band.YSize, 1, band.DataType)
    output_dataset.SetGeoTransform(dataset.GetGeoTransform())
    output_dataset.SetProjection(dataset.GetProjection())
    output_dataset.GetRasterBand(1).WriteArray(band_data)
    output_dataset.FlushCache()

    if output_raster_path is None:
        # Replace the original file
        os.remove(input_raster_path)
        os.rename(temp_output_path, input_raster_path)
    else:
        os.rename(temp_output_path, output_raster_path)


def sieve_multiclass_tif(input_raster, work_dir, output_raster = None, sieve_size = 7, diagonal_flag = False, background_value = 0):
    
    (xmin, ymax, RasterXSize, RasterYSize, pixel_width, projection, epsg, datatype, n_bands,
     imagery_extent_box) = read_raster_info(input_raster)
    # Get the data type of the band
    data_type_name = gdal.GetDataTypeName(datatype)
    # Now, get the constant from gdalconst
    data_type = getattr(gdalconst, 'GDT_' + data_type_name)
        
    rasterarray = raster2array(input_raster)
    rasterarray[np.isnan(rasterarray)] = background_value
    array_mask = np.zeros_like(rasterarray)
    array_mask[rasterarray != background_value] = 1
    array_mask[rasterarray == background_value] = 2
    array_mask_path = work_dir.joinpath(f"{input_raster.stem}_mask.tif")
    array_mask_sieved_path = work_dir.joinpath(f"{input_raster.stem}_sieved_mask.tif")
    save_raster_template(input_raster, array_mask_path, array_mask, data_type=GDT_Int16, nodata_value=0)

    # Use gdal_sieve.py to remove small patches based on the temporary mask
    create_sieved_raster(array_mask_path, array_mask_sieved_path, sieve=sieve_size, diagonal_flag=diagonal_flag)

    mask_array = raster2array(str(array_mask_sieved_path))
    rasterarray[mask_array != 1] = 0
    save_raster_template(str(input_raster), str(output_raster), rasterarray, data_type, nodata_value=background_value)
    log.debug(f"saved sieved raster to {str(output_raster)}")


def burn_first_digit(input_raster, output_raster):
    # Open the existing raster
    dataset = gdal.Open(str(input_raster), gdal.GA_ReadOnly)

    # Get raster band
    band = dataset.GetRasterBand(1)

    # Read raster data as array
    data = band.ReadAsArray()

    # Nodata value
    nodata = KULT_NO_DATAVALUE

    # Process the data to take only the first digit
    new_data = np.where(data == nodata, nodata, data // 10)

    # Create a new raster
    driver = gdal.GetDriverByName('GTiff')
    out_dataset = driver.Create(str(output_raster), dataset.RasterXSize, dataset.RasterYSize, 1, band.DataType)
    out_band = out_dataset.GetRasterBand(1)

    # Set geotransform and projection from the original data
    out_dataset.SetGeoTransform(dataset.GetGeoTransform())
    out_dataset.SetProjection(dataset.GetProjection())

    # Write the processed data to the new raster
    out_band.WriteArray(new_data)
    out_band.SetNoDataValue(nodata)
    out_band.FlushCache()

    # Close datasets
    out_dataset = None
    dataset = None

def vectorize_raster(raster_path, work_dir, field_name="class"):
    output_shp_path = Path(work_dir).joinpath(f"{raster_path.stem}.shp")
    output_gpkg_path = Path(work_dir).joinpath(f"{raster_path.stem}.gpkg")

    # Step 1: Use gdal_polygonize.py to convert raster to polygons (Shapefile)
    cmd_gdal = ['gdal_polygonize.py',
                str(raster_path),
                '-f', 'ESRI Shapefile',
                str(output_shp_path),
                'output_polygons',
                field_name]

    cmd_output = subprocess.run(cmd_gdal, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    log.debug("exit code {} --> {}".format(cmd_output.returncode, cmd_gdal))

    # Step 2: Use ogr2ogr to convert Shapefile to GeoPackage
    cmd_gdal = ['ogr2ogr',
                '-f', 'GPKG',
                str(output_gpkg_path),
                str(output_shp_path)]
    cmd_output = subprocess.run(cmd_gdal, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    log.debug("exit code {} --> {}".format(cmd_output.returncode, cmd_gdal))
    return output_gpkg_path