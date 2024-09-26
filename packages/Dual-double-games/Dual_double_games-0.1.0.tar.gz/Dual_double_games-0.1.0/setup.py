from setuptools import setup, find_packages

setup(
    name='Dual_double_games',
    version='0.1.0',
    author='Matt',
    author_email='matthew.alsop@dci-student.org',
    description='A package containing two games, hangman, rock_paper_scissors.',
    packages=find_packages(),
    install_requires=[
        'colorama',
        'datetime',
        'timedelta',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)