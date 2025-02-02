
.. image:: https://github.com/nlesc-nano/swan/workflows/build%20with%20conda/badge.svg
   :target: https://github.com/nlesc-nano/swan/actions
.. image:: https://codecov.io/gh/nlesc-nano/swan/branch/main/graph/badge.svg?token=1527ficjjx
   :target: https://codecov.io/gh/nlesc-nano/swan
.. image:: https://zenodo.org/badge/191957101.svg
   :target: https://zenodo.org/badge/latestdoi/191957101
.. image:: https://readthedocs.org/projects/swan/badge/?version=latest
   :target: https://swan.readthedocs.io/en/latest/?badge=latest
	    
#####################################
Screening Workflows And Nanomaterials
#####################################

🦢 **Swan** is a Python pacakge to create statistical models using machine learning to predict molecular properties. See Documentation_.


🛠 Installation
===============

- Download miniconda for python3: miniconda_ (also you can install the complete anaconda_ version).

- Install according to: installConda_.

- Create a new virtual environment using the following commands:

  - ``conda create -n swan``

- Activate the new virtual environment

  - ``conda activate swan``

To exit the virtual environment type  ``conda deactivate``.


.. _dependecies:

Dependencies installation
-------------------------

- Type in your terminal:

  ``conda activate swan``

Using the conda environment the following packages should be installed:


- install RDKit_ and H5PY_:

  - `conda install -y -q -c conda-forge h5py rdkit`

- install Pytorch_ according to this_ recipe

- install `Pytorch_Geometric dependencies <https://github.com/rusty1s/pytorch_geometric#installation>`_.

- install `DGL using conda <https://www.dgl.ai/pages/start.html>`_


.. _installation:

Package installation
--------------------
Finally install the package:

- Install **swan** using pip:
  - ``pip install git+https://github.com/nlesc-nano/swan.git``

Now you are ready to use *swan*.


  **Notes:**

  - Once the libraries and the virtual environment are installed, you only need to type
    ``conda activate swan`` each time that you want to use the software.

.. _Documentation: https://swan.readthedocs.io/en/latest/
.. _miniconda: https://docs.conda.io/en/latest/miniconda.html
.. _anaconda: https://www.anaconda.com/distribution/#download-section
.. _installConda: https://conda.io/projects/conda/en/latest/user-guide/install/index.html
.. _Pytorch: https://pytorch.org
.. _RDKit: https://www.rdkit.org
.. _H5PY: https://www.h5py.org/
.. _this: https://pytorch.org/get-started/locally/
