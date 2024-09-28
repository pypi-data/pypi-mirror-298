# MrLou Modules

## Overview
The `MrLou_modules` is a collection of Python package that I keep re-using and thought would be good to share them

## Contributing
If you would like to contribute to this project, please fork the repository and submit a pull request with your changes. Ensure that your code follows the existing style and includes appropriate tests.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Installation

You can install the package from PyPI using pip:

```
pip install MrLou_modules
```

# Random_Message

## Overview

The `Random_Message` in `MrLou_modules` is a Python package that provides a collection of random messages, including fun facts and jokes. 
This package is designed to be easy to use and integrate into your Python projects to add a touch of randomness and fun.
I'm using it in script that takes a bit long to complete so printing out those messages keep me awake

## Usage
To use the package in your Python script, follow these steps:

1. Import the necessary function:

```
from MrLou_modules.Random_Message.random_message import get_random_message
```

2. Get a random message:

```
message = get_random_message()
print(message)
```

The `get_random_message` function will alternately return a joke or a fun fact each time it is called.

## Example
Here’s a simple example of how to use `MrLou_modules`:

```
from MrLou_modules.Random_Message.random_message import get_random_message

# Print a random message
print(get_random_message())
```

### Functions
- `get_random_message()`: Returns a random message, alternating between jokes and fun facts.

### Modules
- `fun_facts.py`: Contains a list of interesting and random fun facts. Example facts include:

- `jokes.py`: Contains a list of light-hearted programming jokes. Example jokes include:

- `random_message.py`: Provides the get_random_message function that alternates between fun facts and jokes.

## Cyberark

The `cyberark_api` is a collection of one API for now :-)
The `variables.py` contain all the configuration values such as URIs, certificate paths, and usernames
the `cyberark_api.py` has one class with a function `get_credentials` that you can use to pull credential stored in Cyberark

## Example
Here’s a simple example of how to use `MrLou_modules`:

```
from MrLou_modules.cyberark_api import CyberArkAPI

cyberark_api = CyberArkAPI()
credentials = cyberark_api.get_credentials()

if credentials:
    print(f"Username: {credentials['Username']}")
    print(f"Password: {credentials['Password']}")
    print(f"Password Change In Process: {credentials['PasswordChangeInProcess']}")
```