const fs = require("fs");
const { ipcRenderer } = require("electron");

const form = document.querySelector("form");
form.addEventListener("submit", submitForm);

function submitForm(e) {
  e.preventDefault();
  let clientID = document.querySelector("#clientIDInput").value;
  let clientSecret = document.querySelector("#clientSecretInput").value;
  let useragent = document.querySelector("#userAgentInput").value;
  let username = document.querySelector("#usernameInput").value;
  let password = document.querySelector("#passwordInput").value;

  fs.appendFileSync("src/praw.ini", "[DEFAULT]\r\n");
  writeToFile("client_id", clientID);
  writeToFile("client_secret", clientSecret);
  writeToFile("user_agent", useragent);
  writeToFile("username", username);
  writeToFile("password", password);

  ipcRenderer.send("close:Settings");
}

function writeToFile(name, data) {
  try {
    fs.appendFileSync("src/praw.ini", `${name}=${data}\r\n`);
  } catch (error) {
    console.log(error);
  }
}
