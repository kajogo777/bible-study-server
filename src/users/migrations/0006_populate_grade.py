import csv
from django.db import migrations
from users.models import User, AdminUser


def populate_user_grade(apps, schema_editor):
    UserModel = apps.get_model('users', 'User')

    for user in UserModel.objects.filter(grade__isnull=True):
        grade = User.OTHER

        if user.group_class is not None:
            if user.group.name.startswith("Primary"):
                grade = user.group_class.grade

            if user.group.name == "Preparatory":
                grade = user.group_class.grade + 6

            if user.group.name == "Secondary":
                grade = user.group_class.grade + 9

        if user.group.name == "University":
            grade = User.UNIVERSITY
        
        user.grade = grade
        user.save()

def populate_admin_grade(apps, schema_editor):
    AdminUserModel = apps.get_model('users', 'AdminUser')

    for user in AdminUserModel.objects.filter(service_class__isnull=False, service_grade__isnull=True):
        grade = None

        if user.service_group.name.startswith("Primary"):
            grade = user.service_class.grade

        if user.service_group.name == "Preparatory":
            grade = user.service_class.grade + 6

        if user.service_group.name == "Secondary":
            grade = user.service_class.grade + 9

        if user.service_group.name == "University":
            grade = AdminUser.UNIVERSITY
        
        user.service_grade = grade
        user.save()

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_grade'),
    ]

    operations = [
        migrations.RunPython(populate_user_grade),
        migrations.RunPython(populate_admin_grade),
    ]
