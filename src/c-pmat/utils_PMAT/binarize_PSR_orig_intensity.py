import os
import numpy as np
import glob
import re
import cv2

# cws_folder = os.path.normpath(r'D:\AMY\230807_thumbnail_img_metadata')
# output_dir = r'D:\AMY\230803_PSR_ROI_tiles\cws'


def natural_key(string_):

    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]

def dark_pink_filter(cws_folder, output_dir):

    wsi_files = sorted(glob.glob(os.path.join(cws_folder, '*.ndpi')))

    # if os.path.exists(output_dir) is False:
    #     os.makedirs(output_dir)

    for wsi in range(0, len(wsi_files)):

        filename = wsi_files[wsi]
        drivepath, slidename = os.path.split(wsi_files[wsi])

        # if os.path.exists(os.path.join(output_dir, filename)) is False:
        #     os.makedirs(os.path.join(output_dir, filename))

         #if not os.path.exists(os.path.join(self.output_dir, cws_dir, slide)):

        if os.path.exists(os.path.join(output_dir, filename, "ROI_TWF_FILTER_ORIG")) is False:
            os.makedirs(os.path.join(output_dir, filename, "ROI_TWF_FILTER_ORIG"))

        if os.path.exists(os.path.join(output_dir, filename, "ROI_TWF_FILTER_INTER")) is False:
            os.makedirs(os.path.join(output_dir, filename, "ROI_TWF_FILTER_INTER"))



        print(os.path.join(output_dir, slidename, "ROI_with_AFC"))

        annotated_dir_i = os.path.join(output_dir, slidename, 'ROI_with_AFC') ######### New directory mentioned to actively take only the .jpg files here ######
        images = sorted(os.listdir(annotated_dir_i), key=natural_key)

        for ii in images:
            #ri=[]
            imagelist =[]
            print(ii)
            if os.path.isdir(os.path.join(output_dir, slidename, 'ROI_with_AFC', ii)):

                if os.path.exists(os.path.join(output_dir, slidename, "ROI_TWF_FILTER_ORIG", ii)) is False:
                    os.makedirs(os.path.join(output_dir, slidename, "ROI_TWF_FILTER_ORIG", ii))

                if os.path.exists(os.path.join(output_dir, filename, "ROI_TWF_FILTER_INTER", ii)) is False:
                    os.makedirs(os.path.join(output_dir, filename, "ROI_TWF_FILTER_INTER", ii))
                 #

                #print(len(os.listdir(os.path.join(annotated_dir, imagename, 'ROI_80_H', ii))))
                for roi_i in os.listdir(os.path.join(output_dir, slidename, 'ROI_with_AFC', ii)):
                    #print(roi_i)
                    roi_name = roi_i
                    #print(roi_name)

                    if roi_name.endswith('.jpg'):
                        if os.path.isfile(os.path.join(output_dir, slidename, 'ROI_with_AFC', ii, roi_name)):

                            orig_PS = cv2.imread(os.path.join(output_dir, slidename, 'ROI_80_PS1', ii, roi_name))
                            bin_mask = cv2.cvtColor(orig_PS, cv2.COLOR_BGR2GRAY)
                            #bin_mask = cv2.threshold(bin_mask, 40, 255, cv2.THRESH_BINARY_INV)[1]


                            # Set the threshold value
                            threshold_value = 100 ####

                            # Create a mask of pixels less than the threshold value
                            mask = bin_mask < threshold_value
                            mask = mask*255
                            mask = np.uint8(mask)
                            ### Add/Modify to 3channel if the mask is two channel
                            mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)

                            da_and_img = cv2.bitwise_and(orig_PS, mask)
                            invert_mask = cv2.bitwise_not(mask)
                            roi_with_bg_img = cv2.bitwise_or(da_and_img, invert_mask)


                            # Define kernel for morphological operations
                            #kernel = np.ones((15, 15), np.uint8)

                            # Perform closing operation to remove small black noise pixels
                            #closed_image = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

                            # Perform opening operation to remove small white noise pixels
                            #opened_image = cv2.morphologyEx(closed_image, cv2.MORPH_OPEN, kernel)
                            # Apply the mask to set the selected pixels to the desired value (255)
                            #thresholded_image = np.where(mask, 255, bin_mask)
                            #
                            #
                            #bin_image_smooth = cv2.GaussianBlur(opened_image, (21, 21), 0)

                            cv2.imwrite(os.path.join(output_dir, slidename, "ROI_TWF_FILTER_INTER", ii, os.path.splitext(roi_name)[0]+".png"), da_and_img)
                            cv2.imwrite(os.path.join(output_dir, slidename, "ROI_TWF_FILTER_ORIG", ii, os.path.splitext(roi_name)[0]+".png"), roi_with_bg_img)

                            print(os.path.join(output_dir, slidename, "ROI_TWF_FILTER_ORIG", ii, os.path.splitext(roi_name)[0]+".png"))



        #filename = wsi_files[wsi]

if __name__ == '__main__':

    params = {
                'cws_folder': os.path.normpath(r'D:\Projects\cbias-nap-AMY\cws1'),
                'output_dir': r'D:\Projects\cbias-nap-AMY\refined_workflow\cws', #r'D:\AMY\230803_PSR_ROI_tiles\cws',
                'refine_mask_dir': r'D:\AMY\230810_low_res_mask_per_ROI',
                'scale': 16
               }
    dark_pink_filter(params['cws_folder'], params['output_dir'])
