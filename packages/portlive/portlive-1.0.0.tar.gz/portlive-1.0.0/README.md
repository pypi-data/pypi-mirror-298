# Overview

`portlive` facilitates installation and usage of python modules from the same script. You can install them in one line and use them on the next.

### Usage

```python
# import the portlive method
>>> from portlive import portlive

# use it with `with` keyword
>>> with portlive(modules=['wrapper-bar.wrapper'], aliases=['wrapper']) as pl:
...     # I know that there is a Wrapper class inside the `wrapper-bar.wrapper` module
...     # I would have used this following import normally:
...     # from wrapper_bar.wrapper import Wrapper
...     wrapper_class = pl.wrapper.Wrapper()
...     # Portlive created a property named `wrapper`
...     # which is an alias for `wrapper-bar.wrapper`.
```

### Installation

Install using `pip`.

```bash
pip install portlive
```

### Issues

Submit any issues found or feature request [here](https://github.com/d33p0st/portlive/issues).

### Pull Requests

Submit pull requests [here](https://github.com/d33p0st/portlive/pulls).