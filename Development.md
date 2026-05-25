## Development

### Project structure

```
sphinxcontrib-coderun/
├── pyproject.toml
├── LICENSE
├── README.md
└── sphinxcontrib/
    ├── __init__.py               # namespace package
    └── coderun/
        ├── __init__.py           # directive + Sphinx setup()
        └── static/
            └── coderun.css       # Run button styling
```

### Local setup

```sh
git clone https://github.com/uthcode/sphinxcontrib-coderun
cd sphinxcontrib-coderun
pip install -e .
```

To test against a Sphinx project, add to its `conf.py`:

```python
extensions = [..., "sphinxcontrib.coderun"]
coderun_url = "http://localhost:1313"   # local codeapi for dev
coderun_sandbox = "gcc"
```

### Building a distribution

```sh
pip install build twine
python -m build
# produces dist/sphinxcontrib_coderun-X.Y.Z.tar.gz
#          dist/sphinxcontrib_coderun-X.Y.Z-py3-none-any.whl
```

Validate before uploading:

```sh
python -m twine check dist/*
```

### Publishing to PyPI

Create an API token at [pypi.org/manage/account/token](https://pypi.org/manage/account/token/)
scoped to this project, then:

```sh
python -m twine upload dist/*
# Username: __token__
# Password: pypi-AgEI...
```

### Releasing a new version

1. Bump `version` in `pyproject.toml`.
2. Delete `dist/`.
3. Run `python -m build`.
4. Run `python -m twine upload dist/*`.
