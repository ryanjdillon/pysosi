# pysosi

Library for reading Kartverket SOSI files to GeoJSON

This is a work in progress and not developed by Kartverket--use with caution.

# Install

```
python3.8 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install git@github.com:ryanjdillon/pysosi.git
```

# Quickstart


```
import sosi
filename = './path-to-file/file.sos'
data = sosi.read_sos(filename)
```

# TODO

* Generalize for 3+ levels using an `h5py` container rather than a `dict()` as the data structure
* Generalize to handle duplicate keys
    * currently handling specifically for `NØ`
* Initialize `keys` list with number of # keys equal to number of levels
    * Currently just making the list large "enough" (i.e. (10,))
