from django.contrib import admin
from .models import MetaTag, OpenGraphMeta, TwitterCardMeta, SeoExtension
from cms.extensions import PageExtensionAdmin


@admin.register(MetaTag)
class MetaTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'content')
    search_fields = ('name', 'content')
    list_filter = ('name',)


@admin.register(OpenGraphMeta)
class OpenGraphMetaAdmin(admin.ModelAdmin):
    list_display = ('property', 'content')
    search_fields = ('property', 'content')
    list_filter = ('property',)


@admin.register(TwitterCardMeta)
class TwitterCardMetaAdmin(admin.ModelAdmin):
    list_display = ('name', 'content')
    search_fields = ('name', 'content')
    list_filter = ('name',)


class MetaTagInline(admin.TabularInline):
    model = SeoExtension.meta_tags.through
    extra = 1


class OpenGraphMetaInline(admin.TabularInline):
    model = SeoExtension.og_meta.through
    extra = 1


class TwitterCardMetaInline(admin.TabularInline):
    model = SeoExtension.twitter_meta.through
    extra = 1


class SeoExtensionAdmin(PageExtensionAdmin):
    inlines = [MetaTagInline, OpenGraphMetaInline, TwitterCardMetaInline]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('extended_object')


admin.site.register(SeoExtension, SeoExtensionAdmin)
