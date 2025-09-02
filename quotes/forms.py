from django import forms
from .models import Quote, Source


class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['source', 'text', 'weight']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned = super().clean()
        source = cleaned.get('source')
        text = cleaned.get('text')

        # Проверка уникальности текста
        if Quote.objects.filter(text=text).exists():
            raise forms.ValidationError("Такая цитата уже есть.")

        if source:
            count = Quote.objects.filter(source=source).count()
            if count >= 3:
                raise forms.ValidationError('У этого источника уже 3 цитаты.')
        return cleaned
    
class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ['name', 'type']