import os


def locationfinder(name):

	# to find location by ip address
	print('Get you ipinfo token from https://ipinfo.io/account')
	ip_address = '45.248.160.61'
	token = str(input("Enter your ipinfo token: "))
	ip_string = 'curl ipinfo.io/'+ip_address+'?token='+token+''
	os.system(ip_string)