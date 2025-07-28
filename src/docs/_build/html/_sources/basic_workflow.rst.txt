Basic Workflow Tutorial
======================

🎯 **Learning Objectives**
   Learn the complete P-MAT workflow from start to finish

📋 **Prerequisites**
   - c-pmat installed and working
   - Sample whole slide image (.ndpi, .svs, .mrxs, .scn or .tif)
   - Corresponding XML annotation file
   - 8GB+ RAM and 10GB+ free disk space

⏱️ **Estimated Time**
   45-60 minutes

📁 **Sample Data**
   Download the tutorial dataset from: `tutorial-data.zip <#>`_

Introduction
------------

This tutorial walks you through the complete c-pmat workflow using a sample Picrosirius Red (PSR) stained tissue slide. You'll learn how to:

1. Generate image tiles from a whole slide image
2. Extract regions of interest using annotations
3. Stitch processed outputs at multiple resolutions
4. Extract quantitative morphological features

The workflow processes collagen fiber organization in tissue samples, providing quantitative measurements of extracellular matrix structure.

Step 1: Prepare Your Data
-------------------------

**1.1 Set Up Directory Structure**

Create a clean workspace for this tutorial:

.. code-block:: bash

   mkdir c-pmat_basic_tutorial
   cd c-pmat_basic_tutorial

   # Create required directories
   mkdir slides
   mkdir tiles
   mkdir roi_output
   mkdir stitched_low_res
   mkdir stitched_high_res

**1.2 Place Your Sample Data**

Copy your sample files:

.. code-block:: text

   pmat_basic_tutorial/
   └── slides/
       ├── P001_sample.ndpi      # Your PSR stain whole slide image
       └── P002_sample.xml       # Corresponding annotation file

.. note::
   The XML file must have the same base name as the slide file for automatic detection.

**1.3 Verify Your Data**

Check that your files are correctly placed:

.. code-block:: bash

   ls -la slides/
   # Should show both .ndpi and .xml files

Step 2: Launch c-pmat
--------------------

**2.1 Start the Application**

.. code-block:: bash

   python main.py

This opens the napari viewer with c-pmat's tabbed interface on the right.

**2.2 Understand the Interface**

The c-pmat interface has four tabs:

1. **Generate tiles from WSIs**: Extract image patches
2. **Generate ROI regions of annotation**: Process only annotated areas
3. **Stitch processed outputs**: Reconstruct images
4. **Feature descriptor extraction**: Quantify morphology

Step 3: Generate Tiles from WSI
-------------------------------

**3.1 Configure Tile Generation**

In the "Generate tiles from WSIs" tab:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Parameter
     - Value
   * - Input slide dir
     - ``/path/to/c-pmat_basic_tutorial/slides``
   * - WSI tiles dir
     - ``/path/to/c-pmat_basic_tutorial/tiles``
   * - File type
     - ``.ndpi`` (or your file extension)
   * - Num process
     - ``4`` (adjust based on your CPU)

**3.2 Run Tile Generation**

1. Click **Run**
2. Monitor progress in the console
3. Wait for "Extraction completed!" message

**3.3 Verify Output**

Check the generated tiles:

.. code-block:: bash

   ls tiles/P001_sample.ndpi/
   # Should show: Da0.jpg, Da1.jpg, ..., param.p, thumbnail.jpg

**What Happened:**
- c-pmat divided your large slide into 2000×2000 pixel tiles
- Each tile is saved as a JPEG file
- Processing parameters are saved in ``param.p``
- A thumbnail image was generated for quick reference

Step 4: Extract ROI Regions
---------------------------

**4.1 Configure ROI Extraction**

In the "Generate ROI regions of annotation" tab:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Parameter
     - Value
   * - Input slide dir
     - ``/path/to/pmat_basic_tutorial/slides``
   * - WSI tiles dir
     - ``/path/to/pmat_basic_tutorial/tiles``
   * - Output dir
     - ``/path/to/pmat_basic_tutorial/roi_output``
   * - File type
     - ``.ndpi``
   * - Thresh d
     - ``80`` (80% tissue threshold)

**4.2 Run ROI Extraction**

1. Click **Run**
2. Processing may take 10-15 minutes for a typical slide
3. Watch for completion message

