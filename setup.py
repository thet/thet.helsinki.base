from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='thet.helsinki.base',
      version=version,
      description="base plone integration package for radio helsinki",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='plone4, zope',
      author='Johannes Raggam',
      author_email='<raggam-nl@adm.at>',
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
          'PILwoTk',
          'plone.app.caching',
          'collective.setuphandlertools',
          'alm.solrindex',
          #'plone.app.discussion',
          #'plone.formwidget.recaptcha',
          #'collective.autoresizetextarea',
          'collective.disqus',
          'collective.flowplayer',
          'collective.gallery',
          'zettwerk.fullcalendar',
          'Products.LinguaPlone',
          'collective.folderishtypes',
          'collective.folderishtraverse',
          'collective.uploadify',
      ],
)
