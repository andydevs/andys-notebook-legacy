"""
Build notebook site

Author:  Anshul Kharbanda
Created: 10 - 12 - 2020
"""
import os
import glob
import nbconvert
import codecs


# Configuration
notebook_dir = 'notebook'
output_dir = 'docs'


def make_directory():
    """
    Ensure that directory exists
    """
    if not os.path.exists(f'./{output_dir}'):
        os.mkdir(f'{output_dir}')


def build_notebooks():
    """
    Build jupyter notebooks
    """
    # Create exporter
    html = nbconvert.HTMLExporter()
    html.template_name = 'classic'

    # Loop through each file
    for filename in glob.glob(f'{notebook_dir}/*.ipynb'):
        # Get output filename
        name = os.path.basename(filename)
        name = os.path.splitext(name)[0]
        outn = f'{output_dir}/{name}.html'

        # Read file and convert
        body, _ = html.from_filename(filename)

        # Write to file
        # Apparently we have to encode the body
        # manually because the exporter doesn't
        # return a properly encoded body string
        encoded = codecs.encode(body, 'utf-16')
        with open(outn, 'wb+') as out:
            out.write(encoded)


if __name__ == "__main__":
    make_directory()
    build_notebooks()