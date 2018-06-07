from setuptools import setup, find_packages

setup(
    name='vrlatency',
    version='0.1',
    description='A library to measure and analyze the latency of virtual reality system',
    license="MIT",
    author='Mohammad Bashiri',
    author_email='mohammadbashiri93@gmail.com',
    url='https://github.com/mohammadbashiri93/VRLatency',
    packages=find_packages(),

    # required packages
    setup_requires=['numpy'],
    install_requires=['matplotlib', 'click', 'pyglet', 'pyserial'],

    entry_points='''
        [console_scripts]
        measure_latency = vrlatency.cmd_api:main
    ''',
)
