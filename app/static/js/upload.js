$(function(){
	
	var dropbox = $('#content'),
		message = $('.message', dropbox);
	
	var	cursor;
	
	dropbox.filedrop({
		paramname: 'file',
		maxfiles: 1,
		url: '/upload',
		uploadFinished:function(i,file,response){

			txt = "![](" + response.filename + ")";
			dropbox.val(dropbox.val().substring(0,cursor) + txt + dropbox.val().substring (cursor));
			$.data(file).addClass('done');
			$.data(file).fadeOut(1000, function() { this.remove(); });
		},
		drop: function() {
			cursor = getCursor(document.getElementById('content'))
		},
    	error: function(err, file) {
			switch(err) {
				case 'BrowserNotSupported':
					showMessage('Your browser does not support HTML5 file uploads!');
					break;
				case 'TooManyFiles':
					alert('Too many files! Please select ' + this.maxfiles + ' at most!');
					break;
				case 'FileTooLarge':
					alert(file.name + ' is too large! The size is limited to ' + this.maxfilesize + 'MB.');
					break;
				default:
					break;
			}
		},
		
		beforeEach: function(file){
			if(!file.type.match(/^image\//)){
				alert('Only images are allowed!');
				return false;
			}
		},
		uploadStarted:function(i, file, len){
			createImage(file);
		},
		
		progressUpdated: function(i, file, progress) {
			$.data(file).find('.progress').width(progress);
		}
    	 
	});
    
    var template = '<div class="imagePreview">'+
						'<span class="imageHolder">'+
							'<img />'+
							'<span class="uploaded"></span>'+
						'</span>'+
						'<div class="progressHolder">'+
							'<div class="progress"></div>'+
						'</div>'+
					'</div>'; 
	
	
	function createImage(file){

		var preview = $(template), 
			image = $('img', preview);
			
		var reader = new FileReader();
		
		reader.onload = function(e){
			image.attr('src',e.target.result);
		};
		
		reader.readAsDataURL(file);
		
		message.hide();
		preview.appendTo($('#the_previewer'));
		
		$.data(file,preview);
	}

	function showMessage(msg){
		message.html(msg);
	}


});
