from setuptools import setup
from setuptools.config import read_configuration  

config = read_configuration("setup.cfg")
args = {'version': config['metadata']['version']}


if __name__ == "__main__":

    setup(**args)
