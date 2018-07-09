  $(function(){
      var len = $(".scroll-con li").length;
      if(len > 1){
          textRoll=function(){
              $(".scroll-wrap").find(".scroll-con").animate({
                  marginTop : "-30px"
              },1000,function(){
                  $(this).css({marginTop : "0px"}).find("li:first").appendTo(this);
              });
          };

          var roll= setInterval('textRoll()',3000);
          $(".scroll-con li").hover(function() {
              clearInterval(roll);
          }).mouseout(function(){
              roll= setInterval('textRoll()',3000);
          });
      }
  })