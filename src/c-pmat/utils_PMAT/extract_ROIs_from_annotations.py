import os
import numpy as np
import cv2
OPENSLIDE_PATH = r'C:\Tools\openslide-win64-20231011\bin'

import os
if hasattr(os, 'add_dll_directory'):
    # Windows
    with os.add_dll_directory(OPENSLIDE_PATH):
        import openslide
else:
    import openslide
#
#import openslide
import xml.dom.minidom
import xml.etree.ElementTree as ET
import re

from utils_PMAT.get_bg_correction import *
from utils_PMAT.Colour_norm import *

# from utils_PMAT.get_bg_correction import *
# from utils_PMAT.Colour_norm import *



def natural_key(string_):
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]


class GenerateWSIannotation_on_cws(object):

    def __init__(self,
                 input_slide_dir,
                 tiles_dir,
                 output_dir,
                 ext,
                 thresh_d):
        self.input_slide_dir = input_slide_dir
        self.tiles_dir = tiles_dir
        self.output_dir = output_dir
        self.ext = ext
        self.thresh_d = thresh_d
        if os.path.exists(self.output_dir) is False:
            os.makedirs(self.output_dir)

    def generate_patch_of_annotated_tiles(self):

        # Annotated tiles positive images will be saved in img_mask directory
        # Background tiles will be saved in Mat_files directory
        # .mat files from this will be used to generate tf records file

        file_names_list =[fname for fname in os.listdir(self.input_slide_dir) if fname.endswith(self.ext) and (fname.startswith('BCPP') or fname.startswith('RADIO') or fname.startswith('PLUMMB')) is True]

        cws_dir = "cws"

        if os.path.exists(os.path.join(self.output_dir, cws_dir)) is False:
            os.makedirs(os.path.join(self.output_dir, cws_dir))

        for slide in file_names_list:

            print(os.path.join(self.output_dir, cws_dir, slide))
            if not os.path.exists(os.path.join(self.output_dir, cws_dir, slide)):


                if os.path.exists(os.path.join(self.output_dir, cws_dir, slide)) is False:
                    os.makedirs(os.path.join(self.output_dir, cws_dir, slide))

                if os.path.exists(os.path.join(self.output_dir, cws_dir, slide, "img_mask")) is False:
                    os.makedirs(os.path.join(self.output_dir, cws_dir, slide, "img_mask"))

                if os.path.exists(os.path.join(self.output_dir, cws_dir, slide, "ROI_DA")) is False:
                    os.makedirs(os.path.join(self.output_dir, cws_dir, slide, "ROI_DA"))

                if os.path.exists(os.path.join(self.output_dir, cws_dir, slide, "ROI_with_AFC")) is False:
                    os.makedirs(os.path.join(self.output_dir, cws_dir, slide, "ROI_with_AFC"))

                if os.path.exists(os.path.join(self.output_dir, cws_dir, slide, "ROI_"+str(self.thresh_d)+"_AFC")) is False:
                    os.makedirs(os.path.join(self.output_dir, cws_dir, slide, "ROI_"+str(self.thresh_d)+"_AFC"))

                if os.path.exists(os.path.join(self.output_dir, cws_dir, slide, "ROI_"+str(self.thresh_d)+"_H1")) is False:
                    os.makedirs(os.path.join(self.output_dir, cws_dir, slide, "ROI_"+str(self.thresh_d)+"_H1"))

                if os.path.exists(os.path.join(self.output_dir, cws_dir, slide, "ROI_"+str(self.thresh_d)+"_PS1")) is False:
                    os.makedirs(os.path.join(self.output_dir, cws_dir, slide, "ROI_"+str(self.thresh_d)+"_PS1"))

                if os.path.exists(os.path.join(self.output_dir, cws_dir, slide, "ROI_TWF_FILTER_ORIG")) is False:
                    os.makedirs(os.path.join(self.output_dir, cws_dir, slide, "ROI_TWF_FILTER_ORIG"))

                osr = openslide.OpenSlide(os.path.join(self.input_slide_dir, slide))
                level = 0
                ds = osr.level_downsamples[level]
                w, h = osr.level_dimensions[0]

                mask_path = os.path.join(self.output_dir, cws_dir, slide, "img_mask")
                da_configpath = os.path.join(self.output_dir, cws_dir, slide, "ROI_DA")
                roi_corrected = os.path.join(self.output_dir, cws_dir, slide, "ROI_with_AFC")
                roi_corrected_da_path = os.path.join(self.output_dir, cws_dir, slide, "ROI_"+str(self.thresh_d)+"_AFC")
                H_da_path = os.path.join(self.output_dir, cws_dir, slide, "ROI_"+str(self.thresh_d)+"_H1")
                PS_da_path = os.path.join(self.output_dir, cws_dir, slide, "ROI_"+str(self.thresh_d)+"_PS1")
                norm_da_path = os.path.join(self.output_dir, cws_dir, slide, "ROI_"+str(self.thresh_d)+"_norm1")
                twf_da_path = os.path.join(self.output_dir, cws_dir, slide, "ROI_TWF_FILTER_ORIG")


                doc = xml.dom.minidom.parse(os.path.join(self.input_slide_dir, os.path.splitext(slide)[0] + '.xml'))
                Region = doc.getElementsByTagName("Region")

                class_types_reg = []
                for Reg in Region:
                    class_types_reg.append(Reg.getAttribute("Text"))
                class_types = np.unique(class_types_reg)
                for cls_type in class_types:
                    mask_path_cls_type = os.path.join(mask_path, cls_type)
                    roi_path_cls_type = os.path.join(da_configpath, cls_type)
                    roi_corrected_cls_type = os.path.join(roi_corrected, cls_type)
                    roi_80_afc_cls_type = os.path.join(roi_corrected_da_path, cls_type)
                    roi_80_H_cls_type = os.path.join(H_da_path, cls_type)
                    roi_80_PS_cls_type = os.path.join(PS_da_path, cls_type)
                    roi_80_norm_cls_type = os.path.join(norm_da_path, cls_type)
                    roi_80_twf_cls_type = os.path.join(twf_da_path, cls_type)
                    if os.path.exists(mask_path_cls_type) is False:
                        os.makedirs(mask_path_cls_type)
                    if os.path.exists(roi_path_cls_type) is False:
                        os.makedirs(roi_path_cls_type)
                    if os.path.exists(roi_corrected_cls_type) is False:
                        os.makedirs(roi_corrected_cls_type)
                    if os.path.exists(roi_80_afc_cls_type) is False:
                        os.makedirs(roi_80_afc_cls_type)
                    if os.path.exists(roi_80_H_cls_type) is False:
                        os.makedirs(roi_80_H_cls_type)
                    if os.path.exists(roi_80_PS_cls_type) is False:
                        os.makedirs(roi_80_PS_cls_type)
                    if os.path.exists(roi_80_norm_cls_type) is False:
                        os.makedirs(roi_80_norm_cls_type)
                    if os.path.exists(roi_80_twf_cls_type) is False:
                        os.makedirs(roi_80_twf_cls_type)

                X = []
                Y = []
                X_BV1 = []
                Y_BV1 = []
                i_reg = 0
                i_BV1 = []
                i_BV2 = []
                for Reg in Region:
                    print("Process Region No:", i_reg)
                    if (Reg.getAttribute("Text") == "BV1"):
                        i_BV1.append(i_reg)
                    if (Reg.getAttribute("Text") == "BV2"):
                        i_BV2.append(i_reg)
                    X.append([])
                    Y.append([])
                    X_BV1.append([])
                    Y_BV1.append([])
                    Vertex = Reg.getElementsByTagName("Vertex")
                    for Vert in Vertex:
                        X[i_reg].append(int(round(float(Vert.getAttribute("X")))))
                        Y[i_reg].append(int(round(float(Vert.getAttribute("Y")))))

                    i_reg += 1

                i1 = 0
                points = []
                for j in range(0, h, 2000):
                    for i in range(0, w, 2000):
                        print(os.path.join(self.tiles_dir, slide, 'Da' + str(i1) + ".jpg"))
                        img = cv2.imread(os.path.join(self.tiles_dir, slide, 'Da' + str(i1) + ".jpg"))
                        [hh, ww, cc] = img.shape
                        blank_image_all = np.zeros((hh, ww), np.uint8)
                        cnt_t = 0
                        for k in range(len(X)):
                            blank_image = np.zeros((hh, ww), np.uint8)
                            # print("######")
                            if i < max(X[k]) and i + 2000 > min(X[k]) and j < max(Y[k]) and j + 2000 > min(Y[k]):

                                points = []
                                for i3 in range(len(X[k])):
                                    points.append([int((X[k][i3] - i) / ds), int((Y[k][i3] - j) / ds)])
                                pts = np.array(points, np.int32)
                                pts = pts.reshape((-1, 1, 2))
                                cnt_t+=1
                                cv2.drawContours(blank_image, [pts], 0, (255), -1)
                                #cv2.drawContours(blank_image_all, [pts], 0, (255), -1)
                                cv2.imwrite(os.path.join(mask_path, class_types_reg[k], 'Da' + str(i1) + ".jpg"), blank_image)
                                bm_img = cv2.cvtColor(blank_image, cv2.COLOR_GRAY2BGR)
                                result_img = cv2.bitwise_and(img, bm_img)
                                invert_mask = cv2.bitwise_not(bm_img)

                                # Keep tiles with white background if they are not part of ROI ##### ROI_DA
                                da_or_img = cv2.bitwise_or(invert_mask, img)
                                cv2.imwrite(os.path.join(da_configpath, class_types_reg[k], 'Da' + str(i1) + ".jpg"), da_or_img)

                                ######################################### artifact filter #########################################
                                ################### Taking the da_or_img after multiply per ROI ###################################
                                mask_artifact_corrected = Artifact_SS1(da_or_img)[1]
                                total_pixels = mask_artifact_corrected.shape[0] * mask_artifact_corrected.shape[1]

                                # Count the number of white pixels
                                white_pixels = np.count_nonzero(mask_artifact_corrected)

                                #Calculate the percentage of white pixels
                                white_percentage = (white_pixels / total_pixels) * 100
                                #print(int(white_percentage))

                                if white_percentage < self.thresh_d:#80
                                    continue

                                cv2.imwrite(os.path.join(roi_corrected, class_types_reg[k], 'Da' + str(i1) + ".jpg"), mask_artifact_corrected)
                                cv2.imwrite(os.path.join(roi_corrected_da_path, class_types_reg[k], 'Da' + str(i1) + ".jpg"), da_or_img)
                                Inorm_img, PS_img, H_img = normalizeStaining(img, saveFile=None, Io=240, alpha=1, beta=0.15)

                                orig_PS = PS_img
                                bin_mask = cv2.cvtColor(orig_PS, cv2.COLOR_BGR2GRAY)

                                # Set the threshold value
                                threshold_value = 100  ####

                                # Create a mask of pixels less than the threshold value
                                mask = bin_mask < threshold_value
                                mask = mask * 255
                                mask = np.uint8(mask)
                                ### Add/Modify to 3channel if the mask is two channel
                                mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)

                                da_and_img = cv2.bitwise_and(orig_PS, mask)
                                invert_mask = cv2.bitwise_not(mask)
                                roi_with_bg_img = cv2.bitwise_or(da_and_img, invert_mask)

                                cv2.imwrite(os.path.join(H_da_path, class_types_reg[k], 'Da' + str(i1) + ".jpg"), PS_img)
                                cv2.imwrite(os.path.join(PS_da_path, class_types_reg[k], 'Da' + str(i1) + ".jpg"), H_img)
                                cv2.imwrite(os.path.join(norm_da_path, class_types_reg[k], 'Da' + str(i1) + ".jpg"), Inorm_img)
                                cv2.imwrite(os.path.join(twf_da_path, class_types_reg[k], 'Da' + str(i1) + ".png"), roi_with_bg_img)
                        i1 += 1
            else: # process only if the output directories and results have not been processed and ready
                continue
def map_of_slides_and_annotations(input_slide_dir, wsi_tiles_dir, output_dir, file_type, thresh_d):

    params_keys = {'input_slide_dir': input_slide_dir,
                   'tiles_dir': wsi_tiles_dir,
                   'output_dir': output_dir,
                   'ext': file_type,
                   'thresh_d': thresh_d}
    obj = GenerateWSIannotation_on_cws(**params_keys)

    obj.generate_patch_of_annotated_tiles()

# slide_directory = r'D:\Projects\cbias-nap-AMY\slides'
# tiles_directory = r'D:\Projects\cbias-nap-AMY\cws'
# output_directory = r'D:\Projects\cbias-nap-AMY\refined_workflow'
# ext = '.ndpi'
#
# map_of_slides_and_annotations(slide_directory, tiles_directory, output_directory, ext)

