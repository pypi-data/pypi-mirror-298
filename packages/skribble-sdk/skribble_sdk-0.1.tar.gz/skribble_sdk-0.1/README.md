# Skribble SDK

I have created this SDK to make it easier for you to get started with the Skribble API. I myself used the Skribble API in many projects and had to write the same code again and again. So I decided to create a SDK for the Skribble API.

## Features
The current version of the SDK includes the following features:

### **Python SDK**
The Python SDK comes with a fully built SDK that includes:

- Error handling
- Easy to use methods for the most common operations
- Pre-configured connection to the Skribble API
- IntelliSense support for the Skribble API
- Extended documentation with examples

## Tech stack

Skribble SDK is fully open-source built using the following technologies:

**Python**

- [Pydantic](https://pydantic-docs.helpmanual.io/) - for data validation and settings management
- [Requests](https://docs.python-requests.org/en/latest/) - for making HTTP requests
- [Base64](https://docs.python.org/3/library/base64.html) - for encoding and decoding data
- [Typing](https://docs.python.org/3/library/typing.html) - for type hints

## Installation

You can install the Skribble SDK using pip:

```bash
pip install skribble
```

## Basic Usage

Here is a basic example of how to use the Skribble Python SDK to create a signature request:

```python
import skribble

# Replace with your actual API credentials
USERNAME = "your_username"
API_KEY = "your_api_key"

# Initialize the SDK
skribble.init(USERNAME, API_KEY)

# Create a signature request
signature_request = {
    "title": "Test Signature Request",
    "message": "Please sign this test document",
    "file_url": "https://pdfobject.com/pdf/sample.pdf",
    "signatures": [
        {
            "account_email": "signer1@example.com"
        }
    ],
}

create_response = skribble.signature_request.create(signature_request)
print(create_response)
```

For more detailed examples and advanced usage, please refer to the [Examples](../docs/documentation/python/examples.mdx) section in our documentation.