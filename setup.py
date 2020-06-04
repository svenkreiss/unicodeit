from setuptools import setup


# extract version from __init__.py
with open('unicodeit/__init__.py', 'r') as f:
    VERSION_LINE = [l for l in f if l.startswith('__version__')][0]
    VERSION = VERSION_LINE.split('=')[1].strip()[1:-1]


setup(
    name='unicodeit',
    version=VERSION,
    packages=[
        'unicodeit',
    ],
    license='',
    description='Converts LaTeX tags to unicode',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Sven Kreiss',
    author_email='research@svenkreiss.com',
    url='https://github.com/svenkreiss/unicodeit',

    install_requires=[
        'six',
    ],
    extras_require={
        'dev': [
            'pytest',
            'pylint',
        ],
    },
)
