CoBRA I/O
=========

CoBRA I/O is an interface to the **C**\ omposable **B**\ enchmark for **R**\ obotics **A**\ pplications `(CoBRA) <https://cobra.cps.cit.tum.de>`_.
With it you can easily upload, download, and interact with CoBRA's robots, tasks and solutions.

.. image:: https://gitlab.lrz.de/tum-cps/cobra-io/badges/main/pipeline.svg
    :target: https://gitlab.lrz.de/tum-cps/cobra-io/-/commits/%main
    :alt: Pipeline Status

.. image:: https://readthedocs.org/projects/cobra-io/badge/?version=latest
    :target: https://cobra-io.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://gitlab.lrz.de/tum-cps/cobra-io/badges/main/coverage.svg
    :target: https://gitlab.lrz.de/tum-cps/cobra-io/-/jobs/artifacts/main/file/ci/coverage/html//index.html?job=coverage&min_acceptable=80&min_good=90
    :alt: Coverage Report


Installation
------------

CoBRA I/O can easily be installed via pip::

    pip install cobra-io

If you want to develop CoBRA I/O, you can clone the repository and install it in editable mode and with developer dependencies::

    git clone https://gitlab.lrz.de/tum-cps/cobra-io.git
    cd cobra-io
    pip install -e .[dev]

Usage
-----

Examples on the usage of CoBRA I/O are provided in the `tutorials <tutorials/>`_ directory and a thorough documentation is available in `doc <doc/>`_ or `online <https://cobra-io.readthedocs.io/en/latest/>`_.
The CoBRA benchmark suite elements are specified on the `documentation subpage of CoBRA <https://cobra.cps.cit.tum.de/crok-documentation/robot>`_.
The CoBRA API is documented `here <https://cobra.cps.cit.tum.de/api/>`_.
CoBRA I/O will generate a configuration file based on the provided `sample <src/cobra/utils/cobra.config.sample>`_; find the currently used with :code:`from cobra.utils.configurations import CONFIG_FILE`.

CoBRA I/O keeps a cached version of all files in CoBRA. To invalidate these caches run :code:`python -m cobra.utils.caches` and follow the instructions.

Support
-------

For software support please use the `issue tracker <https://gitlab.lrz.de/tum-cps/cobra-io/-/issues>`_.
If you have questions with regard to the CoBRA benchmark use the `CoBRA Website <https://cobra.cps.cit.tum.de>`_.

Contributing
------------

Contributions to CoBRA I/O are always welcome.
Source code contributions are made via `merge requests <https://gitlab.lrz.de/tum-cps/cobra-io/-/merge_requests>`_.
Contributions to the benchmark suite are handled via the `CoBRA Website <https://cobra.cps.cit.tum.de>`_.
Please use the provided commit hooks to ensure a consistent code style by installing them :code:`pre-commit install`.
For more details, please refer to our `contribution guidelines <CONTRIBUTING.md>`_.

Authors and acknowledgment
--------------------------
CoBRA I/O is developed at the chair of robotics, artificial intelligence and embedded systems at TU Munich.
It is designed, developed and maintained by Matthias Mayer, Jonathan Külz, and Matthias Althoff.

The developers gratefully acknowledge financial support by the Horizon 2020 EU Framework Project `CONCERT <https://concertproject.eu/>`_.
