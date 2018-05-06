from setuptools import setup, find_packages

setup(
    name='VRLatency',
    version='0.1',
    description='A library to measure and analyze the latency of virtual reality system',
    license="MIT",
    author='Mohammad Bashiri',
    author_email='mohammadbashiri93@gmail.com',
    url='https://github.com/mohammadbashiri93/VRLatency',
    packages=find_packages(),

    # required packages
    install_requires=['matplotlib', 'click', 'pyglet', 'ratcave', 'pyserial'],
    #['matplotlib', 'click', 'pyglet', 'ratcave'],

    entry_points=
    '''
        [console_scripts]
        cmd_echo_test = VRLatency.cmd_echo_test:cli
        measure_latency = VRLatency.cmd_api:main
    ''',
)