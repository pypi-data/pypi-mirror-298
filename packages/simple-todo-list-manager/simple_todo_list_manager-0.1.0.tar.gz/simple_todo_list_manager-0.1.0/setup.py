from setuptools import setup, find_packages

setup(
    name='simple_todo_list_manager',
    version='0.1.0',
    author='Friederike Lessmoellmann',
    author_email='friederike.lessi@eweb.de',
    description='A package to create a simple To-Do list, save it as JSON file and manage it.',
    packages=find_packages(),
    install_requires=[
        'pathlib',
        'string-color',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)