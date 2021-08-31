from setuptools import setup, find_packages
import pathlib

directory_path = pathlib.Path(__file__).parent.resolve()
# Get the long description from the README file
long_description = (directory_path / 'README.md').read_text(encoding='utf-8')
setup(
    name='magicway-payment-gateway',
    version='1.0.0',
    description='MagicWay Payment Gateway',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Arifur Rahman',
    author_email='info@momagicbd.com',
    url='https://github.com/momagicbd/MoMagic-Python',
    keywords='magicway, payment-gateway, e-commerce, shop, local-payment-gateway, international-payment-gateway',
    packages=find_packages(where='.'),
    install_requires=[
        'requests'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: GNU General Public License v3.0',
        'Topic :: Software Development :: Python Package :: Python Modules'
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
)
