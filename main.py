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
        self.remembered_set = set()


stack_refs = set()

first_gen = Generation()
second_gen = Generation()
third_gen = Generation()


def first_gen_collect():
    root_set = stack_refs.copy()

    #TODO: get objects from remembered set and scan their references

    mark_first_gen_recursive(root_set)

    for v in first_gen.objects.values():
        if v.reached:
            second_gen.objects[v.id] = v

    first_gen.objects = defaultdict(lambda: None)


def mark_first_gen_recursive(references):
    for r in references:
        obj = first_gen.objects[r]

        if not obj.reached:
            obj.reached = True
            mark_first_gen_recursive(obj.references)


def second_gen_collect():
    pass


def third_gen_collect():
    pass


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
