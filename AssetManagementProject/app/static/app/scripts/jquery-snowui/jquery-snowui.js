/* =========================================================
 * jquery-snowui.js
 * =========================================================
 * Copyright 2016 黄耀樑
 *
 * ========================================================= */

$(function () {
    // 通用元素动作----------------------------------------------------start

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

            if (option.controller) {
                var url = '/query/' + option.controller;
                var data = option.queryParams || {};
                //$.get(url, data, function (d) {
                //    snowui.create_datagrid(t, d);
                //});

                snowui.datagrid.load(t, {
                    url: url,
                    data: data
                });

                var editUrl = '/' + option.controller + 'Detail/';

                $('#btnAdd').on('click', function () {
                    window.location.href = editUrl;
                });

                $('#btnModify').on('click', function () {
                    var arr = $('input:checked', t);
                    if (arr.length == 1) {
                        window.location.href = editUrl + $(arr[0]).val();
                    } else {
                        snowui.alert('请选择一项信息进行操作！');
                    }
                });

                $('#btnDelete').on('click', function () {
                    var arr = $('input:checked', t);
                    if (arr.length > 0) {
                        var ids = '';
                        for (var i = 0; i < arr.length; i++) {
                            if (ids) ids += ',';
                            ids += $(arr[i]).val();
                        }
                        snowui.confirm('确认删除吗？', function () {
                            //$.post('/remove/' + option.controller, { 'ids': ids }, function (result) {
                            //    if (result.success) {
                            //        snowui.datagrid.load(t, {
                            //            url: url,
                            //            data: data
                            //        });
                            //    } else {
                            //        snowui.alert(result.msg);
                            //    }
                            //});

                            $.ajax({
                                typ: 'POST',
                                contentType: "application/json; charset=utf-8",
                                dataType: "json",
                                url: '/remove/' + option.controller,
                                data: { 'ids': ids },
                                success: function (result) {
                                    if (result.success) {
                                        snowui.datagrid.load(t, {
                                            url: url,
                                            data: data
                                        });
                                    } else {
                                        snowui.alert(result.msg);
                                    }
                                },
                                error: function (e) {
                                    snowui.alert(e.responseText);
                                },
                                beforeSend: function () {
                                    $(":button").attr("disabled", true);
                                },
                                complete: function () {
                                    $(":button").attr("disabled", false);
                                }
                            });
                        });
                    } else {
                        snowui.alert('至少选择一项信息进行操作！');
                    }
                });
            }
        });

        // 排序
        //$('.snowui-datagrid thead tr th').on('click', function () {
        //    var t = $(this);
        //    var s = $.trim(t.attr("data-options"));
        //    if (s) {
        //        if (s.substring(0, 1) != "{") {
        //            s = "{" + s + "}";
        //        }
        //        var d = (new Function("return " + s))();
        //        if (d.sortable) {
        //            alert(d.field);
        //        }
        //    }
        //});
    }
    // datagrid----------------------------------------------------end

    // form----------------------------------------------------start
    // 黄耀樑 2016-07-26
    if ($('.snowui-form').length > 0) {
        var option = {};
        var t = $('.snowui-form');
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

        // 实现form参数功能
        if (option.controller) {
            var url = '/get/' + option.controller + '/';
            var data = option.queryParams || {};
            if (option.id) {
                url += option.id;
            }
            //$.get(url, data, function (d) {
            //    snowui.form.init(t, d);
            //});
            snowui.form.init(t, {
                url: url,
                data: data
            });

            // 绑定保存按钮
            $('#btnSave').on('click', function () {
                //$.post('/edit/' + option.controller, t.serialize(), function (result) {
                //    if (result.success) {
                //        // 回退并刷新
                //        window.location.href = document.referrer;
                //    } else {
                //        snowui.alert(result.msg);
                //    }
                //});
                snowui.form.submit(t, {
                    url: url,
                    data: data
                });
            });
        }

        // 绑定回退按钮
        $('#btnBack').on('click', function () {
            history.back(-1);
        });
    }
    // form----------------------------------------------------end
});

