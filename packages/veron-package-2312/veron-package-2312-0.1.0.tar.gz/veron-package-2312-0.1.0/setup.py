from setuptools import setup, find_packages


setup(
    name='veron-package-2312',
    version='0.1.0',
    author='Veronika Krasilia',
    author_email='veronika_krasilia@epam.com',
    description='A basic hello package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://gitbud.epam.com/veronika_krasilia',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    license='MIT',
    install_requires=[
    ],
)
