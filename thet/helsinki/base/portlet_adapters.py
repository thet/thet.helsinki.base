from Acquisition import aq_parent
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from collective.teaser.interfaces import IPortletAvailable
from zope.interface import implementer

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
