$(function(){

	function readURL(input) {
	if (input) {
		$('#preview').attr('src',input);
	}
	}

$("#previewBtn").click(function(e) {
	e.preventDefault();
readURL($("#img").val());
});

	$("#send").click(function(event){
		event.preventDefault();
		var title = $("#title").val();
		var message = $("#body").val();
		var img = $("#img").val();
		var url = $("#url").val();
		if(title=='' || message=='' || img =='' || url ==''){
			swal("Oh noes!", "Some of the input fields are empty, would you mind filling them properly!", "error");
			return false
		}else{
			$.ajax({
				url : "/admin-api/send-push-notifications", 
				type: "POST", 
				data : {
					"title": title,
					"body": message,
					"img": img,
					"url": url
				}, 
				async : false, 
				success: function(response, textStatus, jqXHR) {
				 console.log(response);
				 document.getElementById("trigger-push-form").reset();
				 $('#preview').attr('src','');
				 swal("Success!", "Push notification sent to all subscribers!", "success");
				},
				error: function (jqXHR, textStatus, errorThrown) {
				console.log(jqXHR);
				console.log(textStatus);
				console.log(errorThrown);
				swal("Oh noes!", "They is an error in your request, please contact the server administrator!", "error");
  }
  });
		}

	});
});