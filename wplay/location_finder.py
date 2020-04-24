# region IMPORTS
import phonenumbers
from phonenumbers import carrier
from phonenumbers import geocoder
from phonenumbers import timezone
import re
import requests
import json
import sys
from pathlib import Path
from wplay.utils.Logger import Logger
#end IMPORTS

# region LOGGER
__logger = Logger(Path(__file__).name)
# endregion

code_info = '[*] '
code_warning = '(!) '
code_result = '[+] '
code_error = '[!] '
code_title = ''

number = '' # Full number format
localNumber = '' # Local number format
internationalNumber = '' # International numberformat
numberCountryCode = '' # Dial code; e.g:"+33"
numberCountry = '' # Country; e.g:France

def formatNumber(InputNumber):
    return re.sub("(?:\+)?(?:[^[0-9]*)", "", InputNumber)

def localScan(InputNumber):
    global number
    global localNumber
    global internationalNumber
    global numberCountryCode
    global numberCountry

    print(code_info + 'Running local scan...')
    FormattedPhoneNumber = "+" + formatNumber(InputNumber)
    PhoneNumberObject = phonenumbers.parse(FormattedPhoneNumber, None)

    if not phonenumbers.is_valid_number(PhoneNumberObject):
        return False

    number = phonenumbers.format_number(PhoneNumberObject, phonenumbers.PhoneNumberFormat.E164).replace('+', '')
    numberCountryCode = phonenumbers.format_number(PhoneNumberObject, phonenumbers.PhoneNumberFormat.INTERNATIONAL).split(' ')[0]

    countryRequest = json.loads(requests.request('GET', 'https://restcountries.eu/rest/v2/callingcode/{}'.format(numberCountryCode.replace('+', ''))).content)
    numberCountry = countryRequest[0]['alpha2Code']

    localNumber = phonenumbers.format_number(PhoneNumberObject, phonenumbers.PhoneNumberFormat.E164).replace(numberCountryCode, '')
    internationalNumber = phonenumbers.format_number(PhoneNumberObject, phonenumbers.PhoneNumberFormat.INTERNATIONAL)

    print(code_result + 'International format: {}'.format(internationalNumber))
    print(code_result + 'Local format: 0{}'.format(localNumber))
    print(code_result + 'Country code: {}'.format(numberCountryCode))
    print(code_result + 'Location: {}'.format(geocoder.description_for_number(PhoneNumberObject, "en")))
    print(code_result + 'Carrier: {}'.format(carrier.name_for_number(PhoneNumberObject, 'en')))
    print(code_result + 'Area: {}'.format(geocoder.description_for_number(PhoneNumberObject, 'en')))
    for timezoneResult in timezone.time_zones_for_number(PhoneNumberObject):
        print(code_result + 'Timezone: {}'.format(timezoneResult))

    if phonenumbers.is_possible_number(PhoneNumberObject):
        print(code_info + 'The number is valid and possible.')
    else:
        print(code_warning + 'The number is valid but might not be possible.')



def scanNumber(InputNumber):
    print(code_title + "[!] ---- Fetching informations for {} ---- [!]".format(formatNumber(InputNumber)))

    localScan(InputNumber)

    global number
    global localNumber
    global internationalNumber
    global numberCountryCode
    global numberCountry

    if not number:
        print((code_error + "Error: number {} is not valid. Skipping.".format(formatNumber(InputNumber))))
        sys.exit()

    print("Scan finished.")



async def location_finder():
    __logger.info("Broadcast message.")
    number=input("Enter full number with country code.")
    scanNumber(number)
    """
    # to find location by ip address
    print('Get you ipinfo token from https://ipinfo.io/account')
    ip_address = '*'
    token = str(input("Enter your ipinfo token: "))
    ip_string = 'curl ipinfo.io/'+ip_address+'?token='+token+''
    os.system(ip_string)
    """
