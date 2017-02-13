//Costant declarations
const WELCOME = "welcomeview";
const PROFILE = "profileview";


displayView = function(){
  var viewId;
  if (localStorage.getItem("token") == "undefined" || localStorage.getItem("token") == null){
    viewId = WELCOME;
  }else{
    viewId = PROFILE;
  }
  document.getElementById("innerDiv").innerHTML = document.getElementById(viewId).innerHTML;
  if (viewId == PROFILE){
    bindFunctionsProfile();
    openTab("menu","home")
  }
  else if (viewId == WELCOME){
    bindFunctionsWelcome();
  }
};


window.onload = function(){
  displayView();
};


function logIn(){

  var email = document.forms["loginForm"]["email"].value;
  var password = document.forms["loginForm"]["password"].value;

  var server_msg = serverstub.signIn(email, password);

  if (!server_msg.success){
    showLogInError(server_msg.message);
    return false;
  }
  else{
    localStorage.setItem("token", server_msg.data);
    displayView();
    return true;
  }

}

function showLogInError(message){
  document.getElementById("messageLogIn").innerHTML = message;
  document.getElementById("logInError").style.display = "block";
}

function showSignUpError(message){
  document.getElementById("messageSignUp").innerHTML = message;
  document.getElementById("logInError").style.display = "block";
}


function checkPasswords(type){

  var password = document.getElementById("s_password");
  var rpassword = document.getElementById("s_rpassword");

  if(password.value != rpassword.value){
    rpassword.setCustomValidity("Passwords do not match!");
  }else{
    rpassword.setCustomValidity('');
  }
}


function signUp(){

  var firstname = document.forms["signupForm"]["name"].value;
  var familyname = document.forms["signupForm"]["f-name"].value;
  var gender_select = document.getElementById("gender");
  var gender = gender_select.options[gender_select.selectedIndex].text;
  var city = document.forms["signupForm"]["city"].value;
  var country = document.forms["signupForm"]["country"].value;
  var email = document.forms["signupForm"]["email"].value;
  var password = document.forms["signupForm"]["password"].value;

  var user = {
    "email": email,
    "password": password,
    "firstname": firstname,
    "familyname": familyname,
    "gender": gender,
    "city": city,
    "country": country
  };

  var server_msg = serverstub.signUp(user);

  if (!server_msg.success){
    showSignUpError(server_msg.message);
    return false;
  }
}


function signOut(){

  serverstub.signOut(localStorage.getItem("token"));
  localStorage.setItem("token", "undefined");
  displayView();
}

function openTab(tabType, tabName){

  var i;
  var tabId;
  var menu = document.getElementsByClassName(tabType);
  var tabLinks = document.getElementsByClassName("tabLink");

  if(tabType == "menu"){
    if(tabName == "home"){
      tabId = "navHome";
    }
    if(tabName == "browse"){
      tabId = "navBrowse";
    }
    if(tabName == "account"){
      tabId = "navAccount";
    }

    for (i = 0; i < menu.length; i++) {
        tabLinks[i].className = tabLinks[i].className.replace(" active", "");
    }

    document.getElementById(tabId).className += " active";
    }


  for(i = 0; i < menu.length; i++){
    menu[i].style.display = "none";
  }

  document.getElementById(tabName).style.display = "block";


  if(tabName == "home"){
    renderHome();
  }

}


function changePassword(){

  var npassword = document.forms["changePassForm"]["new_password"].value;
  var cpassword = document.forms["changePassForm"]["current_password"].value;
  var server_msg = serverstub.changePassword(localStorage.getItem("token"), cpassword, npassword);

  if(!server_msg.success){
    showChangePasswordError(server_msg.message);
  }else{
    showChangePasswordSuccess(server_msg.message);
  }


  return false;
}

function showChangePasswordError(message){
  document.getElementById("messageChPassword").innerHTML = message;
  document.getElementById("chPasswordError").style.display = "block";

  document.getElementById("chPasswordSuccess").style.display = "none";
}

function showChangePasswordSuccess(message){
  document.getElementById("messageChPasswordS").innerHTML = message;
  document.getElementById("chPasswordSuccess").style.display = "block";

  document.getElementById("chPasswordError").style.display = "none";
}


function renderHome(){

  var token = localStorage.getItem("token");
  var server_msg = serverstub.getUserDataByToken(token);
  var userData;

  if (server_msg.success){
    userData = server_msg.data;
  }else{
    return -1; //error
  }

  document.getElementById("nameField").innerHTML = userData.firstname;
  document.getElementById("fNameField").innerHTML = userData.familyname;
  document.getElementById("genderField").innerHTML = userData.gender;
  document.getElementById("countryField").innerHTML = userData.country;
  document.getElementById("cityField").innerHTML = userData.city;
  document.getElementById("emailField").innerHTML = userData.email;

  reloadUserMsgs();
}


