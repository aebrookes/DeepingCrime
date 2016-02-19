#to do
#currently ignoring where crime categories don't match up with https://www.police.uk/about-this-site/faqs/#what-do-the-crime-categories-mean

import csv
import fnmatch
import os



matches = []
for root, dirnames, filenames in os.walk('Dec2010-Dec2015'):
    for filename in fnmatch.filter(filenames, '*csv'):
        matches.append(os.path.join(root, filename))

print(len(matches))

deepingcrime = []
deepingcrime_list = []

crime_cats_dict = {}



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

deepingcrime_dict = {
    'Anti-social behaviour':0,
    'Bicycle theft':0,
    'Burglary':0,
    'Criminal damage and arson':0,
    'Drugs':0,
    'Other crime':0,
    'Other theft':0,
    'Possession of weapons':0,
    'Public disorder and weapons':0,
    'Public order':0,
    'Robbery':0,
    'Shoplifting':0,
    'Theft from the person':0,
    'Vehicle crime':0,
    'Violence and sexual offences':0
    }

f = open("crimeresults.csv", "w")
f.write("Month,")
for key in deepingcrime_dict:
    f.write("%s," % key)

for match in matches:

    #reset for each new CSV file, i.e. month
    deepingcrime_dict = deepingcrime_dict.fromkeys(deepingcrime_dict, 0)

    print("csv file: ",match)
    with open(match) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['LSOA code'] in LSOA_codes:
               # print(row['Month'],row['LSOA name'])
                deepingcrime.append(row['Month'])

                #ignores if Crime type not as per https://www.police.uk/about-this-site/faqs/#what-do-the-crime-categories-mean
                if row['Crime type'] in deepingcrime_dict:
                    deepingcrime_dict[row['Crime type']] += 1
                elif row['Crime type']=="Violent crime":
                    # To handle renaming of category from 'Violent crime' in June 2013, see https://data.police.uk/changelog/
                    deepingcrime_dict['Violence and sexual offences'] += 1
                else:
                    print("Crime type not in list of crime categories: ",row['Crime type'])

        f.write("\n%s," % row['Month'])
        for key in deepingcrime_dict:
            f.write("%s," % deepingcrime_dict[key]) # write all the crime counts, comma separated

   # print(deepingcrime_dict)


f.close()
d = {x:deepingcrime.count(x) for x in deepingcrime}
bins, freq = list(d.keys()), list(d.values())
#print(bins)
#print(freq)

#print(deepingcrime)

f = open("results.csv", "w")

for i in range(len(bins)):
    f.write("{},{}\n".format(bins[i], freq[i]))

f.close()