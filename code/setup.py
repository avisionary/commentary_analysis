import setuptools
with open('README.md', 'r') as f:
    long_description = f.read()
setuptools.setup(
name="commentary_analysis",
version='0.0.1',
author='Avi Arora',
author_email='aa2464@georgetown.edu',
description='Insert description here', long_description=long_description, long_description_content_type='text/markdown', packages=setuptools.find_packages(), python_requires='>=3.6',
)