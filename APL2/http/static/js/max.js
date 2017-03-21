 $(function(){
      $('.form-control:not(.nums):not(.num)').maxlength({
        alwaysShow: true
      })
      $('.nums').on('blur',function(){
        var maxNum=parseInt($(this).attr('max'));
        var vals=$(this).val();
        $(this).val(parseInt(vals));
        if($(this).val()>maxNum){
          $(this).val(maxNum);
        }
      })
      $('.num').on('blur',function(){
          var vals=$(this).val();
          $(this).val(parseInt(vals));
      })
})
      