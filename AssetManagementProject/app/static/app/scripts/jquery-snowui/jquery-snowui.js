/* =========================================================
 * jquery-snowui.js
 * =========================================================
 * Copyright 2016 黄耀樑
 *
 * ========================================================= */

$(function () {
    // datagrid----------------------------------------------------start
    // 黄耀樑 2016-07-20
    if ($('.snowui-datagrid').length > 0) {
        var option = {};
        $.each($('.snowui-datagrid'), function (i, n) {
            var t = $(n);
            var s = $.trim(t.attr("data-options"));
            if (s) {
                if (s.substring(0, 1) != "{") {
                    s = "{" + s + "}";
                }
                option = (new Function("return " + s))();
            }
        });

        if (option.url) {
            var data = option.queryParams || {};
            $.get(option.url, data, function (d) {
                snowui.create_datagrid(d);
            });
        }

        $('.snowui-datagrid thead tr th').on('click', function () {
            var t = $(this);
            var s = $.trim(t.attr("data-options"));
            if (s) {
                if (s.substring(0, 1) != "{") {
                    s = "{" + s + "}";
                }
                var d = (new Function("return " + s))();
                if (d.sortable) {
                    alert(d.field);
                }
            }
        });
    }
    // datagrid----------------------------------------------------end

    // form----------------------------------------------------start
    // 黄耀樑 2016-07-26
    if ($('.snowui-form').length > 0) {
        var option = {};
        $.each($('.snowui-form'), function (i, n) {
            var t = $(n);
            var s = $.trim(t.attr("data-options"));
            if (s) {
                if (s.substring(0, 1) != "{") {
                    s = "{" + s + "}";
                }
                option = (new Function("return " + s))();
            }
        });

        if (option.url) {
            var data = option.queryParams || {};
            $.get(option.url, data, function (d) {
                snowui.create_form(d);
            });
        }
    }
    // form----------------------------------------------------end
});

var snowui = {
    // 构建表格
    // 黄耀樑 2016-07-20
    create_datagrid: function (data) {
        var options = [];
        $.each($('.snowui-datagrid thead tr th'), function (i, n) {
            var t = $(n);
            var s = $.trim(t.attr("data-options"));
            if (s) {
                if (s.substring(0, 1) != "{") {
                    s = "{" + s + "}";
                }
                var d = (new Function("return " + s))();
                options.push(d);
            }
        });

        var tbody = $('.snowui-datagrid').append('<tbody></tbody>');
        if (data && data.rows && options) {
            for (var i = 0; i < data.rows.length; i++) {
                var column = '';
                var row = data.rows[i];
                for (var j = 0; j < options.length; j++) {
                    var colHead = '<td>';
                    var colBody = '';
                    var dic = options[j];
                    for (var k in dic) {
                        var v = dic[k];
                        switch (k) {
                            case 'field':
                                colBody += row[v];
                                break;
                            case 'checkbox':
                                if (v) {
                                    colBody += '<input type="checkbox" value="' + row['id'] + '"/>';
                                }
                                break;
                        }
                    }
                    column += (colHead + colBody + '</td>');
                }
                tbody.append('<tr>' + column + '<tr>');
            }
        }
    },

    // 构建表单
    // 黄耀樑 2016-07-26
    create_form: function (obj) {
        if (obj) {
            for (var o in obj) {
                $('.snowui-form [name="' + o + '"]').val(obj[o]);
            }
        }
    }
}