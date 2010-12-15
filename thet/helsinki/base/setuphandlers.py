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
        {'type': 'Folder', 'title': u'Programm', },
        {'type': 'Folder', 'title': u'Info', },
        {'type': 'Folder', 'title': u'Projekte', },
    ]
    sht.create_item_runner(site, content_structure, logger=logger)

    sht.add_group(site, 'office', roles=['Member'], logger=logger)
    sht.add_group(site, 'programmrat', roles=['Member'], logger=logger)

    sht.add_user(site, 'thet', 'thet',
                 email='johannes@raggam.co.at', fullname="Johannes Raggam",
                 groups=['office'], logger=logger)
