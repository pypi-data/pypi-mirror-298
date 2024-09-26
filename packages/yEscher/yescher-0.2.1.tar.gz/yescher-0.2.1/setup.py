from setuptools import setup, find_packages

setup(
    name="yEscher",               # Your package name
    version="0.2.1",              # Version of your package
    packages=find_packages(),     # Automatically find and include packages (including submodule)
    package_dir={"": "src"},
    include_package_data=True,    # Include additional files from the submodule
    package_data={
        '': ['etfl/*'],           # Include all files from the etfl submodule
    },
    author='Shyam Sai Bethina',
    author_email='shyamsaibethina@gmail.com',
    url='https://github.com/Shyamsaibethina/yEscher',
    install_requires=[
    'beautifulsoup4>=4.11.1',
    'Bio',
    'bokeh',
    'cobra>=0.25.0',
    'Escher>=1.7.3',
    'gurobipy>=11.0.0',
    'joblib>=1.1.0',
    'numpy>=1.22.4',
    'optlang>=1.5.2',
    'pandas>=1.4.2',
    'pymysql>=1.1.1',
    'pytest>=7.1.2',
    'pytfa>=0.9.4',
    'python-dotenv>=1.0.1',
    'PyYAML>=6.0.2',
    'rdkit>=2024.3.5',
    'Requests>=2.32.3',
    'scikit_learn>=1.0.2',
    'scipy>=1.7.3',
    'setuptools>=61.2.0',
    'sphinx_rtd_theme>=2.0.0',
    'SQLAlchemy>=1.4.37',
    'sympy>=1.10.1',
    'tqdm>=4.64.0',
    ],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4',
    description='Run gene knockouts and analyize S. Cerevisae, built on top of yeastGEM',
    keywords=['yeast', 'escher', 'pytfa','ME models','thermodynamics','flux analysis','expression'],

    license='MIT',

    # See https://PyPI.python.org/PyPI?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Environment :: Console',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.9',
    ],
)
