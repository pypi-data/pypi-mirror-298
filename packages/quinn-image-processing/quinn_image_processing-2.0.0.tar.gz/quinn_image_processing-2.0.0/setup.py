from setuptools import setup, find_packages

setup(
    name='quinn_image_processing',  # The name of your package on PyPI
    version='2.0.0',    # Package version
    packages=find_packages(),  # Automatically find packages in the project
    install_requires=[
        'Pillow>=10.0.0',  # Example dependency
    ],
    entry_points={
        'console_scripts': [
            'square-images=quinn_image_processing.script:main',  # Create a command-line tool
            'overlay-images=quinn_image_processing.overlayScript:main',  # Create a command-line tool
        ],
    },
    description='A simple Python package for image processing.',
    long_description=open('README.md').read(),  # Include your README.md as the description
    long_description_content_type='text/markdown',  # Set markdown type for PyPI
    url='https://github.com/brandonq81/imageprocessing',  # Project URL (e.g., GitHub)
    author='Brandon Quinn',
    author_email='brandonq81@gmail.com',
    license='MIT',  # License type
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',  # Specify the minimum Python version
)
