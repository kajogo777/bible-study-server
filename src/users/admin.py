from django.contrib import admin
import io
from django.http import HttpResponse
from .models import Group, User, Response
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
from .models import AdminUser
from django import forms


class AdminUserAdmin(UserAdmin):
    add_form = AdminUserCreationForm
    form = AdminUserChangeForm
    model = AdminUser

    list_display = ('username', 'is_staff', 'is_superuser', 'service_group',)
    list_filter = ('service_group',)
    add_fieldsets = ((None, {'classes': ('wide',), 'fields': (
        'username', 'password1', 'password2', 'service_group')}),)
    fieldsets = ((None, {'fields': ('username', 'password', 'service_group')}), ('Personal info', {'fields': ('first_name', 'last_name',)}), ('Permissions', {
                 'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}), ('Important dates', {'fields': ('last_login', 'date_joined')}))


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'downloads')

    def get_urls(self):
        urls = super(GroupAdmin, self).get_urls()
        urls += [
            url(r'^download-file/(?P<pk>\d+)$', self.download_pdf,
                name='applabel_modelname_download-file'),
        ]
        return urls

    def downloads(self, obj):
        return format_html(
            '<a href="{}">Download QR codes</a>',
            reverse('admin:applabel_modelname_download-file', args=[obj.pk])
        )
    downloads.short_description = "Downloads"

    def download_pdf(self, request, pk):
        if request.user.is_authenticated:
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=group_qr_codes.pdf'
            p = canvas.Canvas(response)

            users = User.objects.filter(group__id=pk)

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
                p.drawString(margin + x_offset, margin +
                             y_offset - 10, user.name)

                y_offset += step

                if i % per_page == per_page - 1:
                    x_offset += step + 60
                    y_offset = 0

                if i % (per_page*3) == (per_page*3) - 1:
                    p.showPage()
                    x_offset = 0
                    y_offset = 0

            p.save()
            return response
        else:
            return HttpResponse('Unauthorized', status=403)


class ResponseInline(admin.TabularInline):
    model = Response
    extra = 0
    min_num = 0


class RegularUserForm(forms.ModelForm):
    def clean_group(self):
        if self.user.service_group is not None and self.user.service_group != self.cleaned_data["group"]:
            raise forms.ValidationError(
                "You can only add users to group {}".format(self.user.service_group.name))
        return self.cleaned_data["group"]


class RegularUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_of_birth', 'gender', 'code')
    list_filter = (
        'date_of_birth',
    )
    inlines = [
        ResponseInline,
    ]
    form = RegularUserForm

    def get_form(self, request, *args, **kwargs):
        form = super(RegularUserAdmin, self).get_form(request, *args, **kwargs)
        form.user = request.user
        return form

    def get_queryset(self, request):
        qs = super(RegularUserAdmin, self).get_queryset(request)
        if request.user.service_group is None:
            return qs
        return qs.filter(group=request.user.service_group)

    # def save_model(self, request, obj, form, change):
    #     if request.user.service_group is None or request.user.service_group == obj.group:
    #         super().save_model(request, obj, form, change)
    #     else:
    #         raise form.ValidationError(
    #             "You cannot add a user to another group")


# Register your models here.
admin.site.register(Group, GroupAdmin)
admin.site.register(User, RegularUserAdmin)
admin.site.register(AdminUser, AdminUserAdmin)
