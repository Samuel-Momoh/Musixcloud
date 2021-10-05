var run;
var i = 0;
$(document).ready(function()
{
var dataState = $('#hidden_val').val();

console.log(dataState);
if(dataState == 'None'){
    return null
}
else
{
var player = $('#content').stickyAudioPlayer(
{
url:       $('.playBtn').data('link'),
position:  'bottom',
text:      $('.playBtn').data('title'),
volume:    40,
image:     $('.playBtn').data('img'),
repeat:    false
}
);
}

// Change songs
$('.playBtn').click(function(e) {
    e.preventDefault(); 
    $('.playBtn').removeClass('pausebtnsvg').addClass('playbtnsvg');
    $(this).removeClass('playbtnsvg').addClass('pausebtnsvg');
    var src = $(this).attr('href');
    var title = $(this).data("title");
    var img = $(this).data("img");
    var id = $(this).attr('id');
    var sondtitle = $(this).data("name");
    var sondartist = $(this).data("artist");
    var sondgenre = $(this).data("genre");
     i = id ;
    player.changeAudio(src,title,img,sondtitle,sondartist,sondgenre);
});
var arr = []
var play_btn=document.querySelectorAll('.playBtn');
for(var i=0;i<play_btn.length;i++){
    var jsonData ={
        'id':i,
        'link':play_btn[i].getAttribute('href'),
       'title':play_btn[i].getAttribute('data-title'),
        'img':play_btn[i].getAttribute('data-img'),
        'name':play_btn[i].getAttribute('data-name'),
        'artist':play_btn[i].getAttribute('data-artist'),
        'genre':play_btn[i].getAttribute('data-genre')
    }
    arr.push(jsonData)
    

}

function next() {
    // Check for last audio file in the playlist
    if (i === arr.length - 1) {
        i = 0;
    } else {
        i++;
    }
    // Change the audio element source
    player.switchAudio(arr[i].id,arr[i].link,arr[i].title,arr[i].img,arr[i].name,arr[i].artist,arr[i].genre);
}
player.audioEnd(next);

$(window).on('resize',function(){
    // alert('window:'+$(this).height(),'float:'+$('.stickyAudioPlayerBoxFloatingButton').height())
    // alert()
})
});

