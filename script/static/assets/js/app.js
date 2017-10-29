$(function () {

    var $fullText = $('.admin-fullText');
    $('#admin-fullscreen').on('click', function () {
        $.AMUI.fullscreen.toggle();
    });

    $(document).on($.AMUI.fullscreen.raw.fullscreenchange, function () {
        $fullText.text($.AMUI.fullscreen.isFullscreen ? '退出全屏' : '开启全屏');
    });

    $('.tpl-switch').find('.tpl-switch-btn-view').on('click', function () {
        $(this).prev('.tpl-switch-btn').prop("checked", function () {
            if ($(this).is(':checked')) {
                return false
            } else {
                return true
            }
        })
        // console.log('123123123')

    })
})
// ==========================
// 侧边导航下拉列表
// ==========================

$('.tpl-left-nav-link-list').on('click', function () {
    $(this).siblings('.tpl-left-nav-sub-menu').slideToggle(80)
        .end()
        .find('.tpl-left-nav-more-ico').toggleClass('tpl-left-nav-more-ico-rotate');
})


// ==========================
// 头部导航隐藏菜单
// ==========================

$('.tpl-header-nav-hover-ico').on('click', function () {
    $('.tpl-left-nav').toggle();
    $('.tpl-content-wrapper').toggleClass('tpl-content-wrapper-hover');
})


// ==========================
// Category Setting
// ==========================

$(function () {
    $('#doc-prompt-toggle').on('click', function () {
        $('#my-prompt').modal({
            relatedTarget: this,
            onConfirm: function (e) {
                axios.post('/api/addNewCategory', {
                    "category": e.data,
                    "type": 0,
                    "parent_id": 0
                }).then(function (response) {
                    alert("创建成功!");

                    var select = document.getElementById('setting_category_list');
                    var opt = document.createElement('option');
                    opt.value = response.data.data.id;
                    opt.innerHTML = response.data.data.category;
                    select.appendChild(opt);

                    $('#setting_category_input').val('');

                }).catch(function (error) {
                    console.log(error);
                });
            },
            onCancel: function (e) {
                console.log(e.data);
                $('#setting_category_input').val('');
            }
        });
    });


    $('#doc-prompt-toggle1').on('click', function () {
        var myselect = document.getElementById("setting_category_list");
        var index = myselect.selectedIndex;

        if (index != -1) {
            var category_id = myselect.options[index].value;
            var category = myselect.options[index].text;
            $('#setting_model_prompt_category_id_input').val(category_id);
            $('#setting_model_prompt_category_name_input').val(category);
            $('#setting_model_prompt_sub_category_input').val('');

            $('#my-prompt1').modal({
                relatedTarget: this,
                onConfirm: function (e) {
                    alert(e.data)
                    if (e.data && e.data.length == 3) {
                        axios.post('/api/addNewCategory', {
                            "category": e.data[2],
                            "type": 1,
                            "parent_id": parseInt(e.data[0])
                        }).then(function (response) {
                            var content = $('#setting_category_table tbody').html();
                            content += "<tr><td>" + response.data.data.id + "</td>";
                            content += "<td><a href=\"#\">" + e.data[1] + "</a></td>";
                            content += "<td class=\"am-hide-sm-only\"><a href=\"/config/product/display/"+ response.data.data.type +"_"+ response.data.data.id +"\">" + response.data.data.category + "</a></td>";
                            content += "<td><div class=\"am-btn-toolbar\"><div class=\"am-btn-group am-btn-group-xs\">";
                            content += "<button class=\"am-btn am-btn-default am-btn-xs am-text-secondary\"><span class=\"am-icon-pencil-square-o\"></span> 编辑</button>";
                            content += "<button class=\"am-btn am-btn-default am-btn-xs am-text-danger am-hide-sm-only\" onclick=\"deleteSubcategoryById(" + response.data.data.id + ")\"><span class=\"am-icon-trash-o\"></span> 删除</button>";
                            content += "</div></div></td></tr>";
                            $('#setting_category_table tbody').html(content);

                            $('#setting_model_prompt_category_id_input').val('');
                            $('#setting_model_prompt_category_name_input').val('');
                            $('#setting_model_prompt_sub_category_input').val('');

                        }).catch(function (error) {
                            console.log(error);
                            $('#setting_model_prompt_category_id_input').val('');
                            $('#setting_model_prompt_category_name_input').val('');
                            $('#setting_model_prompt_sub_category_input').val('');
                        });
                    }
                },
                onCancel: function (e) {
                    console.log(e.data);
                }
            });
        }
    });


    $("#setting_category_delete").on('click', function () {
        var myselect = document.getElementById("setting_category_list");
        var index = myselect.selectedIndex;

        if (index != -1) {
            var category_id = myselect.options[index].value;
            console.log(category_id);
            axios.post('/api/deleteCategoryAndSubCategoryById', {
                "id": parseInt(category_id)
            }).then(function (response) {
                console.log(response);
                console.log("删除成功!");
                window.location.href = "/config";

            }).catch(function (error) {
                console.log(error);
            });
        }
    });
});


