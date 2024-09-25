from django.db import models
from cms.extensions import PageExtension
from cms.extensions.extension_pool import extension_pool
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe
from .utils import META_TAG_NAMES, OG_PROPERTY_NAMES, TWITTER_CARD_PROPERTIES

from textwrap import indent

class MetaTag(models.Model):
    name = models.CharField(_("Meta name"),choices=META_TAG_NAMES, max_length=100)
    content = models.CharField(_("Meta content"), max_length=255)

    class Meta:
        verbose_name = _("Meta Tag")
        verbose_name_plural = _("Meta Tags")

    def __str__(self):
        return f"{self.name}: {self.content}"

class OpenGraphMeta(models.Model):
    property = models.CharField(_("OG property"), choices=OG_PROPERTY_NAMES, max_length=100)
    content = models.CharField(_("OG content"), max_length=255)

    class Meta:
        verbose_name = _("Open Graph Meta")
        verbose_name_plural = _("Open Graph Meta")

    def __str__(self):
        return f"{self.property}: {self.content}"

class TwitterCardMeta(models.Model):
    name = models.CharField(_("Twitter Card name"), choices=TWITTER_CARD_PROPERTIES, max_length=100)
    content = models.CharField(_("Twitter Card content"), max_length=255)

    class Meta:
        verbose_name = _("Twitter Card Meta")
        verbose_name_plural = _("Twitter Card Meta")

    def __str__(self):
        return f"{self.name}: {self.content}"

class SeoExtension(PageExtension):
    meta_tags = models.ManyToManyField(MetaTag, related_name='seo_extensions', blank=True)
    og_meta = models.ManyToManyField(OpenGraphMeta, related_name='seo_extensions', blank=True)
    twitter_meta = models.ManyToManyField(TwitterCardMeta, related_name='seo_extensions', blank=True)

    def __str__(self):
        return f"SEO for {self.extended_object}"

    def get_seo_html(self):
        html = []

        # Generate meta tags
        for meta in self.meta_tags.all():
            html.append(f'<meta name="{meta.name}" content="{meta.content}">')

        # Generate Open Graph tags
        for og in self.og_meta.all():
            html.append(f'<meta property="og:{og.property}" content="{og.content}">')

        # Generate Twitter Card tags
        for twitter in self.twitter_meta.all():
            html.append(f'<meta name="twitter:{twitter.name}" content="{twitter.content}">')

        # Indent the HTML for pretty printing
        pretty_html = indent('\n'.join(html), prefix='    ')

        # Return as safe HTML
        return mark_safe(f'\n{pretty_html}\n')

extension_pool.register(SeoExtension)