# setup.py
from setuptools import setup
from Cython.Build import cythonize

setup(
    name="trex_id",  # The name of your package
    version="0.1",  # The initial release version
    description="A Cython-based ID generation library using a secure and fast unique ID generation technique.",
    author="Aviad Korakin",  # Your name
    author_email="your.email@example.com",  # Your email
    ext_modules=cythonize("trex_id.pyx", compiler_directives={'language_level': "3"}),  # Compile the Cython code
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)