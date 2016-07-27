/* =========================================================
 * jquery-snowui.js
 * =========================================================
 * Copyright 2016 黄耀樑
 *
 * ========================================================= */

$(function () {
    // 通用元素动作----------------------------------------------------start
    $('#btnBack').on('click', function () {
        history.back(-1);
    });
    // 通用元素动作----------------------------------------------------end

    // datagrid----------------------------------------------------start
    // 黄耀樑 2016-07-20
    if ($('.snowui-datagrid').length > 0) {
        $.each($('.snowui-datagrid'), function (i, n) {
            var option = {};
            var t = $(n);
            var s = $.trim(t.attr("data-options"));
            if (s) {
                if (s.substring(0, 1) != "{") {
                    s = "{" + s + "}";
                }
                option = (new Function("return " + s))();
            }

            // 添加脚部
            t.append('<tfoot><tr></tr></tfoot>');

            // 添加 bootstrap 样式
            t.addClass('table table-striped table-condensed'); // table-bordered边框             
            $('thead tr', t).addClass('info');
            $('tfoot tr', t).addClass('success');

            if (option.url) {
                var data = option.queryParams || {};
                $.get(option.url, data, function (d) {
                    snowui.create_datagrid(t, d);
                });
            }
        });

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
        $.each($('.snowui-form'), function (i, n) {
            var option = {};
            var t = $(n);
            var s = $.trim(t.attr("data-options"));
            if (s) {
                if (s.substring(0, 1) != "{") {
                    s = "{" + s + "}";
                }
                option = (new Function("return " + s))();
            }

            // 添加 bootstrap 样式
            t.addClass('form-horizontal');

            // 设置表单通用属性
            t.attr({ method: "post", action: "/edit" });

            // 每个表单必须要有一个id的隐藏域
            t.append('<input type="hidden" name="id" value="0"/>');

            if (option.url) {
                var data = option.queryParams || {};
                $.get(option.url, data, function (d) {
                    snowui.create_form(d);
                });
            }
        });
    }
    // form----------------------------------------------------end
});

var snowui = {
    // 构建表格
    // 黄耀樑 2016-07-20
    create_datagrid: function (element, data) {
        var options = [];
        $.each($('thead tr th', element), function (i, n) {
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

        // 它们的出现次序是：thead、tfoot、tbody，这样浏览器就可以在收到所有数据前呈现页脚了
        if (data && options) {
            // 脚部信息
            if (data.total) {
                //$('.snowui-datagrid').append('<tfoot><tr><td colspan="' + options.length + '" style="font-size:20px;font-weight:bold;">合计：' + data.total + '</td></tr></tfoot>');
                $('tfoot tr', element).append('<td colspan="' + options.length + '" style="font-size:20px;font-weight:bold;">合计：' + data.total + '</td>');
            }

            // 行数据
            if (data.rows) {
                var tbody = element.append('<tbody></tbody>');
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