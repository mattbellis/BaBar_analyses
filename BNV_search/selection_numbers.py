event_numbers = {}
event_numbers["DATA"] = {}
event_numbers["MC"] = {}

for i in range(1,7):
        key = "Run{0}".format(i)
        event_numbers["DATA"][key] = {}

for i in [1235, 1237, 1005, 998, 3429, 3981, 2400, 11975, 11976, 11977, 9456, 9457, 980]:
        key = "{0}".format(i)
        event_numbers["MC"][key] = {}

# First skim at SLAC
event_numbers["DATA"]["Run1"]["skim"] = 116830108
event_numbers["DATA"]["Run2"]["skim"] = 381470233
event_numbers["DATA"]["Run3"]["skim"] = 201752757
event_numbers["DATA"]["Run4"]["skim"] = 662993550
event_numbers["DATA"]["Run5"]["skim"] = 855886010
event_numbers["DATA"]["Run6"]["skim"] = 499945723

event_numbers["MC"]["1235"]["skim"] = 25718483
event_numbers["MC"]["1237"]["skim"] = 21780258
event_numbers["MC"]["1005"]["skim"] = 89213627
event_numbers["MC"]["998"]["skim"] =  444420132
event_numbers["MC"]["3429"]["skim"] = 435212096
event_numbers["MC"]["3981"]["skim"] = 0
event_numbers["MC"]["2400"]["skim"] = 0

event_numbers["MC"]["980"]["skim"] = 709676

event_numbers["MC"]["9456"]["skim"] =  2028701
event_numbers["MC"]["9457"]["skim"] =  2010973
event_numbers["MC"]["11975"]["skim"] = 1959850
event_numbers["MC"]["11976"]["skim"] = 1864139
event_numbers["MC"]["11977"]["skim"] = 1750334

