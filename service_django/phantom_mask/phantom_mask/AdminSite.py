from django.apps import apps
from django.contrib import admin
from django.http import Http404
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache

from phantom_mask import settings


class AdminSite(admin.AdminSite):
    @staticmethod
    def have_same_value(a, b):
        try:
            for i in a:
                if i in b:
                    return True
        except:
            return False

    def each_context(self, request):
        context = super().each_context(request)
        app_list = self.get_app_list(request)
        context['app_list'] = app_list
        context['show_close'] = True

        return context

    def index(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}

        context = {
            **extra_context,
            **self.each_context(request),
        }
        # app_list = self.get_app_list(request)
        # extra_context['app_list'] = app_list
        return super().index(request, context)

    def app_index(self, request, app_label, extra_context=None):
        app_dict = self._build_app_dict(request, app_label)
        for app in self.get_app_list(request):
            if app['app_label'] == app_label:
                app_dict = app

        if not app_dict:
            raise Http404('The requested admin page does not exist.')
        # Sort the models alphabetically within each app.
        # app_dict['models'].sort(key=lambda x: x['name'])
        app_name = apps.get_app_config(app_label).verbose_name
        # print("==="), app_label
        # print(app_dict)
        context = {
            **self.each_context(request),
            'title': _('%(app)s administration') % {'app': app_name},
            'app_name': app_name,
            'app_label': app_label,
            'app': app_dict,
            **(extra_context or {}),
        }

        request.current_app = self.name

        return TemplateResponse(request, self.app_index_template or [
            'admin/%s/app_index.html' % app_label,
            'admin/app_index.html'
        ], context)

    @never_cache
    def logout(self, request, extra_context=None):
        super().logout(request)
        return redirect(reverse('admin:login'))


admin_site = AdminSite(name="admin_site")
admin_site.enable_nav_sidebar = False
admin_site.site_header = 'Phantom Mask'
# admin_site.register(User)
# admin_site.register(Group)
if settings.SITE_URL is not None:
    admin_site.site_url = settings.SITE_URL
