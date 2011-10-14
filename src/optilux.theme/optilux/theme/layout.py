from zope.component import getMultiAdapter
from zope.component import queryMultiAdapter
from zope.component import queryUtility

from plone.portlets.interfaces import IPortletManagerRenderer
from plone.portlets.interfaces import IPortletManager

from plone.app.layout.globals.layout import LayoutPolicy
from plone.memoize.view import memoize

class OptiluxLayoutPolicy(LayoutPolicy):
    @memoize
    def have_portlets(self, manager_name, view=None):
        if manager_name != 'plone.leftcolumn':
            force_disable = self.request.get(
                'disable_' + manager_name, None)
            if force_disable is not None:
                return not bool(force_disable)

        # The rest of this method is a copy of the Plone 4 default
        # implementation
        
        context = self.context
        if view is None:
            view = self

        manager = queryUtility(IPortletManager, name=manager_name)
        if manager is None:
            return False

        renderer = queryMultiAdapter((context, self.request, view, manager), IPortletManagerRenderer)
        if renderer is None:
            renderer = getMultiAdapter((context, self.request, self, manager), IPortletManagerRenderer)

        return renderer.visible

    def bodyClass(self, template, view):
        bodyClass = super(OptiluxLayoutPolicy,self).bodyClass(template, view)

        if not self.have_portlets('plone.rightcolumn', view):
            bodyClass += ' noRightColumn'

        return bodyClass
