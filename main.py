import uuid
from collections import defaultdict


class Object:
    def __init__(self, name):
        self.id = uuid.uuid4()
        self.name = name
        self.references = list()
        self.reached = False

    def add_reference(self, ref: "Object"):
        self.references.append(ref.id)

    def remove_reference(self, ref: "Object"):
        self.references.remove(ref.id)


class Generation:
    def __init__(self):
        self.objects = defaultdict(lambda: None)

        # Deviates from spec: list of objects that are pointed to
        self.remembered_set = set()


stack_refs = set()

first_gen = Generation()
second_gen = Generation()
third_gen = Generation()


def first_gen_collect():
    root_set = stack_refs.union(first_gen.remembered_set)

    mark_recursive(root_set, first_gen.objects)

    for v in first_gen.objects.values():
        if v.reached:
            v.reached = False
            second_gen.objects[v.id] = v

    first_gen.objects = defaultdict(lambda: None)


def second_gen_collect():
    root_set = stack_refs.union(
        first_gen.objects,
        first_gen.remembered_set,
        second_gen.objects,
        second_gen.remembered_set
    )

    objects = {**first_gen.objects, **second_gen.objects}

    mark_recursive(root_set, objects)

    for v in second_gen.objects.values():
        if v.reached:
            v.reached = False
            third_gen.objects[v.id] = v

    second_gen.objects = defaultdict(lambda: None)

    for v in first_gen.objects.values():
        if v.reached:
            v.reached = False
            second_gen.objects[v.id] = v

    first_gen.objects = defaultdict(lambda: None)


def third_gen_collect():
    pass

def mark_recursive(references, objects):
    for r in references:
        obj = objects[r]

        if obj is None:
            continue

        if not obj.reached:
            obj.reached = True
            mark_recursive(obj.references, objects)


a = Object('a')
b = Object('b')
c = Object('c')

a.add_reference(b)
a.add_reference(c)

stack_refs.add(a.id)
first_gen.objects[a.id] = a
first_gen.objects[b.id] = b
first_gen.objects[c.id] = c

a.remove_reference(b)

first_gen_collect()

print(first_gen)

d = Object('d')

stack_refs.add(d.id)
first_gen.objects[d.id] = d

second_gen_collect()

print(first_gen)
