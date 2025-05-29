from django import forms
from .models import Ad, ExchangeProposal


class AdForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = None

    class Meta:
        model = Ad
        fields = [
            'title', 'description', 'image_url',
            'category', 'condition'
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input roboto-text medium black-text',
                'placeholder': 'Название объявления'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input roboto-text medium black-text large',
                'placeholder': 'Подробное описание товара',
                'rows': 5
            }),
            'image_url': forms.ClearableFileInput(attrs={
                'class': 'form-input roboto-text black-text'
            }),
            'category': forms.Select(attrs={
                'class': 'form-input roboto-text black-text'
            }),
            'condition': forms.Textarea(attrs={
                'class': 'form-input roboto-text black-text',
                'placeholder': 'Описание состояния',
                'rows': 3
            }),
        }


class ExchangeProposalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        self.fields['ad_sender'].queryset = Ad.objects.filter(user=user)
        self.fields['ad_sender'].empty_label = None

        self.fields['ad_receiver'].queryset = Ad.objects.exclude(user=user)
        self.fields['ad_receiver'].empty_label = None

    class Meta:
        model = ExchangeProposal
        fields = ['ad_sender', 'ad_receiver', 'comment']
        widgets = {
            'ad_sender': forms.Select(attrs={
                'class': 'form-input roboto-text black-text',
            }),
            'ad_receiver': forms.Select(attrs={
                'class': 'form-input roboto-text black-text',
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-input roboto-text medium black-text large',
                'placeholder': 'Комментарий к предложению',
                'rows': 5
            }),
        }
