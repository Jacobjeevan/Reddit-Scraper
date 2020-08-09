const electron = require("electron");
const url = require("url");
const path = require("path");

const { app, BrowserWindow, Menu, ipcMain } = electron;

app.on("ready", function () {
  mainWindow = new BrowserWindow({
    width: 600,
    height: 630,
    webPreferences: {
      nodeIntegration: true,
      enableRemoteModule: true,
      devTools: true,
    },
  });
  mainWindow.resizable = true;
  mainWindow.loadURL(
    url.format({
      pathname: path.join(__dirname, "src/mainWindow.html"),
      protocol: "file:",
      slashes: true,
    })
  );

  mainWindow.once("ready-to-show", () => {
    mainWindow.show();
  });

  ipcMain.on("close:app", (evt, arg) => {
    app.quit();
  });

  const mainMenu = Menu.buildFromTemplate(mainMenuTemp);
  Menu.setApplicationMenu(mainMenu);
});

// To Do: Move Quit and Settings to Menu
const mainMenuTemp = [
  {
    label: "File",
    submenu: [
      {
        label: "Settings",
        click() {
          createSettingsWindow();
        },
      },

      {
        label: "Exit",
        click() {
          app.quit();
        },
      },
    ],
  },
  {
    label: "View",
    submenu: [
      { role: "reload" },
      { role: "forcereload" },
      { role: "toggledevtools" },
      { type: "separator" },
      { role: "resetzoom" },
      { role: "zoomin" },
      { role: "zoomout" },
      { type: "separator" },
      { role: "togglefullscreen" },
    ],
  },
];

function createSettingsWindow() {
  let settingsWindow = new BrowserWindow({
    width: 700,
    height: 500,
    webPreferences: {
      nodeIntegration: true,
      enableRemoteModule: true,
      resizable: true,
    },
  });

  settingsWindow.loadURL(
    url.format({
      pathname: path.join(__dirname, "src/settingsWindow.html"),
      protocol: "file:",
      slashes: true,
    })
  );
  settingsWindow.show();

  ipcMain.on("close:Settings", () => {
    settingsWindow.close();
  });

  settingsWindow.once("close", () => {
    mainWindow.webContents.send("check:praw");
  });
}
