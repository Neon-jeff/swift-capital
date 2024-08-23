from Countrydetails import countries

def CountryData():
    data=[{
        "name":country['name'],
        "phone_code":country['phone_code'],
        "country_code":country['iso2'],
        "states":[state['name'] for state in country['states']],
        'flag':f'https://flagcdn.com/16x12/{country["iso2"].lower()}.png'
    } for country in countries.all_countries().states_file if len(country['states'])!=0
      ]
    data.append({
        "name":"Hong Kong",
        "phone_code":852,
        "country_code":"HK",
        "states":[
    "Central and Western", "Eastern", "Southern", "Wan Chai",
    "Sham Shui Po", "Kowloon City", "Kwun Tong", "Wong Tai Sin", "Yau Tsim Mong",
    "Islands", "Kwai Tsing", "North", "Sai Kung", "Sha Tin", "Tai Po", "Tsuen Wan", "Tuen Mun", "Yuen Long"
],
"flag":"https://flagcdn.com/16x12/hk.png"
    })
    data=sorted(data,key=lambda k : k['name'])
    
    
    return data

# print(countries.all_countries().states_file[0:2])
