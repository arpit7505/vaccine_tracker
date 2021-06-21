function collapse(id) {
    var col1 = document.getElementById("collapse1");
    var col2 = document.getElementById("collapse2");
    col1.classList.add('collapse');
    col2.classList.add('collapse');
    document.getElementById(id).classList.remove('collapse');
}

function populateSecond() {
   var select1 = document.getElementById("stateselect");
   var select2 = document.getElementById("districtselect");
   while (select2.length > 0) {
        select2.remove(0);
   }
   var selected = select1.options[select1.selectedIndex].value;

   var selectedValue = selected.split('_')[1].replace('[','').replace(']','').replaceAll("'",'').split(',')
   select2.options.add(new Option('Select District'));
   for (index = 0; index < selectedValue.length; index++) {
        select2.options.add(new Option(selectedValue[index].trim(),selectedValue[index].trim()));
}
document.getElementById("hiddenstate").value = selected.split('_')[0];
}

function filter() {
    var age = document.querySelector('input[name="age"]:checked');
    var vaccine = document.querySelector('input[name="vaccine"]:checked');
    var fees = document.querySelector('input[name="fees"]:checked');
    var table = document.getElementById('myTable');
    var dict = {};

    if (age != null){
        dict[age.value.toUpperCase()] = 5;
    }
    if (vaccine != null){
        dict[vaccine.value.toUpperCase()] = 6;
    }
    if (fees != null){
        dict[fees.value.toUpperCase()] = 7;
    }
    var evalstr = '';
    for (var key in dict) {
        if (evalstr == ''){
            evalstr = "(table.rows[i].cells['"+dict[key]+"'].innerHTML.toUpperCase().indexOf('"+key+"') > -1)"
        }else{
            evalstr += " && (table.rows[i].cells['"+dict[key]+"'].innerHTML.toUpperCase().indexOf('"+key+"') > -1)"
        }
    }

    for (var i = 1; i < table.rows.length; i++) {
        if (Object.keys(dict).length != 0){
            if (eval(evalstr)) {
                table.rows[i].style.display = "";
            } else {
                table.rows[i].style.display = "none";
            }
         }else{
         table.rows[i].style.display = "";
         }
    }
}