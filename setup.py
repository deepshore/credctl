from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='credctl',
    version='0.0.1',
    description='credctl',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/deepshore/credctl',
    author='Malte Groth',
    author_email='malte.groth@deepshore.de',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='cli, kubernetes',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6, <4',
    install_requires=['click', 'kubernetes'],
    entry_points={
        'console_scripts': [
            'credctl=credctl.cli:main'
        ],
    }
)
