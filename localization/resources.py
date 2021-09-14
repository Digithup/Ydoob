from import_export import resources


from localization.models.models import Country, Area, City, Governorates


class CountryResource(resources.ModelResource):
    class Meta:
        model = Country

class GovernoratesResource(resources.ModelResource):
    class Meta:
        model = Governorates
class CityResource(resources.ModelResource):
    class Meta:
        model = City
class AreaResource(resources.ModelResource):
    class Meta:
        model = Area