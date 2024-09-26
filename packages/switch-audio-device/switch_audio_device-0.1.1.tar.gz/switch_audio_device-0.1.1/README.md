# Switch Audio Device

Creates a [rofi](https://github.com/davatorium/rofi) menu to select primary audio device on machines running Pulse Audio for managing their audio. No need to have rofi installed on the system for this to work.

## Install from PyPI
```
pip install switch_audio_device
```

## How to use
The installation step should have automatically created an executable script called switch_audio_device.

```
switch_audio_device
```


## How to build

```
mamba create env -yn switch_audio_device
conda activate switch_audio_device
pip install build twine
python3 -m build
```

## Install from local tree

```
pip install .
```

##  Upload to PyPI
```
twine upload dist/*
```
## Upload to test PyPI
```
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

## Install from test PyPI
```
pip install --index-url https://test.pypi.org/simple/ your-package-name
```
