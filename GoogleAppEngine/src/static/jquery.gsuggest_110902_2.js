/* 
  Modified from
  http://www.programmers.org/index.php/2009/12/jquery-google-suggest-jquerygsuggestjs/

  MIT License/GNU License
  http://www.opensource.org/licenses/mit-license.php
  http://www.gnu.org/licenses/gpl.html
  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so.
*/

(function($) {
$.gsuggest = function(settings){ 

$.gsuggest.config = {
	'debug': false,
	'url': '/suggest.cfc',
	'size': 10,
	'cacheenabled': false,
	'cacheaggressive': false,
	'cachefoward':false, //true - complete cache dataset, false - incomplete cache datasets
    'casesensitive': false,
	'sort': true,
	'css0': {'position':'absolute', 'z-index':'1', 'display':'none'},
	'css': {'background-color':'#ffffff', 'border':'solid 1px #000000', 'margin':'0px', 'cursor':'pointer', 'color':'#000000', 'padding':'0px'},
	'highlight': '#bcd5ff'
};

if (settings) $.extend($.gsuggest.config, settings);

var fillok = true;
var cacheinit = true;

var timerstart = null;
var timerend = null;

$.gsuggest.cachedata = [];
$.gsuggest.cachekey = "";

$.gsuggest.synctext = false;
$.gsuggest.mouseoverok = false;
$.gsuggest.mousepos = "";

$.gsuggest.setcase = 
    function(val){
        if ($.gsuggest.config.casesensitive)
            return val;
        else
            return val.toLowerCase();
    };

$.gsuggest.keydown =
    function(obj, e){ 
		clearTimeout($.gsuggest.suggestDelay);

        if (e.which == 38 || e.which == 40){
            $(obj).next().children("div:eq("+$(obj).attr("suggestPos")+")").blur();
        
            switch (e.which){
                case 38: //up
                    if (parseInt($(obj).attr("suggestPos"))-1 < -1)
                        $(obj).attr("suggestPos", $(obj).attr("suggestTtl"));
                    else
                        $(obj).attr("suggestPos", Math.max(-2, parseInt($(obj).attr("suggestPos"))-1));
                    break;
                    
                case 40: //down
                     if (parseInt($(obj).attr("suggestPos"))+1 > parseInt($(obj).attr("suggestTtl")))
                        $(obj).attr("suggestPos", "-1");
                     else   
                        $(obj).attr("suggestPos", Math.min($(obj).attr("suggestTtl"), parseInt($(obj).attr("suggestPos"))+1));
        
                     break;
            }
        
            $.gsuggest.synctext = true;        

            $(obj).next().children("div:eq("+$(obj).attr("suggestPos")+")").focus();
        } else if (e.which == 13){
           if ($(obj).attr("nosubmit") != null){
               //$(obj).next().hide();
               return false;           
           }
           //sk added
           $(obj).next().hide();
        }
    };
    
$.gsuggest.keyup = 
    function(obj){
	   var objval = obj.value;
	   //sk added
	   var fromIndex = 0;
	   if(objval.lastIndexOf('\\') > fromIndex) fromIndex = objval.lastIndexOf('\\'); 
	   if(objval.lastIndexOf('_') > fromIndex) fromIndex = objval.lastIndexOf('_'); 
	   objval = objval.substring(fromIndex);
	   
	   //console.dir($.gsuggest.cachedata);
	   if ($.gsuggest.config.debug)timerstart = new Date().getTime();
	  
       if (objval == $(obj).attr("suggestLast")) return;

	   if (objval.length == 0){
            $(obj).attr("suggestLast", objval);
            $(obj).next().hide();
            return;
        } 
		
       $(obj).attr("suggestLast", objval);
       
       var method = obj.form.name + '_' + obj.name;
       var surl = $.gsuggest.config.url + "?method="+method+"&value="+objval+"&callback=?"
       var data, datat;

	   //fill() *must* be single threaded via fillok	       
       function fill(data){
	   	   while(!fillok){};
		   fillok = false;
		   
		   $(obj).next().empty();
		   //$(obj).next().hide(); *we dont need to hide it unless the results are empty
	   
	   		if ($.gsuggest.config.sort) data.sort();
	   
			// mod by ctk
			$(obj).next().css("left", $(obj).offset().left+5);
            $(obj).next().css("top", $(obj).offset().top+$(obj).height()+13);
			//end mod

            $(obj).attr("suggestTtl", Math.min($.gsuggest.config.size, data.length));
            for (i = 0; i < data.length; i++){
                $(obj).next().append("<div style=\"padding: 3px;\">" + data[i].substr(0, objval.length) + "<strong>" + data[i].substring(objval.length) + "</strong></div>");
                if ( i == $.gsuggest.config.size ) break;
            }
            
            if (i > 0 && !(data.length == 1 && $.gsuggest.setcase(data[0]) == $.gsuggest.setcase(objval))){
                $(obj).attr("suggestPos", "-1");
                //$(obj).next().slideDown("fast");
				$.gsuggest.synctext = false;
                $.gsuggest.mouseoverok = false;
				$(obj).next().show();
            } else {
				$(obj).next().hide();
			}
			
			fillok = true;
       }
       		
	   //cache roll back -force cache forward if ttl suggest items less than max
		if (objval.indexOf($.gsuggest.cachekey) != 0 || (!$.gsuggest.config.cacheforward && !($(obj).attr("suggestTtl") < $.gsuggest.config.size))){ 
	   	   $.gsuggest.cachekey = $.gsuggest.setcase(objval);
	   }
	   //console.log("key: " + $.gsuggest.cachekey);
       if ($.gsuggest.cachedata[$(obj).attr("id")+$.gsuggest.cachekey] || ($(obj).attr("suggest_value") != null && $(obj).attr("suggest_value").length > 0)){
		   if (!$.gsuggest.cachedata[$(obj).attr("id")+$.gsuggest.cachekey] || !$.gsuggest.config.cacheenabled){
		   	   $.gsuggest.config.cacheforward = true;
		   	   datat = eval($(obj).attr("suggest_value"));
			   if ($.gsuggest.config.debug)$("#_debug").html("CACHE INIT<br>"+datat.join("<br>"));
		   }else{
		   	   datat = $.gsuggest.cachedata[$(obj).attr("id")+$.gsuggest.cachekey];	
			   if ($.gsuggest.config.debug)$("#_debug").html(datat.join("<br>"));	   
		   }
		   
	   	
           data = [];
           $.each(datat, function(i, val){
		   		if ($.gsuggest.setcase(val).indexOf($.gsuggest.setcase(objval)) == 0){
                	data.push(val);
                }
           })

		   if ($.gsuggest.config.cacheenabled){ $.gsuggest.cachedata[$(obj).attr("id")+$.gsuggest.setcase(objval)] = data; $.gsuggest.cachekey = $.gsuggest.setcase(objval)}
           fill(data); 
       }else{
           $.getJSON(surl, function(data){if ($.gsuggest.config.cacheenabled){ $.gsuggest.cachedata[$(obj).attr("id")+$.gsuggest.setcase(objval)] = data; $.gsuggest.cachekey = $.gsuggest.setcase(objval); if ($.gsuggest.config.debug)$("#_debug").html("CACHE INIT<br>"+$.gsuggest.cachedata[$(obj).attr("id")+$.gsuggest.setcase(objval)].join("<br>"));} fill(data)}); 	   
       }    

	   if ($.gsuggest.config.debug){
	   	  timerend = new Date().getTime();
	      $("#_debug_timer").html(timerend-timerstart);
	   }
	   
    };     

    $("input[suggest=yes]").each(function(i) {
        if (this.id == null || this.id == '') $(this).attr("id", "_999gsuggest_"+i);
        
        Init("#" + this.id);
    });
    
    function Init(id){
        var suggest_id = "_suggestBox";
        var suggest_idChildren = "#" + suggest_id + " > *";

        $(id).attr("autocomplete", "off");
		$(id).keyup(function(e){
			if (e.which == 27){
				$(this).blur();
				$(this).focus();
				if (!$.gsuggest.config.cacheaggressive){
					$.gsuggest.cachedata=[];
					$.gsuggest.cachekey="";
				}
			} else if (e.which == 13) {
				//sk added
				return false;
			} else if (e.which < 37 || e.which > 40) {
				//sk: the last number on this line is the standard delay
				$.gsuggest.suggestDelay = setTimeout("$.gsuggest.keyup(document.getElementById('"+$(this).attr("id")+"'))", (!!$.gsuggest.cachedata[$(this).attr("id")+$.gsuggest.cachekey]) ? 50 : (e.which == 13) ? 0 : 100);
			}
		});
		//sk $(id).click(function(){$(this).blur(); $(this).focus()});
        $(id).blur(function(){$.gsuggest.mouseout = false; $(this).next().hide(); $(this).attr("suggestPos", "-1");});
        $(id).attr("suggestPos", "-1");
        $(id).keydown(function(e){return $.gsuggest.keydown(this, e)});
        
        //set event handlers for suggest-box | no propgation
        $(suggest_idChildren).live("mouseover", function(e){
        	if (!$.gsuggest.mouseoverok) return false;
        	$(this).parent().children("div:eq("+$(this).parent().prev().attr("suggestPos")+")").blur();
        	$(this).parent().prev().attr("suggestPos", $(this).prevAll().length);
        	$(this).focus();
        	$.gsuggest.synctext=true;
        	return false
        }); 
        $(suggest_idChildren).live("mouseout", function(){$(this).blur(); return false;});
		$(suggest_idChildren).live("focus", function(){
			$(this).css("background-color", $.gsuggest.config.highlight);
			if($.gsuggest.synctext){
				//sk edited
				var fromIndex = 0;
				var objval = $(this).parent().prev().val();
				//alert(objval);
				if(objval.lastIndexOf('\\') > fromIndex) fromIndex = objval.lastIndexOf('\\'); 
				if(objval.lastIndexOf('_') > fromIndex) fromIndex = objval.lastIndexOf('_'); 
				objval = objval.substring(0,fromIndex);
				$(this).parent().prev().attr("value", objval+$(this).text())
			};
			return false;
		});
        $(suggest_idChildren).live("blur", function(){
        	$(this).css("background-color", $(this).parent().css("background-color"));
        	//sk removed
        	//$(this).parent().prev().attr("value", $(this).parent().prev().attr("suggestLast"));
        	return false;
        });
        $(suggest_idChildren).live("click", function(){
        	//sk: added for touch devices that do not have a mouseover before click
        	$(this).focus();
        	
        	$(this).parent().prev().attr("suggestLast", $(this).text());
        	$(this).blur();
        	$(this).parent().prev().focus();
        	return false;
        });
    
        //create suggest-box, set width, and position
        $(id).after("<div id=\""+suggest_id+"\" style=\"display:none\"></div>");
		$(id).next().css($.gsuggest.config.css0);
        $(id).next().css($.gsuggest.config.css);
        $(id).next().width($(id).width());
        $(id).next().css("left", $(id).offset().left+5);
        $(id).next().css("top", $(id).offset().top+$(id).height()+13);

		//mod by ctk
		 $(window).resize(function() {  
			$(id).next().css("left", $(id).offset().left+5);
        	$(id).next().css("top", $(id).offset().top+$(id).height()+13); 
		});
		//end mod

    };
};
})(jQuery);

jQuery(document).ready(function(){
   $(this).mousemove(function(e){
	  if ($.gsuggest.mousepos != e.pageX+'-'+e.pageY){
      	$.gsuggest.synctext = true;
        $.gsuggest.mouseoverok = true;
	  }
	  $.gsuggest.mousepos = e.pageX+'-'+e.pageY;
   });
});

//init
jQuery(document).ready(function(){jQuery.gsuggest({'debug':false})});
//requires cache sets to be tied to attributes


/*
I have not decided if I want to add text-range support for autocomplete; my intent
was to memic the behavior of googles suggest and I feel that I have done this. However
I may decided to implement this as an optional setting in the future... */
