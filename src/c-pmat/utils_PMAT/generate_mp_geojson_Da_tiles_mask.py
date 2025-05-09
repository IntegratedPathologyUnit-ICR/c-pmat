import os
import re
import pickle
import multiprocessing as mp
import numpy as np
import tifffile
import zarr
from PIL import Image
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon
import rasterio
from rasterio import features
from skimage.transform import resize
import cv2


def natural_key(string_):
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill=chr(0x00A3)):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration / total)
    bar = fill * filledLength + '>' + '.' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end="")
    if iteration == total:
        print()


class SAVE_ANNOTATED_TILES(object):
    def __init__(self,
                 slide_directory,
                 geojson_directory,
                 output_directory,
                 extension,
                 num_processes,
                 tile_size=2000):
        self.slide_directory = slide_directory
        self.geojson_directory = geojson_directory
        self.output_directory = output_directory
        self.extension = extension
        self.num_processes = num_processes
        self.tile_size = tile_size

        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

        # Create a directory for mask tiles
        self.mask_directory = os.path.join(self.output_directory, "mask_tiles")
        if not os.path.exists(self.mask_directory):
            os.makedirs(self.mask_directory)

    def create_mask_from_geojson(self, slide_name, slide_dimension):
        """Create a mask from GeoJSON annotation for a given slide"""
        h, w = int(slide_dimension[1]), int(slide_dimension[0])
        mask = np.zeros((h, w), dtype=np.uint8)

        geojson_path = os.path.join(self.geojson_directory,
                                    os.path.splitext(slide_name)[0] + '.geojson')

        if not os.path.exists(geojson_path):
            print(f"Warning: No GeoJSON found for {slide_name}. Skipping.")
            return None

        # Load the GeoJSON file
        try:
            annotations = gpd.read_file(geojson_path)

            # Rasterize all geometries into the mask
            for idx, geom in enumerate(annotations.geometry):
                if isinstance(geom, Polygon):
                    features.rasterize([(geom, 1)], out=mask, out_shape=mask.shape,
                                       merge_alg=rasterio.enums.MergeAlg.add)
                elif isinstance(geom, MultiPolygon):
                    for poly in geom.geoms:
                        features.rasterize([(poly, 1)], out=mask, out_shape=mask.shape,
                                           merge_alg=rasterio.enums.MergeAlg.add)

            return mask

        except Exception as e:
            print(f"Error processing GeoJSON for {slide_name}: {e}")
            return None

    def process_slide(self, slide_name, process_num):
        """Process a single slide to extract annotated tiles"""
        print(f'Process {process_num}: Processing slide {slide_name}')

        slide_output_dir = os.path.join(self.output_directory,
                                        os.path.basename(slide_name))

        if not os.path.exists(slide_output_dir):
            os.makedirs(slide_output_dir)

        # Create slide-specific mask subdirectory
        slide_mask_dir = os.path.join(self.mask_directory,
                                      os.path.basename(slide_name))
        if not os.path.exists(slide_mask_dir):
            os.makedirs(slide_mask_dir)

        # Open the slide
        try:
            img = tifffile.imread(os.path.join(self.slide_directory, slide_name), aszarr=True)
            img_data = zarr.open(img, 'r')

            # Get slide dimensions
            h, w, c = img_data[0].shape
            print(f"Slide dimensions: {h} x {w} x {c}")

            # Create parameter dictionary for the slide
            params = {}
            params['slide_dimension'] = (w, h)
            params['filename'] = slide_name
            params['rescale'] = 1
            params['tiles_read_size'] = (self.tile_size, self.tile_size)

            # Get resolution information if available
            try:
                with tifffile.TiffFile(os.path.join(self.slide_directory, slide_name)) as f:
                    params['XRES'] = f.pages[0].tags['XResolution'].value
                    params['YRES'] = f.pages[0].tags['YResolution'].value
                    params['RESUNIT'] = f.pages[0].tags['ResolutionUnit'].value
            except:
                print(f"Warning: Could not read resolution info for {slide_name}")
                params['XRES'] = (1, 1)
                params['YRES'] = (1, 1)
                params['RESUNIT'] = 1

            # Create mask from GeoJSON
            mask = self.create_mask_from_geojson(slide_name, (w, h))
            if mask is None:
                print(f"Warning: Failed to create mask for {slide_name}. Skipping.")
                return

            # Generate and save tiles
            k = 0
            tiles_saved = 0
            total_tiles = int(np.ceil(h / self.tile_size) * np.ceil(w / self.tile_size))

            for i in range(0, h, self.tile_size):
                for j in range(0, w, self.tile_size):
                    # Determine the tile dimensions (handle edge cases)
                    if (j + self.tile_size > w) and (i + self.tile_size < h):
                        tile = img_data[0][i:i + self.tile_size, j:w]
                        mask_tile = mask[i:i + self.tile_size, j:w]
                    elif (i + self.tile_size > h) and (j + self.tile_size < w):
                        tile = img_data[0][i:h, j:j + self.tile_size]
                        mask_tile = mask[i:h, j:j + self.tile_size]
                    elif (i + self.tile_size > h) and (j + self.tile_size > w):
                        tile = img_data[0][i:h, j:w]
                        mask_tile = mask[i:h, j:w]
                    else:
                        tile = img_data[0][i:i + self.tile_size, j:j + self.tile_size]
                        mask_tile = mask[i:i + self.tile_size, j:j + self.tile_size]

                    # Check if any part of this tile is annotated
                    if np.any(mask_tile > 0):
                        # Generate filenames for both image and mask tiles
                        base_filename = f"Da{k}"#_{os.path.basename(slide_name).replace(self.extension, '')}-{i}-{j}"
                        image_filename = f"{base_filename}.jpg"
                        mask_filename = f"{base_filename}.png"#_mask If you need different name then keep '_mask' as suffix

                        # Save image tile
                        Image.fromarray(tile).save(os.path.join(slide_output_dir, image_filename))

                        # Save high-resolution mask tile
                        # Convert mask tile to binary (0 or 255) for better visualization
                        mask_tile_binary = (mask_tile > 0).astype(np.uint8) * 255

                        # Save mask tile
                        Image.fromarray(mask_tile_binary).save(os.path.join(slide_mask_dir, mask_filename))

                        tiles_saved += 1

                    k += 1

                    if k % 100 == 0:
                        printProgressBar(k, total_tiles, prefix='Progress:',
                                         suffix=f'Processed {k}/{total_tiles} tiles, saved {tiles_saved}', length=50)

            # Save parameters for future reference
            with open(os.path.join(slide_output_dir, 'param.p'), 'wb') as file:
                pickle.dump(params, file)

            print(f"\nCompleted slide {slide_name}. Total tiles saved: {tiles_saved}/{total_tiles}")

        except Exception as e:
            print(f"Error processing slide {slide_name}: {e}")
            import traceback
            traceback.print_exc()

    def apply_multiprocessing(self):
        """Apply multiprocessing to process multiple slides in parallel"""
        slides = [fname for fname in os.listdir(self.slide_directory)
                  if fname.endswith(self.extension)]

        if not slides:
            print(f"No slides found with extension {self.extension} in {self.slide_directory}")
            return

        n = len(slides)
        num_elem_per_process = int(np.ceil(n / int(self.num_processes)))

        file_names_list_list = []
        for i in range(int(self.num_processes)):
            start_ = i * num_elem_per_process
            x = slides[start_: start_ + num_elem_per_process]
            file_names_list_list.append(x)

        print(f'{int(self.num_processes)} processes created.')

        # Create list of processes
        processes = [
            mp.Process(target=self.process_slides, args=(file_names_list_list[process_num], process_num))
            for process_num in range(len(file_names_list_list))]

        # Run processes
        for p in processes:
            p.start()

        printProgressBar(0, len(processes), prefix='Processes:', suffix="Started", length=50)

        # Exit the completed processes
        for p_idx, p in enumerate(processes):
            p.join()
            printProgressBar(p_idx + 1, len(processes), prefix='Processes:', suffix="Completed", length=50)

        print('All Processes finished!')

    def process_slides(self, slide_names_list, process_num):
        """Process a list of slides (called by multiprocessing)"""
        for s_n, slide_name in enumerate(slide_names_list):
            self.process_slide(slide_name, process_num)

    def run(self):
        """Main run method"""
        if int(self.num_processes) == 1:
            slides = [fname for fname in os.listdir(self.slide_directory)
                      if fname.endswith(self.extension)]

            if not slides:
                print(f"No slides found with extension {self.extension} in {self.slide_directory}")
                return

            for slide_name in slides:
                self.process_slide(slide_name, 1)
        else:
            self.apply_multiprocessing()


