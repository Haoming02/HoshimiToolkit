## DISCLAIMER
- All projects in this repo should be used for study purposes only
- You shall take responsibilities yourself for using these tools

## Getting Started
0. Create a <ins>Python</ins> **V**irtual **Env**ironment
```bash
> python -m venv venv
> venv\scripts\activate
```
1. Install the required packages
```bash
(venv) > pip install -r requirements.txt
```
2. **(Optional)** Install the required packages for image resizing
```bash
(venv) > pip install -r requirements_resize.txt
```

## How to Use
1. Obtain the `octocacheevai` from `/data/data/X.Y.Z/files/octo/pdb/foo/bar`
2. Place the `octocacheevai` under `EncryptedCache`
3. **(Optional)** Change the settings in `Main.py`
4. Run
```bash
> venv\scripts\activate
(venv) > cd foo
(venv) \foo > python Main.py
```
5. **(Optional)** Run

> [!WARNING]
> Not implemented yet...

```bash
(venv) \foo > cd ..
(venv) > python Resize.py foo
```
