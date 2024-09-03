##################### batch for images per ROI ################



import pickle
import os
import glob
import cv2
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
        print()

def get_SS1_dimension_image_from_cws_resolution(cws_folder,annotated_dir,output_dir, refine_mask_dir, specific_dir, scale):

    wsi_files = sorted(glob.glob(os.path.join(cws_folder, '*.ndpi')))

    if os.path.exists(output_dir) is False:
        os.makedirs(output_dir)

    if os.path.exists(refine_mask_dir) is False:
        os.makedirs(refine_mask_dir)

    for wsi in range(0, len(wsi_files)):

        filename = wsi_files[wsi]


        param = pickle.load(open(os.path.join(filename, 'param.p'), 'rb'))

        slide_dimension = np.array(param['slide_dimension']) / 1 #1param['rescale']

        slide_w, slide_h = slide_dimension
        print(slide_w, slide_h)
        cws_w, cws_h = 2000, 2000 #param['cws_read_size']

        divisor_w = np.ceil(slide_w / cws_w)
        divisor_h = np.ceil(slide_h / cws_h)

        w, h = int(slide_w / scale), int(slide_h / scale)
        print('%s, Ss1 size: %i,%i'%(os.path.basename(filename), w, h))


        drivepath, imagename = os.path.split(wsi_files[wsi])

        if os.path.exists(os.path.join(output_dir, imagename)) is False:
            os.makedirs(os.path.join(output_dir, imagename))

        if os.path.exists(os.path.join(refine_mask_dir, imagename)) is False:
            os.makedirs(os.path.join(refine_mask_dir, imagename))

        ######### New directory mentioned to actively take only the .jpg files here ######

        annotated_dir_i = os.path.join(annotated_dir, imagename, specific_dir)
        images = sorted(os.listdir(annotated_dir_i), key=natural_key)

        img_all = np.zeros((h, w, 3))
        img_all = img_all.astype(np.uint8)

        img_high_res_all = np.zeros((int(slide_h), int(slide_w), 3))
        img_high_res_all = img_high_res_all.astype(np.uint8)
        scale_0 = 1

        for ii in images:
            #ri=[]
            imagelist =[]
            if os.path.isdir(os.path.join(annotated_dir, imagename, specific_dir, ii)):



                ## ii is checked for being a directory or not and then its created in the output directory for each slide
                if os.path.exists(os.path.join(output_dir, imagename, ii)) is False:
                    os.makedirs(os.path.join(output_dir, imagename, ii))

                if os.path.exists(os.path.join(refine_mask_dir, imagename, ii)) is False:
                    os.makedirs(os.path.join(refine_mask_dir, imagename, ii))
                 #

                #print(len(os.listdir(os.path.join(annotated_dir, imagename, 'ROI_80_H', ii))))
                for roi_i in glob.glob(os.path.join(annotated_dir, imagename, specific_dir, ii, '*.jpg')):
                    #print(roi_i)
                    roi_name = os.path.basename(roi_i)

                    if roi_name.endswith('.jpg'):
                        new_path = roi_name
                        print(os.path.join(annotated_dir, imagename, specific_dir, ii, roi_name))
                        if os.path.isfile(os.path.join(annotated_dir, imagename, specific_dir, ii, roi_name)):
                            imagelist.append(new_path)
                print(imagelist)#   each ROI da image list belonging to individual slide

                imagelist_roi = sorted(imagelist, key=natural_key)
                if len(imagelist)==0: ################################ handle empty roi directory
                    continue
                printProgressBar(0, len(imagelist), prefix='Progress:', suffix='Complete', length=50)

                for i in imagelist_roi:
                    cws_i = int(re.search(r'\d+', i).group())
                    h_i = np.floor(cws_i / divisor_w) * cws_h
                    w_i = (cws_i - h_i / cws_h * divisor_w) * cws_w

                    h_0_i = int(h_i / scale_0)
                    w_0_i = int(w_i / scale_0)

                    h_i = int(h_i / scale)
                    w_i = int(w_i / scale)
                    print(h_i, w_i)



                    # print(cws_i, w_i, h_i)

                    img_H = cv2.imread(os.path.join(annotated_dir, imagename, specific_dir, ii, i))
                    # img_H = cv2.cvtColor(img_H, cv2.COLOR_BGR2GRAY)
                    #img = cv2.imread(os.path.join(annotated_dir, imagename, i))
                    #im_mask = cv2.imread(os.path.join(annotated_dir, imagename, 'img_mask', ii, i))
                    #da_and_img = cv2.bitwise_and(img, im_mask)
                    #mask_artifact_corrected = Artifact_SS1(img)[1]
                    #total_pixels = mask_artifact_corrected.shape[0] * mask_artifact_corrected.shape[1]

                    # Count the number of white pixels
                    #white_pixels = np.count_nonzero(mask_artifact_corrected)

                    #Calculate the percentage of white pixels
                    #white_percentage = (white_pixels / total_pixels) * 100
                    #print(int(white_percentage))

                    # if white_percentage < 80:
                    #     continue

                    img = cv2.resize(img_H, (int(img_H.shape[1]/scale), int(img_H.shape[0]/scale)))



                    img_all[h_i : h_i + int(img.shape[0]), w_i : w_i + int(img.shape[1])] = img

                    img_high_res_all[h_0_i : h_0_i + int(img_H.shape[0]), w_0_i : w_0_i + int(img_H.shape[1])] = img_H

                    #img_H = cv2.resize(img_H, (int(img_H.shape[1]/scale), int(img_H.shape[0]/scale)))

                   # img_all_H[h_i : h_i + int(img.shape[0]), w_i : w_i + int(img.shape[1]), :] = img_H

                    #img_refine = cv2.resize(da_and_img, (int(da_and_img.shape[1]/scale), int(da_and_img.shape[0]/scale)))

                    #img_all_refine[h_i : h_i + int(img.shape[0]), w_i : w_i + int(img.shape[1]), :] = img_refine


                    printProgressBar(cws_i, len(images), prefix='Progress:',
                                     suffix='Completed for %s'%i, length=50)

                    #if w_i + cws_w / scale > w:
                ############# refine Da's for visualisation ######################

                #bm_img_roi_low_res = cv2.imread(os.path.join(refine_mask_dir, imagename, ii, imagename+'_'+ii+".png"))
                # BCPP PSR B22-966 18565-10-A2 s7 batch 2.ndpi ### ROI 4 is empty #####
               # if bm_img_roi_low_res is None: #################### if the ROI is None, then this if condition helps to exclude
                   # continue

              #  result_img = cv2.bitwise_and(np.uint8(img_all_H), bm_img_roi_low_res)
              # invert_mask = cv2.bitwise_not(bm_img_roi_low_res)
               # roi_with_bg_img = cv2.bitwise_or(result_img, invert_mask)

                #
                ############## refine Da's for visualisation ######################
                cv2.imwrite(os.path.join(output_dir, imagename, ii, os.path.splitext(imagename)[0]+'_'+ii+"_AFC.png"), img_all)
                cv2.imwrite(os.path.join(refine_mask_dir, imagename, ii, os.path.splitext(imagename)[0]+'_'+ii+"_PS_AFC.png"),img_high_res_all)

                #cv2.imwrite(os.path.join(output_dir, imagename, ii, os.path.splitext(imagename)[0]+'_'+ii+"_refined_img.png"), img_all_refine)
                #cv2.imwrite(os.path.join(output_dir, imagename, os.path.splitext(imagename)[0]+'_'+ii+"_Heam.png"), result_img)
                #cv2.imwrite(os.path.join(output_dir, imagename, os.path.splitext(imagename)[0]+'_'+ii+"_Heam_white_bg.png"), roi_with_bg_img)






# if __name__ == '__main__':
#
#     params = {
#                 'cws_folder': os.path.normpath(r'D:\Projects\c-PMAT\src\c-PMAT\cws'),
#                 'annotated_dir': r'D:\Projects\c-PMAT\src\c-PMAT\refined_workflow\cws',
#                 'output_dir': r'D:\Projects\c-PMAT\src\c-PMAT\output_LRES_dir',
#                 'refine_mask_dir': r'D:\Projects\c-PMAT\src\c-PMAT\output_LRES_dir',
#                 'specific_dir':'ROI_40_H1',
#                 'scale': 16
#                }
#
#     get_SS1_dimension_image_from_cws_resolution(params['cws_folder'], params['annotated_dir'],
#                                                 params['output_dir'], params['refine_mask_dir'],
#                                                 params['specific_dir'], params['scale'])
