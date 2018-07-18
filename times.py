import csv
import time


#  761124883233 ~ 760994920751
# -759600000000
#    1524883233 ~   1394920751
#     2018-4-28 ~    2014-3-15
# def getTime(timestr):

def getTime(timestr):
	timestemp = int(timestr) - 759600000000
	format_time = time.gmtime(timestemp)
	year = str(format_time.tm_year)
	if len(str(format_time.tm_mon)) == 1:
		month = '0' + str(format_time.tm_mon)
	else:
		month = str(format_time.tm_mon)

	if len(str(format_time.tm_mday)) == 1:
		day = '0' + str(format_time.tm_mday)
	else:
		day = str(format_time.tm_mday)
	return "{:s}/{:s}/{:s}".format(year, month, day)


times = {}
for i, row in enumerate(csv.DictReader(open('Data/train_interaction.csv')), start=1):
	times[getTime(row['time'])] = 1

time_sorted = sorted(times.items(), key=lambda e: e[0])
for key in time_sorted:
	print(key[0])
