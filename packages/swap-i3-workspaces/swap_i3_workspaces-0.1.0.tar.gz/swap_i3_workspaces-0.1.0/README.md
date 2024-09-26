# Swap workspaces

Swap the current i3 workspace with the specified workspace.

## Install from PyPI
```
pip install swap_i3_workspaces
```

## How to use
The installation step should have automatically created an executable script called swap_i3_workspaces.

```
swap_i3_workspaces
```


## How to build

```
mamba create env -yn swap_i3_workspaces
conda activate swap_i3_workspaces
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
pip install --index-url https://test.pypi.org/simple/ swap_i3_workspaces
```
