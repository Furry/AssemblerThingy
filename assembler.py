com_count = 0
assem_code = []

des_file = input("what file do you want to load?\n")
cur_file = open(des_file, "r")

# Iterate over all ines
for line in cur_file:
    # Split by new line
    values = line.split()
    if len(values) == 0:
        com_count += 1
    # RM comment
    elif values[0] == "//":
        com_count += 1
    else:
        assem_code.append(values[0])
map(lambda x: "//".split(x)[0], assem_code)

for i in assem_code:
    print(i)