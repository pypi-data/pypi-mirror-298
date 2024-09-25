from setuptools import setup, find_packages

setup(
    name='dpgdesigner',
    version='0.0.4',
    author='Matthew Sanchez',
    author_email='xxspicymelonxx@gmail.com',
    description='A designer for dear py gui. Allows you to create dpg apps visually with a UI for making the UI',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    package_data={
        "":["fonts/*.ttf"],
    },
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    install_requires=[
        'dearpygui',
        'screeninfo',
    ],
)
