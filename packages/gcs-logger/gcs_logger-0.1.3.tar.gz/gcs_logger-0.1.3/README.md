# GCS Logger

This is a simple logger wrapped by a Color Handler to use across GCS projects.

## Installation

```bash
pip install gcs-logger
```
With poetry:

```bash
poetry add gcs-logger
```

## Usage

```python
from gcs_logger import get_gcs_logger

get_logger = get_gcs_logger(__name__, 'DEBUG')
```
