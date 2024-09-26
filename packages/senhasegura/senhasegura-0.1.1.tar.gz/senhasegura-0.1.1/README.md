# SenhaSegura
## Overview

The A2A module provides an unofficial interface for interacting with the SenhaSegura APIs. This module simplifies the integration of password management functionalities into your applications by offering support for both OAuth1 and OAuth2 authentication methods.
## Features
**Support for HTTP Methods**: Easily make GET, POST, PUT, DELETE, HEAD, OPTIONS, and PATCH requests.
**Hostname Validation**: Ensures that the provided hostname follows standard DNS rules.
**Endpoint Validation**: Validates endpoint strings to prevent malformed URLs.
Dynamic Method Binding: All HTTP methods are dynamically bound, allowing for intuitive usage.
**OAuth Authentication**: Supports **OAuth1** and **OAuth2** for secure API access.
**Error Handling**: Comprehensive error handling for authentication and request parameters.

## Installation

You can use the SenhaSegura using one of the following methods:

pip:
```pip install senhasegura```
Git:
```git clone https://github.com/SrRenks/senhasegura.git```

## Usage

**Initialize the A2A Class**: To create an instance of the A2A module, specify the hostname and authentication parameters:
```
from senhasegura import A2A
import json
with open("oauth1_params.json", "r") as file:
    oauth1_params = json.loads(file.read())
a2a = A2A("senhasegura.construtoratenda.com", "OAuth1", **oauth1_params)
```
**Make API Calls**: Use the instance to call API endpoints with the desired HTTP method:
```
response = a2a.get("/iso/coe/senha", params={"123": 123}, headers={"User-Agent": "example"})
```
**Handle the Response**: You can process the requests.Response as needed:
```
print(response.json())
```

## Example

Here's a complete example of using the A2A module:
```
from senhasegura import A2A
import json

# Load OAuth1 parameters from a JSON file
with open("oauth1_params.json", "r") as file:
    oauth1_params = json.loads(file.read())

# Initialize with your credentials
a2a = A2A("senhasegura.construtoratenda.com", "OAuth1", **oauth1_params)

# Make a GET request
response = a2a.get("/iso/coe/senha", params={"123": 123}, headers={"User-Agent": "example"})

# Print the response
print(response.json())
```
## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or features you would like to see.

## License
This project is licensed under the MIT License. See the LICENSE file for details.