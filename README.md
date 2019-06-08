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
usage: wplay [-h] (-wc | -wb | -wt) NAME

WhatApp-play

positional arguments:
  NAME           contact name of the target

optional arguments:
  -h, --help     show this help message and exit
  -wc, --wchat   chatting from command line
  -wb, --wblast  message blast to a person
  -wt, --wtrack  track online status of person
```
Example - `wplay -wt "target_name_of_your_whatsapp_contact"`

## Things to do
- [x] onlinetracker script - to track the online/offline status.
- [ ] wchat script - to chat with contact from command line.
- [ ] messageblast script - to send message repeatedly to a person.
- [x] argument parser to connect all scripts to one script.
- [ ] telegram bot script for onlinetracker to send the status online/offline status to telegram bot. 
- [x] improve onlinetracker script.
- [ ] improve messageblast script.
- [ ] improve wchat script for chatting.
- [ ] telegram bot script for onlinetracker script to send the online status on telegram.
- [ ] a sound notification in pc system when the person gets online.<br>
(If you have any new idea for this software, please open issue for that :) )

## Disclaimer
This software is for educational purpose only. Keeping eye on a innocent person can make person's life stressful.

## License
MIT license