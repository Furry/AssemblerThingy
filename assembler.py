com_count = 0

# To store it during iteration
assem_cache = []

# To store the code paired with each line
assem_code = {}


# des_file = input("what file do you want to load?\n")
des_file = "Mult.asm"

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

map(lambda x: "//".split(x)[0], assem_cache)

# Assign each line it's own entry in an array, with the key as it's index in the array previously.
index = 0
for line in assem_cache:
    index += 1
    assem_code[index] = line
#END

# ! START OF ASSEMBLER

print(assem_code)
