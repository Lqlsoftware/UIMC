# coding:utf-8
# data pre-process
import collections
import csv
import hashlib
import sys

import time
import pickle
from operator import itemgetter

FIELDS = ['user_id', 'photo_id', 'time', 'duration_time']

NEW_FIELDS = FIELDS + ['user_id_count', 'photo_id_count', 'user_time_count']

NR_BINS = 100000


def hash_str(string):
	return str(int(hashlib.md5(string.encode('utf8')).hexdigest(), 16) % (NR_BINS - 1) + 1)


start = time.time()

# 额外的field 统计用户id出现的次数、视频id出现的次数、用户每个时间交互的次数
user_id_count = collections.defaultdict(int)
photo_id_count = collections.defaultdict(int)
user_time_count = collections.defaultdict(int)
user_id_photo_id = {}
click_count = collections.defaultdict(int)
click_history1 = collections.defaultdict(str)
click_history2 = collections.defaultdict(str)
click_history3 = collections.defaultdict(str)
click_history4 = collections.defaultdict(str)
click_history5 = collections.defaultdict(str)
click_history6 = collections.defaultdict(str)
click_history7 = collections.defaultdict(str)
temp_history = collections.defaultdict(str)
photo_text = {}
photo_face = {}

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

def scan(path):
	templist = []
	last_user_id = 0
	for i, row in enumerate(csv.DictReader(open(path)), start=1):
		# 日志 防止处理的时候感觉卡死了。。。
		if i % 1000000 == 0:
			sys.stderr.write('{0:6.0f}    {1}m\n'.format(time.time() - start, int(i / 1000000)))

		user_id = row['user_id']
		user_id_count[user_id] += 1
		photo_id_count[row['photo_id']] += 1
		user_time_count[user_id + '-' + row['time']] += 1
		# if not user_id in user_id_photo_id:
		# 	user_id_photo_id[user_id] = []
		# user_id_photo_id[user_id].append(row['photo_id'])
	        #若是第一行，令last_user_id和user_id相等
        if i == 1:
			last_user_id = row['user_id']

        #若该行数据与上一行是同一个用户，将user_id,time,click加入templist列表
        if user_id == last_user_id:
			date1 = int(row['time'])- 759600000000
			date2 = time.strftime("%Y%m%d",time.localtime(date1))
			templist.append((row['user_id'],date2,int(row['click'])))
        #若不是同一用户，处理上一个用户的click_history,处理完毕后清空templist列表,继续处理下一个用户数据
        else:
			after_sorted = sorted(templist, key=itemgetter(1),reverse=True)
			click_history(after_sorted,user_id)
			templist = []
        last_user_id = user_id
	# user_id_count
	user_id_count_sorted = sorted(user_id_count.items(), key=lambda e: e[1], reverse=True)
	max_count = user_id_count_sorted[len(user_id_count_sorted) / 10]
	for idx in range(0, len(user_id_count_sorted) / 10):
		user_id_count[user_id_count_sorted[idx][0]] = max_count

	# photo_id_count
	photo_id_count_sorted = sorted(photo_id_count.items(), key=lambda e: e[1], reverse=True)
	max_count = photo_id_count_sorted[len(photo_id_count_sorted) / 10]
	for idx in range(0, len(photo_id_count_sorted) / 10):
		photo_id_count[photo_id_count_sorted[idx][0]] = max_count


def click_history(sorted_list,user_id):
#     print(sorted_list)
    #初始化click为0
    click = 0
    for i,record in enumerate(sorted_list,start=0):
        #列表中的第一项，初始化last_date为最近一天日期
        if i == 0:
			last_date = record[1]#上一天日期
			first_date = record[1]#倒数第一天日期
			#日期计数，列表中第一项日期为第一天
			date_count = 1
        #更新date日期
        date = record[1]
        #计算两日期差值
        date1=datetime.datetime.strptime(first_date,"%Y%m%d")
        date2=datetime.datetime.strptime(date,"%Y%m%d")
        date_diff = (date1-date2).days
        #当列表中两条数据日期一样时(目的在于查看用户该日期是否点击过短视频，每日记录有多条，一条为1即为1)
        if date == last_date:
			#若click=0，什么都不做，若click=1,更新click信息
			if record[2] == 0:
			    pass
			else:
			    click = 1
        #当列表中两条数据日期不一样时,首先处理click_history（上一天的）,然后处理当天的click
        else:
			temp_history[user_id] += str(click)
			if date_count == 1:
			    click_history1[user_id] = temp_history[user_id]
			    click_history7[user_id] =click_history6[user_id] =click_history5[user_id] = click_history4[user_id] =click_history3[user_id] = click_history2[user_id] =click_history1[user_id]
			elif date_diff == 2:
			    click_history2[user_id] = temp_history[user_id]
			    click_history7[user_id] =click_history6[user_id] =click_history5[user_id] = click_history4[user_id] =click_history3[user_id] = click_history2[user_id]
			elif date_diff == 3:
			    click_history3[user_id] = temp_history[user_id]
			    click_history7[user_id] =click_history6[user_id] =click_history5[user_id] = click_history4[user_id] =click_history3[user_id]
			elif date_diff == 4:
			    click_history4[user_id] = temp_history[user_id]
			    click_history7[user_id] =click_history6[user_id] =click_history5[user_id] = click_history4[user_id]
			elif date_diff == 5:
			    click_history5[user_id] = temp_history[user_id]    
			    click_history7[user_id] =click_history6[user_id] =click_history5[user_id] 
			elif date_diff == 6:
			    click_history6[user_id] = temp_history[user_id]    
			    click_history7[user_id] =click_history6[user_id]  
			elif date_diff == 7:
			    click_history7[user_id] = temp_history[user_id]      
			else:
			    break     
			click_count[user_id] = click_history7[user_id].count('1')
			date_count += 1 
			if record[2] == 0:
			    click = 0
			else:
			    click = 1
        last_date = date


