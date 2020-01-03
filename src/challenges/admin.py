from django.contrib import admin
from django import forms
from django.forms.widgets import TextInput
from django.forms.models import BaseInlineFormSet
from .models import Challenge, Answer
from users.models import Group
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
            raise forms.ValidationError(
                'You must have at least one correct answer')


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

    def clean_group(self):
        if self.user.service_group is not None and self.user.service_group != self.cleaned_data["group"]:
            raise forms.ValidationError(
                "You can only add challenges to group {}".format(self.user.service_group.name))
        return self.cleaned_data["group"]

    def clean(self):
        cleaned_data = super().clean()
        start_verse = cleaned_data.get("start_verse")
        end_verse = cleaned_data.get("end_verse")

        if end_verse is not None and start_verse is not None and end_verse.index < start_verse.index:
            raise forms.ValidationError(
                'End verse should be greater than or equal to start verse')


class GroupFilter(admin.SimpleListFilter):
    title = ("group")
    parameter_name = "group"

    def lookups(self, request, model_admin):
        user = request.user
        qs = Group.objects.all()
        if user.service_group is not None:
            qs = qs.filter(id=user.service_group.id)
        return ((obj.id, obj) for obj in qs)

    def queryset(self, request, queryset):
        if self.value():
            queryset = queryset.filter(group=self.value())
        return queryset


class ChallengeAdmin(admin.ModelAdmin):
    form = ChallengeAdminForm
    list_display = ('active_date', 'group', 'verse', 'reward', 'reward_score')
    list_filter = (
        GroupFilter,
        'active_date',
        ('start_verse__chapter__book__name', custom_titled_filter('book name')),
    )
    inlines = [
        AnswerInline,
    ]
    date_hierarchy = 'active_date'

    form = ChallengeAdminForm

    def get_form(self, request, *args, **kwargs):
        form = super(ChallengeAdmin, self).get_form(
            request, *args, **kwargs)
        form.user = request.user
        if request.user.service_group is not None:
            form.base_fields['group'].initial = request.user.service_group
        return form

    def get_queryset(self, request):
        qs = super(ChallengeAdmin, self).get_queryset(request)
        if request.user.service_group is None:
            return qs
        return qs.filter(group=request.user.service_group)

    def save_model(self, request, obj, form, change):
        if request.user.service_group is None or request.user.service_group == obj.group:
            super().save_model(request, obj, form, change)
        else:
            raise form.ValidationError(
                "You cannot add a challenge to another group")

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

    def render_change_form(self, request, context, *args, **kwargs):
        if request.user.service_group is not None:
            context['adminform'].form.fields['group'].queryset = Group.objects.filter(
                id=request.user.service_group.id)
        return super(ChallengeAdmin, self).render_change_form(request, context, *args, **kwargs)


admin.site.site_header = 'Evangelion Administration'
admin.site.register(Challenge, ChallengeAdmin)
