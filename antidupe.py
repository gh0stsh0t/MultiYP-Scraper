filetoopen = raw_input("What to fix? ")
filetooutput = raw_input("What filename? ")

with open(filetoopen+'.csv', 'r') as in_file, open(filetooutput+'.csv', 'w') as out_file:
    seen = set()  # set for fast O(1) amortized lookup
    for line in in_file:
        if line in seen:
            continue  # skip duplicate

        seen.add(line)
        out_file.write(line)
