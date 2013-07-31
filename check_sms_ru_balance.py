#!/usr/bin/env python
# check_sms_ru_balance - Plugin for nagios. Check balance in service http://sms.ru 

# Copyright (C) 2009-2013 by Denis Khabarov aka 'Saymon21'
# E-Mail: saymon at hub21 dot ru (saymon@hub21.ru)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3
# as published by the Free Software Foundation.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys, argparse
if sys.version_info[0] > 2:
	print >> sys.stderr, "You are using python version > 2. But this tool supports only 2.x." # TODO Python 3 support.
	sys.exit(3)

from urllib2 import urlopen, URLError
from socket import error as SocketErrorException

cliparser = argparse.ArgumentParser(description='Plugin for nagios. Check balance in service http://sms.ru Licence: GNU GPLv3')
cliparser.add_argument("--api-id",dest="api_id", metavar="VALUE", help="API ID",required=True)
cliparser.add_argument("--warning",metavar="VALUE",help="Warning balance",required=True)
cliparser.add_argument("--critical",metavar="VALUE",help="Critical balance",required=True)
cliparser.add_argument("--http_timeout",help="Timeout for http connection",default=10)
cliargs = cliparser.parse_args()


def main():
	try:
		res=urlopen("http://sms.ru/my/balance?api_id="+ cliargs.api_id,timeout=cliargs.http_timeout)
	except (URLError,SocketErrorException) as errstr:
		print(errtstr)
		sys.exit(3)
	service_result=res.read().splitlines()
	if service_result[0] and int(service_result[0]) == 100:		
		if (int(cliargs.critical) >= int(service_result[1].split('.')[0])):
			print("CRITICAL Balance of sms.ru " + service_result[1])
			sys.exit(2)
		elif (int(cliargs.warning) >= int(service_result[1].split('.')[0])):
			print("WARNING Balance of sms.ru " + service_result[1])
			sys.exit(1)
		else:
			print("OK Balance of sms.ru " + service_result[1])
			sys.exit(0)
	elif service_result[0] and int(service_result[0]) != 100:
		print("UNKNOWN Unable to get data when has been received code " + service_result[0])
		sys.exit(3)


if __name__ == "__main__":
	main()
