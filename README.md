## Hoshimi Toolkit
A series of dark magics for certain Unity games ⛦ ⚝ 🟊 🟉

### Getting Started

0. Install [Python](https://www.python.org/downloads/)
    - Remember to `Add Python to PATH`
    - This project was built on Python `3.10.x`

<details open>
<summary>One-Click Installation</summary>

1. Run the `user-setup.bat` file

</details>

<details>
<summary>Manual Installation</summary>

1. Create a **v**irtual **env**ironment
```bash
> python -m venv venv
> venv\scripts\activate
```

2. Install the required packages
```bash
(venv) > pip install -r requirements.txt
```

</details>

### How to Use

<ins>Download</ins>

1. Obtain the `octocacheevai` file from `/data/data/com.dev.game/files/octo/pdb/foo/bar` under Android
2. Place the `octocacheevai` file under the `EncryptedCache` folder of the respective game folder
3. Change the [arguments](#commandline-arguments) in `user-download.bat`
4. Change the [settings](#options) in `src/options.py`
5. Run the `user-download.bat` file

<ins>Resize</ins>

1. Change the [arguments](#commandline-arguments) in `user-resize.bat`
2. Run the `user-resize.bat` file

### Commandline Arguments

> You can also use **--help** to get the documents

<ins>Diff Mode</ins>

- **--remote:** download assets from the game server
- **--local:** only process files placed inside the `Assets` folder

<ins>Work Mode</ins>

- **--diff:** only download assets that are different
- **--all:** always try to download everything again

<ins>Game</ins>

- **--ipr:** Idoly Pride
- **--kr:** Idoly Pride *(Korean Server)*
- **--gakumas:** Gakuen Idolmaster

### Options

- **CPU_THREADS:** increase this value to speed up the processes; setting this too high may crash your system
- **MAX_RETRY:** how many retries before a download is considered failed
- **OPTIMIZE:** takes longer to save a more compressed image
- **FILTER:** a [regular expression](https://regexr.com/) to filter the assets to download
    - The default value downloads everything

<hr>

### Code of Conduct
- Refrain from spoiling unreleased contents
- Take responsibilities yourself for any consequences
- Use them at your own risk
