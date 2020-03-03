# whatsapp-play

[![Downloads](https://pepy.tech/badge/wplay)](https://pepy.tech/project/wplay)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/749acf4cad424fbeb96a412963aa83ea)](https://app.codacy.com/app/rpotter12/whatsapp-play?utm_source=github.com&utm_medium=referral&utm_content=rpotter12/whatsapp-play&utm_campaign=Badge_Grade_Settings)
[![PyPi](https://img.shields.io/badge/pypi-v5.0.2-blue)](https://pypi.org/project/wplay/)
![CircleCI](https://circleci.com/gh/rpotter12/whatsapp-play/tree/master.svg?style=svg&circle-token=2b67dd21e60a01fdd36a670629574479aeb2f5c4)
[![twitter](https://img.shields.io/twitter/url/https/github.com/rpotter12/whatsapp-play.svg?style=social)](https://twitter.com/rpotter121998)
[![HitCount](http://hits.dwyl.io/rpotter12/whatsapp-play.svg)](http://hits.dwyl.io/rpotter12/whatsapp-play)
[![Gitter](https://badges.gitter.im/whatsapp-play/community.svg)](https://gitter.im/whatsapp-play/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

It is command line software through which you can play with your WhatsApp. It is having different options to play with your WhatsApp like message blast, online tracking, whatsapp chat.. This software aims to provide all facilities which we can do with WhatsApp. This CLI software does not require any API key for the execution.

***wchat*** stands for WhatsApp chat. Through this you can chat with your WhatsApp contact directly from the command line.

***onlinetracker*** tracks the online and offline timings of your WhatsApp contact. It will check the online status and will immediately stores that data into a .txt file. Blog link: [https://github.com/rpotter12/rpotter12.github.io/blob/master/blogs/blog3-tracking-26-07-2019.md](https://github.com/rpotter12/rpotter12.github.io/blob/master/blogs/blog3-tracking-26-07-2019.md)

***tgbot*** sends the tracking status to our telegram bot.

***messageblast*** is a message bomb script. It sends messages to your WhatsApp contact continously. The number of messages is decided by you. You can blast infinite number of messages to your WhatsApp contact.

***messagetimer*** is a message timer script. It sends messages to your WhatsApp contact from time to time. The number of messages and type of messages is decided by you. It's possible to send messages at random interval and the message type is chosen randomly.

***savechat*** is a script to save all the chat which we backup on our google drive.

---

## Installation 
### Install whatsapp-play from PyPI: <br />
Windows: `python -m pip install wplay` <br />
Unix: `python3 -m pip install wplay` <br />
**Installation Video:** [Simple Installation Link](https://youtu.be/HS6ksu6rCxQ)

### ALTERNATIVE - Run whatsapp-play from source code: <br />
`git clone https://github.com/rpotter12/whatsapp-play.git` <br />
`cd 'whatsapp-play'` <br />
Windows: `python -m pip install -r requirements.txt` <br />
Unix: `python3 -m pip install -r requirements.txt` <br />
Windows: `python -m wplay -h` <br />
Unix: `python3 -m wplay -h` <br />

## Usage
<img src="/images/usage.png"><br>
Example - `wplay -wt "target_name_of_your_whatsapp_contact"` or `wplay -pull "Databases/msgstore.db.crypt12"

***If you like the project, support us by star***
