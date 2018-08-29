from setuptools import setup, find_packages

setup(
    name='vrlatency',
    version='0.1',
    description='A python package to measure and analyze the latency of projector-based virtual reality systems',
    license="MIT",
    author='Mohammad Bashiri',
    author_email='mohammadbashiri93@gmail.com',
    url='https://github.com/mohammadbashiri/vrlatency',
    packages=find_packages(),

    # required packages
    install_requires=['numpy', 'matplotlib', 'click', 'pyglet', 'pyserial', 'pandas', 'tqdm'],

    entry_points='''
        [console_scripts]
        measure_latency = vrlatency.cmd_api:cli
    ''',
)
