from users.models import *


groups = [
    Group.objects.get(name="Primary"),
    Group.objects.get(name="Preparatory"),
    Group.objects.get(name="Secondary"),
]

groups_max_grade = []

for i in range(len(groups)):
    groups_max_grade = (
        Class.objects.filter(group=groups[i]).order_by("-grade").first().grade
    )

trans = {}
trans[groups[0].id] = groups[1]
trans[groups[1].id] = groups[2]
trans[groups[2].id] = Group.objects.get(name="University")


for i in range(len(groups)):
    User.objects.filter(group=groups[i], group_class__grade=groups_max_grade[i]).update(
        group=trans[groups[i].id], group_class=None
    )
