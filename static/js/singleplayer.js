
// Fetch data from database
var songid=  $('#song').val();
var dataString = 'value='+songid
   // Visualization
   var context = new AudioContext();
   var analyser = context.createAnalyser();
   var canvas = document.getElementById("mainCanvas");
   var lrc = new Lyricer({"showLines": 10, "clickable": true});
 
 
$.ajax({
  url:'/sation',
  type:'POST',
  data: dataString,
  dataType:'JSON',
  cache:false,
  success: function (result){
    $.each(result, function(i, field){
if(field[9]!=null){
  lrc.setLrc(field[9]);
  window.addEventListener("lyricerclick", function(e){
    Amplitude.getAudio().currentTime = e.detail.time;
  });
}  
      Amplitude.init({
  visualization: 'michaelbromley_visualization',
        "songs": [
          {
            "id": field[0],
            "name": field[2],
            "artist": field[1],
            "album": field[5],
            "url": '/static/songs/'+field[3],
            "cover_art_url": "/static/album-art/"+field[8],
            "lyrics":field[9],
            "downloads":field[7],
            "count":field[10],
            "like":field[11],
            "visualization": "michaelbromley_visualization"
          }
        ],
        callbacks:{
          initialized: function(){
            if($('#username').val() !=''){
              var username = $('#username').val();
          // Get user like in database
              $.ajax({
                  url:'/user_like_check',
                  type:'post',
                  data:{
                      'username':username,
                      'songid':field[0]
                  },
                  dataType:'JSON',
                  success: function(response){
           if(response>=1){
              $('#song_likes').find($(".fa")).removeClass('fa-heart-o').addClass('fa-heart');
              $('#song_likes').removeClass('unlike').addClass('like');
           }
                  }
              });
            }
          },
          play: function(){
            var audioTag = Amplitude.getAudio()
           var src = context.createMediaElementSource(audioTag);
           canvas.width = window.innerWidth;
           canvas.height = window.innerHeight;
           var ctx = canvas.getContext("2d");
         
           src.connect(analyser);
           analyser.connect(context.destination);
         
           analyser.fftSize = 256;
         
           var bufferLength = analyser.frequencyBinCount;
           console.log(bufferLength);
         
           var dataArray = new Uint8Array(bufferLength);
         
           var WIDTH = canvas.width;
           var HEIGHT = canvas.height;
         
           var barWidth = (WIDTH / bufferLength) * 2.5;
           var barHeight;
           var x = 0;
           
   function renderFrame() {
    requestAnimationFrame(renderFrame);
  
    x = 0;
  
    analyser.getByteFrequencyData(dataArray);
  
    ctx.fillStyle = "#0a0c11";
    ctx.fillRect(0, 0, WIDTH, HEIGHT);
  
    for (var i = 0; i < bufferLength; i++) {
      barHeight = dataArray[i];
      
      var r = barHeight + (25 * (i/bufferLength));
      var g = 250 * (i/bufferLength);
      var b = 50;
  
      ctx.fillStyle = "rgb(" + r + "," + g + "," + b + ")";
      ctx.fillRect(x, HEIGHT - barHeight, barWidth, barHeight);
  
      x += barWidth + 1;
    }
    }
            renderFrame();
            // lyrics
            var newLyric = Amplitude.getActiveSongMetadata().lyrics
            if(newLyric!=null){
              Amplitude.getAudio().addEventListener( "timeupdate", function() {
                lrc.move(Amplitude.getAudio().currentTime);
              });
            }
            // Navigator mediaSession
            if ('mediaSession' in navigator) {
              navigator.mediaSession.metadata = new MediaMetadata({
                title: Amplitude.getActiveSongMetadata().name,
                artist: Amplitude.getActiveSongMetadata().artist,
                album: Amplitude.getActiveSongMetadata().album,
                artwork: [
                  { src: 'https://app.musixcloud.com'+Amplitude.getActiveSongMetadata().cover_art_url,   sizes: '96x96',   type: 'image/png' },
                  { src: 'https://app.musixcloud.com'+Amplitude.getActiveSongMetadata().cover_art_url, sizes: '128x128', type: 'image/png' },
                  { src: 'https://app.musixcloud.com'+Amplitude.getActiveSongMetadata().cover_art_url, sizes: '192x192', type: 'image/png' },
                  { src: 'https://app.musixcloud.com'+Amplitude.getActiveSongMetadata().cover_art_url, sizes: '256x256', type: 'image/png' },
                  { src: 'https://app.musixcloud.com'+Amplitude.getActiveSongMetadata().cover_art_url, sizes: '384x384', type: 'image/png' },
                  { src: 'https://app.musixcloud.com'+Amplitude.getActiveSongMetadata().cover_art_url, sizes: '512x512', type: 'image/png' },
                ]
              });
            
              navigator.mediaSession.setActionHandler('play', function() {
                Amplitude.play()
              });
              navigator.mediaSession.setActionHandler('pause', function() {
                Amplitude.pause()
              });
              navigator.mediaSession.setActionHandler('seekbackward', function() {
                Amplitude.getAudio().currentTime = Amplitude.getAudio().currentTime - 10
              });
              navigator.mediaSession.setActionHandler('seekforward', function() {
                Amplitude.getAudio().currentTime = Amplitude.getAudio().currentTime +10
              });
              navigator.mediaSession.setActionHandler('previoustrack', function() {
                Amplitude.next( playlistKey = null )
              });
              navigator.mediaSession.setActionHandler('nexttrack', function() { 
                Amplitude.prev( playlistKey = null )
              });
            } 
          },
          
        }
      });
      Amplitude.pause();
      });
 
  }
})


  window.onkeydown = function(e) {
      return !(e.keyCode == 32);
  };

  /*
    Handles a click on the song played progress bar.
  */
  document.getElementById('song-played-progress').addEventListener('click', function( e ){
    var offset = this.getBoundingClientRect();
    var x = e.pageX - offset.left;

    Amplitude.setSongPlayedPercentage( ( parseFloat( x ) / parseFloat( this.offsetWidth) ) * 100 );
  });


   