**4.3 Examine the Results**

Explore the generated directories:

.. code-block:: bash

   find roi_output/ -type d
   # Shows the directory structure created

Key output directories:

.. code-block:: text

   roi_output/cws/P001_sample.ndpi/
   ├── img_mask/           # Binary tissue masks
   ├── ROI_80_AFC/         # Artifact-corrected images
   ├── ROI_80_H1/          # Hematoxylin channel
   ├── ROI_80_PS1/         # Picrosirius red channel
   └── ROI_TWF_FILTER_ORIG/  # Filtered original images

**What Happened:**
- c-pmat read your XML annotations
- Extracted annotated regions from tiles
- Applied color normalization (separating H&E and PSR channels)
- Filtered out artifacts and low-quality regions
- Created multiple processing variants for different analyses

Step 5: Stitch Processed Outputs
--------------------------------

**5.1 Configure Stitching**

In the "Stitch processed outputs" tab:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Parameter
     - Value
   * - CWS dir
     - ``/path/to/pmat_basic_tutorial/tiles``
   * - Annot dir
     - ``/path/to/pmat_basic_tutorial/roi_output``
   * - Output low res dir
     - ``/path/to/pmat_basic_tutorial/stitched_low_res``
   * - High res dir
     - ``/path/to/pmat_basic_tutorial/stitched_high_res``
   * - Specific dir
     - ``ROI_80_H1`` (Hematoxylin channel)
   * - Scale
     - ``16`` (16x downsampling)

**5.2 Run Stitching**

1. Click **Run**
2. Processing typically takes 5-10 minutes
3. Check console for progress updates

**5.3 View Stitched Results**

Open the generated images:

.. code-block:: bash

   # Check low-resolution stitched images
   ls stitched_low_res/P001_sample.ndpi/*/

   # Check high-resolution images
   ls stitched_high_res/P002_sample.ndpi/*/

**What Happened:**
- c-pmat reconstructed coherent images from individual processed tiles
- Created both low-resolution (for overview) and high-resolution (for detail) versions
- Organized results by ROI and processing type

Step 6: Extract Feature Descriptors
-----------------------------------

**6.1 Configure Feature Extraction**

In the "Feature descriptor extraction" tab:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Parameter
     - Value
   * - WSI tiles dir
     - ``/path/to/c-pmat_basic_tutorial/tiles``
   * - Output dir
     - ``/path/to/c-pmat_basic_tutorial/roi_output``
   * - File type
     - ``.ndpi``
   * - Shape type
     - ``Tree`` (for fiber tree analysis)

**6.2 Run Feature Extraction**

1. Click **Run**
2. This step can take 15-30 minutes depending on image complexity
3. Monitor progress in console

**6.3 Analyze the Results**

Check the generated feature data:

.. code-block:: bash

   find roi_output/ -name "*.csv"
   # Lists all CSV files with measurements

Key output files:

.. code-block:: text

   roi_output/cws/P001_sample.ndpi/tree_overlay_img/
   ├── ROI_1/
   │   ├── all_tree_da.csv      # Detailed measurements per patch
   │   └── *.png                # Overlay images showing detected features
   ├── ROI_2/
   │   └── ...
   └── all_roi_tree.csv         # Summary measurements per ROI

**What Happened:**
- c-pmat analyzed the morphological structure of fibers
- Detected tree-like collagen organizations
- Calculated quantitative descriptors (length, density, branching)
- Generated overlay images showing detected features
- Exported measurements to CSV files for analysis

Step 7: Interpret Your Results
------------------------------

**7.1 Open the CSV Files**

View your quantitative results:

.. code-block:: python

   import pandas as pd

   # Load ROI-level summary
   roi_data = pd.read_csv('roi_output/cws/P001_sample.ndpi/tree_overlay_img/all_roi_tree.csv')
   print(roi_data.head())

   # Load detailed patch-level data
   patch_data = pd.read_csv('roi_output/cws/P001_sample.ndpi/tree_overlay_img/ROI_1/all_tree_da.csv')
   print(patch_data.head())

**7.2 Understand the Measurements**

