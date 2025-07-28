.. c-pmat Documentation documentation master file, created by
   sphinx-quickstart on Mon Jul 28 11:33:52 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to c-pmat documentation.
==================================

These step-by-step guides will help you master the complete workflow for analyzing picosirius red stain (PSR) pathology images.
---------------



Getting Started
---------------

If you're new to c-pmat, start with these fundamental tutorials:

.. toctree::
   :maxdepth: 2

   basic_workflow
   understanding_parameters
   working_with_annotations

Image Processing Workflows
--------------------------

Learn about the core image processing capabilities:

.. toctree::
   :maxdepth: 2

   tile_generation
   roi_extraction
   color_normalization
   background_correction

Advanced Analysis
-----------------

Dive deeper into advanced features and customization:

.. toctree::
   :maxdepth: 2

   feature_extraction_deep_dive
   batch_processing
   custom_analysis_pipelines
   performance_optimization

Specialized Topics
------------------

Specialized tutorials for specific use cases:

.. toctree::
   :maxdepth: 2

   psr_stain_analysis
   collagen_quantification
   multi_scale_analysis
   integration_with_other_tools

Troubleshooting
---------------

Common issues and solutions:

.. toctree::
   :maxdepth: 2

   common_problems
   performance_tuning
   debugging_workflows

Tutorial Structure
------------------

Each tutorial follows a consistent structure:

**🎯 Learning Objectives**: What you'll learn
**📋 Prerequisites**: What you need before starting
**⏱️ Estimated Time**: How long the tutorial takes
**📁 Sample Data**: Links to example datasets
**🔧 Step-by-Step Instructions**: Detailed walkthrough
**💡 Tips & Tricks**: Pro tips for better results
**🚨 Troubleshooting**: Common issues and solutions
**🏁 Summary**: Key takeaways

Sample Datasets
---------------

Download sample datasets for the tutorials:

* **Small Dataset** (100MB): Perfect for learning and testing

  - 2 sample slides (.ndpi format)
  - Corresponding XML annotations
  - Expected output examples

* **Medium Dataset** (1GB): For more realistic testing

  - 10 sample slides with various staining patterns
  - Complex annotations with multiple ROI types
  - Benchmark timing data

* **Large Dataset** (5GB): For performance testing

  - 50+ slides for batch processing examples
  - Comprehensive annotation sets
  - Full workflow outputs

Before You Begin
----------------

**Check Your Installation**

Ensure c-pmat is properly installed:

.. code-block:: bash

   python -c "import main; print('c-pmat installation OK')"

**Prepare Your Environment**

Create a dedicated workspace:

.. code-block:: bash

   mkdir c-pmat_tutorials
   cd c-pmat_tutorials
   mkdir data results

**System Requirements Check**

- **RAM**: 8GB minimum (16GB+ recommended)
- **Storage**: 20GB free space for tutorials
- **CPU**: Multi-core processor recommended

**Download Tutorial Data**

.. code-block:: bash

   # Download and extract sample data
   wget https://example.com/c-pmat-tutorial-data.zip
   unzip pmat-tutorial-data.zip

Quick Reference
---------------

**Common File Paths**:

.. code-block:: text

   tutorials/
   ├── data/
   │   ├── slides/          # Input WSI files
   │   ├── annotations/     # XML annotation files
   │   └── expected/        # Expected output examples
   ├── results/
   │   ├── tiles/           # Generated tiles
   │   ├── roi_output/      # ROI extraction results
   │   ├── stitched/        # Stitched images
   │   └── features/        # Extracted features
   └── notebooks/           # Jupyter notebooks

**Key Parameters**:

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - Parameter
     - Typical Values
     - Description
   * - ``file_type``
     - .ndpi, .svs, .tif
     - Input slide format
   * - ``num_processes``
     - 1, 2, 4, 8
     - CPU cores for processing
   * - ``thresh_d``
     - 80, 60, 40, 20
     - Tissue percentage threshold
   * - ``scale``
     - 16, 8, 4
     - Output resolution scaling
   * - ``shape_type``
     - Tree, Branch
     - Feature extraction type

**Common Workflows**:

1. **Basic Analysis**: Tiles → ROIs → Features
2. **Quality Control**: Tiles → Stitching → Visual Inspection
3. **Batch Processing**: Multiple slides in parallel
4. **Custom Analysis**: Modified parameters for specific needs

Next Steps
----------

**Choose Your Path**:

- **New Users**: Start with :doc:`basic_workflow`
- **Experienced Users**: Jump to :doc:`batch_processing`
- **Developers**: Check out :doc:`custom_analysis_pipelines`
- **Troubleshooting**: Visit :doc:`common_problems`

**Community Resources**:

- **GitHub**: Report bugs and request features
- **Documentation**: Complete API reference
- **Examples**: Real-world use cases and code

Happy learning! 🎓
