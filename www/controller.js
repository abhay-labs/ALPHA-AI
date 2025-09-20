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

    // Display speak message
    eel.expose(DisplayMessage)
    function DisplayMessage(message) {

        $(".siri-message li:first").text(message);
        $(".siri-message").textillate('start');

    }

    //Display Hood
    eel.expose(ShowHood)
    function ShowHood() {
        $("#Oval").attr("hidden", false);
        $("#SiriWave").attr("hidden", true);
    }


    eel.expose(senderText);
    function senderText(message) {
        var chatBox = document.getElementById("chat-canvas-body");
        if (message.trim() !== "") {
            chatBox.innerHTML += `<div class="row justify-content-end mb-4">
            <div class="width-size">
            <div class="sender_message">${message}</div>
            </div>
        </div>`;

            // Scroll to the bottom of the chatbox
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }



    eel.expose(receiverText);
    function receiverText(message) {
        var chatBox = document.getElementById("chat-canvas-body");
        if (message.trim() !== "") {
            chatBox.innerHTML += `<div class="row justify-content-start mb-4">
            <div class="width-size">
            <div class="receiver_message">${message}</div>
            </div>
        </div>`;

            // Scroll to the bottom of the chatbox
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }




});