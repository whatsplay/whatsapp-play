# whatsapp-play
It is command line software through which you can play with your WhatsApp. It is having different options to play with your WhatsApp like message blast, online tracking, whatsapp chat.. This software aims to provide all facilities which we can do with WhatsApp. 

***wchat*** stands for WhatsApp chat. Through this you can chat with your WhatsApp contact directly from the command line.

***onlinetracker*** tracks the online and offline timings of your WhatsApp contact. It will check the online status and will immediately stores that data into a .txt file.

***messageblast*** is a message bomb script. It sends messages to your WhatsApp contact continously. The number of messages is decided by you. You can blast infinite number of messages to your WhatsApp contact.

---

## Installation
- `pip3 install wplay`

## Usage
```
usage: wplay [-h] (-wc WCHAT | -wb WBLAST | -wt WTRACK)

WhatApp-play

optional arguments:
  -h, --help            show this help message and exit
  -wc WCHAT, --wchat WCHAT
                        chatting from command line
  -wb WBLAST, --wblast WBLAST
                        message blast to a person
  -wt WTRACK, --wtrack WTRACK
                        track online status of person

```
Example - `wplay -wt "target_name_of_your_whatsapp_contact"`

## Things to do
- [x] argument parser to connect all scripts to one script.
- [ ] telegram bot script for onlinetracker to send the status online/offline status to telegram bot. 
- [ ] improve wchat script for chatting.<br>
(If you have any new idea for this software, please open issue for that :) )

## Disclaimer
This software is for educational purpose only.

## License
MIT license