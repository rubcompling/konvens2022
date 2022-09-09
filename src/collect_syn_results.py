# author: Stefanie Dipper
# read in multiple syntax result files
# and collect results in one file 'data_tmp/syntax/syntax_all.csv'

# usage (call from root dir):
# python3 src/collect_syn_results.py

import sys
from pathlib import Path
import csv, ast

input_dir = "results/3_syntax/test_results/"
out_dir = "results/3_syntax/significance/"
output_file = out_dir + "syntax_all.csv"
import os
os.makedirs(out_dir, exist_ok=True)

source_dir = Path(input_dir)
files = source_dir.iterdir()

# key1: year
# key2: feature
# key3: student_no
# value: score
mydict = dict()

# parallel lists for all columns
years = list()
features = list()
student_no = list()
scores = list()

count = 0

# Ueber Dateien in Verzeichnis iterieren
for file in files:
    filename = Path(file).stem

    # Ab hier kann man jeweils auf 1 Datei zugreifen, z.B. so:
    with open(file, mode="r", encoding="UTF-8") as infile:
        count = 0
        csv_reader = csv.reader(infile, delimiter=',')
        # skip first line
        next(csv_reader)
        for line in csv_reader:
            for (i, elt) in enumerate(line):
                if i in [0, 1]: line[i] = int(line[i])
                if i in [2, 4, 5, 6]: line[i] = float(line[i])
                if i == 3:
                    line[i] = ast.literal_eval(line[i])
                    #for val in line[i]:
                    #    line[i][val] = float(line[i])
                    
            (no, year, avg_year, values, sd, mean_all, sd_all) = line
            for val in values:
                count += 1
                years.append(year)
                features.append(filename)
                student_no.append(count)
                scores.append(val)


# print output
with open(output_file, mode="w") as outfile:
    print("year", "measure", "student", "score",
          sep="\t", file=outfile)
                
    for i in range(len(years)):
        print(years[i],
              features[i],
              student_no[i],
              scores[i],
              sep="\t", file=outfile)
    print(file=outfile)
