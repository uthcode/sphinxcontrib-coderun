# sphinxcontrib-coderun

A Sphinx extension that adds an interactive **Run** button to code files in your
documentation. Powered by a self-hosted [codeapi](https://github.com/nalgeon/codapi)
instance — you bring your own server, this extension wires it into Sphinx.

## How it works

1. You self-host a [codeapi](https://github.com/nalgeon/codapi) server (supports C,
   Python, Go, Rust, and [many more](https://github.com/nalgeon/sandboxes)).
2. You add `.. coderun::` directives to your `.rst` files.
3. When a reader clicks **Run**, the code is sent to your codeapi server, executed in
   an isolated sandbox, and the output appears inline on the page.

Nothing is shared with third-party services — all execution happens on your own
infrastructure.

## Install

```sh
pip install sphinxcontrib-coderun
```

## Configuration

In your `conf.py`:

```python
extensions = [..., "sphinxcontrib.coderun"]

# URL of your self-hosted codeapi instance
coderun_url = "https://codapi.example.com"

# Default sandbox (matches a sandbox configured on your codeapi server)
coderun_sandbox = "gcc"
```

Both settings can be overridden per-directive (see below).

## Usage

Replace `.. literalinclude::` with `.. coderun::` wherever you want a Run button:

```rst
.. coderun:: cprogs/hello.c
   :language: c
```

Override the sandbox or URL for a specific snippet:

```rst
.. coderun:: examples/hello.py
   :language: python
   :sandbox: python
   :url: https://codapi.example.com
```

All standard `literalinclude` options work — `:lines:`, `:linenos:`,
`:emphasize-lines:`, etc.

## Self-hosting codeapi

You need a running codeapi instance that the browser can reach. Quickstart:

```sh
# Pull the server and a sandbox image
docker pull nalgeon/codapi
docker pull codapi/gcc   # or python, go, etc.

# Run the server
docker run -p 1313:1313 -v /path/to/config:/opt/codapi nalgeon/codapi
```

For production deployment (Kubernetes, TLS, rate limiting) see the
[codeapi documentation](https://github.com/nalgeon/codapi/tree/main/docs).

Point `coderun_url` at the public URL of your server and you're done.

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

## License

MIT
