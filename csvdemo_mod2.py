import csv

it = 3

result = {'node1':{'voltage':[1,2,3],'lambda':[4,5,6],'power':[7,8,9],'myu':{'myu12':[19,20,21]},'current':{'current12':[25,26,27]}},
'node2':{'voltage':[10,11,12],'lambda':[13,14,15],'power':[16,17,18],'myu':{'myu21':[22,23,24],'myu23':[31,32,33]},'current':{'current21':[28,29,30],'current23':[34,35,36]}}}

data_header_1 = list(result.keys())

data_header_2 = []
for key_1 in data_header_1:
    data_header_2.append(list(result[key_1].keys()))

data_header_3 = {}
for key_8 in range(len(data_header_1)):
    for key_7 in data_header_2[0]:
        if type(result[data_header_1[key_8]][key_7]) == list:
            continue
        else:
            try:
                data_header_3[key_7].append(list(result[data_header_1[key_8]][key_7].keys()))
            except:
                data_header_3[key_7] = [list(result[data_header_1[key_8]][key_7].keys())]
	

data_header = []
for key_2 in range(len(data_header_2[0])): 
    for key_3 in range(len(data_header_2)):
        if type(result[data_header_1[key_3]][data_header_2[key_3][key_2]]) == list:
            data_header.append(data_header_2[key_3][key_2]+data_header_1[key_3][4])
        else:
            for key_9 in range(len(data_header_3[data_header_2[key_3][key_2]][key_3])): #len = 2, key_9 = 0,1
                data_header.append(data_header_3[data_header_2[key_3][key_2]][key_3][key_9])
            
data_fill = []
for key_6 in range(it):
    data_fill_row = []
    for key_4 in range(len(data_header_2[0])):
        for key_5 in range(len(data_header_2)):
            if type(result[data_header_1[key_5]][data_header_2[key_5][key_4]]) == list:
                data_fill_row.append(result[data_header_1[key_5]][data_header_2[key_5][key_4]][key_6])
            else:
                for key_10 in range(len(data_header_3[data_header_2[key_5][key_4]][key_5])):
                    data_fill_row.append(result[data_header_1[key_5]][data_header_2[key_5][key_4]][data_header_3[data_header_2[key_5][key_4]][key_5][key_10]][key_6])
    data_fill.append(data_fill_row)

print(data_header)
print(data_fill)


print('This is result: ',result)

with open('test_2.csv','w',newline='') as fp:
	a = csv.writer(fp,delimiter=',')
	data = [data_header]
	for key_data in range(it):
		data.append(data_fill[key_data])
	a.writerows(data)