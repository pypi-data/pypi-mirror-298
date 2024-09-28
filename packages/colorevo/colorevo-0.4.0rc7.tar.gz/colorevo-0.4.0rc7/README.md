[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5646732.svg)](https://doi.org/10.5281/zenodo.5646732)


# colorevo

An application to register color changes in regions of interest (ROI) of a video source.

The data source can either be a pre-recorded video file or a live stream from an attached camera. The user can interactively define any number of ROIs of arbitrary shapes for which the evolution of their average [Hue, Saturation and Brightness](https://en.wikipedia.org/wiki/HSL_and_HSV) values will be independently computed and plotted as a function of time. 

The data processing can take place *live* (i.e while the video is being acquired) and/or later on based on the saved video (which allows the user to re-analyze the same data with different ROIs, for example).

The code is Free Software under the [GPL](https://www.gnu.org/licenses/gpl.html), and written in pure [Python](https://www.python.org/). It uses [OpenCV](https://opencv.org/) for accessing the video source. The Graphical user interface is based on [PyQt](https://www.riverbankcomputing.com/software/pyqt/) and [PyqtGraph](http://www.pyqtgraph.org/). The video sources are internally converted and stored with [HDF5](https://www.h5py.org/) and processed with [numpy](https://numpy.org/).


## Install

### Using uv:

1. [Install uv](https://docs.astral.sh/uv/getting-started/installation/)
2. Use uv to install the latest colorevo:
```
uv tool install git+https://gitlab.com/c-p/colorevo.git@master
```

### On a raspberri pi (with raspbian buster):

TODO: re-check the installation instructions for RaspberryPi since these may be outdated

```
sudo apt install python3-opencv python3-pyqtgraph python3-pyqt5 python3-h5py python3-click python3-setuptools python3-numpy
pip3 install --no-deps https://gitlab.com/c-p/colorevo/-/archive/master/colorevo-master.zip
# optional, to add shortcut in desktop:
ln -s ~/.local/bin/colorevo ~/Desktop/colorevo
# optional, to permanently add .local/bin to PATH:
echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc
```

## Launch

```
colorevo
```

## Credits

This software was originally developed for the CROMAPOC project (DPI2015-68917-R) of the Ministerio de Economia y Competitividad (MINECO, Spain)




