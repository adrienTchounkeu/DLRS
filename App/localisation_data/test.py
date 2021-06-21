import csv, random

with open('worldcitiespop.csv', errors='ignore') as csvfile:
    readCSV = list(csv.reader(csvfile, delimiter=','))
    localite = [i for i in range(len(readCSV)) if i > 0]
    random.shuffle(localite)
    localite = localite[:2000]
    final_list = [(readCSV[el][1], readCSV[el][5], readCSV[el][6]) for el in localite]

print(final_list)

with open('opportunities.csv', 'w') as csvWrite:
    writer = csv.writer(csvWrite, skipinitialspace=True)
    writer.writerows(final_list)