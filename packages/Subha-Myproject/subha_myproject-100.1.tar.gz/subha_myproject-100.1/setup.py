from setuptools import setup, find_packages

setup(
    name='Subha_Myproject',
    version='100.1',
    author='Subha',
    author_email='subhaplatinum@gmail.com',
    description='Basic arithmatic operator modules',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    # url='https://github.com/yourusername/your_project',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
