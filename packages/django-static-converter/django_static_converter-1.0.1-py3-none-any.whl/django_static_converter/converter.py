import os
from bs4 import BeautifulSoup

def convert_html_files(templates_dir):
    # Traverse the templates directory
    for root, dirs, files in os.walk(templates_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                convert_file(file_path)

def convert_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if the content contains a DOCTYPE, and if so, remove it
    if content.lower().startswith('<!doctype'):
        content = content.split('\n', 1)[1]  # Remove the first line (doctype)

    # Parse the rest of the HTML content with BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')

    # Add {% load static %} at the top of the file if not present
    if not soup.find(text="{% load static %}"):
        content = "{% load static %}\n" + content

    # Update img, script, and link tags
    for tag in soup.find_all(['img', 'script', 'link']):
        if tag.name == 'img':
            src = tag.get('src')
            if src:
                tag['src'] = "{% static '" + src + "' %}"
        elif tag.name in ['script', 'link']:
            src = tag.get('src') or tag.get('href')
            if src:
                if tag.name == 'script':
                    tag['src'] = "{% static '" + src + "' %}"
                else:
                    tag['href'] = "{% static '" + src + "' %}"

    # Rebuild the final content
    final_content = str(soup.prettify())

    # Add the correct {% load static %} followed by <!doctype html>
    final_content = '{% load static %}\n<!doctype html>\n' + final_content

    # Write the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(final_content)

