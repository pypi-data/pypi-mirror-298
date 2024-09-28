Mapping cell locations via multi-layer regionalization constraints
=========================================================================

Introduction
------------
Resolving spatial cell arrangement is crucial for understanding physiological and pathological processes. While scRNA-seq captures gene expression at single-cell resolution, it loses spatial context, and current spatial transcriptomics methods often compromise on throughput or resolution. Existing integration methods face challenges with accuracy and scalability due to noise from molecular diffusion, cell segmentation errors, and disproportionate cell-type representation. We present CellChIP, an algorithm framework employing multi-layered regional constraints to accurately assign cell locations, enhancing spatial accuracy and resilience to noise. Comparative analysis on benchmark datasets demonstrates CellChIP’s superior accuracy and scalability over existing methods. Applied to liver cancer tissue, CellChIP revealed spatial heterogeneity of cDC cells, a detail missed by deconvolution-based techniques, and achieved cell-cell interaction resolution beyond traditional mapping approaches. Additionally, CellChIP outperforms current techniques in computational efficiency and resource usage, particularly with large-scale stereo-seq data, underscoring its potential for broad application.

.. image:: ./overview.png
  :width: 1200
  :align: center
  :alt: Overview of CellChip

Installation
------------
CellChip can be installed either through GitHub or PyPI.

To install from GitHub:

.. code-block:: bash

    git clone https://github.com/caiquanyou/CellChip
    cd CellChip
    python setup.py install # or pip install .

Alternatively, install via PyPI using:

.. code-block:: bash

    pip install CellChip

Usage
-----
After installation, CellChip can be used in Python as follows:

.. code-block:: python

    import CellChip as cc

Contributing
------------
Contributions to CellChip are welcome. Please refer to the project's issues and pull requests for areas where you can help.

License
-------
(Include license information here if available)

Support and Contact
-------------------
For support or to contact the developers, please use the project's GitHub Issues page.

