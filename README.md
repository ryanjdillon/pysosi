# sosi

A utility for reading SOSI-Formatted data from Karverktet to a `python` dictionary.

This is a work in progress so that I may use the higher quality border data for
Norway from Kartverktet--available at http://data.kartverket.no/download.
  
# Install

The plan is to make this a package installable via `pip` for use with plotting
libraries such as `cartopy`, but for now you can just clone the code, or
download it as a `.zip` file, to a location in your `PYTHONPATH`.

```
git clone git@github.com:ryanjdillon/sosi.git
```

# Quickstart

You can use the utility within your own code or `IPython` as follows:

```
import sosi
filename = './path-to-file/file.sos'
data = sosi.read_sos(filename)
```
The plan is to also make this a script which can be run from the commandline to convert files to `.shp` files and other formats. Stay tuned.

# Author

Ryan J. Dillon

# License

GNU General public license - version 3

# TODO

* Generalize for 3+ levels using an `h5py` container rather than a `dict()` as the data structure
* Generalize to handle duplicate keys
    * currently handling specifically for `NØ`
* Initialize `keys` list with number of # keys equal to number of levels
    * Currently just making the list large "enough" (i.e. (10,))
