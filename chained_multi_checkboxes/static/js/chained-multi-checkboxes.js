(function($) {
    $(document).ready(function() {
        $.fn.setChainedMultiCheckboxesCounter = function(selectbox) {
            // 'selectbox' is the parent select object
            var _bignumber = 1048576; // 1024 ^ 2

            // try to rename select items
            var chained_id = $(selectbox).attr('chained-checkbox_id0');
            if (chained_id.indexOf('__prefix__') != -1) {
                chained_id = chained_id.replace('__prefix__', $(selectbox).attr('name').split('-')[1]);
                $(selectbox).attr('chained-checkbox_id0', chained_id);
            }

            var cb_idx;
            var old_group_idx = "not_an_idx", group_idx, group_cnt;
            var pseudo_country = false;

            for (cb_idx = 0 ; cb_idx < _bignumber ; cb_idx++) {
                var cb = $('#'+chained_id+'_'+cb_idx);
                if (cb.length != 1)
                    break;

                var ul = $(cb[0]).parents("ul");
                if (ul.length != 1)
                    continue;
                var group_id = $(ul[0]).attr("id");

                if (group_id.indexOf('__group_') == -1 && group_id.indexOf('__hiddengroup_') == -1)
                    continue;

                var group_idx = group_id.substring(group_id.lastIndexOf("_") + 1);

                if (old_group_idx != group_idx) {
                    // update old_group if real
                    if (old_group_idx != 'not_an_idx' && pseudo_country == false) {
                        // find select item
                        var item = selectbox.get(0).options[old_group_idx];

                        item.text = item.text.replace(/ \([0-9]+\)$/g, "");
                        item.text += " ("+group_cnt+")";
                        // remove count suffix
                        // add new count suffix
                    }
                    else {
                        pseudo_country = false;
                    }
                    // start a new count

                    group_cnt = 0;
                    old_group_idx = group_idx;
                }
                if ($(cb).is(':checked'))
                    group_cnt++;

                if (group_id.indexOf('__hiddengroup_') != -1)
                    pseudo_country = true;
            }
            // update latest select item
            var item = selectbox.get(0).options[old_group_idx];

            item.text = item.text.replace(/ \([0-9]+\)$/g, "");
            item.text += " ("+group_cnt+")";
        },
        $.fn.loadChainedMultiCheckboxes = function(set_dropdown) {
            // 'this' is the parent select object
            var _bignumber = 1048576; // 1024 ^ 2

            if (set_dropdown) {
                // we set the dropdown to the first group with a selected checkbox (or to the first otherwise)
                var first_group = _bignumber;

                // for each chained-checkbox ...
                for (var idx = 0 ; idx < _bignumber ; idx++) {
                    if ($(this).attr('chained-checkbox_id'+idx) == undefined) {
                        break;
                    }
                    var chained_id = $(this).attr('chained-checkbox_id'+idx);
                    if (chained_id.indexOf('__prefix__') != -1) {
                        chained_id = chained_id.replace('__prefix__', $(this).attr('name').split('-')[1]);
                        $(this).attr('chained-checkbox_id'+idx, chained_id);
                    }
                    var cb_idx;
                    for (cb_idx = 0 ; cb_idx < _bignumber ; cb_idx++) {
                        var cb = $('#'+chained_id+'_'+cb_idx);
                        if (cb.length != 1)
                            break;
                        if ($(cb).is(':checked')) {
                            var ul = $(cb[0]).parents("ul");
                            if (ul.length != 1)
                                continue;
                            var group_id = $(ul[0]).attr("id");

                            if (group_id.indexOf('__group_') == -1 && group_id.indexOf('__hiddengroup_') == -1)
                                continue;

                            var group_idx = group_id.substring(group_id.lastIndexOf("_") + 1);

                            if (first_group > group_idx)
                                first_group = group_idx;
                            break;
                        }
                    }
                }
                if (first_group == _bignumber) {
                    first_group = "";
                }

                $(this).val(first_group);
            }

            for (var idx = 0 ; idx < 512 ; idx++) {
                if ($(this).attr('chained-checkbox_id'+idx) == undefined) {
                    break;
                }
                var chained_id = $(this).attr('chained-checkbox_id'+idx);
                if (chained_id.indexOf('__prefix__') != -1) {
                    chained_id = chained_id.replace('__prefix__', $(this).attr('name').split('-')[1]);
                    $(this).attr('chained-checkbox_id'+idx, chained_id);
                }

                // if an hiddengroup element is selected select the related checkbox and
                // deselect all other checkboxes items
                var hiddengroup = $("#" + chained_id + "__hiddengroup_" + $(this).val());

                if (hiddengroup.length == 1) {
                    var item = hiddengroup.find("input");

                    if (item.length == 1) {
                        for (var cb_idx = 0 ; cb_idx < _bignumber ; cb_idx++) {
                            var cb = $('#'+chained_id+'_'+cb_idx);
                            if (cb.length != 1)
                                break;
                            cb.removeAttr('checked');
                        }

                        item.attr('checked','checked');
                    }
                }
                else { // if hiddengroup isn't selected all hiddengroups items must be deselected
                    for (var group_idx = 1 ; group_idx < _bignumber ; group_idx++) {
                        var group = $("#" + chained_id + "__group_" + group_idx);
                        if (group.length == 1)
                            continue;

                        var hiddengroup = $("#" + chained_id + "__hiddengroup_" + group_idx);
                        if (hiddengroup.length == 1) {
                            var item = hiddengroup.find("input");
                            item.removeAttr('checked');
                            continue;
                        }
                        break;
                    }
                }

                // set visibility of the proper group (if isn't an hiddengroup)
                for (var group_idx = 1 ; group_idx < _bignumber ; group_idx++) {
                    var group = $("#" + chained_id + "__group_" + group_idx);

                    if (group.length == 1) {
                        $(group).css("display", (group_idx == $(this).val() ? '' : 'none'));
                        continue;
                    }

                    var hiddengroup = $("#" + chained_id + "__hiddengroup_" + group_idx);
                    if (hiddengroup.length == 1)
                        continue;

                    break;
                }
            }
            $.fn.setChainedMultiCheckboxesCounter(this);
        };

        $('.chained-checkbox-parent-field').live('change', function(e) {
            $(this).loadChainedMultiCheckboxes(false);
        });
    });
})(django.jQuery);