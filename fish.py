
import csv
import matplotlib.pyplot as plt

with open('tuna.csv', "r") as f:
    reader = csv.reader(f)
    tuna = list(reader)

#remove title of CSV
tuna.pop(0)

def process_helper(lst: list)-> list:
    """Takes in unformatted list from CSV and returns a list of the form
    [['year', 'STATE', 'SPECIES', 'sum pounds']]"""
    master_list = []
    for n in lst:
        if n[3] != "":

            master_list.append([n[0], n[1], n[2].replace(",", ""), int(n[3].replace(",", ""))])

    return master_list

#processed list
tuna_slim = process_helper(tuna)

#-------Make lists of all species, states and years included in data------

def rem_dups(lst: list)->list:
    new_list = []
    for n in lst:
        if n not in new_list:
            new_list.append(n)
    return new_list

def species_maker(data: list)-> list:
    """takes in formatted data and reuturns list of species without repeats"""
    species_list = []
    for n in data:
        species_list.append(n[2])
    #remove duplicates
    return rem_dups(species_list)

def states_maker(data: list)-> list:
    """takes in formatted data and reuturns list of states without repeats"""
    states_list = []
    for n in data:
        states_list.append(n[1])
    #remove duplicates
    return rem_dups(states_list)

def year_maker(data: list)-> list:
    """takes in formatted data and returns list of years without repeats"""
    year_list = []
    for n in data:
        year_list.append(int(n[0]))
    #remove duplicates
    return rem_dups(year_list)



def year_totaler(big: list, year: int, to_total: str)-> list:
    """based on year, produce a list of the form [to_total, total catch by to_total]
    to_total can be: 'species', 'state', 'all' """
    result_list = []
    if to_total == "species":
        #yearly catch total for each species in the data set "big"
        for species in species_maker(big):
            species_total = 0
            for f in big:
                if (f[2] == species) and (int(f[0]) == year):
                    species_total += f[3]
            result_list.append([year, species, species_total])
    elif to_total == "state":
        #yearly catch total for each state in the data set
        for state in states_maker(big):
            state_total = 0
            for f in big:
                if (f[1] == state) and (int(f[0]) == year):
                    state_total += f[3]
            result_list.append([year, state, state_total])
    elif to_total == "all":
        all_total = 0
        #total pounds harvested in given year
        for f in big:
            if int(f[0]) == year:
                all_total += f[3]
        return [year, all_total]
    else:
        raise Exception("Not a category")
    return result_list


#making list of most harvested species per year

def top_species_maker(data: list)->list:
    """takes in main data and creates ordered list of the most harvested species
    for each year in the form [['year', 'SPECIES', pounds harvested]]"""
    top_species = []
    year_list = year_maker(data)

    for year in year_list:
        a_list = sorted(year_totaler(data, year, "species"), reverse=-1, key=lambda f: f[2])
        top_species.append([year, a_list[0][1], a_list[0][2]])
    return top_species


def top_three_species_maker(data: list)->list:
    """takes in main data and creates ordered list of the 3 most harvested
    species for each year in the form [['year', 'SPECIES1', pounds harvested,
    'SPECIES2, pounds harvested, 'SPECIES3', pounds harvested]]"""

    top_three_species = []
    year_list = year_maker(data)

    for year in year_list:
        a_list = sorted(year_totaler(tuna_slim, year, "species"), reverse=-1, key=lambda f: f[2])
        top_three_species.append([year, a_list[0][1], a_list[0][2], a_list[1][1],
                                  a_list[1][2], a_list[2][1], a_list[2][2]])
    return top_three_species



def top_three_species_names(data: list)->list:
    """takes in data formatted [['year', 'SPECIES', pounds harvested]] and
    return list of all names"""
    top_names = []

    for year in data:
        top_names.append(year[1])
        top_names.append(year[3])
        top_names.append(year[5])

    return rem_dups(top_names)


top_names_list = top_three_species_names(top_three_species_maker(tuna_slim))


def top_names_data_maker(names: list, data: list)->list:
    """takes in list of names and returns list of yearly harvest of each name
    in the format [[]]"""
    top_names_data = []
    year_list = year_maker(data)

    for year in year_list:
        species_temp = []
        for species in names:
            species_temp.append([species, sorted(year_totaler(tuna_slim, year, "species"),
                                                 reverse=-1, key=lambda f: f[1]==species)[0][2]])
        top_names_data.append([year, species_temp])
    return top_names_data


top_names_data = top_names_data_maker(top_names_list, tuna_slim)


#-------sending top three to CSV---------
result_string = "Year, " + top_names_list[0] + ", " + top_names_list[1] + \
", " + top_names_list[2] + ", " + top_names_list[3]+ ", " + \
top_names_list[4] +", "+ top_names_list[5]+ ", " + top_names_list[6]+ ",\n"

i = 0

while i < len(top_names_data):
    result_string = result_string + str(top_names_data[i][0]) + ", " + str(top_names_data[i][1][0][1]) \
                    + ", " + str(top_names_data[i][1][1][1]) + ", " + str(top_names_data[i][1][2][1]) + ", " + \
                    str(top_names_data[i][1][3][1]) + ", " + str(top_names_data[i][1][4][1]) +", " + \
                    str(top_names_data[i][1][5][1]) + ", " + str(top_names_data[i][1][6][1])+ ",\n"
    i += 1


f2 = open('top_three_tuna_rec_data.csv', "w")
f2.write(result_string)
f2.close()

#--------plotting data---------
import csv
with open('top_three_tuna_rec_data.csv', "r") as f:
    reader = csv.reader(f)
    tuna_data = list(reader)
header_list = tuna_data[0]
tuna_data.pop(0)

#------plotting data-------
#careful of types
year_list = list(map(lambda x: float(x[0]), tuna_data))
species_1 = list(map(lambda x: float(x[1]), tuna_data))
species_2 = list(map(lambda x: float(x[2]), tuna_data))
species_3 = list(map(lambda x: float(x[3]), tuna_data))
species_4 = list(map(lambda x: float(x[4]), tuna_data))
species_5 = list(map(lambda x: float(x[5]), tuna_data))
species_6 = list(map(lambda x: float(x[6]), tuna_data))
species_7 = list(map(lambda x: float(x[6]), tuna_data))

fig = plt.figure()
plt.plot(year_list, species_1, 'b', label=header_list[1])
plt.plot(year_list, species_2, 'g', label=header_list[2])
plt.plot(year_list, species_3, 'r', label=header_list[3])
plt.plot(year_list, species_4, 'y', label=header_list[4])
plt.plot(year_list, species_5, 'olive', label=header_list[5])
plt.plot(year_list, species_6, 'c', label=header_list[6])
plt.plot(year_list, species_7, 'm', label=header_list[7])

plt.figlegend(loc='best')
plt.xlabel('Year')
plt.ylabel('Commercial harvest in pounds')
plt.title('Harvest in pounds of top tuna species from 1981-2017')

plt.show()
