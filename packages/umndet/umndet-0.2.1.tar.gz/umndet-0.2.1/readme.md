# Python code for IMPRESS+EXACT+IMPISH

## How to install
### From `pypi` (normal use)
- All code, including dependencies needed for plotting:
`python -m pip install 'umndet[all]'`
- Just code, no dependencies
`python -m pip install umndet`

### For development
- Clone the code from [GitHub](https://github.com/umn-impish/umn-detector-code/)
- Go to `python` directory
- Run `python -m pip install '.[all]'`

## How to use
- See the `examples` on GitHub

## Components

### Common code between flight/ground (`umn_detector/common`)
Code containing ways to parse binary data to Python (via `ctypes` and `struct`).

### Ground code
Code that runs on the ground once we get the data.
Used to decode packets into JSON for parsing later on.

### Tools
Useful tools--simulate data and other things.

### Rebinner (used in-flight)
Rebins the science data from IMPRESS into smaller files.

Scripts are defined in `pyproject.toml`. Example:
### Rebin data
```bash
impress-rebinner time+energy data/file-ident-*
```
Will rebin the files given along time and energy axes.

