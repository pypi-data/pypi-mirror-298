from setuptools import setup, find_packages

setup(
    name="mathias-utilities",
    version="0.8.4",
    description="mathias-utilities ist ein privates Console-Tool, das die Verwaltung und Bearbeitung von Webprojekten sowie Dateien und Ordnern vereinfacht.",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'mathias = mathias_utilities.cli:main',
        ],
    },
    python_requires='>=3.6',
)
