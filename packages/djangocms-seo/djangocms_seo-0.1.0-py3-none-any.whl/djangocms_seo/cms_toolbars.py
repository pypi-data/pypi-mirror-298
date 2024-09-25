from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar
from cms.utils.urlutils import admin_reverse
from django.utils.translation import gettext_lazy as _
from .models import SeoExtension

@toolbar_pool.register
class SeoToolbar(CMSToolbar):
    def populate(self):
        # Add debug information
        print("SeoToolbar populate method called")
        print(f"Is current app: {self.is_current_app}")
        print(f"User permissions: {self.request.user.get_all_permissions()}")

        # Remove the is_current_app check to make it appear on all pages
        if self.request.user.has_perm('cms.change_page'):
            print("User has cms.change_page permission")
            page = self.request.current_page
            if page:
                print(f"Current page: {page}")
                try:
                    seo_extension = SeoExtension.objects.get(extended_object=page)
                except SeoExtension.DoesNotExist:
                    seo_extension = None

                menu = self.toolbar.get_or_create_menu('seo-menu', _('SEO'))
                
                if seo_extension:
                    url = admin_reverse('djangocms_seo_seoextension_change', args=[seo_extension.pk])
                    menu.add_modal_item(_('Edit SEO'), url=url)
                else:
                    url = admin_reverse('djangocms_seo_seoextension_add') + f'?extended_object={page.pk}'
                    menu.add_modal_item(_('Add SEO'), url=url)

                menu.add_sideframe_item(_('SEO Overview'), url=admin_reverse('djangocms_seo_seoextension_changelist'))
            else:
                print("No current page found")
        else:
            print("User does not have cms.change_page permission")