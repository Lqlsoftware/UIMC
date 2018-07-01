# coding:utf-8
# data pre-process
import collections
import csv
import hashlib
import sys
import time
import pickle

FIELDS = ['user_id', 'photo_id', 'time', 'duration_time']

NEW_FIELDS = FIELDS + ['user_id_count', 'photo_id_count', 'user_time_count']

NR_BINS = 1000000


def hash_str(string):
	return str(int(hashlib.md5(string.encode('utf8')).hexdigest(), 16) % (NR_BINS - 1) + 1)


start = time.time()

# 额外的field 统计用户id出现的次数、视频id出现的次数、用户每个时间交互的次数
user_id_count = collections.defaultdict(int)
photo_id_count = collections.defaultdict(int)
user_time_count = collections.defaultdict(int)
photo_text = {}
photo_face = {}


def scan(path):
	for i, row in enumerate(csv.DictReader(open(path)), start=1):
		# 日志 防止处理的时候感觉卡死了。。。
		if i % 1000000 == 0:
			sys.stderr.write('{0:6.0f}    {1}m\n'.format(time.time() - start, int(i / 1000000)))

		user_id = row['user_id']
		user_id_count[user_id] += 1
		photo_id_count[row['photo_id']] += 1
		user_time_count[user_id + '-' + row['time']] += 1


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
				items = str(row[feat]).split(' ')
				for item in items:
					# feat_index1:1  feat_index2:1 ...
					row_to_write.append(":".join([str(field), hash_str(feat + '-' + item), '1']))
				field += 1

			# addition field
			user_id = row['user_id']
			photo_id = row['photo_id']
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
			field += 1
			if photo_id in photo_face:
				field_str = str(field)
				for face in photo_face[photo_id]:
					row_to_write.append(":".join([field_str, face, '1']))
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
	scanFace('Data/test_face.pkl')
	write('Data/test_interaction.csv', sys.argv[1])