function sendMsg(){

  var token = localStorage.getItem("token");
  var server_msg = serverstub.getUserDataByToken(token);
  var data;

  if (server_msg.success){
    data = server_msg.data;
  }else{
    return -1; //error
  }

  var msg = document.forms["msgForm"]["message"].value;

  document.forms["msgForm"]["message"].value = "";

  serverstub.postMessage(token, msg, data.email);

  reloadUserMsgs();

  document.getElementById("msgToMe").value = "";

  return false;
}


function sendMsgTo(){

  var token = localStorage.getItem("token");
  var email = document.forms["userSearchForm"]["email"].value;
  var msg = document.forms["msgToForm"]["message"].value;

  serverstub.postMessage(token, msg, email);

  reloadMsgs();

  document.getElementById("msgTo").value = "";

  return false;
}


function reloadUserMsgs(){

  var token = localStorage.getItem("token");
  var server_msg = serverstub.getUserMessagesByToken(token);
  var messages;

  if (server_msg.success){
    messages = server_msg.data;
  }else{
    return -1; //error
  }

  var msgDiv = document.getElementById("userMessageDiv");

  while (msgDiv.firstChild) {
    msgDiv.removeChild(msgDiv.firstChild);
  }

  for (var i = 0; i < messages.length; i++){
    var p = document.createElement('p');
    p.innerHTML = "<b>"+messages[i].content+"</b> by "+messages[i].writer;
    msgDiv.appendChild(p);
  }

}


function reloadMsgs(){

  var token = localStorage.getItem("token");
  var email = document.forms["userSearchForm"]["email"].value;
  var server_msg = serverstub.getUserMessagesByEmail(token, email);
  var messages;

  if (server_msg.success){
    messages = server_msg.data;
  }else{
    return -1; //error
  }

  var msgDiv = document.getElementById("messageDiv");

  while (msgDiv.firstChild) {
    msgDiv.removeChild(msgDiv.firstChild);
  }

  for (var i = 0; i < messages.length; i++){
    var p = document.createElement('p');
    p.innerHTML = "<b>"+messages[i].content+"</b> by "+messages[i].writer;
    msgDiv.appendChild(p);
  }

}


function searchUser(){

  var token = localStorage.getItem("token");
  var email = document.forms["userSearchForm"]["email"].value;
  var server_msg = serverstub.getUserDataByEmail(token, email);
  var userData;


  if (!server_msg.success){
    showSearchError(server_msg.message);
  }else{
      userData = server_msg.data;
      renderUserTab(userData);
      openTab("browsetab","user");
  }
  return false;
}

function showSearchError(message){
  document.getElementById("messageSearch").innerHTML = message;
  document.getElementById("searchError").style.display = "block";
}




function renderUserTab(userData){

  document.getElementById("othNameField").innerHTML = userData.firstname;
  document.getElementById("othFNameField").innerHTML = userData.familyname;
  document.getElementById("othCountryField").innerHTML = userData.gender;
  document.getElementById("othCityField").innerHTML = userData.country;
  document.getElementById("othGenderField").innerHTML = userData.city;
  document.getElementById("othEmailField").innerHTML = userData.email;

  reloadMsgs();
}


function back(){
  openTab("browsetab","search");
}


function bindFunctionsWelcome(){

  document.getElementById("loginForm").onsubmit = logIn;
  document.getElementById("signupForm").onsubmit = signUp;

  document.getElementById("s_rpassword").onkeyup = checkPasswords;
}


function bindFunctionsProfile(){

  document.getElementById("navHome").onclick = function() { openTab("menu","home");};
  document.getElementById("navBrowse").onclick = function() { openTab("menu","browse");};
  document.getElementById("navAccount").onclick = function() { openTab("menu","account");};

  document.getElementById("userMsgReloadButton").onclick = reloadUserMsgs;
  document.getElementById("logout").onclick = signOut;
  document.getElementById("back").onclick = back;
  document.getElementById("msgReloadButton").onclick = reloadMsgs;

  document.getElementById("msgForm").onsubmit = sendMsg;
  document.getElementById("msgToForm").onsubmit = sendMsgTo;
  document.getElementById("userSearchForm").onsubmit = searchUser;
  document.getElementById("changePassForm").onsubmit = changePassword;

  document.getElementById("s_rpassword").onkeyup = checkPasswords;
}
