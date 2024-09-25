# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['EFL',
 'EFL.aggregators',
 'EFL.data_structures',
 'EFL.files',
 'EFL.model',
 'EFL.node',
 'EFL.operations',
 'EFL.simulation',
 'EFL.utils']

package_data = \
{'': ['*']}

install_requires = \
['datasets>=2.17.0',
 'numpy==1.26.4',
 'scikit-learn>=1.4',
 'timm>=1.0.8',
 'torch>=2.2.0',
 'torchvision>=0.1.5']

setup_kwargs = {
    'name': 'clustered-fl',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Clustered-Federated-Learning\nA shared library for performing experiments on Clustered Federated Learning, published as a part of the paper by M.K.Zuziak, R.Pellungrini and S.Rinzivillo: One-Shot Clustering for Federated Learning\n',
    'author': 'Maciej Krzysztof Zuziak',
    'author_email': 'maciej.k.zuziak@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
