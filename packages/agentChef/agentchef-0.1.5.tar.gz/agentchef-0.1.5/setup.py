from setuptools import setup, find_packages

setup(
    name='agentChef',
    version='0.1.5',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'pandas',
        'requests',
        'pyarrow',
        'pyyaml',
        'huggingface_hub',
        'datasets',
        'PyGithub',
        'wikipedia',
        'arxiv',
        'tqdm',
        'colorama',
    ],
    entry_points={
        'console_scripts': [
            'agentChef=agentChef.cli:cli',
        ],
    },
    package_data={
        'agentChef': ['templates/*.json'],
    },
    author='Leo Borcherding',
    author_email='borchink@gmail.com',
    description='A tool for collecting, processing, and generating datasets for AI training',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/leoleojames1/agentChef',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)