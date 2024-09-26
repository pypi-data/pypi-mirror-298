from setuptools import setup, find_packages

setup(
    name='tangible_shared_models',
    version='1.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django',
        'python-decouple',
        'psycopg2-binary',
        'django-extensions',   
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
    ],
)