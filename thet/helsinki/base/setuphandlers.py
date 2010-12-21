# -*- coding: utf-8 -*-
#
# GNU General Public License (GPL)
#
__author__ = """Johannes Raggam <johannes@raggam.co.at>"""
__docformat__ = 'plaintext'

import collective.setuphandlertools as sht
import logging
logger = logging.getLogger("thet.helsinki.base")

def setup_content(context):
    if sht.isNotThisProfile(context, 'thet.helsinki.base-setup_content.txt'):
        return

    site = context.getSite()

    sht.delete_items(site, ('front-page', 'news', 'events'), logger)

    content_structure = [
        {'type': 'Folder', 'title': u'Programm', 'childs': [
                {'type': 'Folderish Document', 'title':u'Tagesansicht'},
                {'type': 'Folderish Document', 'title':u'Wochenansicht'},
                {'type': 'Folderish Document', 'title':u'Sendungen'},
                {'type': 'Folderish Document', 'title':u'SendungsmacherInnen'},
                {'type': 'Folderish Document', 'title':u'Tipps'},
                {'type': 'Folderish Document', 'title':u'Programmschienen'},
                {'type': 'Folderish Document', 'title':u'Programmflyer'},
        ]},
        {'type': 'Folder', 'title': u'Info', 'childs': [
            {'type': 'Folderish Document', 'title':u'Über uns', 'childs':[
                {'type': 'Folderish Document', 'title':u'Charta der freien Radios'},
                {'type': 'Folderish Document', 'title':u'Geschichte'},
                {'type': 'Folderish Document', 'title':u'Gremien'},
                {'type': 'Folderish Document', 'title':u'Presse'},
            ]},
            {'type': 'Folderish Document', 'title':u'Mitmachen', 'childs':[
                {'type': 'Folderish Document', 'title':u'UnterstützerInnen'},
            ]},
            {'type': 'Folderish Document', 'title':u'Downloads'},
            {'type': 'Link', 'title':u'Wiki',
                'data':{'remoteUrl':u'https://intranet.helsinki.at/wiki/'}
            },
            {'type': 'Folderish Document', 'title':u'Kontakt'},
        ]},
        {'type': 'Folder', 'title': u'Projekte', 'childs':[
                {'type': 'Topic', 'title':u'Aktuelles'},
                {'type': 'Topic', 'title':u'Kommendes'},
                {'type': 'Topic', 'title':u'Vergangenes'},
        ]},
    ]
    sht.create_item_runner(site, content_structure, logger=logger)

    sht.add_group(site, 'office', roles=['Member'], logger=logger)
    sht.add_group(site, 'programmrat', roles=['Member'], logger=logger)

    sht.add_user(site, 'thet', 'thet',
                 email='johannes@raggam.co.at', fullname="Johannes Raggam",
                 groups=['office'], logger=logger)
