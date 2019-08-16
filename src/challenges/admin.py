from django.contrib import admin
from django import forms
from django.forms.widgets import TextInput
from django.forms.models import BaseInlineFormSet
from .models import Challenge, Answer
from bible.models import BibleChapter, BibleVerse
from django.utils.html import format_html

def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper

class AnswerInlineFormSet(BaseInlineFormSet):
    def _construct_form(self, i, **kwargs):
        form = super(AnswerInlineFormSet, self)._construct_form(i, **kwargs)
        form.empty_permitted = False
        return form

    def clean(self):
        # get forms that actually have valid data
        count = 0
        correct = 0
        for form in self.forms:
            try:
                if form.cleaned_data:
                    count += 1
                    if form.cleaned_data.get('correct'):
                        correct += 1
            except AttributeError:
                # annoyingly, if a subform is invalid Django explicity raises
                # an AttributeError for cleaned_data
                pass
        if count < 2:
            raise forms.ValidationError('You must have at least two answers')
        if correct < 1:
            raise forms.ValidationError('You must have at least one correct answer')

class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 0
    min_num = 2
    formset = AnswerInlineFormSet

class ChallengeAdminForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = '__all__'
        widgets = {
            'reward_color': TextInput(attrs={'type': 'color'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_verse = cleaned_data.get("start_verse")
        end_verse = cleaned_data.get("end_verse")

        if end_verse is not None and start_verse is not None and end_verse.index < start_verse.index:
            raise forms.ValidationError('End verse should be greater than or equal to start verse')

class ChallengeAdmin(admin.ModelAdmin):
    form = ChallengeAdminForm
    list_display = ('group', 'active_date', 'verse', 'reward')
    list_filter = (
        ('group__name', custom_titled_filter('group name')),
        'active_date',
        ('start_verse__chapter__book__name', custom_titled_filter('book name')), 
    )
    inlines = [
        AnswerInline,
    ]

    def verse(self, obj):
        if obj.start_verse == obj.end_verse:
            return "{}:{} {}".format(obj.start_verse.index, obj.start_verse.chapter.index, obj.start_verse.chapter.book.name)
        else:
            return "{}-{}:{} {}".format(obj.start_verse.index, obj.end_verse.index, obj.start_verse.chapter.index, obj.start_verse.chapter.book.name)
    
    def reward(self, obj):
        return format_html(
            '<span style="color: {};">{}</span>',
            obj.reward_color,
            obj.reward_name,
        )

admin.site.site_header = 'Evangelion Administration'
admin.site.register(Challenge, ChallengeAdmin)