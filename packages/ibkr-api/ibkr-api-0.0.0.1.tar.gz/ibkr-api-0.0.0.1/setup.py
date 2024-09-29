from setuptools import setup, find_packages

# with open('README.md', 'r', encoding='utf-8') as f:
#     long_description = f.read()

setup(
    name='ibkr-api',
    version='0.0.0.1',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[

    ],
    author='louisnw',
    license='MIT',
    description="Asynchronous framework for IBKR's new web API.",
    # long_description=long_description,
    # long_description_content_type='text/markdown',
    url='',
)
