import {replacements} from './data';
import {replace} from './replace';

const latexInput = $('#latexInput');
const unicodeOutput = $('#unicodeOutput');
const permaLink = $('.permalink');


// copy replacements and sort case insensitive
var listOfReplacements = replacements
  .map(function(r) { return { value: r[0], unicode: r[1] }; })
  .sort(function(a, b) { return a.value.toLowerCase().localeCompare(b.value.toLowerCase()); });

// reorder such that when just typing '\' suggestions starting with '\a' appear
var indexOfFirstA = listOfReplacements
  .map(function(r) { return r.value.slice(0, 2).toLowerCase(); })
  .indexOf('\\a');
listOfReplacements = listOfReplacements.slice(indexOfFirstA).concat(listOfReplacements.slice(0, indexOfFirstA));


// Bloodhound: the source (dataset) for typeahead
var mySource = new Bloodhound({
  datumTokenizer: function(d) { return Bloodhound.tokenizers.whitespace(d.value); },
  queryTokenizer: function(d) { var i = d.lastIndexOf('\\'); var r = [d.substr(0, i), d.substr(i)]; console.log(r); return r; },
  local: listOfReplacements,
});
mySource.initialize();

// apply typeahead to input text field
latexInput.typeahead({
  hint: false,
  highlight: true,
  minLength: 0,
}, {
  display: 'value',
  source: mySource.ttAdapter(),
  limit: 15,
  templates: {
    suggestion: function(datum: {unicode:string, value:string}) {
      return '<div><span style="display:inline-block;width:3em;">'+datum.unicode+'</span><strong>'+datum.value+'</strong></div>';
    },
  },
});


latexInput.on('typeahead:selected', function (object, datum) {
  $('input#unicodeOutput').val(datum.unicode);
});
// $('.tt-query').css('background-color','#fff');
latexInput.focus();


// click handler for LaTeX examples
$('.latexExample').on('click', function(e) {
  latexInput
    .typeahead('val', $(this).html())
    .trigger('change')
    .focus();
});

// generate unicode output and permalink
latexInput.on('keyup change', function(e) {
  const input = <string>$(this).val();
  unicodeOutput.val(replace(input));
  permaLink.attr('href', 'https://www.unicodeit.net/?'+encodeURIComponent(input));
});


if (location.search) {
  var latex = decodeURIComponent(location.search.slice(1));
  latexInput
    .typeahead('val', latex)
    .trigger('change')
    .focus();
}
