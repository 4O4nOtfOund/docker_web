/**
 * Created by GAOYY on 2017/12/13 0013.
 */


$('#chkAll').click(function(){
    console.log('toggle checked');
    var that = this;
    $(this).closest('table').find('tr > td:first-child input:checkbox')
    .each(function() {
        this.checked = that.checked;
        $(this).closest('tr').toggleClass('selected');
    });
});
//
// 	$('[data-rel="tooltip"]').tooltip({placement: tooltip_placement});
// 	function tooltip_placement(context, source) {
// 		var $source = $(source);
// 		var $parent = $source.closest('table')
// 		var off1 = $parent.offset();
// 		var w1 = $parent.width();
//
// 		var off2 = $source.offset();
// 		var w2 = $source.width();
//
// 		if( parseInt(off2.left) < parseInt(off1.left) + parseInt(w1 / 2) ) return 'right';
// 		return 'left';
// 	}
// })


var user=[{"id": 1, "name": "张三","age":"25"},
    {"id": 2, "name": "李四","age":"35"},
    {"id": 3, "name": "王五","age":"20"},
    {"id": 4, "name": "老王","age":"20"},
    {"id": 5, "name": "老张","age":"25"},
    {"id": 6, "name": "李四","age":"35"},
    {"id": 7, "name": "王五","age":"20"},
    {"id": 8, "name": "老王","age":"20"},
    {"id": 9, "name": "abc","age":"25"},
    {"id": 10, "name": "李b四","age":"35"},
    {"id": 11, "name": "125","age":"20"},
    {"id": 12, "name": "246","age":"20"},
    {"id": 13, "name": "张三","age":"25"},
    {"id": 14, "name": "李四","age":"35"},
    {"id": 15, "name": "王五","age":"20"},
    {"id": 16, "name": "老王","age":"20"},
    {"id": 17, "name": "张三","age":"25"},
    {"id": 18, "name": "李四","age":"35"},
    {"id": 19, "name": "王五","age":"20"},
    {"id": 20, "name": "老王","age":"20"}];

$(function(){
    $("#ContainerSearch").keyup(function(event){
        var searchText = $("#ContainerSearch").val();
        console.log(searchText);
        var tableBody = "";
        if (searchText==""){

        }
        else {
            $.each(user, function(id, item){
                if (item.name.indexOf(searchText)!=-1){
                    tableBody+="<tr class='odd'><td class='center sorting_1'><label><input type='checkbox' class='ace'><span class='lbl'></span></label></td><td class=''><a href='#'>"+item.id+"</a></td><td class=''>"+item.name+"</td><td class='hidden-480'>"+item.age+"</td><td class=''>"+item.id+"</td><td class='hidden-480'><span class='label label-sm label-warning'>Expiring</span></td><td class=''><div class='visible-md visible-lg hidden-sm hidden-xs action-buttons'><a class='blue' href='#'><i class='icon-zoom-in bigger-130'></i></a> <a class='green' href='#'><i class='icon-pencil bigger-130'></i></a> <a class='red' href='#'><i class='icon-trash bigger-130'></i></a></div><div class='visible-xs visible-sm hidden-md hidden-lg'><div class='inline position-relative'><button class='btn btn-minier btn-yellow dropdown-toggle' data-toggle='dropdown'><i class='icon-caret-down icon-only bigger-120'></i></button><ul class='dropdown-menu dropdown-only-icon dropdown-yellow pull-right dropdown-caret dropdown-close'><li><a href='#' class='tooltip-info' data-rel='tooltip' title='' data-original-title='View'><span class='blue'><i class='icon-zoom-in bigger-120'></i></span></a></li><li><a href='#' class='tooltip-success' data-rel='tooltip' title='' data-original-title='Edit'><span class='green'><i class='icon-edit bigger-120'></i></span></a></li><li><a href='#' class='tooltip-error' data-rel='tooltip' title='' data-original-title='Delete'><span class='red'><i class='icon-trash bigger-120'></i></span></a></li></ul></div></div></td></tr>";
                    $("#ContainerBody").html(tableBody);
                }
            })
        }
    })
});

