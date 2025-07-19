from setuptools import setup, find_packages

setup(
    name='osal',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # Add your dependencies here
    ],
    authors=[
        {
            "name" : "Kisejjere Rashid",
            "email" : "rashidkisejjere0784@gmail.com"
        },
        {
            "name" : "Magala Reuben",
            "email" : "magalareuben@gmail.com"
        }
    ],
    description='A Python package for Text-to-Speech and Text Generation based on the OSAL models.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Uganda-lang/OSAL',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
