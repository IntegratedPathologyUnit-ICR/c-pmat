import os
from skimage import io
import tifffile
from tifffile import TiffWriter
import re
import numpy as np

def natural_key(string_):

    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]

def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='='): #chr(0x00A3)
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration / total)
    bar = fill * filledLength + '>' + '.' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end="")
    # Print New Line on Complete
    if iteration == total:
        print('\n')



annotated_dir_i = r'R:\Computational Team\analysisVisualisation\stitching\tiles'
stitch_dir = r'test_stitch'
divisor_w = 1
cws_h = 2000
cws_w =2000
slide_h = 4000
slide_w = 18000
PATCH_SIZE = 2000

img_all = np.zeros((4000, 18000, 3)).astype(np.uint8)

print(img_all.shape, img_all.dtype)


images = sorted([fname for fname in os.listdir(annotated_dir_i) if
                 fname.startswith('tiles') and fname.endswith('.tif') is True], key=natural_key)
print(len(images))
printProgressBar(0, len(images), prefix='Progress:', suffix='Complete', length=50)
cnt = 0


for i in range(0, slide_h, 2000):
    for j in range(0, slide_w, 2000):
        #print(cnt)
        img = io.imread(os.path.join(annotated_dir_i, images[cnt]))

        if (j + 2000 > slide_w):
            img_all[i: i + PATCH_SIZE, j: slide_w, :] = img
            #print(i + PATCH_SIZE, cnt)
        if (i + 2000 >= slide_h) and (j + 2000 <= slide_w):
            img_all[i: slide_h, j: j + PATCH_SIZE, :] = img
            #print(j, j + PATCH_SIZE, cnt)
        if (i + 2000 <= slide_h) and (j + 2000 <= slide_w):
            img_all[i: i + PATCH_SIZE, j: j + PATCH_SIZE, :] = img
            print(i + PATCH_SIZE, j+PATCH_SIZE, cnt)



        cnt+=1



        options = dict(
                photometric=tifffile.TIFF.PHOTOMETRIC.RGB,
                tile=(256, 256),
                compression=tifffile.TIFF.COMPRESSION.LZW,
                metadata=None)
with TiffWriter(os.path.join(stitch_dir, 'BH45' + '_basemag_18.tif'), bigtiff=True) as tif:
    tif.write(img_all,
              # resolution=(param['XRES'], param['YRES'], param['RESUNIT']),
              subifds=2,
              # resolution=None,# To do tiling code need to export resolution to the param file
              # metadata=metadata
              **options)

    for i in range(2):
        mag = 2 ** (i + 1)
        tif.write(
            img_all[::mag, ::mag, :],
            #resolution=(param['XRES'], param['YRES'], param['RESUNIT']),
            subfiletype=1,
            **options
        )

    thumbnail = img_all[::32, ::32, :]
    tif.write(thumbnail, metadata={'Name': 'thumbnail'})
