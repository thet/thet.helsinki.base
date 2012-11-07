from zope.interface import implements, Interface
from zope.component import adapts
from plone.app.portlets.portlets.navigation import QueryBuilder
from plone.app.layout.navigation.interfaces import INavigationQueryBuilder
from plone.app.portlets.portlets.navigation import INavigationPortlet
from plone.app.layout.navigation.root import getNavigationRoot


class CustomQueryBuilder(QueryBuilder):
    implements(INavigationQueryBuilder)
    adapts(Interface, INavigationPortlet)

    def __init__(self, context, portlet):
        super(CustomQueryBuilder, self).__init__(context, portlet)
        if portlet.name == 'navigation-projekte':
            self.query['sort_on'] = 'end'
            self.query['sort_order'] = 'reverse'
            self.query['portal_type'] = [
                'Document', 'Folder', 'Link', 'Project', 'File',
                'Folderish Document', 'Folderish Event',
                'Folderish News Item']

        rootPath = getNavigationRoot(context, relativeRoot=portlet.root)
        if portlet.name == 'navigation-main':
            # navtree not 1 for sitemap like expanded trees
            self.query['path'] = {'query': rootPath}
