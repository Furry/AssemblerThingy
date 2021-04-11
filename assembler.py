import json

dict_file = open("dicts.json")
dicts = json.load(dict_file)

des_file = input("What file do you want to load?\n>")
blank_list = des_file.split(".")
# gets name of the file
name_file = blank_list[0]

assem_file = open(des_file, "r")

errorStatus = False
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
    line = line[1:]

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

# Debugger to stop the assembler if there is a syntax error
# and return what line the error was on.
# Guys this debugger is pretty poggers amirite

def debugger(lineInput, instType, index):
    error = False # Sets the default error state to false.
    errorType = "none" # Defaults the error type to none.
    # If the instruction is an a instruction
    if instType == "a": 
        atCount = 0
        for i in lineInput:
            if i == "@":
                atCount = atCount + 1
            if atCount > 1:
                error = True
                errorType = "atCountExceeds1"
    # If the instruction is a c instruction
    else: 
        # Sets the counter for how many = and ; there are to 0.
        chCount = 0
        # Check to see if multiple equals or semicolons exist.
        for i in lineInput:
            if i == "=":
                chCount = chCount + 1
            elif i == ";":
                chCount = chCount + 1
        if chCount > 1: # If there is more than one = or ;, set an error.
            error = True
            errorType = "separatorLimitReached"
            
        eqsplit = lineInput.split("=")
        cjsplit = lineInput.split(";")
        
        # Checks if equation or comp jump instruction.
        if len(eqsplit) == 2: 
            # Checks if the first part of the equation is a valid instruction.
            if not(eqsplit[0] in dicts["comp"].keys()) and not(eqsplit[0] in dicts["dest"].keys()):
                error = True
                errorType = "invalidInstruction"
            # Checks if the second part of the equation is a valid instruction.    
            if not(eqsplit[1] in dicts["comp"].keys()) and not(eqsplit[1] in dicts["dest"].keys()):
                error = True
                errorType = "invalidInstruction"     
        elif len(cjsplit) == 2:
            # Checks if the first part of the jump instruction is valid.
            if not(cjsplit[0] in dicts["jumpprefix"]):
                error = True
                errorType = "invalidJumpPrefix"
            # Checks if the second part of the jump instruction is valid.
            if not(cjsplit[1] in dicts["jump"].keys()):
                error = True
                errorType = "invalidJumpInstruction"
                
        else: # If the C instruction is incomplete.
            # Checks if the incomplete instruction is part of a valid instruction and sets the error accordingly.
            if chCount == 0 and not(eqsplit[0] in dicts["comp"].keys()) and not(eqsplit[0] in dicts["dest"].keys()):
                error = True
                errorType = "invalidInstruction"
            elif chCount == 0:
                error = True
                errorType = "incompleteInstruction"
                
    if error == False:
        return True
    else:
        print("OOPSIE WOOPSIE!!")
        print("----------------")
        print("It looks like you made a freaky deaky...")
        print("Error " + errorType + " @ Line: " +str(index+1))
        print(">>> "+lineInput)
        return False

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
map(lambda x: "//".split(x)[0], assem_code) # hehe shush 


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
        # Runs the debugger function. If there are no errors, proceed.
        if debugger(line, "a", index):
            binary_code.append(handleInstructionA(line))
        else:
            errorStatus = True
            break
    else:
        if debugger(line, "c", index):
            binary_code.append(handleInstructionC(line))
        else:
            errorStatus = True
            break
    #END
#END

filename = name_file + ".hack"
newFile = open(filename, "w")

# Write each line of binary code
for line in binary_code:
    newFile.write(line + "\n")
    
if errorStatus is False:
    print("Done! Wrote "+str(index+1)+" lines into " + filename)

newFile.close() # Close the file like a good boy uwu
