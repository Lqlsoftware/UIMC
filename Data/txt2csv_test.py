# coding:utf-8

DST_FIELDS = ['user_id', 'photo_id', 'time', 'duration_time']

with open('test_interaction.txt', 'r') as reader:
	with open('test_interaction.csv', 'w+') as writer:
		# header
		writer.write(",".join(DST_FIELDS) + '\n')
		for _, line in enumerate(reader):
			feature = line.strip('\n').split('\t')
			to_write = [feature[0],feature[1],feature[2], feature[-1]]
			writer.write(",".join(to_write) + '\n')
