#
from django.contrib import admin
from django import forms
from django.utils.html import strip_tags
from ckeditor.widgets import CKEditorWidget
from .models import Faq

class FaqAdminForm(forms.ModelForm):
    answer = forms.CharField(widget=CKEditorWidget())
    
    class Meta:
        model = Faq
        fields = '__all__'

    def clean_answer(self):
        answer = self.cleaned_data.get('answer')
        if answer and not strip_tags(answer).strip():
            raise forms.ValidationError("Answer cannot be empty")
        return answer

@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    form = FaqAdminForm
    
    list_display = ('id', 'question', 'get_short_answer', 'has_hindi', 'has_spanish')
    list_display_links = ('id', 'question')
    search_fields = ('question', 'answer', 'question_hi', 'question_esp')
    readonly_fields = ('question_hi', 'answer_hi', 'question_esp', 'answer_esp')
    
    fieldsets = (
        ('English Content', {
            'fields': ('question', 'answer'),
        }),
        ('Hindi Translation', {
            'fields': ('question_hi', 'answer_hi'),
            'classes': ('collapse',),
        }),
        ('Spanish Translation', {
            'fields': ('question_esp', 'answer_esp'),
            'classes': ('collapse',),
        })
    )

    def get_short_answer(self, obj):
        clean_answer = strip_tags(obj.answer)
        return (clean_answer[:75] + '...') if len(clean_answer) > 75 else clean_answer
    get_short_answer.short_description = 'Answer Preview'
    
    def has_hindi(self, obj):
        return bool(obj.question_hi and obj.answer_hi)
    has_hindi.boolean = True
    has_hindi.short_description = 'Hindi'
    
    def has_spanish(self, obj):
        return bool(obj.question_esp and obj.answer_esp)
    has_spanish.boolean = True
    has_spanish.short_description = 'Spanish'