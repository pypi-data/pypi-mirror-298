from setuptools import setup, find_packages

# Open the README.md file and use it as the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='SVMargin',
    version='1.4',
    description='A package for cost-sensitive multiclass classification that increases the sensitivity of important classes by shifting the decision boundary between them according to a prioritization vector.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Eran Kaufman',
    author_email='erankfmn@gmail.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scikit-learn',
        'tensorflow'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
