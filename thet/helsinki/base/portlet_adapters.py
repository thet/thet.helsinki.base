from Acquisition import aq_parent
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from collective.teaser.interfaces import IPortletAvailable
from zope.interface import implementer, implements, Interface
from zope.component import adapts
from plone.app.layout.navigation.interfaces import INavigationQueryBuilder
from Products.CMFCore.utils import getToolByName
from plone.app.layout.navigation.root import getNavigationRoot
from plone.app.portlets.portlets.navigation import INavigationPortlet
from Products.CMFPlone import utils

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


class NavtreeQueryBuilder(object):
    implements(INavigationQueryBuilder)
    adapts(Interface, INavigationPortlet)

    def __init__(self, context, portlet):
        self.context = context
        self.portlet = portlet
        portal_properties = getToolByName(context, 'portal_properties')
        navtree_properties = getattr(portal_properties, 'navtree_properties')
        portal_url = getToolByName(context, 'portal_url')

        query = {}

        currentPath = '/'.join(context.getPhysicalPath())
        query['path'] = {'query' : currentPath, 'navtree' : 1}

        topLevel = portlet.topLevel
        if topLevel and topLevel > 0:
            query['path']['navtree_start'] = topLevel + 1

        # Abuse includeTop for portlet_type filter
        if not portlet.includeTop:
            # Only list the applicable types
            query['portal_type'] = utils.typesToList(context)
        else:
            query['portal_type'] = [
                    'Document',
                    'Folder',
                    'Folderish Document',
                    'Folderish Event',
                    'Folderish News Item',
                    'Link',
                    'Project',
                    'File']

        # Apply the desired sort
        sortAttribute = navtree_properties.getProperty('sortAttribute', None)
        if sortAttribute is not None:
            query['sort_on'] = sortAttribute
            sortOrder = navtree_properties.getProperty('sortOrder', None)
            if sortOrder is not None:
                query['sort_order'] = sortOrder

        # Filter on workflow states, if enabled
        if navtree_properties.getProperty('enable_wf_state_filtering', False):
            query['review_state'] = navtree_properties.getProperty('wf_states_to_show', ())

        self.query = query

    def __call__(self):
        return self.query