def save_annotated_tiles(slide_directory, geojson_directory, output_directory, extension, num_processes=1,
                         tile_size=2000):
    """
    Save only the tiles that fall within GeoJSON annotations, along with corresponding mask tiles.

    Parameters
    ----------
    slide_directory : str
        Path to the slides directory
    geojson_directory : str
        Path to the directory containing GeoJSON annotations
    output_directory : str
        Path where the annotated tiles will be saved
    extension : str
        File extension of the slides (e.g., '.ndpi', '.qptiff')
    num_processes : int
        Number of processes for parallel processing
    tile_size : int
        Size of the tiles (default: 2000)

    Returns
    -------
    None

    Notes
    -----
    The function will create two directories:
    - output_directory/: Contains the image tiles from annotated regions
    - output_directory/mask_tiles/: Contains the corresponding binary masks
    """
    processor = SAVE_ANNOTATED_TILES(
        slide_directory=slide_directory,
        geojson_directory=geojson_directory,
        output_directory=output_directory,
        extension=extension,
        num_processes=num_processes,
        tile_size=tile_size
    )
    processor.run()


if __name__ == "__main__":
    # Example usage:
    save_annotated_tiles(
        slide_directory=r"R:\TRIALS IHC-mIF images\IHC images\Asteroid\KI67\Ki67 2025",
        geojson_directory=r"R:\TRIALS IHC-mIF images\IHC images\Asteroid\KI67\Analysis Ki67\Annotations_by_case\2025 new cases\Annotations full slide",
        output_directory=r"R:\TRIALS IHC-mIF images\IHC images\Asteroid\KI67\Analysis Ki67\Annotated_da_tiles_with_mask",
        extension=".ndpi",
        num_processes=4,  # Using 4 processes for parallel execution
        tile_size=2000
    )