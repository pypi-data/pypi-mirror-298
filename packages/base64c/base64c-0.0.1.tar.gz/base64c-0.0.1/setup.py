# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['base64c']

package_data = \
{'': ['*']}

install_requires = \
['setuptools>=75.1.0,<76.0.0']

setup_kwargs = {
    'name': 'base64c',
    'version': '0.0.1',
    'description': 'Fast Base64 encoding/decoding with SSE2 and VSX optimizations',
    'long_description': '# base64c\n\nA faster base64 encoding/decoding library for Python, implemented in C with SSSE3 optimizations.\n\n## Installation\n\n```bash\npip install base64c\n```\n\n## Usage\n\n```python\n\nfrom base64c import b64encode, b64decode\n\nprint(b64encode(b"Hello, World!"))\nprint(b64decode(b64encode(b"Hello, World!")))\n```\n\n## License\n\nMIT\n\n\n\n',
    'author': 'obahamonde',
    'author_email': 'oscar.bahamonde@indiecloud.co',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
