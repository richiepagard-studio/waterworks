from django.forms import Select

import django_filters

from apps.technicians.models import Technician, SkillLevelChoice


class TechnicianFilter(django_filters.FilterSet):
    """
    Search filter on technicians.
    """
    skill_level = django_filters.ChoiceFilter(
        choices=SkillLevelChoice.choices,
        widget=Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = Technician
        fields = ("skill_level",)
