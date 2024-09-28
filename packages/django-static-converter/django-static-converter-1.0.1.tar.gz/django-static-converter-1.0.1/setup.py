from setuptools import setup, find_packages

# Read the content of README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='django-static-converter',
    version='1.0.1',
    packages=find_packages(),
    author='Pezhman Najafi, Sahel Shiravand',
    author_email='pezhman3500@gmail.com, sahelshiravand@yahoo.com',  # Replace with your actual email
    description='A Django package that automatically converts src and href attributes in HTML templates to Django\'s static template tags, making it easier to manage static files efficiently.',
    long_description=long_description,  # Add long description from README.md
    long_description_content_type="text/markdown",  # Set the content type for the long description
    url="https://github.com/pezhman-najafi, https://github.com/sahel-shiravand ",  # Replace with your actual GitHub repository
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # License used
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'beautifulsoup4',  # Specify dependencies
    ],
)
