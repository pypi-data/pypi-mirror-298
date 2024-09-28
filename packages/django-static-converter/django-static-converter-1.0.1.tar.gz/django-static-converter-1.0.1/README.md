

## Description

This package modifies the HTML content of a file by replacing all `<link>` tags' `href` attributes, all `<script>` tags' `src` attributes, and all `<img>` tags' `src` attributes with Django template tags. It also adds `{% load static %}` at the beginning of the file to facilitate efficient static file management.

## Installation

To use this package, simply install it with pip. The `beautifulsoup4` library is included by default, but if you encounter any issues, you can install it separately:

```bash
pip install django-static-converter
```

## Usage

```python

# settings.py
INSTALLED_APPS = [
    # Other apps
    'django_static_converter',
    # Other apps
]

# This will process all HTML files in the 'templates' directory and its subdirectories.
```


## Example

Suppose you have an HTML file named `index.html` that looks like this:


```html
<!DOCTYPE html>
<html>
<head>
    <title>My Website</title>
    <link rel="stylesheet" href="styles.css">
    <script src="script.js"></script>
</head>
<body>
    <h1>Hello, World!</h1>
    <img src="image.png">
</body>
</html>
```

## Running the py manage.py convert-static

## will modify the file to look like this:

```html
{% load static %}
<!DOCTYPE html>
<html>
<head>
    <title>My Website</title>
    <link href="{% static 'styles.css' %}" rel="stylesheet">
    <script src="{% static 'script.js' %}"></script>
</head>
<body>
    <h1>Hello, World!</h1>
    <img src="{% static 'image.png' %}">
</body>
</html>

```

In this modified version, the `<link>`, `<script>`, and `<img>` tags' `href` and `src` attributes have been replaced with Django template tags, and `{% load static %}` has been added to the beginning of the file.

## Parameters

- `directory` (str): The path to the directory containing HTML files to process.

## Returns

None: The function modifies the input files in place.

## Raises

FileNotFoundError: If the input files cannot be found or accessed.

## Authors

- [Pezhman Najafi](https://github.com/pezhman-najafi)
- [Sahel Shiravand](https://github.com/sahel-shiravand)

--- 

Feel free to adjust any sections or details to better fit your project's specifics!