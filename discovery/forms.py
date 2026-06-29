from django import forms
from core.models import Company, Location


class DiscoveryRunForm(forms.Form):
    company = forms.ModelChoiceField(label='Firma', queryset=Company.objects.filter(is_active=True).order_by('name'))
    location = forms.ModelChoiceField(label='Lokasyon', queryset=Location.objects.none(), required=False)
    cidr = forms.CharField(label='IP Aralığı', initial='192.168.1.0/24', help_text='Örnek: 192.168.7.0/24')
    scan_tcp = forms.BooleanField(label='TCP Port Taraması', required=False, initial=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].widget.attrs.update({'class': 'form-select noc-input'})
        self.fields['location'].widget.attrs.update({'class': 'form-select noc-input'})
        self.fields['cidr'].widget.attrs.update({'class': 'form-control noc-input', 'placeholder': '192.168.7.0/24'})
        self.fields['scan_tcp'].widget.attrs.update({'class': 'form-check-input'})
        company_id = self.data.get('company') or self.initial.get('company')
        if company_id:
            self.fields['location'].queryset = Location.objects.filter(company_id=company_id, is_active=True).order_by('name')
        else:
            self.fields['location'].queryset = Location.objects.filter(is_active=True).order_by('company__name', 'name')
