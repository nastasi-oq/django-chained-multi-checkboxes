from django import forms
from django.forms.models import ChoiceField, ModelChoiceIterator
from chained_multi_checkboxes.widgets import ChainedCheckboxSelectMultiple

import widgets as example_widgets

class ChainedModelChoiceIterator(ModelChoiceIterator):
    def __init__(self, *args, **kwargs):
        self.parent_field = args[0].parent_field
        super(ChainedModelChoiceIterator, self).__init__(*args, **kwargs)

    def __iter__(self):
        if self.field.empty_label is not None:
            yield ("", self.field.empty_label)
        if self.field.cache_choices:
            if self.field.choice_cache is None:
                self.field.choice_cache = [
                    self.choice(obj) for obj in self.queryset.order_by(self.parent_field)
                ]
            for choice in self.field.choice_cache:
                yield choice
        else:
            for obj in self.queryset.order_by(self.parent_field):
                yield self.choice(obj)


    def choice(self, obj):
        return (self.field.prepare_value(obj), self.field.label_from_instance(obj), getattr(obj, self.parent_field), obj.is_visible)

class ModelChainedMultipleChoiceField(forms.ModelMultipleChoiceField):

    def __init__(self, parent_field, *args, **kwargs):
        if not 'widget' in kwargs:
            kwargs['widget'] = ChainedCheckboxSelectMultiple(parent_field)
        self.parent_field = parent_field
        super(ModelChainedMultipleChoiceField, self).__init__(*args, **kwargs)

    # override ModelMultipleChoiceField ->  ModelChoiceField :: _get_choices
    def _get_choices(self):
        # If self._choices is set, then somebody must have manually set
        # the property self.choices. In this case, just return self._choices.
        if hasattr(self, '_choices'):
            return self._choices

        # Otherwise, execute the QuerySet in self.queryset to determine the
        # choices dynamically. Return a fresh ModelChoiceIterator that has not been
        # consumed. Note that we're instantiating a new ModelChoiceIterator *each*
        # time _get_choices() is called (and, thus, each time self.choices is
        # accessed) so that we can ensure the QuerySet has not been consumed. This
        # construct might look complicated but it allows for lazy evaluation of
        # the queryset.
        return ChainedModelChoiceIterator(self)

    # override ModelMultipleChoiceField ->  ModelChoiceField :: choices
    choices = property(_get_choices, ChoiceField._set_choices)

