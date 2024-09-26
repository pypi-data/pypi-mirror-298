from setuptools import setup, find_packages

setup(
    name='nilgiri_python',
    version='1.0.1',
    author='Priya',
    author_email='priyasenthil1712@gmail.com',
    description='An Automation tool with Python like Nilgiri',
    packages=find_packages(),
    install_requires=[
        'playwright',
        'pytest',
        'behave',
        # Add any other dependencies your framework needs
    ],
    entry_points={
        'console_scripts': [
            'nilgiri_pyhton=nilgiri_python.main:main',  # Entry point for your tool
        ],
    },
)