from setuptools import setup, find_packages

setup(
    name='pageweaver',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'pylatex',
        'argparse'
    ],
    entry_points={
        'console_scripts': [
            'pageweaver=pageweaver.novel_crawler_service:main',
        ],
    },
    author='Krishnatejaswi S, Sridhar D Kedlaya',
    author_email='shentharkrishnatejaswi@gmail.com, sridhardkedlaya.cs21@rvce.edu.in',
    description='A web crawler to fetch web novel chapters and generate a PDF.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/KTS-o7/pageweaver.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)