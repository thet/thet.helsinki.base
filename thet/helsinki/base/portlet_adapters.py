from Acquisition import aq_parent
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from collective.teaser.interfaces import ITeaserAvailable
from zope.interface import implementer

@implementer(ITeaserAvailable)
def main_teaser_available(context, manager):
    if IPloneSiteRoot.providedBy(context) or\
       IPloneSiteRoot.providedBy(aq_parent(context)) and\
       aq_parent(context).getDefaultPage() == context.id:
        # wether plone root or a default page of plone root
        return True
    return False

@implementer(ITeaserAvailable)
def portlet_enabled(context, manager):
    return True

@implementer(ITeaserAvailable)
def portlet_disabled(context, manager):
    return False
