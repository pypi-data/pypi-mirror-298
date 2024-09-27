from setuptools import setup, find_packages

setup(
    name='vishwa_data_python',
    version='111.2',
    packages=find_packages(),
    install_requires=[
        # Add your dependencies here
    ],
    description='A Basic arthimetic Operators modules',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Vishwa',
    author_email='vishwa.automationhub@gmail.com',
    #url='https://github.com/your_username/your_project',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Change as necessary
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
