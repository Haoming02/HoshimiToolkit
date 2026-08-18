<h2 align="center">Hoshimi Toolkit</h2>
<p align="center">A series of dark magics for certain Unity games ⛦ ⚝ 🟊 🟉</p>

### Getting Started

0. Install [uv](https://github.com/astral-sh/uv)

<details>
<summary>Automatic Installation</summary>

1. Run the `user-setup.bat` file

</details>

<details>
<summary>Manual Installation</summary>

1. Create a **v**irtual **env**ironment
```bash
> uv venv venv
> venv\scripts\activate
```

2. Install the required packages
```bash
(venv) > uv pip install -r requirements.txt
```

</details>

### How to Use

##### Download

1. Obtain the `octocacheevai` file from `/data/data/com.dev.game/files/octo/pdb/foo/bar` under Android
2. Place the `octocacheevai` file under the `EncryptedCache` folder of the respective game folder
3. Change the [arguments](#commandline-arguments) in `user-download.bat`
4. Change the [settings](#options) in `src/options.py`
5. Run the `user-download.bat` file

##### Extract Images

1. Change the [arguments](#commandline-arguments) in `user-resize.bat`
2. Run the `user-resize.bat` file

##### Extract Audio

1. Change the [arguments](#commandline-arguments) in `user-audio.bat`
2. Run the `user-audio.bat` file

### Commandline Arguments

> You can also use **--help** to get the documents

<ins>Work Mode</ins>

- **--remote:** download assets from the game server
- **--local:** only process files placed inside the `Assets` folder

<ins>Diff Mode</ins>

- **--diff:** only download assets that are different
- **--all:** always try to download everything again

<ins>Game</ins>

- **--ipr:** Idoly Pride *(JP Server)*
- **--gakumas:** Gakuen Idolmaster

### Options

- **CPU_THREADS:** increase this value to speed up the processes; setting this too high may crash your system
- **MAX_RETRY:** how many retries before a download is considered failed
- **OPTIMIZE:** save a more compressed image
- **LOSSLESS:** use only lossless algorithm
- **FORMAT:** `jpg` / `png` / `webp`
- **FILTER:** a [regular expression](https://regexr.com/) to filter the assets to download
    - <b><ins>Examples</ins></b>
        - `r"(.*(img|sud).*)"` downloads images and audios *(default)*
        - `r".*img.*"` only downloads images
        - `r".*"` simply downloads everything

For **Resize**, if you simply want to extract every single image, change the `resize.py` script as follow:

```py
RESOLUTION: dict[re.Pattern, tuple[int, int, int | None] | None] = {
    re.compile(r".*"): (None, None, None)
}
```

<hr>

### Code of Conduct
- Refrain from spoiling unreleased contents
- Take responsibilities yourself for any consequences
- Use them at your own risk
