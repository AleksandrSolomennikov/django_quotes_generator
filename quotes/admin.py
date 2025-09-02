from django.contrib import admin
from .models import Quote, Source
from django import forms

class QuoteAdminForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = '__all__'

    def clean(self):
        cleaned = super().clean()
        source = cleaned.get('source')
        if source and not self.instance.pk:
            if Quote.objects.filter(source=source).count() >= 3:
                raise forms.ValidationError('У этого источника уже 3 цитаты.')
        return cleaned

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    form = QuoteAdminForm
    list_display = ('short_text', 'source', 'weight', 'views', 'likes', 'dislikes', 'created_at')
    list_filter = ('source',)
    search_fields = ('text',)

    def short_text(self, obj):
        return obj.text[:60]
    short_text.short_description = 'Текст'

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'count_quotes')

    def count_quotes(self, obj):
        return obj.quotes.count()
    count_quotes.short_description = 'Цитат'
