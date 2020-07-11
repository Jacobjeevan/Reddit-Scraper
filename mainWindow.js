const path = require('path')
const url = require('url')
const { dialog, BrowserWindow } = require('electron').remote
const { ipcRenderer } = require('electron');
const { spawn } = require('child_process')
let loadExistingFile = false;
let savepath = null

const formSwitch = document.querySelector("input[name=checkbox]");
formSwitch.addEventListener('change', function () {
    disableSubmit()
    if (this.checked) {
        document.getElementById("saveChooser").textContent = "Select file";
        document.querySelector("label[for=saveChooser]").textContent = "No file chosen"
        loadExistingFile = true;

    }
    else {
        document.getElementById("saveChooser").textContent = "Select directory";
        document.querySelector("label[for=saveChooser]").textContent = "No folder chosen"
        loadExistingFile = false;
    }
});

let saveChooser = document.getElementById("saveChooser")
saveChooser.addEventListener('click', saveDialog)


function saveDialog() {
    if (loadExistingFile) {
        options = ['openFile']
    }
    else {
        options = ['openDirectory']
    }
    dialog.showOpenDialog({
        properties: options
    }).then(result => {
        if (!result.canceled) {
            document.querySelector("label[for=saveChooser]").textContent = result.filePaths[0] + " selected"
            savepath = result.filePaths[0]
            enableSubmit()
        }
    }).catch(err => {
        console.log(err)
    })
}

function enableSubmit() {
    let submitbtn = document.getElementById('submitbtn')
    submitbtn.disabled = false;
    submitbtn.classList.remove('disabled', 'btn-danger')
    submitbtn.classList.add('btn-success')
    submitbtn.setAttribute('aria-disabled', false)
    submitbtn.textContent = "Start scraping"
}

(function () {
    'use strict';
    window.addEventListener('load', function () {
        var forms = document.getElementsByClassName('needs-validation');
        var validation = Array.prototype.filter.call(forms, function (formElement) {
            formElement.addEventListener('submit', function (event) {
                if (formElement.checkValidity() === false) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                formElement.classList.add('was-validated')
            }, false);
        });
    }, false);
})();

const form = document.querySelector("form")
form.addEventListener('submit', submitForm);


function submitForm(e) {
    if (validate()) {
        e.preventDefault()
        runScraper()
    };
};

function validate() {
    var inputs = document.getElementsByClassName('form_inputs')
    for (elem of inputs) {
        if (elem.checkValidity() === false) {
            return false;
        }
    }
    if (!savepath) {
        return false;
    }
    return true;
}

function runScraper() {
    disableSubmit()
    disableSaveChooser()
    handleElapsedTime();
    document.getElementById('submitbtn').textContent = "Running";
    let subreddit = document.querySelector("#subredditInput").value
    let minimumComments = document.querySelector("#minimumCommentsInput").value
    argsArray = ["-u", path.join(__dirname, 'script', 'Scraper.py'), subreddit, "-m", minimumComments, "-g"]
    if (savepath) {
        argsArray.push("-s", savepath)
        if (loadExistingFile) {
            argsArray.push("-l", 1)
        }
    }
    spawnChild(argsArray, minimumComments)
}

function disableSubmit() {
    let submitbtn = document.getElementById('submitbtn')
    submitbtn.disabled = true;
    submitbtn.classList.add('disabled', 'btn-danger')
    submitbtn.setAttribute('aria-disabled', true)
}

function handleElapsedTime() {
    var startTime = new Date();
    displayTime()
    function displayTime() {
        var endTime = new Date();
        var timeDiff = endTime - startTime;
        timeDiff /= 1000;
        var seconds = Math.round(timeDiff % 60);
        timeDiff = Math.floor(timeDiff / 60);
        var minutes = Math.round(timeDiff % 60);
        timeDiff = Math.floor(timeDiff / 60);
        var hours = Math.round(timeDiff % 24);
        timeDiff = Math.floor(timeDiff / 24);
        var days = timeDiff;
        setTimeout(displayTime, 1000);
        var fullmsg = `Elasped Time: ${days} day(s), ${hours} hour(s), ${minutes} minute(s), ${seconds} seconds`
        document.getElementById("ElapsedTime").textContent = fullmsg;
    }
}

function spawnChild(argsArray, minimumComments) {
    subprocess = run();

    const closeApp = document.getElementById('quit');
    closeApp.textContent = "Quit Scraping"
    closeApp.style.visibility = "visible"
    closeApp.addEventListener('click', () => {
        console.log(subprocess.kill());
        closeApp.textContent = "Quit Program";
    });

    function run() {
        return spawn('python', argsArray);
    }

    subprocess.stdout.on('data', (data) => {
        handleScraperOutput(`${data}`, minimumComments);
    });

    subprocess.stderr.on('data', (data) => {
        console.log(`error:${data}`);
    });

    subprocess.on('close', () => {
        handleExit()
        console.log("Closed");
    });

};

function handleExit() {
    handleProgressBarWhenComplete()
    disableSaveChooser()
    document.getElementById("quit").style.visibility = "visible"
    const closeApp = document.getElementById('quit');
    closeApp.addEventListener('click', () => {
        ipcRenderer.send('close:app')
    });
}

function handleProgressBarWhenComplete() {
    let progressbar = document.getElementById("progress-bar")
    progressbar.classList.remove("bg-info")
    progressbar.classList.add("bg-success")
    progressbar.textContent = "Done"
}

function disableSaveChooser() {
    let saveChooser = document.getElementById("saveChooser")
    saveChooser.disabled = true
    saveChooser.classList.add('disabled')
    saveChooser.setAttribute('aria-disabled', true)
}

function handleScraperOutput(data, minimumComments) {
    if (data != "Done") {
        console.log(data)
        samplesCollected = Number(data)
        var progress = samplesCollected / minimumComments * 100
        handleProgressBar(progress)
    }
}

function handleProgressBar(progress) {
    progress = progress.toFixed(1)
    let progressbar = document.getElementById("progress-bar")
    progressbar.setAttribute('aria-valuenow', progress)
    progressbar.setAttribute('style', `width: ${progress}%`)
    progressbar.textContent = progress + '%'
    if (progress >= 100.0) {
        progressbar.classList.add("bg-info")
        progressbar.textContent = "Almost Done"
    }
}

const settingbtn = document.getElementById("settings");
settingbtn.addEventListener("click", event => {
    let settingsWindow = new BrowserWindow({
        width: 600,
        height: 500,
        webPreferences: {
            nodeIntegration: true,
            enableRemoteModule: true,
            resizable: true,
        }
    });

    settingsWindow.loadURL(url.format({
        pathname: path.join(__dirname, 'settingsWindow.html'),
        protocol: 'file:',
        slashes: true
    }));
    settingsWindow.show();
});