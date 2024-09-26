from django.contrib import admin
from django.utils.translation import gettext_lazy as _

class DynamicFilter(admin.SimpleListFilter):
    title = ""
    template = "dropdown_filters/filters/filter.html"
    parameter_name = ""
    _sort_reverse = False

    def get_queryset(self, request, model_admin):
        """ Override this method in subclasses or pass the queryset logic in here """
        return model_admin.get_queryset(request)

    def get_filter_list(self, queryset):
        """ Override this method to build the filter list """
        raise NotImplementedError("Subclasses must implement get_filter_list()")

    def lookups(self, request, model_admin):
        queryset = self.get_queryset(request, model_admin)
        filter_list = self.get_filter_list(queryset)
        if self._sort_reverse:
            return sorted(filter_list, key=lambda value: value[1], reverse=True)
        else:
            return sorted(filter_list, key=lambda value: value[1])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(**{self.parameter_name: self.value()})
        return queryset

    @property
    def sort_reverse(self):
        return self._sort_reverse
    
    @sort_reverse.setter
    def sort_reverse(self, is_reverse: bool) -> None:
        self._sort_reverse = is_reverse