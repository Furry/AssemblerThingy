com_count = 0
assem_code = []

des_file = input("what file do you want to load?\n")
cur_file = open(des_file, "r")

for line in cur_file:
	values = line.split()
	if len(values) == 0:
		com_count += 1
	elif values[0] == "//":
		com_count += 1
	else:
		assem_code.append(values[0])
		
for i in assem_code:
	print(i)