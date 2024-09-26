from setuptools import setup, find_packages

setup(
    name='StatsChitran',  # Name of your package
    version='0.3.5',  # Package version
    packages=find_packages(),  # Automatically find sub-packages
    install_requires=[],  # List your dependencies here
    author='Chitran Ghosal',
    author_email='ghosal.chitran@gmail.com',
    description='A collection of few statistical functions in a package for direct use',
    url='https://github.com/yourusername/my_package',  # Your package's URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)