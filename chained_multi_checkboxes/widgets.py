from django import forms
from django.utils.safestring import mark_safe
from django.forms import CheckboxSelectMultiple
from django.forms.widgets import CheckboxInput
from django.utils.encoding import force_text
from django.utils.html import format_html
from itertools import chain

class ChainedCheckboxSelectMultiple(CheckboxSelectMultiple):
    def __init__(self, parent_field=None, item_index=None, *args, **kwargs):
        print "PARENT: ", parent_field
        self.parent_field = parent_field
        self.item_index = 0
        if item_index:
            self.item_index = item_index
        super(CheckboxSelectMultiple, self).__init__(*args, **kwargs)

    class Media:
        js = ['admin/js/jquery.min.js', 'admin/js/jquery.init.js', 'js/chained-multi-checkboxes.js']

    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = []

        field_prefix = attrs['id'][:attrs['id'].rfind('-') + 1]
        formset_prefix = attrs['id'][:attrs['id'].find('-') + 1]

        if not field_prefix:
            paretnfield_id = "id_" + self.parent_field
        else:
            paretnfield_id = field_prefix + self.parent_field

        # Normalize to strings
        str_values = set([force_text(v) for v in value])
        last_taste=-1
        for i, (option_value, option_label, option_taste) in enumerate(chain(self.choices, choices)):
            if last_taste != option_taste:
                if last_taste != -1:
                    output.append(format_html("</ul>"))
                output.append(format_html("<ul id='%s__group_%d' style='display: none;'>" % (attrs['id'], option_taste)))
                last_taste = option_taste

            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = format_html(' for="{0}"', final_attrs['id'])
            else:
                label_for = ''

            cb = CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            option_value = force_text(option_value)
            rendered_cb = cb.render(name, option_value)
            option_label = force_text(option_label)
            output.append(format_html('<li><label{0}>{1} {2}</label></li>',
                                      label_for, rendered_cb, option_label))
        output.append('</ul>')

        js = """
        <script type="text/javascript">
        //<![CDATA[
        (function($) {
            $(document).ready(function(){
                var parent_field = $("#%(paretnfield_id)s");
                parent_field.addClass('chained-checkbox-parent-field');
                parent_field.attr('chained-checkbox_id%(item_index)s', "%(chained_id)s");
                /* run it explicitly to initialize the dropdown and show the correct checkboxes group */
                $("#%(paretnfield_id)s").loadChainedMultiCheckboxes(true);
            }
            )
        })(django.jQuery);


        //]]>
        </script>

        """ % {"paretnfield_id":paretnfield_id, 'item_index': self.item_index, 'chained_id': attrs['id']}

        output.append(js)

        return mark_safe('\n'.join(output))
