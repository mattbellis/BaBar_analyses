event_numbers = {}
event_numbers["MC"] = {}

for i in ['pmu', 'pe', 'pnu', 'nmu', 'ne']:
    key = f"{i}"
    event_numbers["MC"][key] = {}

    for j in [11975, 11976, 11977, 9456, 9457, 980]:
            key2 = f"{j}"
            event_numbers["MC"][key][key2] = {"selection_cuts_TESTING":0}

# pmu
event_numbers["MC"]["pmu"]["9456"]["selection_cuts_TESTING"] = 847295
# pe
event_numbers["MC"]["pe"]["9457"]["selection_cuts_TESTING"] = 816161
# pnu
event_numbers["MC"]["pnu"]["11975"]["selection_cuts_TESTING"] = 1093221
# nmu
event_numbers["MC"]["nmu"]["11976"]["selection_cuts_TESTING"] = 1010864
# ne
event_numbers["MC"]["ne"]["11977"]["selection_cuts_TESTING"] = 990241
