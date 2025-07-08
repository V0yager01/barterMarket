from django.forms import (ModelForm,
                          Textarea,
                          TextInput,
                          Select)

from .models import Ad, ExchangeProposal


class AdForm(ModelForm):
    class Meta:
        model = Ad
        fields = ['title',
                  'description',
                  'image_url',
                  'category',
                  'condition']
        widgets = {
            'title': TextInput(attrs={'class':'form-control'}),
            'description': Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': Select(attrs={'class':'form-control'}),
            'condition': Select(attrs={'class':'form-control'}),
            'image_url': TextInput(attrs={'class': 'form-control'})
        }


class ExchangeProposalForm(ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['ad_sender',
                  'comment']
        widgets = {
            'ad_sender': Select(attrs={'class': 'form-control'}),
            'comment': Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['ad_sender'].queryset = Ad.objects.filter(user=user)
