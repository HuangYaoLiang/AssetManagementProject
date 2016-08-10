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
            // 默认值
            var option = {
                usually: true // 渲染 CRUD
            };
            var $t = $(n);
            var s = $.trim($t.attr("data-options"));
            if (s) {
                if (s.substring(0, 1) != "{") {
                    s = "{" + s + "}";
                }
                $.extend(option, (new Function("return " + s))());
            }

            // 添加脚部
            $t.append('<tfoot><tr></tr></tfoot>');

            // 添加 bootstrap 样式
            $t.addClass('table table-striped table-condensed'); // table-bordered边框             
            $('thead tr', $t).addClass('info');
            $('tfoot tr', $t).addClass('success');

            if (option.controller) {
                option.url = '/query/' + option.controller;
                option.data = option.queryParams || {};

                // 默认排序
                if (option.sortName) {
                    option.data.sortName = option.sortName;
                    if (option.sortOrder) {
                        option.data.sortOrder = option.sortOrder;
                    } else {
                        option.data.sortOrder = 'asc';
                    }
                }
            }

            $t.attr('data-index', i);

            // 放进容器
            snowui.datagrid.container[i] = { $element: $t, option: option };
            // 渲染标题列
            snowui.datagrid.init($t);
            // 获取数据
            snowui.datagrid.load($t, {
                url: option.url,
                data: option.data
            });

            // 是否启用通用编辑功能，[添加 修改 删除]，默认启用,先渲染其他，因为搜索需要其他数据
            if (option.usually) {
                var fieldDropdown = ''; // 下拉标题
                var fieldAllDropdown = [];
                var f_option = snowui.datagrid.container[i].option;
                $.each(f_option.columns, function (f_i, f_o) {
                    if (f_o.field && f_o.searchable) {
                        fieldAllDropdown.push(f_o.field);
                        fieldDropdown += ('<li><a href="#" data-search="' + f_o.field + '">' + f_o.title + '</a></li>');
                    }
                });
                f_option.data.searchName = fieldAllDropdown.join();

                $t.before('<br/>' +
    '<div class="row">' +
    '   <div class="col-xs-4">' +
    '       <button class="snowui-linkbutton snowui-datagrid-btn-' + i + ' btn btn-primary">添加</button>' +
    '       &nbsp;&nbsp;&nbsp;' +
    '       <button class="snowui-linkbutton snowui-datagrid-btn-' + i + ' btn btn-warning">编辑</button>' +
    '       &nbsp;&nbsp;&nbsp;' +
    '       <button class="snowui-linkbutton snowui-datagrid-btn-' + i + ' btn btn-danger">删除</button>' +
    '   </div>' +
    '   <div class="col-xs-4 col-xs-offset-4" style="text-align:right;">' +
    '       <div class="input-group">' +
    '           <div class="input-group-btn">' +
    '               <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" data-index="' + i + '">全部 <span class="caret"></span></button>' +
    '               <ul class="dropdown-menu snowui-datagrid-search-dropdown-menu">' +
    fieldDropdown +
    '                   <li role="separator" class="divider"></li>' +
    '                   <li><a href="#" data-search="' + f_option.data.searchName + '">全部</a></li>' +
    '               </ul>' +
    '           </div>' +
    '           <input type="text" class="form-control" placeholder="搜索..." id="snowui-datagrid-txt-' + i + '">' +
    '           <span class="input-group-btn">' +
    '               <button class="snowui-linkbutton snowui-datagrid-btn-' + i + ' btn btn-default">Go!</button>' +
    '           </span>' +
    '       </div>' +
    '   </div>' +
    '</div>' +
    '<br/>');
                var editUrl = '/' + option.controller + 'Detail/';

                $.each($(".snowui-datagrid-btn-" + i), function (btn_i, btn_o) {
                    if (btn_i == 0) {
                        // 添加
                        $(btn_o).on('click', function () {
                            window.location.href = editUrl;
                        });
                    }
                    else if (btn_i == 1) {
                        // 编辑
                        $(btn_o).on('click', function () {
                            var id = snowui.datagrid.getCheckedOne($t);
                            if (id) {
                                window.location.href = editUrl + id;
                            }
                        });
                    }
                    else if (btn_i == 2) {
                        // 删除
                        $(btn_o).on('click', function () {
                            var ids = snowui.datagrid.getCheckedAll();
                            if (ids) {
                                snowui.confirm('确认删除吗？', function () {
                                    $.ajax({
                                        type: 'POST',
                                        dataType: "json",
                                        url: '/remove/' + option.controller,
                                        data: { 'ids': ids },
                                        success: function (result) {
                                            if (result.success) {
                                                snowui.datagrid.load($t, {
                                                    url: option.url,
                                                    data: snowui.datagrid.container[i].option.data
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
                                            snowui.datagrid.clearCheckbox($t);
                                        }
                                    });
                                });
                            }
                        });
                    }
                    else if (btn_i == 3) {
                        // 搜索
                        $(btn_o).on('click', function () {
                            var s_value = $('#snowui-datagrid-txt-' + i).val();
                            var s_option = snowui.datagrid.container[i].option;
                            var s_data = s_option.data;
                            s_data.searchVal = s_value;

                            if (s_data.searchName && s_data.searchVal) {
                                snowui.datagrid.load($t, {
                                    url: option.url,
                                    data: s_data
                                });
                            }
                        });
                    }
                });
            }
        });

        // 搜索框 下拉菜单
        $(".snowui-datagrid-search-dropdown-menu li a").bind("click", function () {
            var $this = $(this);
            var $btn = $this.parent().parent().prev();
            $btn.text($this.text() + ' ');
            $btn.append("<span class='caret'>");
            var i = $btn.attr('data-index');
            var option = snowui.datagrid.container[i].option;
            option.data.searchName = $this.attr('data-search');
        });
    }
    // datagrid----------------------------------------------------end

    // form----------------------------------------------------start
    // 黄耀樑 2016-07-26
    if ($('.snowui-form').length > 0) {
        // 默认值
        var option = {
            usually: true // 返回和保存
        };
        var $t = $('.snowui-form');
        var s = $.trim($t.attr("data-options"));

        if (s) {
            if (s.substring(0, 1) != "{") {
                s = "{" + s + "}";
            }

            $.extend(option, (new Function("return " + s))());
        }

        // 添加 bootstrap 样式
        $t.addClass('form-horizontal');

        // 设置表单通用属性
        $t.attr({ method: "post", action: "/edit" });

        // 实现form参数功能
        if (option.controller) {
            var init_url = '/get/' + option.controller + '/';
            var save_url = '/edit/' + option.controller;
            var data = option.queryParams || {};
            data.id = 0;

            if (option.id) {
                init_url += option.id;
                data.id = option.id;
            }

            snowui.form.init($t, {
                url: init_url,
                data: data
            });

            // 是否启用通用编辑功能，[返回 保存]，默认启用
            if (option.usually) {
                $t.before(
                    '<br/>' +
'<div class="row">' +
'     <div class="col-xs-11">' +
'        <button class="snowui-linkbutton snowui-form-btn btn btn-info">返回</button>' +
'    </div>' +
'    <div class="col-xs-1">' +
'        <button class="snowui-linkbutton snowui-form-btn btn btn-success">保存</button>' +
'    </div>' +
'</div>' +
'<br/>');
            }

            $.each($(".snowui-form-btn"), function (btn_i, btn_o) {
                if (btn_i == 0) {
                    // 回退按钮
                    $(btn_o).on('click', function () {
                        history.back(-1);
                    });
                }
                else if (btn_i == 1) {
                    // 保存按钮
                    $(btn_o).on('click', function () {
                        snowui.form.submit($t, {
                            url: save_url,
                            data: data
                        });
                    });
                }
            });
        }
    }
    // form----------------------------------------------------end

    // linkbutton----------------------------------------------------start
    // 黄耀樑 2016-08-08
    $.each($('.snowui-linkbutton'), function (i, n) {
        if (this.tagName == 'button') {
            $(this).attr('type', 'button');
        }
    });
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
        container: [], // 定义 datagrid 容器
        // 获取复选框一个选择值
        // 黄耀樑 2016-08-05
        getCheckedOne: function ($element) {
            var $t = {};
            if ($element) {
                if ($.type($element) === "string") {
                    $t = $($element);
                } else {
                    $t = $element;
                }
            } else {
                $t = $('.snowui-datagrid');
            }

            var arr = $('input:checked', $t);
            if (arr.length == 1) {
                snowui.datagrid.clearCheckbox($t);
                return $(arr[0]).val();
            } else {
                snowui.alert('请选择一项信息进行操作！', function () {
                    snowui.datagrid.clearCheckbox($t);
                });
                return false;
            }
        },
        // 获取复选框全部选择值
        // 黄耀樑 2016-08-05
        getCheckedAll: function ($element) {
            var $t = {};
            if ($element) {
                if ($.type($element) === "string") {
                    $t = $($element);
                } else {
                    $t = $element;
                }
            } else {
                $t = $('.snowui-datagrid');
            }

            var arr = $('input:checked', $t);
            if (arr.length > 0) {
                var ids = '';
                for (var i = 0; i < arr.length; i++) {
                    if (ids) ids += ',';
                    ids += $(arr[i]).val();
                }
                return ids;
            } else {
                snowui.alert('至少选择一项信息进行操作！', function () {
                    snowui.datagrid.clearCheckbox($t);
                });
                return false;
            }
        },
        // 清空复选框
        // 黄耀樑 2016-07-28
        clearCheckbox: function ($element) {
            $(":checkbox", $element).prop("checked", false);
        },
        // 渲染 datagrid
        // 黄耀樑 2016-07-26
        init: function ($element, data) {
            var option = snowui.datagrid.container[$element.attr('data-index')].option;
            //var options = [];
            if (!option.columns) {
                option.columns = [];
                $.each($('thead tr th', $element), function (i, n) {
                    var $t = $(n);
                    var s = $.trim($t.attr("data-options"));
                    if (s) {
                        if (s.substring(0, 1) != "{") {
                            s = "{" + s + "}";
                        }

                        // 列 默认值
                        var column = {
                            title: $t.text(),   // 列标题
                            sortable: true,     // 启用排序
                            searchable: true    // 启用搜索      
                        };

                        $.extend(column, (new Function("return " + s))());

                        option.columns.push(column);
                    }
                });
            }

            $.each(option.columns, function (i, n) {
                if (n.field) {
                    // 排序 
                    if (n.sortable) {
                        var $t = $('thead tr th[data-options*="field:\'' + n.field + '\'"]', $element);
                        $t.css("cursor", "pointer");
                        if ($('.datagrid-sort-icon', $t).length == 0 && $('.caret', $t).length == 0) {
                            $t.append('<span class="datagrid-sort-icon"></span>');
                        }
                        $t.on('click', function () {
                            // 还原其他的排序图标
                            var sortEle = $('thead tr th span.caret', $element);
                            if (sortEle.length > 0) {
                                var sortThEle = sortEle.parent();
                                sortEle.remove();
                                sortThEle.append('<span class="datagrid-sort-icon"></span>');
                            }
                            var ele = $(this);
                            var op = option;
                            $('.datagrid-sort-icon', ele).remove(); // 先移除默认排序图标  
                            if ($('.caret', ele).length == 0) {
                                ele.append('<span class="caret" style="margin-left:5px;"></span>');
                            }
                            if (ele.hasClass("dropup")) {
                                //desc
                                ele.removeClass("dropup");
                                op.data.sortOrder = "desc";
                            } else {
                                // asc
                                ele.addClass("dropup");
                                op.data.sortOrder = "asc";
                            }

                            op.data.sortName = n.field;
                            snowui.datagrid.load($element, {
                                url: op.url,
                                data: op.data
                            });
                        });
                    }
                }
            });
        },
        // 加载 datagrid 数据
        // 黄耀樑 2016-07-26
        load: function ($element, op) {
            $.ajax({
                typ: 'GET',
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                url: op.url,
                data: op.data,
                success: function (result) {
                    var columns = snowui.datagrid.container[$element.attr('data-index')].option.columns;
                    // 它们的出现次序是：thead、tfoot、tbody，这样浏览器就可以在收到所有数据前呈现页脚了
                    if (columns && result) {
                        // 脚部信息
                        if (result.total) {
                            $('tfoot tr', $element).empty().append('<td colspan="' + columns.length + '" style="font-size:20px;font-weight:bold;">合计：' + result.total + '</td>');
                        }

                        // 行数据
                        if (result.rows) {
                            var $tbody = $('tbody', $element);
                            if ($tbody.length == 0) {
                                $tbody = $element.append('<tbody></tbody>');
                            }
                            else {
                                $tbody.empty();
                            }
                            for (var i = 0; i < result.rows.length; i++) {
                                var column = '';
                                var row = result.rows[i];
                                for (var j = 0; j < columns.length; j++) {
                                    var colHead = '<td>';
                                    var colBody = '';
                                    var dic = columns[j];
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
                                $tbody.append('<tr>' + column + '<tr>');
                            }
                        }
                    }
                },
                error: function (e) {
                    snowui.alert(e.responseText);
                },
                beforeSend: function () {
                    snowui.load.show();
                },
                complete: function () {
                    snowui.load.hide();
                }
            });
        }
    },

    // 构建表单
    // 黄耀樑 2016-07-26
    form: {
        // 渲染 form
        // 黄耀樑 2016-07-27
        init: function ($element, op) {
            $.ajax({
                typ: 'GET',
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                url: op.url,
                data: op.data,
                success: function (obj) {
                    if (obj) {
                        for (var o in obj) {
                            $('[name="' + o + '"]', $element).val(obj[o]);
                        }
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
        },
        // 提交 form
        // 黄耀樑 2016-07-27
        submit: function ($element, op) {
            var data = $element.serialize();
            if (op.data) {
                data = $.param(op.data) + '&' + data;
            }

            $.ajax({
                type: 'POST',
                dataType: "json",
                url: op.url,
                data: data,
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
                },
                complete: function () {
                    $(":button").attr("disabled", false);
                }
            });
        }
    },

    // load 遮罩层
    load: {
        show: function () {
            if ($(".snowui-load").length == 0) {
                // data-backdrop="static"  点击空白的时候 就不会关闭 要用事件关闭
                $('body').append('<div class="modal fade snowui-load" tabindex="-1" style="text-align:center;" data-backdrop="static"></div>');
            }
            $(".snowui-load").modal('show');
        },
        hide: function () {
            if ($(".snowui-load").length > 0) {
                $(".snowui-load").modal('hide');
            }
        }
    },

    // 构建表单
    // 黄耀樑 2016-07-27
    alert: function (msg, func) {
        var id = snowui.generateMixed();
        $('body').append('<div class="modal fade" id="' + id + '" tabindex="-1" role="dialog"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button><h4 class="modal-title">提示框</h4></div><div class="modal-body">' + msg + '</div><div class="modal-footer"><button type="button" class="btn btn-default" data-dismiss="modal" id="btnClose' + id + '">关闭</button></div></div></div></div>');
        $("#" + id).modal('show');
        $("#btnClose" + id).on('click', function () {
            $("#" + id).modal('hide');
            if (func) {
                func();
            }
        });
    },

    // 构建表单
    // 黄耀樑 2016-07-27
    confirm: function (msg, funcOK, funcCancel) {
        var id = snowui.generateMixed();
        $('body').append('<div class="modal fade" id="' + id + '" tabindex="-1" role="dialog"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button><h4 class="modal-title">提示框</h4></div><div class="modal-body">' + msg + '</div><div class="modal-footer"><button type="button" class="btn btn-default" data-dismiss="modal" id="btnClose' + id + '">取消</button><button type="button" class="btn btn-primary" id="btnOK' + id + '">确认</button></div></div></div></div>');
        $("#" + id).modal('show');
        $("#btnOK" + id).on('click', function () {
            $("#" + id).modal('hide');
            if (funcOK) {
                funcOK();
            }
        });
        $("#btnClose" + id).on('click', function () {
            $("#" + id).modal('hide');
            if (funcCancel) {
                funcCancel();
            }
        });
    }
}