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
from pathlib import Path

from sosi import read_sos

data = sosi.read_sos(Path(".", "file.sos"))
```
