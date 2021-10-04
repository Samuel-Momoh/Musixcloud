$(document).ready(function(){
"use strict";
// Song upload
$('#save').click(function(e){
  $('#add_song').modal('hide')
  e.preventDefault();
var datastring = new FormData($('#song_upload')[0]);
$.ajax({
  url:'/song-post',
  type:'POST',
  contentType: false,
  processData: false,
  data:datastring,
  xhr: function(){
var xhr = $.ajaxSettings.xhr();
    xhr.upload.onprogress = function (e) {
      // uploads
      if(e.lengthComputable){
        var value = (e.loaded / e.total)*100;
        $('#barval').css('width', value+'%');
      }
    };
    return xhr;
  },
  success: function(data){
swal("Song sucessfully upload", "success");
$('#artist').val('');
$('#title').val('');
 $('#lyrics').val('');
 $('#description').val('');
 $('#genre').val('');
$('#song').val('');
$('#image').val('');

  }
}).fail( function (e){
  swal("!Oops you upload was not complete", "warning");
}).done(function(e){
  $('#barval').css('width', '0%');
})
})
})