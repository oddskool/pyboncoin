Alert Bot
=======

## Setup

Install Python 3.6 with Miniconda
```
$ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
$ bash Miniconda3-latest-Linux-x86_64.sh
```

Install dependencies
```
$ pip3 install -r requirements.txt
``` 

Install missing libs to run Chromium on Ubuntu server: 
```
$ sudo apt install gconf-service libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxss1 libxtst6 libappindicator1 libnss3 libasound2 libatk1.0-0 libc6 ca-certificates fonts-liberation lsb-release xdg-utils
```

Install ``Xvfb`` to simulate a graphic server (for rendering the webpage)
```
$ sudo apt install xvfb
```

Start ``Xvfb`` inside a ``screen`` session:
```
$ Xvfb :99 -screen 0 1024x768x16
```

Install a ``crontab``

```
BASH_ENV=/home/ubuntu/.bashrc
SHELL=/bin/bash
PATH=/home/ubuntu/miniconda3/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
DISPLAY=:99.0
*/15 * * * * cd /home/ubuntu/pyboncoin && PYTHONPATH=pyboncoin python -m pyboncoin.monitor sample.conf >> sample.log 2>&1
```


