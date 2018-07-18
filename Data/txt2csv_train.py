# coding:utf-8

SRC_FIELDS = ['user_id', 'photo_id', 'click', 'like', 'follow', 'time', 'playing_time', 'duration_time']

DST_FIELDS = ['user_id', 'photo_id', 'click', 'time', 'playing_time', 'duration_time']

with open('train_interaction.txt', 'r') as reader:
	with open('train_interaction.csv', 'w+') as writer:
		# header
		writer.write(",".join(DST_FIELDS) + '\n')
		for _, line in enumerate(reader):
			feature = line.strip('\n').split('\t')
			to_write = [feature[0],feature[1],feature[2], feature[5],  feature[6], feature[7]]
			writer.write(",".join(to_write) + '\n')
