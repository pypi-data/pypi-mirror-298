# cfgdict
A lightweight dict-like config library with validation support

## Features
- Supports nested dictionary structures
- Provides configuration validation with customizable rules
- Includes utility functions for flattening and reconstructing dictionaries
- Easy-to-use API for creating and managing configurations

## Installation

You can install cfgdict directly from GitHub using pip:

```bash
pip install git+https://github.com/gseismic/cfgdict.git
```

For development installation:

```bash
git clone https://github.com/gseismic/cfgdict.git
cd cfgdict
pip install -e .
```

## Usage

### Creating a Config

```python
from cfgdict import Config

config_schema = [
    dict(field='n_step', required=True, default=3, rules=dict(type='int', gt=0)),
    dict(field='learning_rate', required=True, default=0.1, rules=dict(type='float', gt=0, max=1)),
    dict(field='nest.gamma', required=True, default=0.99, rules=dict(type='float', min=0, max=1)),
    dict(field='nest.epsilon', required=True, default=0.1, rules=dict(type='float', min=0, max=1)),
    dict(field='nest.verbose_freq', required=True, default=10, rules=dict(type='int', gt=0)),
]

cfg_dict = {
    'n_step': 3,
    'learning_rate': 0.1,
    'nest': {
        'gamma': 0.99,
        'epsilon': 0.1,
        'verbose_freq': 10
    }
}

config = Config.from_dict(cfg_dict, schema=config_schema, strict=True)
print(config.to_dict())
```

### Flattening and Unflattening Dictionaries

```python
from cfgdict import flatten_dict, unflatten_dict

nested_dict = {
    'a': 1,
    'b': {
        'c': 2,
        'd': {
            'e': 3
        }
    },
    'f': 4
}

flattened = flatten_dict(nested_dict)
print(f'Flattened: {flattened}')
# Output: {'a': 1, 'b.c': 2, 'b.d.e': 3, 'f': 4}

unflattened = unflatten_dict(flattened)
print(f'Unflattened: {unflattened}')
# Output: {'a': 1, 'b': {'c': 2, 'd': {'e': 3}}, 'f': 4}
```

## Validation Rules

cfgdict supports the following validation rules:

- `type`: Specify field type (e.g., 'int', 'float', 'str', etc.)
- `required`: Whether the field is required (True/False)
- `default`: Default value if not provided

Comparison operators:
- `eq`: Equal to
- `ne`: Not equal to
- `gt`: Greater than
- `ge`: Greater than or equal to
- `lt`: Less than
- `le`: Less than or equal to
- `min`: Minimum value (inclusive)
- `max`: Maximum value (inclusive)

Example usage:

```python
config_schema = [
    dict(field='age', required=True, rules=dict(type='int', ge=18, lt=100)),
    dict(field='score', required=False, default=0, rules=dict(type='float', min=0, max=100)),
    dict(field='status', required=True, rules=dict(type='str', ne='inactive')),
]
```

In this example:
- 'age' must be an integer, greater than or equal to 18, and less than 100
- 'score' is optional with a default of 0, must be a float between 0 and 100 (inclusive)
- 'status' is required and must be a string not equal to 'inactive'

### Nested configurations with logger
set `verbose=True`

cfgdict supports nested configurations:

```python
from cfgdict import Config

nested_schema = [
    dict(field='database.host', required=True, rules=dict(type='str')),
    dict(field='database.port', required=True, rules=dict(type='int', min=1, max=65535)),
    dict(field='api.version', required=True, rules=dict(type='str')),
    dict(field='api.endpoints.users', required=True, rules=dict(type='str')),
    dict(field='api.endpoints.products', required=True, rules=dict(type='str')),
]

nested_config = Config.from_dict({
    'database': {
        'host': 'localhost',
        'port': 5432
    },
    'api': {
        'version': 'v1',
        'endpoints': {
            'users': '/api/v1/users',
            'products': '/api/v1/products'
        }
    }
}, schema=nested_schema, verbose=True)
# verbose=True: log enabled

print(config.to_dict())
```

### Custom Validation Rules
You can extend the validation system with custom rules:

```python
from cfgdict import Config, ConfigValidationError

def validate_even(value):
    if value % 2 != 0:
        raise ConfigValidationError(f"Value {value} is not even")

config_schema = [
    dict(field='even_number', required=True, rules=dict(type='int', custom=validate_even))
]

config = Config.from_dict({'even_number': 4}, schema=config_schema) 
 # Valid
# config = Config.from_dict({'even_number': 3}, schema=config_schema)  # Raises ValidationError
```

## More Examples
For more usage examples, please refer to:
- [tests/test_config.py](./tests/test_config.py)
- [tests/test_utils.py](./tests/test_utils.py)

## Contributing
We welcome issue reports and pull requests. If you have any suggestions or improvements, please feel free to contribute.

## License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
