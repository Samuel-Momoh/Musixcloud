$(document).ready(function(){
    const username = $('#username').val();
    if($('#username').val() !=''){
        
    // Get all user like in database
        $.ajax({
            url:'/user_like',
            type:'post',
            data:{
                'username':username
            },
            dataType:'JSON',
            success: function(response){
     
      $.each(response,function(index,value){
        $('#songid'+value[0]).find($(".fa")).removeClass('fa-heart-o').addClass('fa-heart');
        $('#songid'+value[0]).removeClass('unlike').addClass('like');
    
    });
            }
        });
    }
        // Adding Like
    $('.heart').click(function(){
        if(username !=''){
        var id = $(this).attr('id');
        var newid = id.replace('songid','');
        if($(this).hasClass('unlike')){
            $(this).find($(".fa")).removeClass('fa-heart-o').addClass('fa-heart');
            $(this).removeClass('unlike').addClass('like');
           var count = parseInt($('#likeCount'+newid).text());
            document.getElementById('likeCount'+newid).innerText=(1 + count)
            $.ajax({
                url:'/like',
                type:'post',
                data:{
                    'username':username,
                    'songid':newid
                },
                dataType:'JSON',
                success: function(response){
                    console.log(response);
                }
            });
        }else{
            $(this).find($(".fa")).removeClass('fa-heart').addClass('fa-heart-o');
            $(this).removeClass('like').addClass('unlike');
            var count = parseInt($('#likeCount'+newid).text());
            document.getElementById('likeCount'+newid).innerText=(count - 1)
            $.ajax({
                url:'/unlike',
                type:'post',
                data:{
                    'username':username,
                    'songid':newid
                },
                dataType:'JSON',
                success: function(response){
    console.log(response);
                }
            });
        }
    }else{
        window.location.href='https://app.musixcloud.com/login';
      }
    })
    
    // Adding Likes in player
        $('.heart_player').click(function(){
            if(username !=''){
            var songid = $('#songid').text();
            if($(this).hasClass('unlike')){
                $(this).find($(".fa")).removeClass('fa-heart-o').addClass('fa-heart');
                $(this).removeClass('unlike').addClass('like');
               var count = parseInt($('#likeCount').text());
                document.getElementById('likeCount').innerText=(1 + count)
                $.ajax({
                    url:'/like',
                    type:'post',
                    data:{
                        'username':username,
                        'songid':songid
                    },
                    dataType:'JSON',
                    success: function(response){
                        console.log(response);
                    }
                });
            }else{
                $(this).find($(".fa")).removeClass('fa-heart').addClass('fa-heart-o');
                $(this).removeClass('like').addClass('unlike');
                var count = parseInt($('#likeCount').text());
                document.getElementById('likeCount').innerText=(count - 1)
                $.ajax({
                    url:'/unlike',
                    type:'post',
                    data:{
                        'username':username,
                        'songid':songid
                    },
                    dataType:'JSON',
                    success: function(response){
        console.log(response);
                    }
                });
            }
        }else{
            window.location.href='https://app.musixcloud.com/login';
          }
        });

   
    });