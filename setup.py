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
        # BASE
        'Plone',
        'Pillow',
        'plone.app.theming',
        'plone.resource',

        # PROJECT
        'thet.helsinki.project',

        # EXTRA
        # 'collective.autoresizetextarea',
        # 'plone.formwidget.recaptcha',
        'collective.folderishtraverse',
        'collective.folderishtypes',
        'collective.folderorder',
        'collective.gcs',
        'plone.app.caching',
        'z3c.jbot',

        # NEW
        'collective.plonetruegallery',
        'collective.quickupload',
        'collective.proxytype',
    ],
)