function refreshCategoryList() {
    axios.get('/api/getRootCategory').then(function (response) {
        var select = document.getElementById('setting_category_list');
        for (var i = 0; i < response.data.data.length; i++) {
            var opt = document.createElement('option');
            opt.value = response.data.data[i].id;
            opt.innerHTML = response.data.data[i].category;
            select.appendChild(opt);
        }

    }).catch(function (error) {
        console.log(error);
    });
}

function refreshSubCategoryTable(){
    var value = $('#setting_category_list').val();
    var text = $("select#setting_category_list option:selected").text();

    axios.get('/api/getSubCategoryById/' + value).then(function (response) {
        var len = $("tbody").children().length;
        if (len > 0) {
            $("tbody").children().remove();
        }

        var content = "";
        for (var j = 0; j < response.data.data.length; j++) {

            content += "<tr><td>" + response.data.data[j].id + "</td>";
            content += "<td><a href=\"#\">" + text + "</a></td>";
            content += "<td class=\"am-hide-sm-only\"><a href=\"/config/product/display/"+ response.data.data[j].type + "_" + response.data.data[j].id +"\">" + response.data.data[j].category + "</a></td>";
            content += "<td><div class=\"am-btn-toolbar\"><div class=\"am-btn-group am-btn-group-xs\">";
            content += "<button class=\"am-btn am-btn-default am-btn-xs am-text-secondary\"><span class=\"am-icon-pencil-square-o\"></span> 编辑</button>";
            content += "<button class=\"am-btn am-btn-default am-btn-xs am-text-danger am-hide-sm-only\" onclick=\"deleteSubcategoryById(" + response.data.data[j].id + ")\"><span class=\"am-icon-trash-o\"></span> 删除</button>";
            content += "</div></div></td></tr>";

        }
        $('#setting_category_table tbody').html(content);

    }).catch(function (error) {
        console.log(error);
    });
}

$('#setting_category_list').change(function () {
    var value = $(this).val();
    var text = $("select#setting_category_list option:selected").text();

    axios.get('/api/getSubCategoryById/' + value).then(function (response) {
        var len = $("tbody").children().length;
        if (len > 0) {
            $("tbody").children().remove();
        }

        var content = "";
        for (var j = 0; j < response.data.data.length; j++) {

            content += "<tr><td>" + response.data.data[j].id + "</td>";
            content += "<td><a href=\"#\">" + text + "</a></td>";
            content += "<td class=\"am-hide-sm-only\"><a href=\"/config/product/display/"+ response.data.data[j].type + "_" + response.data.data[j].id +"\">" + response.data.data[j].category + "</a></td>";
            content += "<td><div class=\"am-btn-toolbar\"><div class=\"am-btn-group am-btn-group-xs\">";
            content += "<button class=\"am-btn am-btn-default am-btn-xs am-text-secondary\"><span class=\"am-icon-pencil-square-o\"></span> 编辑</button>";
            content += "<button class=\"am-btn am-btn-default am-btn-xs am-text-danger am-hide-sm-only\" onclick=\"deleteSubcategoryById(" + response.data.data[j].id + ")\"><span class=\"am-icon-trash-o\"></span> 删除</button>";
            content += "</div></div></td></tr>";

        }
        $('#setting_category_table tbody').html(content);

    }).catch(function (error) {
        console.log(error);
    });
});


function deleteSubcategoryById(id) {
    axios.post('/api/deleteSubCategoryById', {
        "id": parseInt(id)
    }).then(function (response) {
        console.log("删除成功!");
        window.location.href = "/config";

    }).catch(function (error) {
        console.log(error);
    });
}

$('#a_category').on('click', function () {
    window.location.href = "/config";
});

$('#a_products').on('click', function () {
    window.location.href = "/config/products";
});


// ==========================
// Products Setting
// ==========================
function LoadProductCategoryList() {
    axios.get('/api/getRootCategory').then(function (response) {
        console.log(response.data);
        var select = document.getElementById('product_category');
        for (var i = 0; i < response.data.data.length; i++) {
            var opt = document.createElement('option');
            opt.value = response.data.data[i].id;
            opt.innerHTML = response.data.data[i].category;
            select.appendChild(opt);
        }

    }).catch(function (error) {
        console.log(error);
    });
}


$('#product_category').change(function () {
    var value = $(this).val();
    var text = $("select#product_category option:selected").text();

    axios.get('/api/getSubCategoryById/' + value).then(function (response) {
        $('#product_sub_category').html('');
        var select = document.getElementById('product_sub_category');
        for (var i = 0; i < response.data.data.length; i++) {
            var opt = document.createElement('option');
            opt.value = response.data.data[i].id;
            opt.innerHTML = response.data.data[i].category;
            select.appendChild(opt);
        }

    }).catch(function (error) {
        console.log(error);
    });
});