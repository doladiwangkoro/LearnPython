import csv

result = {'node1':{'voltage':[1,2,3],'lambda':[4,5,6],'power':[7,8,9]},
'node2':{'voltage':[10,11,12],'lambda':[13,14,15],'power':[16,17,18]}}

data_header_1 = list(result.keys())

data_header_2 = []
for key_1 in data_header_1:
	data_header_2.append(list(result[key_1].keys()))

data_header = []
for key_2 in range(len(data_header_2[0])):
	for key_3 in range(len(data_header_2)):
		data_header.append(data_header_2[key_3][key_2]+data_header_1[key_3][4])

data_fill = []
for key_6 in range(3):
	data_fill_row = []
	for key_4 in range(len(data_header_2[0])):
		for key_5 in range(len(data_header_2)):
			data_fill_row.append(result[data_header_1[key_5]][data_header_2[key_5][key_4]][key_6])
	data_fill.append(data_fill_row)


print(data_header_1)
print(data_header_2)
print(data_header)
print(data_fill_row)
print(data_fill)

print(result)

with open('test.csv','w',newline='') as fp:
	a = csv.writer(fp,delimiter=',')
	data = [data_header]
	for key_data in range(3):
		data.append(data_fill[key_data])
	a.writerows(data)
