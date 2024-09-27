from setuptools import setup, find_packages

setup(
    name='netpeakPsel',  # Netpeak Parser Sitewide external links
    version='0.1.0',  # Версия
    description='A tool for parsing external links from specific sections of a website (header, footer, nav, aside).',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Masik',
    author_email='v.krasovskyi@netpeak.net',
    url='https://github.com/VsevolodKrasovskyi/netpeakPsel',  # Repo
    license='MIT',  # License
    packages=find_packages(),  # All package
    install_requires=[  # requires
        'requests',
        'beautifulsoup4',
        'lxml',
        'tqdm',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimal py version
)
