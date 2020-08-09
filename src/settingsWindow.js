const fs = require("fs");
const { ipcRenderer } = require("electron");

try {
  if (fs.existsSync("src/prawConfig.json")) {
    fs.readFile("src/prawConfig.json", "utf-8", (err, data) => {
      if (err) {
        console.log(err);
      }
      const user = JSON.parse(data.toString());
      let { clientID, clientSecret, useragent, username, password } = user;
      console.log(user);
      document.querySelector("#clientIDInput").value = clientID;
      document.querySelector("#clientSecretInput").value = clientSecret;
      document.querySelector("#userAgentInput").value = useragent;
      document.querySelector("#usernameInput").value = username;
      document.querySelector("#passwordInput").value = password;
    });
  }
} catch (error) {
  console.log(error);
}

const form = document.querySelector("form");
form.addEventListener("submit", submitForm);

function submitForm(e) {
  e.preventDefault();
  let clientID = document.querySelector("#clientIDInput").value;
  let clientSecret = document.querySelector("#clientSecretInput").value;
  let useragent = document.querySelector("#userAgentInput").value;
  let username = document.querySelector("#usernameInput").value;
  let password = document.querySelector("#passwordInput").value;

  const prawConfig = { clientID, clientSecret, useragent, username, password };
  const data = JSON.stringify(prawConfig);

  try {
    fs.writeFileSync("src/prawConfig.json", data);
  } catch (error) {
    console.error(err);
  }

  ipcRenderer.send("close:Settings");
}
