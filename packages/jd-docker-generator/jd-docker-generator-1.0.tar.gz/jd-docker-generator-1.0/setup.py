from setuptools import setup

setup(
    name="jd-docker-generator",  # Name of your package
    version="1.0",               # Version number
    py_modules=["main"],         # List of modules to include
    install_requires=["Jinja2"], # Dependencies required by your package
    entry_points={
        'console_scripts': [
            'jd-docker-create = main:main',  # CLI command and entry point
        ],
    },
    python_requires='>=3.6',    # Specify the Python version requirement
)
