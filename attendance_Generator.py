import csv

def convert():
    with open('a.csv','r') as in_file, open('b.csv','w') as out_file:
        seen = set() # set for fast O(1) amortized lookup
        for line in in_file:
            if line in seen: continue # skip duplicate
            seen.add(line)
            out_file.write(line)

if __name__ == '__main__':
    convert()