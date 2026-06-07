<!DOCTYPE html>
<html>
<head>
<title>The Fallen Grim</title>

<style>
body {
    background: linear-gradient(135deg, #0a0a0a, #1a001f);
    color: white;
    font-family: Arial;
    margin: 0;
    padding: 20px;
}

h1 {
    text-align: center;
}

img {
    display: block;
    width: 120px;
    border-radius: 50%;
    box-shadow: 0 0 20px purple;
    margin: 0 auto 20px;
}

.box {
    background: rgba(20,20,20,0.8);
    padding: 20px;
    margin: 20px auto;
    max-width: 300px;
    border-radius: 15px;
    box-shadow: 0 0 10px black;
}

.box p {
    text-align: center;
    margin: 10px 0;
}

input {
    width: 70%;
    padding: 10px;
    border-radius: 10px;
    border: none;
    box-sizing: border-box;
}

button {
    padding: 10px 15px;
    background: purple;
    color: white;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    margin-left: 5px;
}

button:hover {
    background: #aa00aa;
}

#chat {
    max-height: 200px;
    min-height: 250px;
    overflow-y: auto;
    text-align: left;
    margin-bottom: 10px;
    padding: 10px;
    background: rgba(10,10,10,0.5);
    border-radius: 5px;
}

.chat-message {
    padding: 10px;
    border-radius: 12px;
    margin: 8px 0;
    background: rgba(255,255,255,0.05);
    word-wrap: break-word;
}

.chat-message b {
    color: #bb00ff;
}

.input-container {
    display: flex;
    justify-content: center;
    gap: 5px;
    flex-wrap: wrap;
}

input {
    flex: 1;
    min-width: 200px;
}

</style>

</head>

<body>

<h1>💀 The Fallen Grim</h1>

<img src="/static/profile.jpg" alt="The Fallen Grim Chatbot Avatar">

<div class="box">
<p>1 → Music</p>
<p>2 → Business</p>
<p>3 → Development</p>
<p>4 → My Music Career</p>
</div>

<div class="box">
<div id="chat"></div>
<div class="input-container">
    <input id="userInput" placeholder="Type..." autocomplete="off">
    <button onclick="send()">Send</button>
</div>
</div>

<script>
async function send() {
    const inputField = document.getElementById("userInput");
    const input = inputField.value.trim();

    if (!input) return;

    const chatDiv = document.getElementById("chat");

    // Message utilisateur
    const userMsg = document.createElement("p");
    userMsg.className = "chat-message";
    userMsg.innerHTML = "<b>You:</b> ";
    userMsg.appendChild(document.createTextNode(input));
    chatDiv.appendChild(userMsg);

    // Indicateur de chargement
    const loading = document.createElement("p");
    loading.className = "chat-message";
    loading.innerHTML = "<b>Bot:</b> typing...";
    chatDiv.appendChild(loading);

    chatDiv.scrollTop = chatDiv.scrollHeight;

    inputField.value = "";

    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: input
            })
        });

        const data = await res.json();

        loading.remove();

        const botMsg = document.createElement("p");
        botMsg.className = "chat-message";
        botMsg.innerHTML = "<b>Bot:</b> ";
        botMsg.appendChild(
            document.createTextNode(data.reply || "No response")
        );

        chatDiv.appendChild(botMsg);

    } catch (error) {
        loading.remove();

        const errorMsg = document.createElement("p");
        errorMsg.className = "chat-message";
        errorMsg.innerHTML = "<b>Error:</b> Failed to connect.";
        chatDiv.appendChild(errorMsg);
    }

    chatDiv.scrollTop = chatDiv.scrollHeight;
}

// Allow sending message with Enter key
document.getElementById("userInput").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        send();
    }
});
</script>

</body>
</html>
