/**
 * Created by leizhang on 17/5/12.
 */

    // Initialize Firebase
var config = {
        apiKey: "AIzaSyBdU2GHoz_Witkf2KgzRFI4XSlzAP2Weow",
        authDomain: "opendata-cw2-166700.firebaseapp.com",
        databaseURL: "https://opendata-cw2-166700.firebaseio.com",
        projectId: "opendata-cw2-166700",
        storageBucket: "opendata-cw2-166700.appspot.com",
        messagingSenderId: "530820680296"
    };
firebase.initializeApp(config);

var uiConfig = {
    signInSuccessUrl: "/widget",
    signInOptions: [
        // Specify providers you want to offer your users.
        firebase.auth.GoogleAuthProvider.PROVIDER_ID,
        firebase.auth.EmailAuthProvider.PROVIDER_ID,
        firebase.auth.FacebookAuthProvider.PROVIDER_ID,
        firebase.auth.TwitterAuthProvider.PROVIDER_ID
    ],
    // Terms of service url can be specified and will show up in the widget.
    tosUrl: '<your-tos-url>'
};
// Initialize the FirebaseUI Widget using Firebase.
var ui = new firebaseui.auth.AuthUI(firebase.auth());
// The start method will wait until the DOM is loaded.
ui.start('#firebaseui-auth-container', uiConfig);