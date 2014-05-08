from django import forms
from django.utils.safestring import mark_safe
from django.forms import CheckboxSelectMultiple
from django.forms.widgets import CheckboxInput
from django.utils.encoding import force_text
from django.utils.html import format_html
from itertools import chain

class ChainedCheckboxSelectMultiple(CheckboxSelectMultiple):
    def __init__(self, parent_field=None, order_fields=None, item_index=None, *args, **kwargs):
        print "PARENT: ", parent_field
        self.parent_field = parent_field
        self.order_fields = order_fields
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
        last_group = -1
        output_group = []
        is_visible_group = False
        for i, (option_value, option_label, option_group, option_is_visible) in enumerate(chain(self.choices, choices, ((-1, "noval", -1, False), ) )):
            if last_group != option_group:
                if last_group != -1:
                    if is_visible_group:
                        output.append(format_html("<ul id='%s__group_%d' style='display: none;'>" % (attrs['id'], last_group)))
                        final_attrs_all = self.build_attrs(onChange="$=django.jQuery ; if ($(this).is(':checked')) { $($(this).parents()[1]).siblings().find('input').attr('checked','checked'); } else { $($(this).parents()[1]).siblings().find('input').removeAttr('checked'); }")
                        cb_all = CheckboxInput(final_attrs_all)
                        rendered_cb_all = cb_all.render("ALL", False)
                        option_label_all = "ALL"
                        output.append(format_html('<li><label{0}>{1} {2}</label></li>',
                                      '', rendered_cb_all, option_label_all))
                    else:
                        output.append(format_html("<ul id='%s__hiddengroup_%d' style='display: none;'>" % (attrs['id'], last_group)))
                    output += output_group
                    output_group = []
                    is_visible_group = False
                    output.append(format_html("</ul>"))

                last_group = option_group

            if option_is_visible:
                is_visible_group = True
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
            output_group.append(format_html('<li><label{0}>{1} {2}</label></li>',
                                      label_for, rendered_cb, option_label))

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
