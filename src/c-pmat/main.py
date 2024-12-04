import napari
from magicgui import magicgui, widgets
from qtpy.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget, QLabel, QTabWidget
from skimage import color, filters
import numpy as np
import sys
import pathlib

### QWidget implementation from napIPUvis and napari-tma github references ###
# P-MAT - a napari-based workflow for scale-independent quantification 
# of the extracellular matrix and its topological scale-independent descriptors
'''
https://github.com/IntegratedPathologyUnit-ICR/POPIDD/tree/napari_tma

'''
# Usage in napari

def main():
    viewer = napari.Viewer()

    @magicgui(
            input_slide_dir={"widget_type": "FileEdit", "mode": "d"},
            wsi_tiles_dir={"widget_type": "FileEdit", "mode": "d"},
            file_type={"widget_type": "FileEdit", "mode": "r"},
            num_process={"widget_type": "ComboBox", "choices": ["1", "2", "4", "8"]},
            call_button="Run"  # This adds a Run button to the widget
            )
    def wGTauto(
            input_slide_dir=pathlib.Path("slides"),
            wsi_tiles_dir=pathlib.Path("cws"),
            file_type=pathlib.Path(".ndpi"),
            num_process="1",
            ):
        try:
            from utils_PMAT import generate_tiles_from_PSR_wsi_slides
            generate_tiles_from_PSR_wsi_slides.perform_tiling(str(input_slide_dir), str(wsi_tiles_dir), str(file_type), num_process)
            print("Extraction completed!")
            print(f"Parameters: {input_slide_dir}, {wsi_tiles_dir}, {file_type}, {num_process}")
        except ModuleNotFoundError as e:
            print(f"Error: Could not import from PMAT module. {e}")
            print(f"Python path: {sys.path}")
        except Exception as e:
            print(f"An error occurred: {e}")

    @magicgui(
            input_slide_dir={"widget_type": "FileEdit", "mode": "d"},
            wsi_tiles_dir={"widget_type": "FileEdit", "mode": "d"},
            output_dir={"widget_type": "FileEdit", "mode": "d"},
            file_type={"widget_type": "ComboBox", "choices": [".svs", ".ndpi", ".tif"]},
            thresh_d={"widget_type": "ComboBox", "choices": ["80", "60", "40", "20"]},
            call_button="Run"  # This adds a Run button to the widget
            )
    def wTSauto(
            input_slide_dir=pathlib.Path("slides"),
            wsi_tiles_dir=pathlib.Path("cws"),
            output_dir=pathlib.Path("refined_workflow"),
            file_type=".ndpi",
            thresh_d="80",
            ):
        try:
            from utils_PMAT import extract_ROIs_from_annotations
            extract_ROIs_from_annotations.map_of_slides_and_annotations(str(input_slide_dir), str(wsi_tiles_dir), str(output_dir), file_type, int(thresh_d))
            print("Extraction completed!")
            print(f"Parameters: {input_slide_dir}, {wsi_tiles_dir}, {output_dir}, {file_type}, {(thresh_d)}")
        except ModuleNotFoundError as e:
            print(f"Error: Could not import from PMAT module. {e}")
            print(f"Python path: {sys.path}")
        except Exception as e:
            print(f"An error occurred: {e}")

    @magicgui(
        cws_dir={"widget_type": "FileEdit", "mode": "d"},
        annot_dir={"widget_type": "FileEdit", "mode": "d"},
        output_low_res_dir={"widget_type": "FileEdit", "mode": "d"},
        high_res_dir={"widget_type": "FileEdit", "mode": "d"},
        specific_dir={"widget_type": "ComboBox",
                      "choices": ["ROI_80_AFC", "ROI_80_H1", "ROI_80_PS1", "ROI_60_AFC", "ROI_60_H1", "ROI_60_PS1",
                                  "ROI_40_AFC", "ROI_80_H1", "ROI_40_PS1"]},
        scale={"widget_type": "ComboBox", "choices": ["16", "8", "4"]},
        call_button="Run"  # This adds a Run button to the widget
    )
    def wSTauto(
            cws_dir=pathlib.Path("cws_folder"),
            annot_dir=pathlib.Path("refined_workflow"),
            output_low_res_dir=pathlib.Path("output_LRES_dir"),
            high_res_dir=pathlib.Path("output_HRES_dir"),
            specific_dir="ROI_80_H1",
            scale="16",

    ):
        try:
            from utils_PMAT import stitch_Low_res_per_ROI_with_80percent_tile_selection_TWF
            stitch_Low_res_per_ROI_with_80percent_tile_selection_TWF.get_SS1_dimension_image_from_cws_resolution(
                str(cws_dir), str(annot_dir), str(output_low_res_dir), str(high_res_dir), str(specific_dir), int(scale))

        except ModuleNotFoundError as e:
            print(f"Error: Could not import from PMAT module. {e}")
            print(f"Python path: {sys.path}")
        except Exception as e:
            print(f"An error occurred: {e}")

    @magicgui(
        wsi_tiles_dir={"widget_type": "FileEdit", "mode": "d"},
        output_dir={"widget_type": "FileEdit", "mode": "d"},
        file_type={"widget_type": "ComboBox", "choices": [".svs", ".ndpi", ".tif"]},
        shape_type={"widget_type": "ComboBox", "choices": ["Tree", "Branch"]},
        call_button="Run"  # This adds a Run button to the widget
    )
    def wSFauto(
            wsi_tiles_dir=pathlib.Path("cws"),
            output_dir=pathlib.Path("refined_workflow"),
            file_type=".ndpi",
            shape_type="Tree",
    ):
        try:
            from utils_PMAT import extract_features
            extract_features.get_patch_level_features(str(wsi_tiles_dir), str(output_dir), file_type, shape_type)
            print("Extraction completed!")
            print(f"Parameters: {wsi_tiles_dir}, {output_dir}, {file_type}, {shape_type}")
        except ModuleNotFoundError as e:
            print(f"Error: Could not import from PMAT module. {e}")
            print(f"Python path: {sys.path}")
        except Exception as e:
            print(f"An error occurred: {e}")

    tab_widget = QTabWidget()
    #
    ## tile ##
    tab_GT = QWidget()
    gt_layout = QVBoxLayout()
    tab_GT.setLayout(gt_layout)
    gt_layout.addWidget(wGTauto.native)


    # %%#Annotated tissue ROI selection ##
    tab_TS = QWidget()
    ts_layout = QVBoxLayout()
    tab_TS.setLayout(ts_layout)
    ts_layout.addWidget(wTSauto.native)

    # stitch #
    tab_ST = QWidget()
    st_layout = QVBoxLayout()
    tab_ST.setLayout(st_layout)
    st_layout.addWidget(wSTauto.native)

    # Feature descriptives #
    tab_SF = QWidget()
    sf_layout = QVBoxLayout()
    tab_SF.setLayout(sf_layout)
    sf_layout.addWidget(wSFauto.native)
    # %%
    tab_widget.addTab(tab_GT, "Generate tiles from WSIs")
    tab_widget.addTab(tab_TS, "Generate ROI regions of annotation")
    tab_widget.addTab(tab_ST, "Stitch processed outputs")
    tab_widget.addTab(tab_SF, "Feature descriptor extraction")

    # Connect the update button to the update_info method
    #tab_widget.update_info_btn.clicked.connect(tab_widget.update_info)

    tab_widget.setFixedHeight(500)
    # tab_widget1.setFixedHeight(400)
    viewer.window.add_dock_widget(
        tab_widget, name="ECM c-pmat pipeline", area="right",
        add_vertical_stretch=False, tabify=True)


    #

    napari.run()
if __name__=='__main__':
    main()





