/* =====================================================
   Project : ALPHA (Smart AI Assistant)
   Author  : Abhay Jaiswal
   Year    : 2025
   Copyright (c) 2025 Abhay Jaiswal
   All Rights Reserved.
   Unauthorized copying or use is strictly prohibited.
   Repo    : https://github.com/kingabhay2005/ALPHA
   Unique Token : ALPHA-SEC-2025-ABJ-UNQ-9173X
   ===================================================== */


$(document).ready(function () {

    // Text Animation
    $('.text').textillate({
        loop: true,
        sync: true,
        in: { effect: "bounceIn" },
        out: { effect: "bounceOut" },
    });

    // Siri Wave Animation
    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 800,
        height: 200,
        style: "ios9",
        amplitude: "1",
        speed: "0.25",
        autostart: true
    });

    $('.siri-message').textillate({
        loop: true,
        sync: true,
        in: { effect: "fadeInUp", sync: true },
        out: { effect: "fadeOutUp", sync: true },
    });

    // Start Listening Function
    function startListening() {
        $("#Oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);
        
        eel.allCommands().then(response => {
            console.log("Voice command received:", response);
            // Response ko yahan handle karo
        });

        setTimeout(function () {
            eel.playAssistantSound();
        }, 1);
    }

    // Mic Button Click
    $("#MicBtn").click(function () {
        startListening();
    });

    // Keyboard Shortcut Command
    function doc_keyUp(e) {
        if(e.key === 'j' && e.metaKey) {
            startListening();
        }
    }
    document.addEventListener('keyup', doc_keyUp, false);

    // Play Assistant with message
    function playAssistant(message) {
        if(message.trim() != "") {
            $("#Oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);

            eel.allCommands(message).then(response => {
                console.log("Text command received:", response);
                // Response ko yahan handle karo
            });

            $("#chatbox").val("");
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
        }
    }

    // Show or Hide Buttons based on input
    function ShowHideButton(message) {
        if(message.trim().length == 0) {
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
        } else {
            $("#MicBtn").attr('hidden', true);
            $("#SendBtn").attr('hidden', false);
        }
    }

    // Input Box Keyup Event
    $("#chatbox").keyup(function () {
        let message = $("#chatbox").val();
        ShowHideButton(message);
    });

    // Send Button Click
    $("#SendBtn").click(function () {
        let message = $("#chatbox").val();
        playAssistant(message);
    });


    // Enter key press event in chatbox
    $("#chatbox").on('keypress', function(e) {
        if(e.which == 13) {   // 13 is the Enter key code
            let message = $("#chatbox").val();
            playAssistant(message);
        }
    });


    

});
