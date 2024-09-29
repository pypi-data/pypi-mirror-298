from setuptools import setup, Extension
from Cython.Build import cythonize

# Define the extension module using your .pyx file
extensions = [
    Extension("trex_id", ["trex_id.pyx"])
]

setup(
    name="trex_id",
    version="0.2.0",
    description="A Cython-based ID generation library using a secure and fast unique ID generation technique.",
    author="Aviad Korakin",
    author_email="aviad825@gmail.com",
    license="MIT",
    ext_modules=cythonize(extensions, compiler_directives={'language_level': "3"}),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
)