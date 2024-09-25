from setuptools import find_packages, setup

# Setup custom import schema
# cortex.__version__
import os
import sys
current = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current)

from base_model_tools import __version__

setup(
    name         = 'base_model_tools',
    version      = __version__,
    packages     = find_packages(exclude=['tests*']),
    author       = 'Nearly Human',
    author_email = 'support@nearlyhuman.ai',
    description  = 'Nearly Human Base Model Tools dependency for training, saving, loading, deploying, and inferencing models.',
    keywords     = 'nearlyhuman, nearly human, model, tools',

    python_requires  = '>=3.8.10',
    install_requires = [
        'mlflow-skinny>=2.8.0',
    ]
)
