from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from .models import *

@plugin_pool.register_plugin
class HelloPlugin(CMSPluginBase):
    model = Hello
    name = _("Hello Plugin")
    render_template = "hello_plugin.html"
    cache = False

    def render(self, context, instance, placeholder):
        context = super(HelloPlugin, self).render(context, instance, placeholder)
        return context

class EmployeeCustomPlugin(CMSPluginBase):
    model = Employee_Custom_Plugin
    name = _('User Data')
    render_template = "ViewData.html"
    
    fieldsets = (
        (None, {
            'fields': (
                'items_per_page',
            )
        }),
    )
    
    def render(self, context, instance, placeholder):
        employee = Employee.objects.all().order_by('-id')[:instance.items_per_page]
        context['employees'] = employee
        context = super(EmployeeCustomPlugin, self).render(context, instance, placeholder)
        context.update({
            'latest_event': Employee_Custom_Plugin.objects.order_by('-fname').all()[:3],
            'placeholder': placeholder
        })

        return context


class ProductCustomPlugin(CMSPluginBase):
    model = Product_Custom_Plugin
    name = _('Product Data')
    render_template = "ProductData.html"

    fieldsets = (
        (None, {
            'fields': (
                'items_per_page',
            )
        }),
    )

    def render(self, context, instance, placeholder):
        product = Product.objects.all().order_by('-id')[:instance.items_per_page]
        context['products'] = product
        context = super(ProductCustomPlugin, self).render(context, instance, placeholder)
        return context


plugin_pool.register_plugin(EmployeeCustomPlugin)
plugin_pool.register_plugin(ProductCustomPlugin)