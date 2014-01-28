// Copyright (c) 2010 Sven Kreiss, Kyle Cranmer
// Sven Kreiss <sk@svenkreiss.com>, Kyle Cranmer <kyle.cranmer@nyu.edu>
// version 0.6

var replacements = [];
var combiningmarks = [];
var subsuperscripts = [];


var replace = function(inp) {
    return inp.map( function(f) {
        // escape combining marks with a space after the backslash
        for( ic in combiningmarks ) {
            var c = combiningmarks[ic];

            var i = -1;
            while( (i = f.indexOf(c[0],i+1)) > -1 ) {
                f = f.slice(0,i+1)+' '+f.slice(i+1);
            }
        }

        // console.log(replacements);            
        for( ir in replacements ) {
            var r = replacements[ir];
            // dirty way of a replaceAll():
            f = f.split(r[0]).join(r[1]);
        }


        // expand groups of subscripts: _{01234}    
        while( (i = f.indexOf("_{")) > -1   &&   f.indexOf("}") > i ) {
            f = f.slice(0,i)+'_'+f[i+2]+'_{'+f.slice(i+3);
            f = f.replace('_{}','');
        }
            
        // expand groups of superscripts: ^{01234}    
        while( (i = f.indexOf("^{")) > -1   &&   f.indexOf("}") > i ) {
            f = f.slice(0,i)+'^'+f[i+2]+'^{'+f.slice(i+3);
            f = f.replace('^{}','');
        }
        
        // now replace subsuperscripts
        for( ir in subsuperscripts ) {
            var r = subsuperscripts[ir];
            // dirty way of a replaceAll():
            f = f.split(r[0]).join(r[1]);
        }


        // combining marks (unicode char modifies previous char)
        for( ic in combiningmarks ) {
            var c = combiningmarks[ic];

            var i = -1;
            while( (i = f.indexOf('\\ '+c[0].slice(1)+'{',i+1)) > -1 ) {
                var newString = f[i+c[0].length+2] + c[1];
                f = f.slice(0,i)+newString+f.slice(i+1+c[0].length+3);
            }
        }

        return f;
    });
};

