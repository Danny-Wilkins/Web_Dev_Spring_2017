function search()
{
	var address = $("#add").val()
	var link = "/search/" + address;
	window.open(link, "_self");
}

$("#add").bind("keypress", {}, keypressInBox);

function keypressInBox(e) {
    var code = (e.keyCode ? e.keyCode : e.which);
    if (code == 13) { //Enter keycode                        
        e.preventDefault();

        var address = $("#add").val();
    	var link = "/search/" + address;
		window.open(link, "_self");
    }
};

//Idea: Have Python direct to /results, where a JS function is called to parse a JSON passed
//in and dynamically load results
//Or program a whole new HTML page okay I got this