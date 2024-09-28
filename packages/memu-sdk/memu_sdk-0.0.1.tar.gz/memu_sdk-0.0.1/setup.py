from setuptools import setup, find_packages

setup(
    name='memu-sdk',
    version='0.0.1',
    author='Juan Fernando Lavieri',
    author_email='juan.f.lavieri@memu.life',
    description='MeMu SDK for medical-focused tasks with FHIR compliance.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Medical-Multimodal/MeMu_Package.git',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'openai',
        'psycopg2',  # for PostgreSQL
        'fhir.resources',  # FHIR-compliance
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
