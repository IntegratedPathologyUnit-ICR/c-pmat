import numpy as np
import cv2
import math
from scipy.ndimage import binary_fill_holes
def calculate_magnitude(od):

    channel = cv2.split(od)
    square_b = cv2.pow(channel[0], 2)
    square_g = cv2.pow(channel[1], 2)
    square_r = cv2.pow(channel[2], 2)
    square_bgr = square_b + square_g + square_r
    magnitude = cv2.sqrt(square_bgr)

    return magnitude

def normaliseOD(od,magnitude):

    channels=cv2.split(od)#, (channels[0],channels[1],channels[2]))

    od_norm_b = cv2.divide(channels[0], magnitude)
    od_norm_g = cv2.divide(channels[1], magnitude)
    od_norm_r = cv2.divide(channels[2], magnitude)

    od_norm = cv2.merge((od_norm_b,od_norm_g, od_norm_r))

    return od_norm

#remove artefacts based off optical density e.g edge of slide
def Artifact_SS1(img):
    I = img.transpose()
    k, width, height = I.shape
    I = I.reshape(k, width * height)
    I = np.float32(I)

    od = cv2.max(I, 1)

    grey_angle = 0.2

    magnitude_threshold = 0.05

    channels = cv2.split(od)
    #
    magnitude = np.zeros(od.shape)
    #
    background = 245
    #
    # Convert channels to a list to allow modification
    channels = list(channels)

    # Perform the operation
    background = 245
    channels[0] /= background

    # Convert the list back to a tuple
    channels = tuple(channels)
    # channels[0]/=background # old code line converted to suppport the processing
    # Extract the array from the tuple
    # image_array = channels[0]
    # # Modify the first channel (index 0)
    # image_array[0] /= background
    # # If you need to keep it as a tuple, you can recreate it
    # channels = (image_array,)
    # Assuming 'channels' is a tuple of numpy arrays
    # channels = list(channels)  # Convert tuple to list
    # channels[0] = channels[0] / background  # Use numpy array division
    # channels = tuple(channels)

    od = cv2.merge(channels)

    od = cv2.log(od)

    od *= (1 / cv2.log(10)[0])

    od = -od
    od = od.reshape(3, width, height).transpose()
    magnitude = calculate_magnitude(od)

    tissue_and_artefact_mask = (magnitude > magnitude_threshold)

    od_norm = normaliseOD(od, magnitude)

    chan = cv2.split(od_norm)

    grey_mask = (chan[0] + chan[1] + chan[2]) >= (math.cos(grey_angle) * cv2.sqrt(3)[0])

    other_colour_mask = (chan[2] > chan[1]) | (chan[0] > chan[1])

    mask = grey_mask | other_colour_mask

    mask = (255 - mask) & tissue_and_artefact_mask
    mask1 = mask.astype(np.int8)

    mask_img = mask1*255
    mask_img = mask_img.astype(np.uint8)

    mask_img_smooth = cv2.GaussianBlur(mask_img, (151, 151), 0)
    mask_img_smooth = cv2.threshold(mask_img_smooth, 20, 255, cv2.THRESH_BINARY)[1]

    mask_img_smooth = binary_fill_holes(mask_img_smooth)
    mask_img_smooth = mask_img_smooth.astype(np.uint8)*255


    clean = cv2.bitwise_and(img, img, mask=mask1)
    clean = cv2.bitwise_not(clean)

    clean = cv2.bitwise_and(clean, clean, mask=mask1)
    clean = cv2.bitwise_not(clean)

    img_s = cv2.cvtColor(clean, cv2.COLOR_BGR2GRAY)
    img_th = cv2.threshold(img_s, 120, 255, cv2.THRESH_BINARY)
    #print(img_th)

    #write_mask1 = mask.astype(np.uint8)*255

    #cv2.imwrite(os.path.join(output_dir, os.path.splitext(im)[0]+'_Mask.jpg'), write_mask1)
    return clean, mask_img_smooth
