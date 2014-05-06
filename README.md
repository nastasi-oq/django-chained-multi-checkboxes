USAGE
=====
  ModelChainedMultipleChoiceField allows you to add a grouped list of checkboxes, what group shows is managed by
  a dropdown menu associated to it with the ``parent_field`` attribute.

  To work properly you must pass the queryset associated, it will be grouped by parent_field attribute.

From application forms.py:

```python
  ingredients = ModelChainedMultipleChoiceField(parent_field='group', queryset=Ingredient.objects.all(), required=False)
```

TODO
====
  - make 'ALL' checkbox optional
  - documentation

DONE
====
  - from .group attribute to a dynamic field
  - dynamic order_by instead of Meta ordering
  - add 'ALL' checkbox utility per group
  - add another example with nested inlines
  - manage hidden checkbox when associated group is selected
  - add the hidden group
  - pass a new attribute "is_hidden"
