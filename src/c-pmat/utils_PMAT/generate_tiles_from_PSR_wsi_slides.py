### Import libraries ###


import pickle
import os
import multiprocessing as mp


import tqdm
import scipy.io as sio
import numpy as np
import tifffile
import zarr
from PIL import Image

### Import libraries ###



def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill=chr(0x00A3)):#'='): #chr(0x00A3)
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration / total)
    bar = fill * filledLength + '>' + '.' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end="")
    # Print New Line on Complete
    if iteration == total:
        print()


class GEN_TILES(object):
    def __init__(self,
                 input_dir,
                 output_dir,
                 ext,
                 num_processes,
                 exp_dir,
                 objective_power,
                 slide_dimension,
                 rescale,
                 filename,
                 tiles_objective_value,
                 tiles_read_size
                 ):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.ext = ext
        self.num_processes = num_processes
        self.objective_power = objective_power
        self.tiles_read_size = tiles_read_size
        self.rescale = rescale

        if os.path.exists(self.output_dir) is False:
            os.makedirs(self.output_dir)

    def generate_tiles(self, slide_names_name_list, process_num):

        for s_n, slide_name in enumerate(slide_names_name_list):

            print('Process number:{}...Creating patches from slide {}... {}/{}'.format(process_num, slide_name, s_n,
                                                                                       process_num))

            if os.path.exists(
                    os.path.join(self.output_dir, os.path.basename(slide_name))) is False:
                os.mkdir(os.path.join(self.output_dir, os.path.basename(slide_name)))

            img = tifffile.imread(os.path.join(self.input_dir, slide_name), aszarr=True)
            img_data = zarr.open(img, 'r')
            #
            h, w, c = img_data[0].shape
            print(h, w, c)
            k = 0
            #
            PATCH_SIZE = self.tiles_read_size[0]

            img_num = int(np.ceil(h / PATCH_SIZE) * np.ceil(w / PATCH_SIZE))
            ### Image tiling code ###
            for i in range(0, h, 2000):
                for j in range(0, w, 2000):

                    if (j + 2000 > w) and (i + 2000 <h):
                        out = img_data[0][i:i +PATCH_SIZE, j:w]
                    if (i + 2000 > h) and (j + 2000 < w):
                        out = img_data[0][i:h, j:j + PATCH_SIZE]
                    if (i + 2000 > h) and (j + 2000 > w):
                        out = img_data[0][i:h, j:w]
                    if (i + 2000 < h) and (j + 2000 < w):
                        out = img_data[0][i:i + PATCH_SIZE, j:j + PATCH_SIZE]

                    Image.fromarray(out).save(os.path.join(self.output_dir,
                                                           os.path.basename(slide_name),
                                                           f"{'Da'}{k}{'.jpg'}"))

                    k += 1

            printProgressBar(img_num, len(range(0, img_num)), prefix='Progress:',
                             suffix='Completed and created total number of patches = %s' % img_num, length=5)



    # Multi processing by taking into consideration
    # the number of processes.

    def generate_params(self):

        for slide_name in os.listdir(self.input_dir):
            if not slide_name.endswith('.ndpi'):
                continue
            if os.path.exists(
                    os.path.join(self.output_dir, os.path.basename(slide_name))) is False:
                os.mkdir(os.path.join(self.output_dir, os.path.basename(slide_name)))
            params = {}
            img = tifffile.imread(os.path.join(self.input_dir, slide_name), aszarr=True)
            img_data = zarr.open(img, 'r')

            h, w, c = img_data[0].shape

            # Generate thumbnail image
            thumbx, thumby, thumbc = h // 16, w // 16, c

            # print(thumbx, thumby)
            thumb = img_data[4][0:thumbx, 0:thumby, :]

            print(thumb.shape)
            Image.fromarray(thumb).save(os.path.join(self.output_dir, os.path.basename(slide_name),
                                                     os.path.basename(slide_name) +
                                                     '_thumbnail.jpg'))

            with tifffile.TiffFile(os.path.join(self.input_dir, slide_name)) as f:
                XRES = f.pages[0].tags['XResolution'].value
                YRES = f.pages[0].tags['YResolution'].value
                RESUNIT = f.pages[0].tags['ResolutionUnit'].value

            h, w, c = img_data[0].shape
            dimension_y, dimension_x, dim_c = w, h, c
            params['slide_dimension'] = (dimension_y, dimension_x)
            params['exp_dir'] = os.path.join(self.output_dir, slide_name)
            params['filename'] = slide_name
            params['XRES'] = XRES
            params['YRES'] = YRES
            params['RESUNIT'] = RESUNIT
            params['rescale'] = self.rescale
            params['tiles_read_size'] = self.tiles_read_size
            with open(os.path.join(self.output_dir, os.path.basename(slide_name), 'param.p'),
                      'wb') as file:
                pickle.dump(params, file)
                sio.savemat(os.path.join(self.output_dir, os.path.basename(slide_name),
                                         'param.mat'), params)

    def apply_multiprocessing(self):
        l = [fname for fname in os.listdir(self.input_dir) if fname.endswith(self.ext) is True]
        n = len(l)
        num_elem_per_process = int(np.ceil(n / int(self.num_processes)))

        file_names_list_list = []

        for i in range(int(self.num_processes)):
            start_ = i * num_elem_per_process
            x = l[start_: start_ + num_elem_per_process]
            file_names_list_list.append(x)

        print('{} processes created.'.format(int(self.num_processes)))
        # create list of processes
        processes = [
            mp.Process(target=self.generate_tiles, args=(file_names_list_list[process_num], process_num)) for
            process_num in range(int(self.num_processes))]

        # Run processes
        for p in processes:
            p.start()

            printProgressBar(0, int(self.num_processes), prefix='Progress:', suffix="Complete\n", length=1)

        # Exit the completed processes
        for p in processes:
            p.join()
        print('All Processes finished!!!')

    def run(self):

        if int(self.num_processes) == 1:
            file_names_list = [fname for fname in os.listdir(self.input_dir) if fname.endswith(self.ext) is True]
            self.generate_tiles(file_names_list, 1)
        else:
            self.apply_multiprocessing()


