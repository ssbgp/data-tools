from setuptools import setup, find_packages

setup(
    name='ssbgp-data-tools',
    version='0.1',
    description='Set of tools to process data obtained from the SS-BGP routing '
                'simulator',
    url='',
    license='MIT',
    author='David Fialho',
    author_email='fialho.david@protonmail.com',

    packages=find_packages(),

    entry_points={
        'console_scripts': [
            'plot-times=tools.plot_times:main',
            'basic-data=tools.basic_data:main',
        ],
    }
)
