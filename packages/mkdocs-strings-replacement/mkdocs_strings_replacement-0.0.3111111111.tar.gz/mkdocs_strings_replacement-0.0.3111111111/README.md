# mkdocs-strings-replacement

[![PyPI][pypi-version-badge-link]][pypi-link]
[![License][license-image]][license-link]

Mkdocs Markdown strings replacement plugin.

## Installation

```bash
pip install mkdocs-strings-replacement
```

## Documentation

### Setup

Enable the plugin in your `mkdocs.yml`:

```yaml
plugins:
  - mkdocs-strings-replacement:
      strings_replacements:
        - old_value: "This string will be replaced"
          new_value: "with this string"
```

[pypi-link]: https://pypi.org/project/mkdocs-strings-replacement
[pypi-version-badge-link]: https://img.shields.io/pypi/v/mkdocs-strings-replacement?logo=pypi&logoColor=white
[license-image]: https://img.shields.io/pypi/l/mkdocs-strings-replacement?color=light-green&logo=apache&logoColor=white
[license-link]: https://github.com/innersource-nn/midgard-mkdocs-plugins/blob/main/mkdocs-strings-replacement-plugin/LICENSE