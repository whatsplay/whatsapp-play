# region IMPORTS
from wplay.utils import browser_config
from wplay.utils import target_search
from wplay.utils import target_select
import phonenumbers
from phonenumbers import carrier
from phonenumbers import geocoder
from phonenumbers import timezone
import re
import sys
from pathlib import Path
from wplay.utils.Logger import Logger
# end IMPORTS


# region LOGGER
__logger = Logger(Path(__file__).name)
# endregion


def formatNumber(InputNumber):
    return re.sub(r"(?:\+)?(?:[^[0-9]*)", "", InputNumber)


def localScan(InputNumber, print_results=True):
    print("Running local scan...")

    FormattedPhoneNumber = "+" + formatNumber(InputNumber)

    try:
        PhoneNumberObject = phonenumbers.parse(FormattedPhoneNumber, None)
    except Exception as e:
        print(e)
    else:
        if not phonenumbers.is_valid_number(PhoneNumberObject):
            return False

        number = phonenumbers.format_number(PhoneNumberObject, phonenumbers.PhoneNumberFormat.E164).replace("+", "")
        numberCountryCode = phonenumbers.format_number(PhoneNumberObject, phonenumbers.PhoneNumberFormat.INTERNATIONAL).split(" ")[0]
        numberCountry = phonenumbers.region_code_for_country_code(int(numberCountryCode))

        localNumber = phonenumbers.format_number(PhoneNumberObject, phonenumbers.PhoneNumberFormat.E164).replace(numberCountryCode, "")
        internationalNumber = phonenumbers.format_number(PhoneNumberObject, phonenumbers.PhoneNumberFormat.INTERNATIONAL)

        country = geocoder.country_name_for_number(PhoneNumberObject, "en")
        location = geocoder.description_for_number(PhoneNumberObject, "en")
        carrierName = carrier.name_for_number(PhoneNumberObject, "en")

        if print_results:
            print("International format: {}".format(internationalNumber))
            print("Local format: {}".format(localNumber))
            print("Country found: {} ({})".format(country, numberCountryCode))
            print("City/Area: {}".format(location))
            print("Carrier: {}".format(carrierName))
            for timezoneResult in timezone.time_zones_for_number(PhoneNumberObject):
                print("Timezone: {}".format(timezoneResult))

            if phonenumbers.is_possible_number(PhoneNumberObject):
                print("The number is valid and possible.")
            else:
                print("The number is valid but might not be possible.")

    numberObj = {}
    numberObj["input"] = InputNumber
    numberObj["default"] = number
    numberObj["local"] = localNumber
    numberObj["international"] = internationalNumber
    numberObj["country"] = country
    numberObj["countryCode"] = numberCountryCode
    numberObj["countryIsoCode"] = numberCountry
    numberObj["location"] = location
    numberObj["carrier"] = carrierName

    return numberObj


def scanNumber(InputNumber):
    print("[!] ---- Fetching informations for {} ---- [!]".format(formatNumber(InputNumber)))
    number = localScan(InputNumber)

    if not number:
        print(("Error: number {} is not valid. Skipping.".format(formatNumber(InputNumber))))
        sys.exit()

    print("Scan finished.")


def target_contact_number(num):
    target_contact_number.phone_number = num


async def target_info(target):
    page, _ = await browser_config.configure_browser_and_load_whatsapp()

    if target is not None:
        try:
            await target_search.search_and_select_target(page, target)
        except Exception as e:
            print(e)
            await page.reload()
            await target_search.search_and_select_target_without_new_chat_button(page, target)
    else:
        await target_select.manual_select_target(page)
    """
    # to find location by ip address
    print('Get you ipinfo token from https://ipinfo.io/account')
    ip_address = '*'
    token = str(input("Enter your ipinfo token: "))
    ip_string = 'curl ipinfo.io/'+ip_address+'?token='+token+''
    os.system(ip_string)
    """
    __logger.info("Writing target's information")
    scanNumber(target_contact_number.phone_number)
