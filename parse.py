import csv
import fnmatch
import os



matches = []
for root, dirnames, filenames in os.walk('Dec2010-Dec2015'):
    for filename in fnmatch.filter(filenames, '*csv'):
        matches.append(os.path.join(root, filename))

print(len(matches))

deepingcrime = []

#found using http://www.research-lincs.org.uk/LROPresentationTools/UI/Pages/MappingTool.aspx?dataInstanceID=2006
#compared with https://www.police.uk/lincolnshire/NC47/crime/2015-02/
LSOA_codes = [
'E01026303',
'E01026304',
'E01026305',
'E01026306',
'E01026307',
'E01026334',
'E01026335',
'E01026336',
'E01026337',
'E01026362',
'E01026363',
'E01026364'
]
for match in matches:
    with open(match) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['LSOA code'] in LSOA_codes:
                print(row['Month'],row['LSOA name'])
                deepingcrime.append(row['Month'])

d = {x:deepingcrime.count(x) for x in deepingcrime}
bins, freq = list(d.keys()), list(d.values())
print(bins)
print(freq)

print(deepingcrime)

f = open("results.csv", "w")

for i in range(len(bins)):
    f.write("{},{}\n".format(bins[i], freq[i]))

f.close()