var snowui = {

    // 获取随机数
    // 黄耀樑 2016-07-26
    generateMixed: function (n) {
        var chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];
        var res = "";
        if (!n) {
            n = 6;
        }
        for (var i = 0; i < n ; i++) {
            var id = Math.ceil(Math.random() * 35);
            res += chars[id];
        }
        return res;
    },
    // 构建表格
    // 黄耀樑 2016-07-20
    datagrid: {
        init: function (element, data) {
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
        load: function (element, op) {
            $.ajax({
                typ: 'GET',
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                url: op.url,
                data: op.data,
                success: function (result) {
                    snowui.datagrid.init(element, result);
                },
                error: function (e) {
                    snowui.alert(e.responseText);
                }
            });
        }
    },

    // 构建表单
    // 黄耀樑 2016-07-26
    form: {
        init: function (element, op) {
            //if (obj) {
            //    for (var o in obj) {
            //        $('[name="' + o + '"]', element).val(obj[o]);
            //    }
            //}

            $.ajax({
                typ: 'GET',
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                url: op.url,
                data: op.data,
                success: function (obj) {
                    if (obj) {
                        for (var o in obj) {
                            $('[name="' + o + '"]', element).val(obj[o]);
                        }
                    }
                },
                error: function (e) {
                    snowui.alert(e.responseText);
                },
                beforeSend: function () {
                    $(":button").attr("disabled", true);
                    // self.message("正在登陆处理，请稍候...");
                },
                complete: function () {
                    $(":button").attr("disabled", false);
                }
            });
        },
        submit: function (element, op) {
            //$.post('/edit/' + option.controller, t.serialize(), function (result) {
            //    if (result.success) {
            //        // 回退并刷新
            //        window.location.href = document.referrer;
            //    } else {
            //        snowui.alert(result.msg);
            //    }
            //});
            $.ajax({
                typ: 'POST',
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                url: op.url,
                data: op.data,
                success: function (result) {
                    if (result.success) {
                        // 回退并刷新
                        window.location.href = document.referrer;
                    } else {
                        snowui.alert(result.msg);
                    }
                },
                error: function (e) {
                    snowui.alert(e.responseText);
                },
                beforeSend: function () {
                    $(":button").attr("disabled", true);
                    // self.message("正在登陆处理，请稍候...");
                },
                complete: function () {
                    $(":button").attr("disabled", false);
                }
            });
        }
    },

    // 构建表单
    // 黄耀樑 2016-07-27
    alert: function (msg, func) {
        var id = snowui.generateMixed();
        $('body').append('<div class="modal fade" id="' + id + '" tabindex="-1" role="dialog"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button><h4 class="modal-title">提示框</h4></div><div class="modal-body">' + msg + '</div><div class="modal-footer"><button type="button" class="btn btn-default" data-dismiss="modal" id="btnClose' + id + '">关闭</button></div></div></div></div>');
        $("#" + id).modal('show');
        if (func) {
            $("#btnClose" + id).on('click', func);
        }
    },

    // 构建表单
    // 黄耀樑 2016-07-27
    confirm: function (msg, funcOK, funcCancel) {
        var id = snowui.generateMixed();
        $('body').append('<div class="modal fade" id="' + id + '" tabindex="-1" role="dialog"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button><h4 class="modal-title">提示框</h4></div><div class="modal-body">' + msg + '</div><div class="modal-footer"><button type="button" class="btn btn-default" data-dismiss="modal" id="btnClose' + id + '">取消</button><button type="button" class="btn btn-primary" id="btnOK' + id + '">确认</button></div></div></div></div>');
        $("#" + id).modal('show');
        if (funcOK) {
            $("#btnOK" + id).on('click', funcOK);
        }
        if (funcCancel) {
            $("#btnClose" + id).on('click', funcCancel);
        }
    }
}