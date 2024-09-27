from setuptools import setup, find_packages

setup(
    name='Lunara',
    version='0.1.0',
    packages=find_packages(),
    description='''For an easy understanding of this module, please check the documentation at https://github.com/sapkota-coder/Lunara. 
    We plan to create a website in the future for updates. Stay tuned!''',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Ankit',
    author_email='sapkotasa8@gmail.com',
    url='https://github.com/sapkota-coder/Lunara',  # Link to your GitHub repo
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
