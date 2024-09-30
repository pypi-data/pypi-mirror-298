from setuptools import setup, find_packages
import pathlib

# Get the long description from the README file
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='oban_classifier',  # Your package name
    version='0.1.86',
    description='Oban Classifier: A Skorch-based flexible neural network for binary and multiclass classification',
    long_description=README,  # This will use the content from README.md
    long_description_content_type="text/markdown",  # Ensure it renders markdown properly on PyPI
    author='Dr. Volkan OBAN',
    author_email='volkanobn@gmail.com',
    #url='https://github.com/yourusername/oban_classifier',  # Your project URL
    packages=find_packages(),  # Automatically find all packages
    install_requires=[
        'numpy',
        'pandas',
        'scikit-learn',
        'skorch',
        'torch',
    ],
     classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
],
    python_requires='>=3.8',  # Minimum Python version
)
