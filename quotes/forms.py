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
        weight = cleaned.get('weight')

        # Проверка уникальности текста
        if Quote.objects.filter(text=text).exists():
            raise forms.ValidationError("Такая цитата уже есть.")

        if source:
            count = Quote.objects.filter(source=source).count()
            if count >= 3:
                raise forms.ValidationError('У этого источника уже 3 цитаты.')

        if weight is not None and (weight < 1 or weight > 5):
            raise forms.ValidationError('Вес должен быть от 1 до 5.')
        return cleaned
    
class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ['name', 'type']