# Parcelhub API Client

[![Python](https://img.shields.io/pypi/pyversions/parcelhub-api-client.svg)](https://badge.fury.io/py/parcelhub-api-client)
[![PyPI](https://badge.fury.io/py/parcelhub-api-client.svg)](https://badge.fury.io/py/parcelhub-api-client)
[![PyPI](https://github.com/ChemicalLuck/parcelhub-api-client/actions/workflows/python-publish.yml/badge.svg)](https://github.com/ChemicalLuck/parcelhub-api-client/actions/workflows/python-publish.yml)
![PyPI - Downloads](https://img.shields.io/pypi/dm/parcelhub-api-client)

## Installation

```bash
pip install parcelhub-api-client
```

## Usage

```python
from parcelhub import Parcelhub

client = parcelhub(account_id='XXXXX', access_code='XXXXX')

shipments = client.list_shipments()
```

For more details on the content of the reponses, visit the [official parcelhub API docs](https://api.parcelhub.net/docs/).

## Resources Available

### v1 Tracking API

- List Shipments
- Get Latest Tracking Event
- Get Tracking History
- Search Shipment

## Resources

- [parcelhub API](https://api.parcelhub.net/docs/)

## License

[MIT](LICENSE)
