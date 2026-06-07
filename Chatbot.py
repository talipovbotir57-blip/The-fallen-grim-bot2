<!DOCTYPE html>
<html>
<head>
<title>The Fallen Grim</title>

<style>
body {
    background: linear-gradient(135deg, #0a0a0a, #1a001f);
    color: white;
    font-family: Arial;
    text-align: center;
}

img {
    width: 120px;
    border-radius: 50%;
    box-shadow: 0 0 20px purple;
}

.box {
    background: rgba(20,20,20,0.8);
    padding: 20px;
    margin: 20px auto;
    width: 300px;
    border-radius: 15px;
    box-shadow: 0 0 10px black;
}

input {
    width: 70%;
    padding: 10px;
    border-radius: 10px;
    border: none;
}

button {
    padding: 10px;
    background: purple;
    color: white;
    border: none;
    border-radius: 10px;
    cursor: pointer;
}

#chat {
    max-height: 200px;
    overflow-y: auto;
}
</style>

</head>

<body>

<h1>💀 The Fallen Grim</h1>

<img src="/static/profile.jpg">

<div class="box">
<p>1 → Music</p>
<p>2 → Business</p>
<p>3 → Development</p>
<p>4 → My Music Career</p>
</div>

<div class="box">
<div id="chat"></div>
<input id="userInput" placeholder="Type...">
<button onclick="send()">Send</button>
</div>

<script>
async function send() {
    let input = document.getElementById("userInput").value;

    let res = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: input})
    });

    let data = await res.json();

    document.getElementById("chat").innerHTML += 
        "<p><b>You:</b> " + input + "</p>" +
        "<p><b>Bot:</b> " + data.reply + "</p>";
}
</script>

</body>
</html>
