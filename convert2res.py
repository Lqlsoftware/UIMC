#!/usr/bin/env python
import csv
import sys

test_dataset = csv.DictReader(open("Data/test_interaction.csv"))
result = enumerate(open(sys.argv[1], 'rb'))
output = open(sys.argv[2], "w+")
row = test_dataset.next()
output.write('{:s}\t{:s}\t{:.6f}'.format(row['user_id'], row['photo_id'], float(result.next()[1])))

for i, row in enumerate(test_dataset, start=1):
    output.write('\n{:s}\t{:s}\t{:.6f}'.format(row['user_id'], row['photo_id'], float(result.next()[1])))