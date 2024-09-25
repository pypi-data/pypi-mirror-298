# IsaacSim for OmniGibson

This package provides IsaacSim dependencies for OmniGibson, ensuring compatibility with Linux x86_64 Ubuntu 20.04 (GLIBC 2.31) and Python 3.10.

## Description

IsaacSim for OmniGibson is a package that installs the necessary IsaacSim components required to run OmniGibson simulations. It simplifies the process of setting up the IsaacSim environment by automatically downloading and installing the required packages from NVIDIA's PyPI repository.

## How to Update Version
1. Look up the package version in `pypi.nvidia.org` for each dependency, and copy the version number to `ISAAC_SIM_PACKAGES` in `setup.py`.
2. At the bottom of the `setup.py` file update the package version to match the Isaac Sim version.
3. Push your changes to GitHub
4. Go to the releases tab, click Create a new release
5. Click on the Choose A Tag button and enter a version tag that matches the Isaac Sim version exactly, click the Create button below it.
6. Do **NOT** enter a release name or info - you need to JUST enter the version as the tag.
7. Click Publish Release.
8. Monitor the PyPI release through the actions tab 

**Important notes for updates:**
- If you make changes to the `CustomInstallCommand` class or add new dependencies, make sure to test the installation process on both Linux and Windows systems.
- To ensure the update functions correctly, create a new conda environment and run `pip install ..` After installation, verify that running `isaacsim` in terminal operates as intended.

## Installation for Users

Once the package is uploaded to PyPI, users can install it using: ```pip install isaacsim-for-omnigibson```

## More Information

For more information on installing Isaac Sim using pip, please visit the [official Isaac Sim documentation](https://docs.omniverse.nvidia.com/isaacsim/latest/installation/install_python.html).

## License

Please refer to the license information provided by NVIDIA for IsaacSim components.

## Support

For issues related to OmniGibson, please visit the [OmniGibson GitHub repository](https://github.com/StanfordVL/OmniGibson).

For IsaacSim-specific issues, please refer to the NVIDIA IsaacSim support channels.
