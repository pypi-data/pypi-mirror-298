# django-srcdoc

[![PyPI - Version](https://img.shields.io/pypi/v/django-srcdoc.svg)](https://pypi.org/project/django-srcdoc)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-srcdoc.svg)](https://pypi.org/project/django-srcdoc)

-----

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

1. Install django-srcdoc from PyPI:
    ```console
    pip install django-srcdoc
    ```

2. Add django-srcdoc to `INSTALLED_APPS` in your `settings.py`:
    ```python
   INSTALLED_APPS = [
       # ...
       'django_srcdoc',
       # ...
   ]
    ```

## Usage
After installation, use the `{% srcdoc %}` tag much like the `{% filter %}` tag. A brief example:
```html
<iframe srcdoc="{% srcdoc %}{{ some_html_from_your_project }}{% endsrcdoc %}"></iframe>
```
HTML to be escaped could be written by hand, passed in as a variable, or added with an `{% include %}` tag (or any other method you like).

The tag will escape HTML per the [iframe specification](https://html.spec.whatwg.org/multipage/iframe-embed-object.html#an-iframe-srcdoc-document).

## License

`django-srcdoc` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
