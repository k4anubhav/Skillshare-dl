# Skillshare Downloader in python

I needed offline access to some skillshare courses. I don't have stable internet connection.
Video download is only available in the skillshare mobile apps and can't watch on a tiny mobile screen.

### Disclaimer
This project is for educational purposes only. I am not responsible for any misuse of this piece of code.

### Support your content creators, do **NOT** use this for **Piracy**!

You will need a skillshare premium account to access premium content.
This script will not handle login for you.

1. Log-in to Skillshare in your browser and open up the developer console.
(cmd/ctrl-shift-c for chrome)

2. Use it to grab your cookie by typing:
```
document.cookie
```

3. Copy-paste cookie from developer console (without " if present) into cookie.txt.

#### Install dependencies:
```
pip install -r requirements.txt
```
or
```
pip3 install -r requirements.txt
```

#### Download Cources:
Run downloder.py
```
python downloader.py
```
or 
```
python3 downloader.py
```