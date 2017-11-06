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
            'plot-total-times=tools.total_times:main',
            'plot-avg-times=tools.avg_times:main',
        ],
    }
)
