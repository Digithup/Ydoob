import django
from django.contrib.admin import RelatedFieldListFilter
from django.contrib.admin.widgets import SELECT2_TRANSLATIONS
from django.urls import reverse, NoReverseMatch
from django.utils.datastructures import OrderedSet
from django.utils.translation import get_language


def get_request():
    """Walk the stack up to find a request in a context variable."""
    import inspect

    frame = None
    try:
        for f in inspect.stack()[1:]:
            frame = f[0]
            code = frame.f_code
            if code.co_varnames and "context" in code.co_varnames:
                return frame.f_locals["context"]["request"]
    finally:
        del frame


class AutocompleteListFilter(RelatedFieldListFilter):
    """Admin list_filter using autocomplete select 2 widget."""

    template = "admin/filter_autocomplete.html"

    def has_output(self):
        """Show the autocomplete filter at all times."""
        return True

    @staticmethod
    def get_admin_namespace():
        request = get_request()
        return request.resolver_match.namespace

    def get_url(self):
        if django.VERSION > (3, 2):
            return self.get_generic_url()

        remote_model = self.field.related_model
        args = (
            self.get_admin_namespace(),
            remote_model._meta.app_label,
            remote_model._meta.model_name,
        )
        return reverse("%s:%s_%s_autocomplete" % args)

    def get_generic_url(self):
        try:
            return reverse("admin:autocomplete")
        except NoReverseMatch:
            pass

        namespace = self.get_admin_namespace()
        return reverse("%s:autocomplete" % namespace)

    def field_choices(self, field, request, model_admin):
        # Do not populate the field choices with a huge queryset
        return []

    def choices(self, changelist):
        """
        Get choices for the widget.
        Yields a single choice populated with template context variables.
        """
        url = self.get_url()

        placeholder = "PKVAL"
        query_string = changelist.get_query_string(
            {self.lookup_kwarg: placeholder}, [self.lookup_kwarg_isnull]
        )

        lookup_display = None
        if self.lookup_val:
            instance = self.field.related_model.objects.get(pk=self.lookup_val)
            lookup_display = str(instance)

        model = self.field.model

        yield {
            "url": url,
            "selected": self.lookup_val,
            "selected_display": lookup_display,
            "query_string": query_string,
            "query_string_placeholder": placeholder,
            "query_string_all": changelist.get_query_string(
                {}, [self.lookup_kwarg, self.lookup_kwarg_isnull]
            ),
            # Data attrs required for Django 3.2+
            "app_label": model._meta.app_label,
            "model_name": model._meta.model_name,
            "field_name": self.field.name,

    }

class AutocompleteFilterMixin:
    @property
    def media(self):
        media = super().media

        i18n_file = None
        i18n_name = SELECT2_TRANSLATIONS.get(get_language(), None)
        if i18n_name:
            i18n_file = "admin/js/vendor/select2/i18n/%s.js" % i18n_name

        extra_js = [
            "admin/js/vendor/jquery/jquery.js",
            "admin/js/vendor/select2/select2.full.js",
        ]
        if i18n_file:
            extra_js.append(i18n_file)
        extra_js.extend(
            [
                "admin/js/jquery.init.js",
                "admin/js/autocomplete.js",
                "admin/js/autocomplete_filter.js",
            ]
        )
        extra_css = [
            "admin/css/vendor/select2/select2.css",
            "admin/css/autocomplete.css",
        ]
        if django.VERSION >= (2, 2, 0, "final", 0):
            media._js_lists.append(extra_js)
            media._css_lists.append({"screen": extra_css})
        else:
            media._js = OrderedSet(extra_js + media._js)
            media._css.setdefault("screen", [])
            media._css["screen"].extend(extra_css)
        return media