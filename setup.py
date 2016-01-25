from setuptools import setup, find_packages

version = '1.0'

setup(
    name='thet.helsinki.base',
    version=version,
    description="Plone integration package for Radio Helsinki Graz",
    long_description=open("README.rst").read(),
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
    ],
    keywords='plone4, zope',
    author='Johannes Raggam',
    author_email='<thetetet@gmail.com>',
    url='https://github.com/thet/thet.helsinki.base',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['thet', 'thet.helsinki'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
        'Plone',
        'Pillow',
        'z3c.jbot',
        'plone.app.caching',
        #'plone.formwidget.recaptcha',
        #'collective.autoresizetextarea',
        'Products.LinguaPlone',
        'collective.folderishtypes',
        'collective.folderishtraverse',
        'collective.folderorder',
        'thet.helsinki.project',
        'collective.gcs',
        'plone.app.contenttypes < 1.2',
        'collective.plonetruegallery',
        'collective.quickupload'
    ],
)
