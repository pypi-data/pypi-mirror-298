from setuptools import setup,find_packages

setup(
	name='luhn_abstract',
	version='0.1.0',
	author='',
	author_email='',
	description='luhn_abstract is a Python module for automatically generating an abstract from a document using unsupervised techniques.  The Luhn paper was published in 1958, and the general concept of the algorithm is outlined in the diagram below.',
	packages=find_packages(),
	classifiers=[
		'Programming Language :: Python :: 3',
		'Operating System :: OS Independent',
	],
	python_requires='>=3.6',
)