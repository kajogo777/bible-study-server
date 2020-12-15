from django.core.management.base import BaseCommand, CommandError
from users.models import Group, Class, User


MAIN_GROUPS = ["Primary", "Preparatory", "Secondary"]


class Command(BaseCommand):
    help = "Transition users at the end of each group class to the next group"

    def handle(self, *args, **options):
        groups = []

        for g in MAIN_GROUPS:
            groups.append(Group.objects.get(name=g))

        groups_max_grade = []

        for i in range(len(MAIN_GROUPS)):
            try:
                groups_max_grade.append(
                    Class.objects.filter(group=groups[i])
                    .order_by("-grade")
                    .first()
                    .grade
                )
            except Exception:
                raise CommandError(f"Group {groups[i]} does not have classes")

        trans = {}

        trans[groups[0].id] = groups[1]
        trans[groups[1].id] = groups[2]
        trans[groups[2].id], _ = Group.objects.get_or_create(name="University")

        for i in range(len(MAIN_GROUPS)):
            print(groups[i])
            print(trans[groups[i].id])
            result = User.objects.filter(
                group=groups[i], group_class__grade=groups_max_grade[i]
            ).update(group=trans[groups[i].id], group_class=None)

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully transitioned {result} users from group {groups[i]} to group {trans[groups[i].id]}"
                )
            )

            result = User.objects.filter(
                group=groups[i], group_class__grade__lt=groups_max_grade[i]
            ).update(group_class=None)

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully removed {result} users from classes in group {groups[i]}"
                )
            )
