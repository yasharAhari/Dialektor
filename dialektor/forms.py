from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from dialektor.models import Researcher, User

class ResearcherSignUpForm(UserCreationForm):
    inst_name = forms.CharField(label='Institution Name', max_length=200, required=True)
    inst_addr = forms.CharField(label='Institution Address', max_length=100, required=True)
    inst_city = forms.CharField(label='Institution City', max_length=100, required=True)
    inst_country = forms.CharField(label='Institution Country', max_length=100, required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_research = True
        user.save()
        researcher = Research.objects.create(user=user)
        researcher.inst_name.add(*self.cleaned_data.get('inst_name'))
        researcher.inst_addr.add(*self.cleaned_data.get('inst_addr'))
        researcher.inst_city.add(*self.cleaned_data.get('inst_city'))
        researcher.inst_country.add(*self.cleaned_data.get('inst_country'))
        return user
