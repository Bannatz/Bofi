# Bofi
A Lofi Scraper and Player written in Python.

# Installation
```bash
$ pip install -r requirements
```
if on ArchLinux:
Some of the Libraries used are in the AUR.
So you can easily use your AUR-Helper like `yay` or `paru` to install the Libraries.

Im using `yay`:
```bash
$ sudo yay -S python-beautifulsoup4 python-requests python-pygame python-pydub
```

# Usage
```bash
$ python main.py
```
On first Launch it caches the Songs.
If used with the arg `help` it shows you a help message.

If this:
```
<frozen importlib._bootstrap>:488: RuntimeWarning: Your system is avx2 capable but pygame was not built with support for it. The performance of some of your blits could be adversely affected. Consider enabling compile time detection with environment variables like PYGAME_DETECT_AVX2=1 if you are compiling without cross compilation.

```
shows up you can safely ignore it.

# Configuration
## Still in Development


