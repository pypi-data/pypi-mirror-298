from setuptools import setup, find_packages

setup(
    name='massdataanalyst',
    version='111.111',
    packages=find_packages(),
    install_requires=[
        # Add your dependencies here
    ],
    description='A brief description of your project',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='vishwa',
    author_email='vishwa.automationhub@gmail.com',
    #url='https://github.com/your_username/your_project',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Change as necessary
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
