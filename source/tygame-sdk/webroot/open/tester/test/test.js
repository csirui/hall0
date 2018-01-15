
function onloadhtml(){
    document.write("网页JS文件初始化...\n")
//    alert('网页JS文件初始化22...')
}

//
//$().ready(function() {
//    alert('网页结构准备好...')
//    callNative('getTaskList');
//});
//
//function callNative(args){
//    setTimeout(function() {
//        try {
//            //alert("123123:"+window._javascript_4_java_+window.name)
//            alert("检查本地对象："+window._javascript_4_java_)
//            if (window._javascript_4_java_) {
//                args = args.replace(/\\/g, '\\\\')
//                args = args.replace(/\'/g, '\\\'')
//                var str = 'window._javascript_4_java_.getTaskList(\'' + args + '\')';
////                alert(str)
//                alert("准备调用本地代码...")
//                eval(str);
//            }
//        } catch (e) {
//            alert('js->' + e)
//        }
//    }, 200);
//}
//
//function getTaskListBack(params) {
//    alert("获得内容："+params)
//    var datas = JSON.parse(params);
//    var tasks = datas['result']['tasks'];
//    creatHtml('div_task_global', tasks);
//    alert("完成!")
////    bindBtnEvents();
////    onTabClick('tab_0');
////    myglobal.callNativeShow();
//}
//
//function filterTasks(tasks){
//    var task1=[];
//    var task2=[];
//    for ( var i = 0; i < tasks.length; i++) {
//        var medal = tasks[i];
//        if(checkNeedFetchMedal(medal)){
//            task1.push(medal)
//        }else{
//            task2.push(medal)
//        }
//    }
//    return task1.concat(task2)
//}
//
//function checkNeedFetchMedal(medal){
//    if ((medal[7] == 2 && medal[5] == medal[6])
//        || (medal[7] == 0 && medal[5] == medal[6])){
//        return true;
//    }
//    return false;
//}
//
//function creatHtml(divId, tasks) {
//    tasks=filterTasks(tasks)
////    alert(JSON.stringify(tasks))
//    var html = [];
//    html.push('<div style="display:block;" id="' + divId + '">');
//    for ( var i = 0; i < tasks.length; i++) {
//        var medal = tasks[i];
//        var oddclass='odd'
//        if(i%2==0){
//            oddclass=''
//        }
//        var medal_title = medal[3];
//        var progress_str = '进行中';
//        var btn_class = 'ui-btn-going ui-btn-zos';
//        var reward_ref = '';
//        var medal_icon = '';
//        if (medal[7] == 3 || medal[7] == 1) {
//            progress_str = '已经领取';
//        } else if ((medal[7] == 2 && medal[5] == medal[6])
//            || (medal[7] == 0 && medal[5] == medal[6])) {
//            progress_str = '领取奖励';
//            btn_class = 'ui-btn-reward ui-btn-orange-up';
//            reward_ref = 'ref=' + medal[0];
//        }
//        if (i < 5) {
//            medal_icon = 'images/task1.png';
//        } else {
//            medal_icon = 'images/task2.png';
//        }
//        var progress = medal[5] + '/' + medal[6];
//        var reward = medal[4] + '金币';
//
//        html.push('<div class="ui-grid ui-grid-c '+ oddclass +'">');
//        html.push('<div class="ui-block-a">');
//        html.push('<div class="left">');
////        html.push('<img class="s-icon" src="' + medal_icon + '">');
//        html.push('</div>');
//        html.push('<div class="item_c">');
//        html.push('<div class="list_title">' + medal_title + '</div>');
//        html.push('<div class="list_describe">进度：<span class="coin_desc">'
//            + progress + '</span></div>');
//        html.push('</div>');
//        html.push('</div>');
//        html.push('<div class="ui-block-b">');
//        html.push('奖励：<span class="coin_desc">' + reward + '</span>');
//        html.push('</div>');
//        html.push('<div class="ui-block-c">');
//        html.push('<button class="ui-btn ' + btn_class + ' " '
//            + reward_ref + ' >' + progress_str + '</button>');
//        html.push('</div>');
//        html.push('</div>');
//    }
//    html.push('</div>');
//    var htmlstr = html.join('')
//    $('.dataList').append(htmlstr);
//}

