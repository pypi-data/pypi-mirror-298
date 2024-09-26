# Filtro Dinámico para Django Admin

Este filtro dinámico para Django Admin permite crear filtros reutilizables y altamente configurables, evitando la necesidad de crear una nueva clase para cada filtro específico. Se puede personalizar su lógica mediante herencias y sobrescribir métodos clave.

## Clase Base: `DynamicFilter`

La clase `DynamicFilter` es una clase base que proporciona la infraestructura para crear filtros personalizados de forma más eficiente. 

### Atributos Personalizables

- **`title`**: Define el título que aparecerá en la interfaz de administración.
- **`template`**: La ruta del template HTML para personalizar la apariencia del filtro.
- **`parameter_name`**: El nombre del parámetro que será filtrado.
- **`sort_reverse`**: Indica si los elementos del filtro deben ordenarse en orden inverso (por defecto es `False`).

### Métodos Sobrescribibles

- **`get_queryset(request, model_admin)`**: Devuelve el conjunto de datos que se utilizará para generar las opciones del filtro. Se puede sobrescribir en las subclases para ajustar la lógica del queryset.
- **`get_filter_list(queryset)`**: Debe implementarse en las subclases. Se encarga de construir la lista de valores que aparecerán en el filtro. Esta lista debe ser una lista de tuplas `[(value, human-readable)]`.
- **`lookups(request, model_admin)`**: Devuelve la lista de opciones que aparecerán en el filtro. Por defecto, esta lista se genera a partir del método `get_filter_list()`.
- **`queryset(request, queryset)`**: Filtra el queryset original en base al valor seleccionado en el filtro.

### Propiedades

- **`sort_reverse`**: 
  - **Getter**: Devuelve el estado actual de si la lista de opciones está ordenada en reversa.
  - **Setter**: Permite establecer si la lista debe ordenarse en reversa.

## Ejemplo de Uso

Aquí hay un ejemplo de cómo heredar de `DynamicFilter` para crear un filtro específico:

```python
from django.utils.translation import gettext_lazy as _
from my_custom_filters.filters import DynamicFilter

class InstallationNameFilter(DynamicFilter):
    title = _("By Installation name")
    template = "dropdown_filters/filters/filter.html"
    parameter_name = 'id__exact'
    
    def get_queryset(self, request, model_admin):
        client_selected = request.GET.get('installation_client__organization_ptr__exact')
        if client_selected:
            return model_admin.get_queryset(request).filter(installation_client__organization_ptr=client_selected)
        return model_admin.get_queryset(request)

    def get_filter_list(self, queryset):
        return [(installation.id, installation.installation_name) for installation in queryset]
