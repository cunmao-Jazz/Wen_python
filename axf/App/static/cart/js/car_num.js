function doCart(goodsId,state) {
    $.post('/do_cart/',{'goodsId':goodsId,'state':state},function (data) {
            var num = data.num;
            // console.log(num);
            if(state !== 2){
                $('#'+goodsId+'num').text(num);
            }
            if(num == 0){
                $('#'+goodsId+'ul').remove();
            }
            $('#totalMoney').text(data.totaMoney);
            if(state == 2){
              var span =  $('#'+goodsId+'choose');
                 if(data.Bool){
                    span.text('√');
                 }else{
                    span.text('');
                 }
            }
            if(state == 3){
              var spanall =  $('.choose');
              var all = $('#all');
                 if(data.Bool){
                     all.text('√');
                     spanall.text('√');
                 }else{
                     spanall.text('');
                     all.text('');
                 }
            }
    });
}