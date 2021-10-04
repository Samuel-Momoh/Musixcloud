  // Visualization
  var context = new AudioContext();
  var analyser = context.createAnalyser();
  var canvas = document.getElementById("mainCanvas");
// Intialize Lyricer js
var lrc = new Lyricer({"showLines": 8, "clickable": true});
/*
	When the Song Name link is pressed, stop all propagation so AmplitudeJS doesn't
	play the song.
*/
let Links = document.getElementsByClassName('song-meta-data');

for( var i = 0; i < Links.length; i++ ){
	Links[i].addEventListener('click', function(e){
		e.stopPropagation();
	});
}


let songElements = document.getElementsByClassName('song');

for( var i = 0; i < songElements.length; i++ ){

	songElements[i].addEventListener('click', function(){	
		setTimeout(function(){
			// fetch lyrics
		$('#lyricer').empty('')
		var newLyric = Amplitude.getActiveSongMetadata().lyrics
			if(newLyric!=null){
				lrc.setLrc(newLyric);
			}
	// User likes
	if($('#username').val() !=''){
		$('#song_likes').find($(".fa")).removeClass('fa-heart').addClass('fa-heart-o');
		$('#song_likes').removeClass('like').addClass('unlike');
		var songid = Amplitude.getActiveSongMetadata().id;
			var username = $('#username').val();
		// Get all user like in database
			$.ajax({
				url:'/user_like_check',
				type:'post',
				data:{
					'username':username,
					'songid':songid
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

		},100)
		
	});
}

/*
	Initializes AmplitudeJS
*/
var songid=  $('#song').val();
var json=[]
var dataString = 'value='+songid
$.ajax({
  url:'/sartist',
  type:'POST',
  data: dataString,
  dataType:'JSON',
  cache:false,
  success: function (data){
if(data[0][9]!=null){
	//    fecth lyrics
	   var newText2 = data[0][9]
	   lrc.setLrc(newText2);
	   window.addEventListener("lyricerclick", function(e){
		Amplitude.getAudio().currentTime = e.detail.time;
	   });
}

	for(var i in data) {
		var arr={
			"id": data[i][0],
			"name": data[i][2],
			"artist": data[i][1],
			"album": data[i][5],
			"url": '/static/songs/'+data[i][3],
			"cover_art_url": "/static/album-art/"+data[i][8],
			"lyrics": data[i][9],
			"downloads":data[i][7],
			"count":data[i][10],
			"like":data[i][11],
			"visualization": "michaelbromley_visualization"
		}
		json.push(arr)
	}

Amplitude.init({
	visualization: 'michaelbromley_visualization',
	callbacks:{
		initialized: function(){
			if($('#username').val() !=''){
				// alert(data[0][0])
					var username = $('#username').val();
				// Get all user like in database
					$.ajax({
						url:'/user_like_check',
						type:'post',
						data:{
							'username':username,
							'songid':data[0][0]
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
		next: function(){
			$('#lyricer').empty('')
			var newLyric = Amplitude.getActiveSongMetadata().lyrics
			if(newLyric!=null){
				lrc.setLrc(newLyric);
			}
	// Get user likes
	if($('#username').val() !=''){
		$('#song_likes').find($(".fa")).removeClass('fa-heart').addClass('fa-heart-o');
		$('#song_likes').removeClass('like').addClass('unlike');
			var username = $('#username').val();
			var songid = Amplitude.getActiveSongMetadata().id;
		// Get all user like in database
			$.ajax({
				url:'/user_like_check',
				type:'post',
				data:{
					'username':username,
					'songid':songid
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
		prev: function(){ 
                                 
			$('#lyricer').empty('')
			var newLyric = Amplitude.getActiveSongMetadata().lyrics
			if(newLyric!=null){
				lrc.setLrc(newLyric);
			}
			// User likes
			if($('#username').val() !=''){
				$('#song_likes').find($(".fa")).removeClass('fa-heart').addClass('fa-heart-o');
				$('#song_likes').removeClass('like').addClass('unlike');
				var songid = Amplitude.getActiveSongMetadata().id;
					var username = $('#username').val();
				// Get all user like in database
					$.ajax({
						url:'/user_like_check',
						type:'post',
						data:{
							'username':username,
							'songid':songid
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
		}

	},
	"songs": json,
	waveforms: {
		sample_rate: 50
	  }
  });
  Amplitude.pause();
  }
});
