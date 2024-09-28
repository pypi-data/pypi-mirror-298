[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5646732.svg)](https://doi.org/10.5281/zenodo.5646732) ![PyPI - License](https://img.shields.io/pypi/l/colorevo) 
![PyPI - Version](https://img.shields.io/pypi/v/colorevo) 

# colorevo

A Graphical User Interface to register color changes in regions of interest (ROI) of a video source.

The data source can either be a pre-recorded video file or a live stream from an attached camera. The user can interactively define any number of ROIs of arbitrary shapes for which the evolution of their average [Hue, Saturation and Brightness](https://en.wikipedia.org/wiki/HSL_and_HSV) values will be independently computed and plotted as a function of time. 

The data processing can take place *live* (i.e while the video is being acquired) and/or later on based on the saved video (which allows the user to re-analyze the same data with different ROIs, for example).

The code is Free Software under the [GPL](https://www.gnu.org/licenses/gpl.html), and written in pure [Python](https://www.python.org/). It uses [OpenCV](https://opencv.org/) for accessing the video source. The Graphical user interface is based on [PyQt](https://www.riverbankcomputing.com/software/pyqt/) and [PyqtGraph](http://www.pyqtgraph.org/). The video sources are internally converted and stored with [HDF5](https://www.h5py.org/) and processed with [numpy](https://numpy.org/).


## Install

### Using uv (recommended):

1. Install `uv` (follow the [official installation instructions](https://docs.astral.sh/uv/getting-started/installation/))
2. Use uv to install the latest release of colorevo:
    ```
    uv tool install colorevo
    ```

> **Tip:** to install the latest development version, replace `colorevo` by `git+https://gitlab.com/c-p/colorevo.git@master` in the previous command


### Using pip
1. Create a python virtual environment (e.g. with `conda`, or `pyhon -m venv` or ...) and activate it.
2. Run `pip install colorevo`

## Launch
Run: 
```
colorevo
```

## Credits

This software was originally developed for the CROMAPOC project (DPI2015-68917-R) of the Ministerio de Economia y Competitividad (MINECO, Spain)




