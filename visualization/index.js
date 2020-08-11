function showNone() {
    $('#loginModal').modal('hide');
    $('#signUpModal').modal('hide');
}

function loginPage() {
    showNone();
    $('#loginModal').modal('show');
}

function signupPage() {
    showNone();
    $('#signUpModal').modal('show');
}

function dashboardPage() {
    showNone();
}

function addSitePage() {
    showNone();
}

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

function login() {
    var userEmail = document.getElementById("login_email_field").value;
    var userPass = document.getElementById("login_password_field").value;

    firebase
        .auth()
        .signInWithEmailAndPassword(userEmail, userPass)
        .then(function(user) {$("#loginGoogle").modal('hide');})
        .catch(function(error) {
            // Handle Errors here.
            var errorCode = error.code;
            var errorMessage = error.message;

            var loginError = document.getElementById("login-error-msg");
            loginError;
            loginError.innerHTML = "Error: " + errorMessage;
        });
}

function loginGoogle() {
    var provider = new firebase.auth.GoogleAuthProvider();
    firebase
        .auth().signInWithPopup(provider).then(function(result) {
            var token = result.credential.accessToken;
            var user = result.user;
        })
        .then(function(user) {$("#loginGoogle").modal('hide');})
        .catch(function(error) {
            var errorCode = error.code;
            var errorMessage = error.message;
            var email = error.email;
            var credential = error.credential;
        });
}

function signup() {
    //TODO: Add more features to sign up page
    var userEmail = document.getElementById("signup_email_field").value;
    var userPass = document.getElementById("signup_password_field").value;
    firebase.auth().createUserWithEmailAndPassword(userEmail, userPass).catch(function(error) {
        var errorCode = error.code;
        var errorMessage = error.message;
    });
}

function logout() {
    firebase.auth().signOut();
    console.log("Logged out")
}

var lastUpdate = 0;

function initializeDashboard() {
    lastUpdate = 0;
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (this.status != 200) {
            console.log("POST to /dashboards returned a non-200 status of " + this.status);
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
            opt.appendChild(document.createTextNode(txt));
            opt.value = key;

            sel.appendChild(opt);
        });

        updateDashboard();
    }
    xhr.open("POST", "/dashboards", true);
    firebase.auth().currentUser.getIdToken(true).then(function(idToken) {
        xhr.send(JSON.stringify({ "idtoken": idToken }));
    }).catch(function(error) { console.error(error); });
}

function updateDashboardArgs(dashboardID) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (this.status != 200) {
            console.log("POST to /environment returned a non-200 status of " + this.status);
        }

        //console.log("Success in getting response from Post request to get environment file", xhr.responseText);
        var config = JSON.parse(xhr.responseText);

        if (config["authorized"] && !config["toDate"]) {
            lastUpdate = config["currentTime"];
            var dashboard = config["dashboard"];
            update(dashboard);
        }
    }
    xhr.open("POST", "environment", true);
    firebase.auth().currentUser.getIdToken(true).then(function(idToken) {
        xhr.send(JSON.stringify({ "idtoken": idToken, "dashboard": dashboardID, "lastUpdate": lastUpdate }));
    }).catch(function(error) { console.error(error); });
}

function updateDashboard(forceUpdate = false) {
    var selectObj = document.getElementById("dashboard-select");
    if (selectObj.selectedIndex != -1) {
        if (forceUpdate)
            lastUpdate = 0;
        var dashboardID = selectObj.options[selectObj.selectedIndex].value;
        //console.log("Currently selected dashboard", dashboardID);
        updateDashboardArgs(dashboardID);
    }
}
firebase.auth().onAuthStateChanged(function(user) {
    if (user) {
        initializeDashboard();
        dashboardPage();
        var user = firebase.auth().currentUser;
        if (user != null) {
            var email_id = user.email;
            console.log("Welcome User:", email_id);
        }
        $('#loginModal').modal('hide');
    } else {
        loginPage();
    }
});

function submitAddSite() {
    firebase.auth().currentUser.getIdToken(true).then(function(idToken) {
        document.getElementById("user-token").setAttribute("hidden", false);
        document.getElementById("user-token").value = idToken;
        document.getElementById("add-site-form").submit();
    }).catch(function(error) { console.error(error); });
}

//setInterval(function(){updateDashboard()}, 1000);