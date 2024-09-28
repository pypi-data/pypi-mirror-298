# Mantle SDK Documentation

## Generate the RST files

From the root directory of the SDK repo:
```
sphinx-apidoc -o docs/source mantlebio -e -P --force
```


## Generate the HTML

from the /docs folder:

```
make clean
make html
```