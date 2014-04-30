(function($) {
    $(document).ready(function() {
        $.fn.loadChainedMultiCheckboxes = function(set_dropdown) {
            // 'this' is the parent select object
            var _bignumber = 1048576; // 1024 ^ 2

            if (set_dropdown) {
                // we set the dropdown to the first group with a selected checkbox (or to the first otherwise)
                var first_group = _bignumber;
                
                for (var idx = 0 ; idx < _bignumber ; idx++) {
                    if ($(this).attr('chained-checkbox_id'+idx) == undefined) {
                        break;
                    }
                    var chained_id = $(this).attr('chained-checkbox_id'+idx);
                    if (chained_id.indexOf('__prefix__') != -1) {
                        chained_id = chained_id.replace('__prefix__', $(this).attr('name').split('-')[1]);
                        $(this).attr('chained-checkbox_id'+idx, chained_id);
                    }
                    for (var cb_idx = 0 ; cb_idx < _bignumber ; cb_idx++) {
                        var cb = $('#'+chained_id+'_'+cb_idx);
                        if (cb.length != 1) 
                            break;
                        if ($(cb[0]).is(':checked')) {
                            var ul = $(cb[0]).parents("ul");
                            if (ul.length != 1)
                                continue;
                            var group_id = $(ul[0]).attr("id");
                            
                            if (group_id.indexOf('__group_') == -1) 
                                continue;
                            
                            var group_idx = group_id.substring(group_id.lastIndexOf("_") + 1);

                            if (first_group > group_idx)
                                first_group = group_idx;
                            break;
                        }
                    }
                }
                if (first_group == 10240)
                    first_group = 1;
                
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

                for (var group_idx = 1 ; group_idx < 10240 ; group_idx++) {
                    var group = $("#" + chained_id + "__group_" + group_idx);
                    
                    if (group.length != 1)
                        break;
                    group[0].style.display = (group_idx == $(this).val() ? '' : 'none');
                }
            }
        };

        $('.chained-checkbox-parent-field').live('change', function(e) {
            $(this).loadChainedMultiCheckboxes(false);
        });
    });
})(django.jQuery);