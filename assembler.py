import json

dict_file = open("dicts.json")
dicts = json.load(dict_file)

assem_file = open("Pong.asm", "r")


# To track what memory addresses we can use
memLocation = 16

assem_code = [ ]
binary_code = [ ]

# A pre-defined list of addresses
# This is also mutated as new variable names are written here.
addresses = {
    "SCREEN": 16384,
    "KBD": 24576
}

def handleInstructionA(line):
    # Parse out the actual name of a given command
    if line.startswith("@"): line = line[1:]

    if line in addresses.keys():
        # If the value already exists in the address table,
        # Give it the stored value.
        res = "{0:b}".format(addresses[line])
    elif line.isdigit():
        # If it's a number, set directly to it.
        res = "{0:b}".format(int(line))
    else:
        # If it's a unique 'variable name',
        # Give it a mem value of the closest possible location, and save it
        # to 'addresses'

        global memLocation
        addresses[line] = memLocation
        res = "{0:b}".format(memLocation)
        memLocation += 1
    #END

    # Return the binary, and pad it up to 16 characters with 0s
    return "0" * (16 - len(res)) + res
#END

def handleInstructionC(line):
    # Split on all instances of =
    eqsplit = line.split("=")
    # Split on all instances of ;
    cjsplit = line.split(";")

    # Construct an array of dest, comp, and jump values
    # Depending on if it split on = or split on ;
    if len(eqsplit) == 2:
        item = [eqsplit[0], eqsplit[1], "null"]
    else:
        item = ["null", cjsplit[0], cjsplit[1]]
    #END

    destpre, comppre, jumppre = item

    dest = dicts["dest"][destpre]
    comp = dicts["comp"][comppre]
    jump = dicts["jump"][jumppre]

    # Concatinate the value from each dict into one string, prefixed with the signature '111' for C instructions
    res = "111" + "".join([str(int) for int in comp]) + "".join([str(int) for int in dest]) + "".join([str(int) for int in jump])

    return res
#END

# Write each valid line to the 'assem_code' array
for line in assem_file:
    # Strip all whitespace
    stripped = line.strip()

    # Parse out comments
    if not stripped.startswith("//") and stripped:
        assem_code.append(line.strip())
    #END
#END

# This line is bc of u, ferris.
map(lambda x: "//".split(x)[0], assem_code)


# Create a cache of the modified assembly code with tags removed
tmp_cache = []
lineCounter = 0
for (index, line) in enumerate(assem_code):
    # If a tag is seen, remove it, and assign it a new memory address for the current line
    if line.startswith("("):
        name = line[1:-1]
        addresses[name] = lineCounter
    else:
        # If there's no tag, increment the lines by one
        lineCounter += 1
        tmp_cache.append(line)
    #END
#END
# Apply the filtered code to our main assembly code
assem_code = tmp_cache


for (index, line) in enumerate(assem_code):
    if line.startswith("@"):
        binary_code.append(handleInstructionA(line))
    else:
        binary_code.append(handleInstructionC(line))
    #END
#END

newFile = open("res.hack", "w")

# Write each line of binary code
for line in binary_code:
    newFile.write(line + "\n")
newFile.close() # Close the file like a good boy uwu