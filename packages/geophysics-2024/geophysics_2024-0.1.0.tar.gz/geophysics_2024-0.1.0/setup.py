from setuptools import setup, find_packages

setup(
    name='geophysics_2024',  # Replace with your package's name
    version='0.1.0',
    description='introduction_to_geophysics',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Pongthep',
    author_email='pongthep.t@gmail.com',
    url='https://github.com/PongthepGeo/pip_geophysics_24.git',  # GitHub URL
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)