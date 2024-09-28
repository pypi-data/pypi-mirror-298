from setuptools import setup
with open("README.md", "r") as fh:
    readme = fh.read()
setup(
    name = 'uml_django',
    version = '0.0.1',
    author = 'Pedro Vieira',
    author_email = 'pedrophdv8@outlook.com',
    packages = ['uml_django'],
    url = 'https://github.com/Pedro-V8/uml-django',
    project_urls = {
        'Código fonte': 'https://github.com/Pedro-V8/uml-django',
        'Download': 'https://github.com/Pedro-V8/uml-django/archive/0.0.1.zip'
    },
    install_requires=['django' , 'plantuml' , 'six'],
    description = 'A UML Generator for Django and Django Rest Framework projects',
    long_description=readme,
    long_description_content_type="text/markdown",
    license = 'MIT',
    keywords = 'generator converter convert UML Django Rest Framework',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Portuguese (Brazilian)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Internationalization',
        'Topic :: Scientific/Engineering :: Physics'
    ]
)