def parse_options(opts_in):
    # params = opts_in
    params_keys = {'slides': 'input_dir', 'patches': 'output_dir', 'ext': 'ext', 'nump': 'num_processes'}

    params = {params_keys[key]: value for key, value in opts_in.items()}

    params.update({'exp_dir': '', 'objective_power': 20, 'slide_dimension': [],
                   'rescale': 1, 'filename': [], 'tiles_objective_value': 20,
                   'tiles_read_size': (2000, 2000)})

    print(params)

    obj = GEN_TILES(**params)
    obj.run()
    obj.generate_params()


def perform_tiling(slide_directory, output_directory, extension, num_processes):
      """Perform tile extraction given a directory of slides, an output directory,
      extension of the slides, and the number of the processes to be used for tiling.

      Parameters
      ----------
      slide_directory : Path
        Path to the slides directory
      output_directory : Path
        Path to the patches saved in corresponding slide directory
      extension : {'.ndpi', '.svs', '.qptiff', '.mrxs', '.tif', '.tiff', '.scn'}
        Type of the slide or custom scanner extension
      num_processes : int
        Number of process needed to run on the CPU

      Returns
      -------
      None
      """
      params_keys = {'input_dir': slide_directory,
                     'output_dir': output_directory,
                     'ext':extension,
                     'num_processes': num_processes}

      params_keys.update({'exp_dir': '', 'objective_power': 20, 'slide_dimension': [],
                       'rescale':1, 'filename': [], 'tiles_objective_value': 20,
                        'tiles_read_size': (2000, 2000)})


      obj = GEN_TILES(**params_keys)
      obj.run()
      obj.generate_params()


# slides = r'D:\Projects\HE_Int_ts_cc\Sarcoma\Well_Diff\slides\new_slides'
# output = r'D:\Projects\HE_Int_ts_cc\Sarcoma\Well_Diff\tiles'
#
# #perform_tiling('./slides', './output', '.ndpi', 1)
# perform_tiling(slides, output, '.ndpi', 1)

