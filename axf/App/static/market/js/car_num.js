function doCart(goodsId,state) {
    $.post('/do_cart/',{'goodsId':goodsId,'state':state},function (data) {
        // console.log(data.code)
        // 1未登录
        if(data.code == 1){
            if(window.confirm('您还没有登录 是否前去登录')){
                window.location.href = '/login/?next=market';
            }
        }else{
            var num = data.num;
            console.log(num);
            $('#'+goodsId+'num').text(num);
        }
    });
}