from setuptools import setup, find_packages

setup(
    name='AIDSTK',
    version='0.2.0',
    description='A modular and flexible AI library for processing text data',
    author='Alex Mendoza',
    author_email='alexander.mendoza.am@gmail.com',
    url='https://github.com/amendoxa/AIDSTK',
    packages=find_packages(),
    install_requires=[
        'langchain_community',
        'pandas',
        'tqdm',
    ],
    include_package_data=True,
    package_data={
        'AIDSTK': ['prompts/*.txt', 'configs/*.json'],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
