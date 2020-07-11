const fs = require('fs');

const form = document.querySelector("form")
form.addEventListener('submit', submitForm);

function submitForm(e) {
    e.preventDefault();
    let clientID = document.querySelector("#clientIDInput").value
    let clientSecret = document.querySelector("#clientSecretInput").value
    let useragent = document.querySelector("#userAgentInput").value
    let username = document.querySelector("#usernameInput").value
    let password = document.querySelector("#passwordInput").value
    writeToFile('client_id', clientID);
    writeToFile('client_secret', clientSecret);
    writeToFile('user_agent', useragent);
    writeToFile('username', username);
    writeToFile('password', password);
}

function writeToFile(name, data) {
    try {
        fs.appendFileSync('praw.ini', `${name}=${data}\n`);
    } catch (error) {
        console.log(error);
    }   
}