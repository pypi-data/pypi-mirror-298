from setuptools import setup,find_packages

setup(
    name='py-calendar-entry-management-functions',
    version='0.1.0',
    author='Leon',
    author_email='leonz99@web.de',
    description='A package to store and access calendar entries in a json file .',
    packages=find_packages(),
    install_requires = [
        #'calendar',        #not existing in pip
        'datetime',
        #'json',            #not existing in pip
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)