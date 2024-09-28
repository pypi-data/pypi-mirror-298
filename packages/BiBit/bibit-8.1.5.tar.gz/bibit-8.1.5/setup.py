from setuptools import setup, find_packages

setup(
    name='BiBit',
    version='8.1.5',
    author='Your Name',
    author_email='your.email@example.com',
    description='A brief description of your package.',
    long_description=open('README.md').read(),  # Assuming you have a README.md file
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/BiBit',  # Replace with your actual URL
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Adjust license as necessary
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify the minimum Python version
    install_requires=[
        # List your package dependencies here
        # 'package_name',
    ],
    entry_points={
        'console_scripts': [
            'bibit=your_module:main',  # Adjust to your main function
        ],
    },
)
