from setuptools import setup, find_packages

setup(
    name='STITCHED',  # Project name
    version='0.1.0',  # Project version
    author='UZH STITCHED',  # Author's name
    author_email='',  # Author's email
    description='',  # Project description
    long_description=open('README.md').read(),  # Detailed description (usually read from README)
    long_description_content_type='text/markdown',  # Format of the detailed description
    url='https://github.com/Master-Project-Hate-Speech/Data-Pipeline',  # URL of the project homepage
    packages=find_packages(),  # Automatically find all packages in the project
    install_requires=[  # Dependencies required for the project
        # 'requests>=2.0',
        # 'numpy>=1.19.2',
    ],
    classifiers=[  # Project classification information
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',  # License type
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Required Python version
    license='Apache License 2.0',  # License type
    keywords='NLP hate speech pipeline',  # Keywords for the project
    project_urls={  # Additional URLs for the project
        # 'Documentation': 'https://github.com/yourusername/my_project/wiki',
        'Source': 'https://github.com/Master-Project-Hate-Speech/Data-Pipeline'
    },
)
