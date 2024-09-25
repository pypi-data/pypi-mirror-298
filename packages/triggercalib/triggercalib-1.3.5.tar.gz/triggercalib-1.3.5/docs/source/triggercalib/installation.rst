Installing TriggerCalib
=======================================================

TriggerCalib can be installed from PyPI (`triggercalib <https://pypi.org/project/triggercalib/>`_) with

.. code-block::

    pip install triggercalib

This will also install all of the dependencies **except** for ``ROOT``, so it is advised that you add TriggerCalib to an environment already containing ``ROOT``.


Installing TriggerCalib for local development
-------------------------------------------------------

The TriggerCalib repository can be installed for local development:

#. Clone the repository
#. Source ``LbEnv``:
   
   .. code-block::
    
     source /cvmfs/lhcb.cern.ch/lib/LbEnv

#. Create a virtual environment:
   
   .. code-block::
    
     lb-conda-dev virtual-env default/2024-06-08 .venv

#. Install the packages required for development:
   
   .. code-block::

     .venv/run pip install -r requirements-dev.txt
