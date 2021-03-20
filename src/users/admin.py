from django.contrib import admin
import io
from django.http import HttpResponse
from .models import Group, User, Response, AdminUser, Class
from django.utils.html import format_html
from django.urls import reverse
from django.conf.urls import url
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph
from django.contrib.auth.admin import UserAdmin
from .forms import AdminUserCreationForm, AdminUserChangeForm
from django import forms
from django.utils import timezone
from challenges.models import Challenge
from django.db.models import (
    Count,
    Sum,
    Q,
    Subquery,
    OuterRef,
    F,
    Value,
    Case,
    When,
    IntegerField,
)
import itertools
from topics.models import TopicUser, TopicGroup
from ch_app_server.utils import get_year_start, get_days_since_year_start
from calendar import monthrange


class AdminUserAdmin(UserAdmin):
    add_form = AdminUserCreationForm
    form = AdminUserChangeForm
    model = AdminUser

    list_display = (
        "username",
        "is_staff",
        "is_superuser",
        "service_group",
        "service_class",
    )
    list_filter = ("service_group", "service_class")
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "service_group",
                    "service_class",
                    "is_staff",
                    "groups",
                ),
            },
        ),
    )
    fieldsets = (
        (None, {"fields": ("username", "password", "service_group", "service_class")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    def get_form(self, request, *args, **kwargs):
        form = super(AdminUserAdmin, self).get_form(request, *args, **kwargs)
        form.base_fields["is_staff"].initial = True
        return form


class ClassInline(admin.TabularInline):
    model = Class
    verbose_name = "Class"
    verbose_name_plural = "Classes"


class TopicGroupInline(admin.TabularInline):
    model = TopicGroup
    extra = 0
    min_num = 0
    verbose_name = "Topic"
    verbose_name_plural = "Topics"


class GroupAdmin(admin.ModelAdmin):
    list_display = ("name",)  # 'downloads')

    inlines = [ClassInline, TopicGroupInline]


class TopicUserInline(admin.TabularInline):
    model = TopicUser
    extra = 0
    min_num = 0
    verbose_name = "Topic"
    verbose_name_plural = "Topics"


class LimitModelFormset(forms.BaseInlineFormSet):
    """ Base Inline formset to limit inline Model query results. """

    def __init__(self, *args, **kwargs):
        super(LimitModelFormset, self).__init__(*args, **kwargs)
        _kwargs = {
            self.fk.name: kwargs["instance"],
        }
        if kwargs["instance"].id is not None:
            _kwargs["challenge__group"] = kwargs["instance"].group

        self.queryset = (
            kwargs["queryset"]
            .filter(**_kwargs)
            .order_by("-challenge__active_date")[:10]
        )


class ResponseInline(admin.TabularInline):
    model = Response
    extra = 0
    min_num = 0
    formset = LimitModelFormset
    fields = ["challenge", "answer"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "challenge":
            # if request.user.service_group is not None:
            #     kwargs["queryset"] = Challenge.objects.filter(
            #         group=request.user.service_group)
            if request._obj_ is not None:
                kwargs["queryset"] = Challenge.objects.filter(
                    group=request._obj_.group)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


def download_pdf(modeladmin, request, queryset):
    if request.user.is_authenticated:
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = "attachment; filename=group_qr_codes.pdf"
        p = canvas.Canvas(response)

        users = queryset  # User.objects.filter(group__id=pk)

        per_page = 6
        x_offset = 0
        y_offset = 0
        step = 130
        margin = 50

        for i, user in enumerate(users):
            qrw = QrCodeWidget(user.code)

            d = Drawing(50, 50)
            d.add(qrw)
            renderPDF.draw(d, p, margin + x_offset, margin + y_offset)
            p.drawString(margin + x_offset, margin + y_offset - 10, user.name)

            y_offset += step

            if i % per_page == per_page - 1:
                x_offset += step + 60
                y_offset = 0

            if i % (per_page * 3) == (per_page * 3) - 1:
                p.showPage()
                x_offset = 0
                y_offset = 0

        p.save()
        return response
    else:
        return HttpResponse("Unauthorized", status=403)


download_pdf.short_description = "Download QR codes"


class RegularUserForm(forms.ModelForm):
    def clean_group(self):
        if (
            self.user.service_group is not None
            and self.user.service_group != self.cleaned_data["group"]
        ):
            raise forms.ValidationError(
                "You can only add users to group {}".format(
                    self.user.service_group.name
                )
            )
        return self.cleaned_data["group"]

    def clean_group_class(self):
        if (
            self.user.service_class is not None
            and self.user.service_class != self.cleaned_data["group_class"]
        ):
            raise forms.ValidationError(
                "You can only add users to class {}".format(
                    self.user.service_class)
            )
        return self.cleaned_data["group_class"]


class ClassFilter(admin.SimpleListFilter):
    title = "class"
    parameter_name = "group_class"

    def lookups(self, request, model_admin):
        user = request.user
        qs = Class.objects.all()
        if user.service_group is not None:
            qs = qs.filter(group=user.service_group)
        if user.service_class is not None:
            qs = qs.filter(id=user.service_class.id)
        return ((obj.id, obj) for obj in qs)

    def queryset(self, request, queryset):
        if self.value():
            queryset = queryset.filter(group_class=self.value())
        return queryset


class GroupFilter(admin.SimpleListFilter):
    title = "group"
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


class ReadingsFilter(admin.SimpleListFilter):
    title = "total solved"
    parameter_name = "solved_count"

    def lookups(self, request, model_admin):
        return (
            ("4", "75-100%"),
            ("3", "50-74%"),
            ("2", "25-49%"),
            ("1", "0-24%"),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == "4":
            return queryset.filter(_percentage_solved__range=(75, 100))
        elif value == "3":
            return queryset.filter(_percentage_solved__range=(50, 74))
        elif value == "2":
            return queryset.filter(_percentage_solved__range=(25, 49))
        elif value == "1":
            return queryset.filter(_percentage_solved__range=(0, 24))
        return queryset


class MonthFilter(admin.SimpleListFilter):
    title = "challenge month"
    parameter_name = "challenge_month"

    def lookups(self, request, model_admin):
        now = timezone.now()
        current_year = now.year
        current_month = now.month
        years = [current_year, current_year - 1]
        months = [
            (12, "December"),
            (11, "November"),
            (10, "October"),
            (9, "September"),
            (8, "August"),
            (7, "July"),
            (6, "June"),
            (5, "May"),
            (4, "April"),
            (3, "March"),
            (2, "February"),
            (1, "January"),
        ]

        options = itertools.product(years, months)
        options = [
            (f"{y}-{m[0]}", f"{m[1]} {y}")
            for y, m in options
            if y < current_year or m[0] <= current_month
        ]
        return options

    def queryset(self, request, queryset):
        value = self.value()
        if value is not None:
            value = value.split("-")
            year, month = int(value[0]), int(value[1])
            _, days_in_month = monthrange(year, month)
            queryset = queryset.annotate(
                _read_count=Count(
                    "response",
                    filter=Q(
                        response__challenge__active_date__month=month,
                        response__challenge__active_date__year=year,
                    ),
                ),
                _solved_count=Count(
                    "response",
                    filter=Q(
                        response__answer__correct=True,
                        response__challenge__active_date__month=month,
                        response__challenge__active_date__year=year,
                    ),
                ),
                _total_challenges=Value(days_in_month, IntegerField()),
                # _total_challenges=Subquery(
                #     Group.objects.filter(id=OuterRef("group_id"))
                #     .annotate(
                #         _challenge_count=Count(
                #             "challenge",
                #             filter=Q(
                #                 challenge__active_date__lte=timezone.localtime(
                #                     timezone.now()
                #                 ).date(),
                #                 challenge__active_date__month=month,
                #                 challenge__active_date__year=year,
                #             ),
                #         )
                #     )
                #     .values("_challenge_count")[:1],
                #     output_field=IntegerField(),
                # ),
                _percentage_solved=Case(
                    When(_total_challenges=0, then=0),
                    default=(100.0 * F("_solved_count") / \
                             F("_total_challenges")),
                ),
                _total_score=Sum(
                    "response__challenge__reward_score",
                    filter=Q(
                        response__answer__correct=True,
                        response__challenge__active_date__month=month,
                        response__challenge__active_date__year=year,
                    ),
                ),
            )
        return queryset


class RegularUserAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "group",
        "group_class",
        "solved_count",
        "read_count",
        "total_score",
        "date_of_birth",
        "gender",
        "login_url"
    )
    list_filter = (
        GroupFilter,
        ClassFilter,
        MonthFilter,
        ReadingsFilter,
    )
    readonly_fields = ('code', 'login_url',)
    search_fields = ("name",)
    inlines = [ResponseInline, TopicUserInline]
    actions = [download_pdf]
    # date_hierarchy = 'response__challenge__active_date'
    form = RegularUserForm

    def get_form(self, request, obj=None, **kwargs):
        request._obj_ = obj
        form = super(RegularUserAdmin, self).get_form(request, obj, **kwargs)
        form.user = request.user
        if request.user.service_group is not None:
            form.base_fields["group"].initial = request.user.service_group
        if request.user.service_class is not None:
            form.base_fields["group_class"].initial = request.user.service_class
        return form

    def get_queryset(self, request):
        qs = super(RegularUserAdmin, self).get_queryset(request)
        if request.user.service_group is not None:
            qs = qs.filter(group=request.user.service_group)
        if request.user.service_class is not None:
            qs = qs.filter(group_class=request.user.service_class)
        year_start = get_year_start()
        qs = qs.annotate(
            _read_count=Count(
                "response",
                filter=Q(
                    response__challenge__active_date__gte=year_start,
                ),
            ),
            _solved_count=Count(
                "response",
                filter=Q(
                    response__answer__correct=True,
                    response__challenge__active_date__gte=year_start,
                ),
            ),
            # _total_challenges=Subquery(
            #     Group.objects.filter(id=OuterRef("group_id"))
            #     .annotate(
            #         _challenge_count=Count(
            #             "challenge",
            #             filter=Q(
            #                 challenge__active_date__lte=timezone.localtime(
            #                     timezone.now()
            #                 ).date(),
            #                 challenge__active_date__gte=year_start,
            #             ),
            #         )
            #     )
            #     .values("_challenge_count")[:1],
            #     output_field=IntegerField(),
            # ),
            _total_challenges=Value(
                get_days_since_year_start(), IntegerField()),
            _percentage_solved=Case(
                When(_total_challenges=0, then=0),
                default=(100.0 * F("_solved_count") / F("_total_challenges")),
            ),
            _total_score=Sum(
                "response__challenge__reward_score",
                filter=Q(
                    response__answer__correct=True,
                    response__challenge__active_date__gte=year_start,
                ),
            ),
        )

        return qs

    def login_url(self, obj):
        return f"https://evangelion.stmary-rehab.com/deeplink/{obj.code}"

    def challenge_month(self, obj):
        return None

    def total_score(self, obj):
        return obj._total_score

    total_score.short_description = "Total Score"
    total_score.admin_order_field = "_total_score"

    def read_count(self, obj):
        return f"{obj._read_count}/{obj._total_challenges}"

    read_count.short_description = "Read"
    read_count.admin_order_field = "_read_count"

    def solved_count(self, obj):
        return f"{obj._solved_count}/{obj._total_challenges} ({obj._percentage_solved:.2f}%)"

    solved_count.short_description = "Correct"
    solved_count.admin_order_field = "_solved_count"

    def render_change_form(self, request, context, *args, **kwargs):
        if request.user.service_group is not None:
            context["adminform"].form.fields["group"].queryset = Group.objects.filter(
                id=request.user.service_group.id
            )
        # unable to filter class options as well because of chaining field
        return super(RegularUserAdmin, self).render_change_form(
            request, context, *args, **kwargs
        )


# Register your models here.
admin.site.register(Group, GroupAdmin)
admin.site.register(User, RegularUserAdmin)
admin.site.register(AdminUser, AdminUserAdmin)
