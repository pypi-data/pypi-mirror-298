# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['parldl']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.7,<9.0.0', 'requests>=2.32.3,<3.0.0']

entry_points = \
{'console_scripts': ['parldl = parldl.__main__:main']}

setup_kwargs = {
    'name': 'parldl',
    'version': '0.1.0',
    'description': 'Download files parallely from a list of URLs in a file',
    'long_description': '# Parldl\n\nDownload files parallely from a list of URLs in a file.\n\n## Installation\n\n###### Recommended\n\n```bash\npipx install parldl\n```\n(To install pipx click [here](https://github.com/pypa/pipx#install-pipx))\n\n###### or\n\n```bash\npip install parldl\n```\n\n#### Or upgrade by:\n\n```bash\npipx upgrade parldl\n```\n\n###### or\n\n```bash\npip install --upgrade parldl\n```\n\n## Usage\n\n1. Create a file containing a list of URLs, one URL per line.\n2. Run `parldl` with the path to the file as an argument.\n3. `parldl` will download the images and save them in a directory provided or in "pardl-downloads" by default.\n\n## Example\n\n```bash\nparldl image_urls.txt output_dir\n```\n\n```bash\nparldl image_urls.txt\n```\n\n```\nUsage: parldl [OPTIONS] [URL_FILE] [OUTPUT_DIR]\n\n  Download files parallely from a list of URLs in a file\n\nOptions:\n  -i, --input PATH            File containing newline-separated URLs\n  -o, --output PATH           Output directory path\n  -m, --max-attempts INTEGER  Maximum number of download attempts\n  -p, --parallel INTEGER      Maximum number of parallel downloads\n  --help                      Show this message and exit.\n```\n\n# Install from source\n\nPoetry is required. For installation click [here](https://python-poetry.org/docs/#installation).\n\nDownload the source and install the dependencies by running:\n\n  ```bash\n  git clone https://github.com/aqdasak/parldl.git\n  cd parldl\n  poetry install\n  ```\n\n### Run\n\nIn the source folder containing pyproject.toml\n\n```bash\npoetry shell\n```\n\nthen cd into the folder containing url file and execute:\n\n```bash\nparldl <url_file> <output_dir>\n```\n\n## License\n\nThis project is licensed under the MIT License.\n',
    'author': 'Aqdas Ahmad Khan',
    'author_email': 'aqdasak@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/aqdasak/parldl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
