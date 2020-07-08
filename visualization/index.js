var lastUpdate = 0;

function initializeDashboard() {
  lastUpdate = 0;
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (this.status != 200) {
      console.log("Error in obtaining list of environments with a status of " + this.status);
      return;
    }

    var accessibleEnvironments = JSON.parse(xhr.responseText);
    var sel = document.getElementById('dashboard-select');
    
    //first clearing the child nodes
    while (sel.hasChildNodes())
      sel.removeChild(sel.firstChild);

    Object.keys(accessibleEnvironments).forEach(function(key) {
      //TODO: use name specified in dashboard configuration rather than the one in accessibleEnvironments
      var txt = accessibleEnvironments[key];
      var opt = document.createElement('option');
      opt.appendChild( document.createTextNode(txt));
      opt.value = key; 

      sel.appendChild(opt);
    });

    updateDashboard();
  }
  xhr.open("POST", "dashboards", true);
  firebase.auth().currentUser.getIdToken(true).then(function(idToken) {
    xhr.send(JSON.stringify({"idtoken":idToken}));
  }).catch(function(error) { console.error(error); });
}

function updateDashboardArgs(dashboardID) {
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (this.status != 200) {
      console.log("Error in obtaining environment file with a status of " + this.status);
      return;
    }

    console.log("Success in getting response from Post request to get environment file", xhr.responseText);
    var config = JSON.parse(xhr.responseText);
    if (config["authorized"] && !config["toDate"]) {
      lastUpdate = config["currentTime"];
      update(config["dashboard"]);
    }
  }
  xhr.open("POST", "environment", true);
  firebase.auth().currentUser.getIdToken(true).then(function(idToken) {
    xhr.send(JSON.stringify({"idtoken":idToken, "dashboard":dashboardID, "lastUpdate":lastUpdate}));
  }).catch(function(error) { console.error(error); });
}

function updateDashboard(forceUpdate=false) {
  var selectObj = document.getElementById("dashboard-select");
  if (selectObj.selectedIndex != -1) {
    if (forceUpdate)
      lastUpdate = 0;
    var dashboardID = selectObj.options[selectObj.selectedIndex].value;
    console.log("Currently selected dashboard", dashboardID);
    updateDashboardArgs(dashboardID);
  }
}

firebase.auth().onAuthStateChanged(function(user) {
  if (user) {
    initializeDashboard();

    document.getElementById("dashboardPage").style.display = "block";
    document.getElementById("signup_div").style.display = "none";
    document.getElementById("login_div").style.display = "none";

    var user = firebase.auth().currentUser;

    if(user != null){
      var email_id = user.email;
      console.log("Welcome User:", email_id);
    }

  } else {
    // No user is signed in.

    document.getElementById("dashboardPage").style.display = "none";
    document.getElementById("signup_div").style.display = "none";
    document.getElementById("login_div").style.display = "block";
  }
});

function loginPage() {
  document.getElementById("dashboardPage").style.display = "none";
  document.getElementById("signup_div").style.display = "none";
  document.getElementById("login_div").style.display = "block";
}

function signupPage() {
  document.getElementById("dashboardPage").style.display = "none";
  document.getElementById("signup_div").style.display = "block";
  document.getElementById("login_div").style.display = "none";
}

function login(){
  var userEmail = document.getElementById("login_email_field").value;
  var userPass = document.getElementById("login_password_field").value;

  firebase.auth().signInWithEmailAndPassword(userEmail, userPass).catch(function(error) {
    // Handle Errors here.
    var errorCode = error.code;
    var errorMessage = error.message;

    var loginButton = document.getElementById("login-error-msg");
    loginButton.style.display = "block";
    loginButton.innerHTML = "Error: " + errorMessage;
  });
}

function loginGoogle(){
  var provider = new firebase.auth.GoogleAuthProvider();
  firebase.auth().signInWithPopup(provider).then(function(result) {
    var token = result.credential.accessToken;
    var user = result.user;
  }).catch(function(error) {
    var errorCode = error.code;
    var errorMessage = error.message;
    var email = error.email;
    var credential = error.credential;
  });
}

function signup(){
  //TODO: Add more features to sign up page
  var userEmail = document.getElementById("signup_email_field").value;
  var userPass = document.getElementById("signup_password_field").value;
  firebase.auth().createUserWithEmailAndPassword(userEmail, userPass).catch(function(error) {
    var errorCode = error.code;
    var errorMessage = error.message;
  });
}

function logout(){
  firebase.auth().signOut();
}

//setInterval(function(){updateDashboard()}, 1000);

function showpasswordmain() {
  var x = document.getElementById("login_password_field");
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}

function showpasswordsignup() {
  var x = document.getElementById("signup_password_field");
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}