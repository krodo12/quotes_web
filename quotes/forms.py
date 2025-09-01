from django import forms
from .models import Quote

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['text', 'source', 'weight']
        widgets = {
            'weight': forms.NumberInput(attrs={
                'type': 'range',
                'min': '1',
                'max': '10',
                'value': '1',
                'oninput': 'this.nextElementSibling.value = this.value'
            })
        }
    def clean(self):
        cleaned_data = super().clean()
        quote = Quote(**cleaned_data)
        quote.full_clean()  # вызывает нашу проверку clean() в модели
        return cleaned_data