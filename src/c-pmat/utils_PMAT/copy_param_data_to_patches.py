import os
import shutil

cws_path=r'D:\AMY\230803_PSR_ROI_tiles\cws'


copy_ss1_path =r'E:\CODE\CD-31 staining quantization project\stain_mask'
name=[]

for slide in os.listdir(cws_path):
    if slide.endswith('.ndpi'):
        try:
            for roi_dir in os.listdir(os.path.join(cws_path, slide, 'ROI_TWF')):
                if os.path.isdir(os.path.join(cws_path, slide, 'ROI_TWF', roi_dir)):
                    if os.path.exists(os.path.join(copy_ss1_path, slide, roi_dir)) is False:
                        os.makedirs(os.path.join(copy_ss1_path, slide, roi_dir))
                    #print(roi_dir)
                    for Da_img in os.listdir(os.path.join(cws_path, slide, 'ROI_TWF', roi_dir)):

                        if Da_img.endswith('_smooth.jpg'):
                            # print(img)

                            # imgname=img.split('.ndpi_Ss1.jpg')[0]
                            # name.append(imgname)
                            src = os.path.join(cws_path, slide, 'ROI_TWF', roi_dir, Da_img)
                            dst = os.path.join(copy_ss1_path, slide, roi_dir, Da_img)
                            #print(dst)
                            shutil.copy(src, dst)
                            #srcname = Da_img
                            print(dst)
                    # print(srcname)
                    # copyfile(os.path.join(cws_path, slide,srcname),dst)
        except Exception:
            print(slide)
            pass
