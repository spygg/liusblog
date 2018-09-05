$(function(){

  var h2 = $('h2')
  var h3 = $('h3')

  if (h2.length == 0){
    return
  }

  html_toc = ''
  for(var i = 0; i < h2.length; i++){
    //添加id属性
    var id = $(h2.get(i)).text().trim();
    $(h2.get(i)).attr({'id': id})

    var toc = '';
    //toc += "<li>" +  "<a href='#" + $(h2.get(i)).text().trim() +"'>" + $(h2.get(i)).text()  + "</a>" 
    toc += "<li>" +  "<a href='javascript:void(0)'>" + $(h2.get(i)).text()  + "</a>" 
   
    // console.log($(h2.get(i)).text(), $(h2.get(i)).position().top)

    toc += '<ul class="toc-level2">'

    for(var j = 0; j < h3.length; j++){
      var next_top = h2.get(i + 1);

      if(next_top != undefined){
        if($(h3.get(j)).position().top > $(h2.get(i)).position().top && $(h3.get(j)).position().top < $(next_top).position().top){
          // console.log($(h3.get(j)).text()) 
            id = $(h3.get(j)).text().trim();
            $(h3.get(j)).attr({'id': id})
          toc +=   "<li>" +  "<a href='javascript:void(0)'>" + $(h3.get(j)).text()  + "</a></li>" 
          //toc +=   "<li>" +  "<a href='#" + $(h3.get(j)).text().trim() +"'>" + $(h3.get(j)).text()  + "</a></li>" 
        }
      }
      else{
         if($(h3.get(j)).position().top > $(h2.get(i)).position().top){
          // console.log($(h3.get(j)).text())    
            //toc +=   "<li>" +  "<a href='#" + $(h3.get(j)).text().trim() +"'>" + $(h3.get(j)).text()  + "</a></li>" 

            id = $(h3.get(j)).text().trim();
            $(h3.get(j)).attr({'id': id})
            toc +=   "<li>" +  "<a href='javascript:void(0)'>" + $(h3.get(j)).text()  + "</a></li>" 

         }
      } 

     }


     toc +=  "</ul></li>"

    // console.log(toc)
    html_toc += toc;

  }

  //创建toc
  $(".toc-level1").html(html_toc)

  //跳转
  $("a").each(function(){
    //把标签转义
    $(this).click(function(event) {
      var id_text = "#" + $(this).text().trim()
              .replace('/', '\\/')
              .replace('&', '\\&')
              .replace('#', '\\#')
              .replace('+', '\\+')
              .replace('!', '\\!')
              .replace('=', '\\=')
              .replace('>', '\\>')
              .replace('|', '\\|')
              .replace('^', '\\^')
              .replace('*', '\\*')
              .replace('~', '\\~')
              .replace(':', '\\:')
              .replace('$', '\\$')
              .replace('.', '\\.')
              .replace(';', '\\;')
              .replace(',', '\\,')
       
      console.log(id_text)
      //if($(id_text).offset() != undefined)
      {
          $("html,body").animate({
              scrollTop: $(id_text).offset().top - $('#nav-area').height() - 5
            },
            100 //时间
        )
      }

    });
  });
})