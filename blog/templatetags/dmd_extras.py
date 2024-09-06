import markdown
from markdown.inlinepatterns import LINK_RE, LinkInlineProcessor
from django.urls import reverse
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe


class SlugFieldLinkInlineProcessor(LinkInlineProcessor):
    def getLink(self, data, index):
        href, title, index, handled = super().getLink(data, index)
        if href.startswith("slug"):
            slug = href.split(":")[1]
            relative_url = reverse("markdown-content", args=[slug])
            href = relative_url
        return href, title, index, handled


class SlugFieldExtension(markdown.Extension):
    def extendMarkdown(self, md, *args, **kwargs):
        md.inlinePatterns.register(
            SlugFieldLinkInlineProcessor(LINK_RE, md), "link", 160
        )


def makeExtension(**kwargs):
    return SlugFieldExtension(**kwargs)


register = template.Library()


@register.filter
def render_markdown(value):
    """Converte o conteúdo Markdown para HTML e retorna HTML seguro."""
    md = markdown.Markdown(extensions=["fenced_code", "codehilite"])
    return mark_safe(md.convert(value))
