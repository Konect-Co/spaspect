//UTILS FUNCTIONS

function showNone() {
    $('#loginModal').modal('hide');
    $('#signUpModal').modal('hide');
}

function loginPage() {
    showNone();
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

//LISTENER FUNCTIONS (do something on some event)
function login() {
    var userEmail = document.getElementById("login_email_field").value;
    var userPass = document.getElementById("login_password_field").value;

    firebase
        .auth()
        .signInWithEmailAndPassword(userEmail, userPass)
        .then(function(user) {$("#loginModal").modal('hide');})
        .catch(function(error) {
            // Handle Errors here.
            var errorCode = error.code;
            var errorMessage = error.message;

            var loginError = document.getElementById("login-error-msg");
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
        .then(function(user) {$("#loginModal").modal('hide');})
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
    console.log("Logged out");
}

var lastUpdate = 0;

function initializeDashboard() {
    lastUpdate = 0;
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        var accessibleEnvironments = JSON.parse(xhr.responseText);
        var ids = ["dashboard-select", "selectLocation"];
        ids.forEach(id => {
            var sel = document.getElementById(id);

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
        });
    }
    xhr.open("POST", "/dashboards", true);
    var user = firebase.auth().currentUser;
    if (typeof(user) != undefined && user != null) {
        user.getIdToken(true).then(function(idToken) {
            xhr.send(JSON.stringify({ "idtoken": idToken }));
        }).catch(function(error) { console.error(error); });
    } else {
        xhr.send(JSON.stringify({ "idtoken": null }));
    }
}

function updateRealtimeArgs(dashboardID) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        var data = JSON.parse(xhr.responseText);
        //TODO: Update with new format of data
        renderRealtime(data);
    }
    //TODO: Replace this with new POST request
    xhr.open("POST", "/realtimeData", true);
    var user = firebase.auth().currentUser;
    if (typeof(user) != undefined && user != null) {
        user.getIdToken(true).then(function(idToken) {
            xhr.send(JSON.stringify({ "idtoken": idToken, "dashboardId": dashboardID}));
        }).catch(function(error) { console.error(error); });
    } else {
        xhr.send(JSON.stringify({ "idtoken": null, "dashboardId": dashboardID }));
    }
}

function updateRealtime(forceUpdate = false) {
    var selectObj = document.getElementById("dashboard-select");
    if (selectObj.selectedIndex != -1) {
        if (forceUpdate)
            lastUpdate = 0;
        var dashboardID = selectObj.options[selectObj.selectedIndex].value;
        //console.log("Currently selected dashboard", dashboardID);
        updateRealtimeArgs(dashboardID);
    }
}

function updateAggregateArgs(dashboardID) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        //console.log(xhr.responseText);
        var data = JSON.parse(xhr.responseText);
        //console.log(data);
        //TODO: Update with new format of data
        renderAgg(data);
    }
    //TODO: Replace this with new POST request
    xhr.open("POST", "/aggregateData", true);
    var user = firebase.auth().currentUser;
    if (typeof(user) != undefined && user != null) {
        user.getIdToken(true).then(function(idToken) {
            xhr.send(JSON.stringify({ "idtoken": idToken, "dashboardId": dashboardID}));
        }).catch(function(error) { console.error(error); });
    } else {
        xhr.send(JSON.stringify({ "idtoken": null, "dashboardId": dashboardID }));
    }
}

function updateAggregate(forceUpdate = false) {
    var selectObj = document.getElementById("dashboard-select");
    if (selectObj.selectedIndex != -1) {
        if (forceUpdate)
            lastUpdate = 0;
        var dashboardID = selectObj.options[selectObj.selectedIndex].value;
        //console.log("Currently selected dashboard", dashboardID);
        updateAggregateArgs(dashboardID);
    }
}

firebase.auth().onAuthStateChanged(function(user) {
    if (user) {
        initializeDashboard();
        dashboardPage();
        var user = firebase.auth().currentUser;
        if (typeof(user) != undefined && user != null) {
            var email_id = user.email;
            console.log("Welcome User:", email_id);
            document.getElementById("signin-text").innerHTML = "Logout";
        }
        $('#loginModal').modal('hide');
    } else {
        loginPage();
        document.getElementById("signin-text").innerHTML = "Login";
    }
});

function getCustomDisplay() {
    var formElements = ["startTime", "endTime", "violations-option", "unmasked-option", "undistanced-option", "selectLocation"];
    var data = {};
    formElements.forEach(element => {
        if (element == "violations-option" || element == "unmasked-option" || element == "undistanced-option") {
            data[element] = document.getElementById(element).checked;
        } else {
            data[element] = document.getElementById(element).value;
        }
    });

    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        var aggData = JSON.parse(xhr.responseText);
        var plotID = Date.now().toString(10);

        var newDiv = document.createElement("div");
        newDiv.id = plotID;
        document.getElementById("aggPlots1").appendChild(newDiv);

        renderCustomPlot(plotID, aggData, data);
        //TODO: Use this data to make the custom plot
    }
    xhr.open("POST", "/customAggregate", true);
    xhr.send(JSON.stringify(data));
}

//TODO: We should delete this soon, as it's not providing much value
function submitAddSite() {
    firebase.auth().currentUser.getIdToken(true).then(function(idToken) {
        document.getElementById("user-token").setAttribute("hidden", false);
        document.getElementById("user-token").value = idToken;
        document.getElementById("add-site-form").submit();
    }).catch(function(error) { console.error(error); });
}

//TODO: Add command to update these variables depending on which is active
//STARTUP SCRIPT
function startupScript() {
    setInterval(function(){
            updateRealtime();
            updateAggregate();
    }, 1000);
}

startupScript();

//TODO: PLACE CORRECTLY