Key measurements in the CSV files:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Measurement
     - Description
   * - ``file_name``
     - Path to the analyzed image patch
   * - ``mask``
     - Total tissue area in pixels
   * - ``tree_count``
     - Number of tree-like structures detected
   * - ``tree_ratio``
     - Tree density per unit area (normalized)

**7.3 Visualize Your Results**

Open the overlay images in napari:

.. code-block:: python

   import napari
   from skimage import io

   # Load an overlay image
   overlay = io.imread('roi_output/cws/BCPP_sample.ndpi/tree_overlay_img/ROI_1/Da0_skel.png')

   viewer = napari.Viewer()
   viewer.add_image(overlay, name='Feature Overlay')
   napari.run()

Step 8: Next Steps and Analysis
-------------------------------

**8.1 Statistical Analysis**

Analyze your measurements:

.. code-block:: python

   import matplotlib.pyplot as plt

   # Plot tree density distribution
   plt.figure(figsize=(10, 6))
   plt.hist(roi_data['tree_ratio'], bins=20, alpha=0.7)
   plt.xlabel('Tree Density')
   plt.ylabel('Frequency')
   plt.title('Distribution of Collagen Tree Density')
   plt.show()

   # Summary statistics
   print(roi_data['tree_ratio'].describe())

**8.2 Compare Different ROIs**

.. code-block:: python

   # Group by ROI type if you have multiple annotation classes
   roi_summary = roi_data.groupby('file_name').agg({
       'tree_count': ['mean', 'std'],
       'tree_ratio': ['mean', 'std']
   })
   print(roi_summary)

**8.3 Quality Control**

Check processing quality:

1. **Visual Inspection**: Open stitched images to verify processing quality
2. **Measurement Validation**: Look for outliers or unexpected values
3. **Overlay Verification**: Check that detected features match visual expectations

Common Quality Issues:
- Very high or very low tree counts may indicate processing artifacts
- Check overlay images to ensure features are correctly detected
- Verify that tissue regions are properly segmented

**8.4 Export for Publication**

Prepare results for analysis or publication:

.. code-block:: python

   # Export summary statistics
   summary_stats = roi_data.groupby('ROI_type').agg({
       'tree_ratio': ['mean', 'std', 'count']
   }).round(3)

   summary_stats.to_csv('summary_statistics.csv')

   # Create publication-ready figures
   plt.figure(figsize=(8, 6), dpi=300)
   # Add your plotting code here
   plt.savefig('collagen_analysis_results.png', dpi=300, bbox_inches='tight')

Troubleshooting
---------------

**Common Issues and Solutions:**

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Problem
     - Solution
   * - "OpenSlide not found"
     - Check OpenSlide installation and path
   * - Empty output directories
     - Verify file paths and XML annotation format
   * - Very long processing times
     - Reduce number of processes or image size
   * - Memory errors
     - Close other applications, use fewer processes
   * - No features detected
     - Check image quality and processing parameters

**Getting Help:**

- Check the console output for detailed error messages
- Verify your input data format matches requirements
- Try with smaller test images first
- Visit the `GitHub Issues <#>`_ page for community support

Summary
-------

🎉 **Congratulations!** You've completed the basic c-pmat workflow!

**What You've Learned:**

✅ How to set up c-pmat for analysis
✅ Tile generation from whole slide images
✅ ROI extraction using XML annotations
✅ Image stitching and reconstruction
✅ Quantitative feature extraction
✅ Basic result interpretation

**Key Takeaways:**

- c-pmat provides a complete workflow for pathology image analysis
- Each step builds on the previous one, creating a data processing pipeline
- Quantitative measurements enable objective comparison of tissue samples
- Visual overlays help validate computational results

**Next Steps:**

- Try :doc:`batch_processing` for analyzing multiple slides
- Learn about :doc:`understanding_parameters` to customize analysis
- Explore :doc:`feature_extraction_deep_dive` for advanced morphological analysis
- Check out :doc:`psr_stain_analysis` for specialized collagen analysis

**Your Results:**

You now have:
- Processed image tiles with quality control
- Quantitative measurements of collagen organization
- Visual overlays showing detected morphological features
- Data ready for statistical analysis and publication

Keep experimenting with different parameters to optimize results for your specific research needs!