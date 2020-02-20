# whatsapp-play

[![Downloads](https://pepy.tech/badge/wplay)](https://pepy.tech/project/wplay)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/749acf4cad424fbeb96a412963aa83ea)](https://app.codacy.com/app/rpotter12/whatsapp-play?utm_source=github.com&utm_medium=referral&utm_content=rpotter12/whatsapp-play&utm_campaign=Badge_Grade_Settings)
[![PyPi](https://img.shields.io/badge/pypi-v2.0.0-blue)](https://pypi.org/project/wplay/)
[![codecov](https://codecov.io/gh/rpotter12/whatsapp-play/branch/master/graph/badge.svg)](https://codecov.io/gh/rpotter12/whatsapp-play)
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

First, it is recommended to create a virtual environment but it is not mandatory. To create follow the steps below: <br />
`cd 'whatsapp-play'` <br />
`python3 -m venv .venv` <br />
*Windows*: `./.venv/Scripts/activate` <br />
*Unix*: `source .venv/bin/activate` <br />

Secondly: <br /> 
Install whatsapp-play from PyPI: <br />
*With Virtual Environment*: `pip install wplay`. <br />
*Without Virtual Environment*: `python3 -m pip install wplay`. <br />

Or

Install whatsapp-play from source code: <br />
`cd 'whatsapp-play'` <br />
*Windows*: `./build.bat` <br />
*Unix*: `sh build.sh` <br />
`cd dist` <br />
`ls` -> get the name of the file ending with 'whl' <br />
*With Virtual Environment*: `pip install <name_of_file>.whl`. <br />
*Without Virtual Environment*: `python3 -m pip install <name_of_file>.whl`. <br />

## Usage
<img src="/images/usage.png"><br>
Example - `wplay -wt "target_name_of_your_whatsapp_contact"` or `wplay -pull "Databases/msgstore.db.crypt12"`

## Contribute
To contribute you can solve our [issues](https://github.com/rpotter12/whatsapp-play/issues) and help us find new ones. To debug with Visual Studio Code it is necessary to create a launcher with the arguments. <br />

To create a launcher with arguments follow the steps bellow: <br />
1. Click in 'Debug' tab
1. Click in 'Add Configuration'
1. Select 'Module'
1. Type 'wplay' and press Enter
1. A json file will be opened. Inside configurations add the args, for example: "args":["-wb","name"] 

## Disclaimer
This software is for educational purpose only. Keeping eye on a innocent person can make person's life stressful.

## License
[![License](https://img.shields.io/github/license/rpotter12/whatsapp-play.svg)](https://github.com/rpotter12/whatsapp-play/blob/master/README.md)

***If you like the project, support us by star***
