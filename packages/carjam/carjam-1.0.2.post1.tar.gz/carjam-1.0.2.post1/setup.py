from setuptools import setup, find_packages

setup(
    name='carjam',
    version='1.0.2.post1',
    description='Unoffical Python API for CarJam NZ',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/kianz20/CarJam-API',
    author='Kian Jazayeri',
    author_email='kianja02@gmail.com',
    packages=find_packages(exclude=["tests"]),
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", 
        "Operating System :: OS Independent",
    ],
)