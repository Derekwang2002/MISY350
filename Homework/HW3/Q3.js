function errorHandle(id, name, num) {
    var divLabel = document.getElementById(id);
    document.getElementsByTagName('strong')[num].setAttribute('class', 'error');

    //add a new div element as a child node of the div element with corresponding id
    var subDivLabel = document.createElement('div');
    subDivLabel.className = 'errorln';
    subDivLabel.innerHTML = 'Please enter your ' + name + '!';
    divLabel.appendChild(subDivLabel);
    }

function checkInputs(event) {
    //first remove error messages
    var errorDiv = document.querySelectorAll('div div');
    var errorHeader = document.querySelectorAll('.error');
    //remove the classes from each label
    if (errorHeader){
        errorHeader.forEach(function(element) {
            element.classList.remove('error');
        });
    }
    //remove error message line
    if (errorDiv){
        errorDiv.forEach(function(element) {
            element.parentNode.removeChild(element);
        });
    }
    //remove bottom error output 
    document.getElementById('output').innerHTML = '';

    //console.log("in the function");
    var frmObject = document.forms[0];
    var output = "Please correct the errors on the page.";
    var checkError = false;

    //check the full name text box.
    //If there is an error, set checkError to true and add a new text node for the error message
    if (frmObject.fullName.value.trim() == '') {
        errorHandle('theName', 'fullname', 0);
        //update the checkError value to true
        checkError = true;  
    }

    //check the address text area
    //If there is an error, set checkError to true and add a new text node for the error message
    if (frmObject.address.value.trim() == '') {
        errorHandle('theAddress', 'address', 1);
        //update the checkError value to true
        checkError = true;
    }

    //check the gender radio button
    //If there is an error, set checkError to true and add a new text node for the error message
    if (frmObject.gender.value == '') {
        errorHandle('thegender', 'gender', 2);
        //update the checkError value to true
        checkError = true;
    }
    //check the major dropdown selection
    //If there is an error, set checkError to true and add a new text node for the error message
    if (frmObject.major.value == '') {
        errorHandle('themajor', 'major', 3);
        //update the checkError value to true
        checkError = true;
    }

    //check the date of birth input value
    //If there is an error, set checkError to true and add a new text node for the error message
    if (frmObject.year.value < 1900 || frmObject.year.value > 2022) {
        errorHandle('theyear', 'year', 4);
        //update the checkError value to true
        checkError = true;
    }


    //stop the event from continuing if errors exist
    if (checkError) {
        event.preventDefault();
        document.getElementById("output").innerHTML = output;
    }
}

function init() {
    //specify the function checkInputs as the event listner for the submit event of the form element
    //first get the reference to the form element
    var form1 = document.getElementsByTagName("form")[0];
    //then define an event handler for the submit event of the form object
    form1.addEventListener("submit", checkInputs);
}

//Define the DOMContentLoaded event handler, which will be triggered after the document finishes loading
document.addEventListener("DOMContentLoaded", init);
