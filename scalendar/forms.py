from django import forms
from django.utils.translation import ugettext_lazy as _
from scalendar.widgets import WorkdaysWidget

class ScalendarForm(forms.ModelForm):
    workdays = forms.fields.IntegerField(min_value=0, initial=31, label=_('Work-days'), widget=WorkdaysWidget())