$(function(){
    $("#HostSearch").keyup(function(event){
        var searchText = $("#HostSearch").val();
        console.log(searchText);
        var tableBody = "";
        if (searchText==""){

        }
        else {
            $.each(user, function(id, item){
                if (item.name.indexOf(searchText)!=-1){
                    tableBody+="<tr class='odd'><td class='center sorting_1'><label><input type='checkbox' class='ace'><span class='lbl'></span></label></td><td class=''><a href='#'>"+item.id+"</a></td><td class=''>"+item.name+"</td><td class='hidden-480'>"+item.age+"</td><td class=''>"+item.id+"</td><td class='hidden-480'><span class='label label-sm label-warning'>Expiring</span></td><td class=''><div class='visible-md visible-lg hidden-sm hidden-xs action-buttons'><a class='blue' href='#'><i class='icon-zoom-in bigger-130'></i></a> <a class='green' href='#'><i class='icon-pencil bigger-130'></i></a> <a class='red' href='#'><i class='icon-trash bigger-130'></i></a></div><div class='visible-xs visible-sm hidden-md hidden-lg'><div class='inline position-relative'><button class='btn btn-minier btn-yellow dropdown-toggle' data-toggle='dropdown'><i class='icon-caret-down icon-only bigger-120'></i></button><ul class='dropdown-menu dropdown-only-icon dropdown-yellow pull-right dropdown-caret dropdown-close'><li><a href='#' class='tooltip-info' data-rel='tooltip' title='' data-original-title='View'><span class='blue'><i class='icon-zoom-in bigger-120'></i></span></a></li><li><a href='#' class='tooltip-success' data-rel='tooltip' title='' data-original-title='Edit'><span class='green'><i class='icon-edit bigger-120'></i></span></a></li><li><a href='#' class='tooltip-error' data-rel='tooltip' title='' data-original-title='Delete'><span class='red'><i class='icon-trash bigger-120'></i></span></a></li></ul></div></div></td></tr>";
                    $("#HostBody").html(tableBody);
                }
            })
        }
    })
});

$(function(){
    $("#ImageSearch").keyup(function(event){
        var searchText = $("#ImageSearch").val();
        console.log(searchText);
        var tableBody = "";
        if (searchText==""){

        }
        else {
            $.each(user, function(id, item){
                if (item.name.indexOf(searchText)!=-1){
                    tableBody+="<tr class='odd'><td class='center sorting_1'><label><input type='checkbox' class='ace'><span class='lbl'></span></label></td><td class=''><a href='#'>"+item.id+"</a></td><td class=''>"+item.name+"</td><td class='hidden-480'>"+item.age+"</td><td class=''>"+item.id+"</td><td class='hidden-480'><span class='label label-sm label-warning'>Expiring</span></td><td class=''><div class='visible-md visible-lg hidden-sm hidden-xs action-buttons'><a class='blue' href='#'><i class='icon-zoom-in bigger-130'></i></a> <a class='green' href='#'><i class='icon-pencil bigger-130'></i></a> <a class='red' href='#'><i class='icon-trash bigger-130'></i></a></div><div class='visible-xs visible-sm hidden-md hidden-lg'><div class='inline position-relative'><button class='btn btn-minier btn-yellow dropdown-toggle' data-toggle='dropdown'><i class='icon-caret-down icon-only bigger-120'></i></button><ul class='dropdown-menu dropdown-only-icon dropdown-yellow pull-right dropdown-caret dropdown-close'><li><a href='#' class='tooltip-info' data-rel='tooltip' title='' data-original-title='View'><span class='blue'><i class='icon-zoom-in bigger-120'></i></span></a></li><li><a href='#' class='tooltip-success' data-rel='tooltip' title='' data-original-title='Edit'><span class='green'><i class='icon-edit bigger-120'></i></span></a></li><li><a href='#' class='tooltip-error' data-rel='tooltip' title='' data-original-title='Delete'><span class='red'><i class='icon-trash bigger-120'></i></span></a></li></ul></div></div></td></tr>";
                    $("#ImageBody").html(tableBody);
                }
            })
        }
    })
});