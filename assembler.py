com_count = 0

# To store it during iteration
assem_cache = []

# To store the code paired with each line
assem_code = {}

# AAAA dest and jump dictionaries
dest = {
    "null": [0, 0, 0],
    "M": [0, 0, 1],
    "D": [0,  1,  0],
    "MD": [0, 1, 1],
    "A": [1, 0 , 0],
    "AM": [1, 0, 1],
    "AD": [1, 1, 0],
    "AMD": [1, 1, 1]
}

jump = {
    "null": [0, 0, 0],
    "JGT": [0, 0, 1],
    "JEQ": [0, 1, 0],
    "JGE": [0, 1, 1],
    "JLT": [1, 0, 0],
    "JNE": [1, 0, 1],
    "JLE": [1, 1, 0],
    "JMP": [1, 1, 1]
}

# comp dict
comp = {
    "0": [1, 0, 1, 0, 1, 0],
    "1": [1, 1, 1, 1, 1, 1],
    "-1": [1, 1, 1, 0, 1, 0],
    "D": [0, 0, 1, 1, 0, 0],
    "A": [1, 1, 0, 0, 0, 0],
    "!D": [0, 0, 1, 1, 0, 1],
    "!A": [1, 1, 0, 0, 0, 1],
    "-D": [0, 0, 1, 1, 1, 1],
    "-A": [1, 1, 0, 0, 1, 1],
    "D+1": [0, 1, 1, 1, 1, 1],
    "A+1": [1, 1, 0, 1, 1, 1],
    "D-1": [0, 0, 1, 1, 1, 0],
    "A-1": [1, 1, 0, 0, 1, 0],
    "D+A": [0, 0, 0, 0, 1, 0],
    "D-A": [0, 1, 0, 0, 1, 1],
    "A-D": [0, 0, 0, 1, 1, 1],
    "D&A": [0, 0, 0, 0, 0, 0],
    "D|A": [0, 1, 0, 1, 0, 1]
}

des_file = input("what file do you want to load?\n")
# des_file = "Mult.asm"

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
        assem_cache.append(values[0])
    #END
#END

# Filters out inline commnets by splitting each line by // and only taking the first element.
map(lambda x: "//".split(x)[0], assem_cache)

# Assign each line it's own entry in an array, with the key as it's index in the array previously.
index = 0
for line in assem_cache:
    index += 1
    assem_code[index] = line
#END

# ! START OF ASSEMBLER

for key in assem_code.keys():
    elem = assem_code[key] # The current item in iteration

    if elem.startswith("@"): # Handle A address
        aVal = elem[1:]
        if aVal.isdigit():
            aValBinary = "{0:b}".format(int(aVal))
            assem_code[key] = "0" * (16 - len(aValBinary)) + aValBinary
        else:
            aValBinary = "{0:b}".format(key)
            assem_code[key] = "0" * (16 - len(aValBinary)) + aValBinary
        #END
    #END

    

# Write to a file
# print(assem_code)

assem_list = []
for key in assem_code:
    assem_list.append(assem_code[key])
    # move to a list ! exciting

assem_file = open("assem_code.txt", "w")
# open / create file, then write to that file
assem_file.write("\n".join(assem_list))
assem_file.close()
