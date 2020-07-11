const electron = require('electron')
const url = require('url')
const path = require('path')

const { app, BrowserWindow, Menu, ipcMain} = electron;

let mainWindow;

app.on('ready', function () {
    mainWindow = new BrowserWindow({
        width: 600,
        height: 630,
        webPreferences: {
            nodeIntegration: true,
            enableRemoteModule: true
        }
    });
    mainWindow.resizable = false;
    mainWindow.loadURL(url.format({
        pathname: path.join(__dirname, 'mainWindow.html'),
        protocol: 'file:',
        slashes: true
    }));

    mainWindow.once('ready-to-show', () => {
        mainWindow.show()
    });

    ipcMain.on('close:app', (evt, arg) => {
        app.quit()
    })

    // const mainMenu = Menu.buildFromTemplate(mainMenuTemp);
    // TO DO: Possibly move quit and start functionality 
    // to Menu
    //Menu.setApplicationMenu(mainMenu)

});


/* const mainMenuTemp = [
    {
        label: 'File',
        submenu: [
            {
                label: 'Exit',
                click() {
                    app.quit();
                }
            }
        ]
    }
]; */