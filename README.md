<p align="center">
  <img src="images/Screenshot%20from%202020-03-31%2016-16-31.png">
</p>
            
[![Downloads](https://pepy.tech/badge/wplay)](https://pepy.tech/project/wplay)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/749acf4cad424fbeb96a412963aa83ea)](https://app.codacy.com/app/rpotter12/whatsapp-play?utm_source=github.com&utm_medium=referral&utm_content=rpotter12/whatsapp-play&utm_campaign=Badge_Grade_Settings)
[![PyPi](https://img.shields.io/pypi/v/wplay)](https://img.shields.io/pypi/v/wplay)
![CircleCI](https://circleci.com/gh/rpotter12/whatsapp-play/tree/master.svg?style=svg&circle-token=2b67dd21e60a01fdd36a670629574479aeb2f5c4)
[![twitter](https://img.shields.io/twitter/url/https/github.com/rpotter12/whatsapp-play.svg?style=social)](https://twitter.com/rpotter121998)
[![HitCount](http://hits.dwyl.io/rpotter12/whatsapp-play.svg)](http://hits.dwyl.io/rpotter12/whatsapp-play)
[![Gitter](https://badges.gitter.im/whatsapp-play/community.svg)](https://gitter.im/whatsapp-play/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)
[![Gitpod Ready-to-Code](https://img.shields.io/badge/Gitpod-Ready--to--Code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/rpotter12/whatsapp-play) 

It is command line software through which you can play with your WhatsApp. It is having different options to play with your WhatsApp like message blast, online tracking, whatsapp chat.. This software aims to provide all facilities which we can do with WhatsApp. This CLI software does not require any API key for the execution.

***wchat*** stands for WhatsApp chat. Through this you can chat with your WhatsApp contact directly from the command line.

***onlinetracker*** tracks the online and offline timings of your WhatsApp contact. It will check the online status and will immediately stores that data into a .txt file. Blog link: [https://github.com/rpotter12/rpotter12.github.io/blob/master/blogs/blog3-tracking-26-07-2019.md](https://github.com/rpotter12/rpotter12.github.io/blob/master/blogs/blog3-tracking-26-07-2019.md)

***tgbot*** sends the tracking status to our telegram bot.

***messageblast*** is a message bomb script. It sends messages to your WhatsApp contact continously. The number of messages is decided by you. You can blast infinite number of messages to your WhatsApp contact.

***messagetimer*** is a message timer script. It sends messages to your WhatsApp contact from time to time. The number of messages and type of messages is decided by you. It's possible to send messages at random interval and the message type is chosen randomly.

***savechat*** is a script to save all the chat which we backup on our google drive.

***scheduleMessage*** is a script to send message at a schedule time.

***changeAbout*** is a script to change the about section of your profile. User can select personal quote, news, quotes, etc.

***wnews*** is a script to get all types of news in your whatsapp group.

***get_media*** is a script to download profile photos of all the contacts in your whatsapp contact list and save them in the `wplay` folder.

---

## Installation

### Install whatsapp-play from PyPI: <br />
Windows: `python -m pip install wplay` <br />
Unix/Linux: `python3 -m pip install wplay` <br />
**Installation Video:** [Simple Installation Link](https://youtu.be/HS6ksu6rCxQ)

### Alternate way - Run whatsapp-play from source code: <br />
**Windows**<br />
`$ git clone https://github.com/rpotter12/whatsapp-play.git` <br />
`$ cd 'whatsapp-play'` <br />
`$ python -m pip install -r requirements.txt` <br />
`$ python -m wplay -h` <br />

**Unix/Linux/Mac**<br />
`$ git clone https://github.com/rpotter12/whatsapp-play.git` <br />
`$ cd 'whatsapp-play'` <br />
`$ python3 -m pip install -r requirements.txt` <br />
`$ python3 -m wplay -h` <br />

## Usage
<img src="images/usage.png"><br />

For detailed usage of command visit: [https://github.com/rpotter12/whatsapp-play/wiki/Usage](https://github.com/rpotter12/whatsapp-play/wiki/Usage)

## Contribute

The easiest way to contribute to **Whatsapp-Play** is by starring the repository and opening more and more [issues](https://github.com/rpotter12/whatsapp-play/issues) for features you'd like to see in future. <br />

First step is to create a fork and clone, then you can solve the [issues](https://github.com/rpotter12/whatsapp-play/issues) listed and help us find new ones. Then try debugging with Visual Studio Code it is necessary to create a launcher with the arguments. <br />

Steps to create a launcher with arguments follow the steps bellow: <br />
1. Click in 'Debug' tab
1. Click in 'Add Configuration'
1. Select 'Module'
1. Type 'wplay' and press Enter
1. A json file will be opened. Inside configurations add the args, for example: "args":["-wb","name"] 

**Debug Tutorial Video:** [Debug Tutorial Link](https://youtu.be/NyJgUGvyWnY)<br />
Check more about contribution guidelines [here](https://www.github.com/rpotter12/whatsapp-play/CONTRIBUTION.md)

## Disclaimer
This software is for educational purpose only. Keeping eye on a innocent person can make person's life stressful.

## License
[![License](https://img.shields.io/github/license/rpotter12/whatsapp-play.svg)](https://github.com/rpotter12/whatsapp-play/blob/master/README.md)

***If you like the project, support us by star***
