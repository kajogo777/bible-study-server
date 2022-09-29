from django.core.management.base import BaseCommand
from django.db.models import F
from users.models import Group, User


class Command(BaseCommand):
    help = "Transition users by 1 grade and move them to new groups"

    def handle(self, *args, **options):
        primary_group = Group.objects.get(name="Primary")
        preparatory_group = Group.objects.get(name="Preparatory")
        secondary_group = Group.objects.get(name="Secondary")
        university_group = Group.objects.get(name="University")


        result = User.objects.filter(grade__lt=13).update(grade=F('grade')+1)
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully incremented grade of {result} users"
            )
        )

        result = User.objects.filter(grade__gte=1, grade__lte=6).update(group=primary_group)
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully set {result} users Primary"
            )
        )

        result = User.objects.filter(grade__gte=7, grade__lte=9).update(group=preparatory_group)
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully set {result} users Preparatory"
            )
        )

        result = User.objects.filter(grade__gte=10, grade__lte=12).update(group=secondary_group)
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully set {result} users Secondary"
            )
        )

        result = User.objects.filter(grade=13).update(group=university_group)
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully set {result} users University"
            )
        )