def scanText(path):
	with open(path, 'r') as f:
		global photo_text
		photo_text = pickle.load(f)


def scanFace(path):
	with open(path, 'r') as f:
		global photo_face
		photo_face = pickle.load(f)


def write(src_path, dst_path):
	with open(dst_path, 'w+') as f:
		for i, row in enumerate(csv.DictReader(open(src_path)), start=1):
			if i % 1000000 == 0:
				sys.stderr.write('write: {0:6.0f}\t{1}m\n'.format(time.time() - start, int(i / 1000000)))
			row_to_write = []
			field = 0
			# dataset field
			for feat in FIELDS:
				if feat == 'time':
					row_to_write.append(":".join([str(field), hash_str('time-' + getTime(row[feat])), '1']))
				else:
					row_to_write.append(":".join([str(field), hash_str(feat + '-' + row[feat]), '1']))
				field += 1

			# addition field
			user_id = row['user_id']
			photo_id = row['photo_id']
			# row_to_write.append(":".join([str(field), hash_str('bag_photo_id-' + ','.join(user_id_photo_id[user_id])), '1']))
			# field += 1
			row_to_write.append(
				":".join([str(field), hash_str('user_id_count-' + str(user_id_count[user_id])), '1']))
			field += 1
			row_to_write.append(
				":".join([str(field), hash_str('photo_id_count-' + str(photo_id_count[photo_id])), '1']))
			field += 1
			row_to_write.append(
				":".join(
					[str(field), hash_str('user_time_count-' + str(user_time_count[user_id + '-' + row['time']])),
					 '1']))
			# field += 1
			# if photo_id in photo_face:
			# 	field_str = str(field)
			# 	for face in photo_face[photo_id]:
			# 		row_to_write.append(":".join([field_str, face, '1']))
			field += 1
			row_to_write.append(":".join([str(field), hash_str('user_id-' + 'click_history1-' + click_history1[user_id]), '1']))
			field += 1
			row_to_write.append(":".join([str(field), hash_str('user_id-' + 'click_history2-' + click_history2[user_id]), '1']))
			field += 1
			row_to_write.append(":".join([str(field), hash_str('user_id-' + 'click_history3-' + click_history3[user_id]), '1']))
			field += 1
			row_to_write.append(":".join([str(field), hash_str('user_id-' + 'click_history4-' + click_history4[user_id]), '1']))
			field += 1
			row_to_write.append(":".join([str(field), hash_str('user_id-' + 'click_history5-' + click_history5[user_id]), '1']))
			field += 1
			row_to_write.append(":".join([str(field), hash_str('user_id-' + 'click_history6-' + click_history6[user_id]), '1']))
			field += 1
			row_to_write.append(":".join([str(field), hash_str('user_id-' + 'click_history7-' + click_history7[user_id]), '1']))
			field += 1
			row_to_write.append(":".join([str(field), hash_str('user_id-' + 'click_count-' + str(click_count[user_id])), '1']))
			field += 1
			field_str = str(field)
			for text in photo_text[photo_id]:
				row_to_write.append(
					":".join(
						[field_str, text, '1']))
			# write a row
			row_to_write = " ".join(row_to_write)
			f.write(row_to_write + '\n')


if __name__ == "__main__":
	# 假设数据集是个csv文件 (我会完成到csv的转换代码)
	scan('Data/test_interaction.csv')
	scanText('Data/test_text.pkl')
	# scanFace('Data/test_face.pkl')
	write('Data/test_interaction.csv', sys.argv[1])
