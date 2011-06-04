from Acquisition import aq_parent
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from collective.teaser.interfaces import IPortletAvailable
from zope.interface import implementer, implements, Interface
from zope.component import adapts
from plone.app.portlets.portlets.navigation import QueryBuilder
from plone.app.layout.navigation.interfaces import INavigationQueryBuilder
from plone.app.portlets.portlets.navigation import INavigationPortlet

@implementer(IPortletAvailable)
def main_teaser_available(portlet, manager, context):
    if IPloneSiteRoot.providedBy(context) or\
       IPloneSiteRoot.providedBy(aq_parent(context)) and\
       aq_parent(context).getDefaultPage() == context.id:
        # wether plone root or a default page of plone root
        return True
    return False

@implementer(IPortletAvailable)
def portlet_enabled(portlet, manager, context):
    return True

@implementer(IPortletAvailable)
def portlet_disabled(portlet, manager, context):
    return False

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

