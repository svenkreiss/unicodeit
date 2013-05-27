var result = "";

function submitForm() {
	//$("#maininput input[name=submit]").hide();
	//$("#loading").show();
	$("#mainresult>input[name=result]").val("...");
	latex = $("#maininput input[name=latex]").val(); 
	$.get("/api/unicodeit/"+encodeURI(latex), function(data) {
		result = data;
		$("#mainresult>input[name=result]").val(data);
		//$("#mainresult").text(data);
		link = 'http://www.unicodeit.net/?expr='+encodeURI(latex);
		$("#permalink").replaceWith('<a id="permalink" href="'+link+'">permalink</a>');
		//$("#loading").hide();
		//$("#maininput input[name=submit]").show();
	});
}

$(document).ready(function () {
	
	$("#maininput").submit(function() {
		submitForm();
		return false;
	});
	$("#mainresult").submit(function() {
		return false;
	});
	
	$("#mainresult>input[name=result]").keyup(function() {
		if( $(this).val() != result ) $(this).val(result);
		return false;
	});
	
});
	
