event_numbers = {}
event_numbers["DATA"] = {}
event_numbers["MC"] = {}

decays = ['pmu', 'pe', 'pnu', 'nmu', 'ne']
for decay in decays:
    event_numbers['DATA'][decay] = {}
    for i in range(1,7):
            key = "Run{0}".format(i)
            event_numbers["DATA"][decay][key] = {}

    event_numbers['MC'][decay] = {}
    for i in [1235, 1237, 1005, 998, 3429, 3981, 2400, 11975, 11976, 11977, 9456, 9457, 980]:
            key = "{0}".format(i)
            event_numbers["MC"][decay][key] = {}

# pmu
event_numbers["MC"]["pmu"]["11975"]["cuts1"] = 159
event_numbers["MC"]["pmu"]["11976"]["cuts1"] = 476
event_numbers["MC"]["pmu"]["11977"]["cuts1"] = 2
event_numbers["MC"]["pmu"]["9456"]["cuts1"] = 1030079
event_numbers["MC"]["pmu"]["9457"]["cuts1"] = 54
event_numbers["MC"]["pmu"]["1235"]["cuts1"] = 113
event_numbers["MC"]["pmu"]["1237"]["cuts1"] = 124
event_numbers["MC"]["pmu"]["1005"]["cuts1"] = 7844
event_numbers["MC"]["pmu"]["3429"]["cuts1"] = 1455
event_numbers["MC"]["pmu"]["998"]["cuts1"] = 105783
event_numbers["DATA"]["pmu"]["Run1"]["cuts1"] = 8779
event_numbers["DATA"]["pmu"]["Run2"]["cuts1"] = 27003
event_numbers["DATA"]["pmu"]["Run3"]["cuts1"] = 17180
event_numbers["DATA"]["pmu"]["Run4"]["cuts1"] = 51117
event_numbers["DATA"]["pmu"]["Run5"]["cuts1"] = 66803
event_numbers["DATA"]["pmu"]["Run6"]["cuts1"] = 33669
# pe
event_numbers["MC"]["pe"]["11975"]["cuts1"] = 20
event_numbers["MC"]["pe"]["11976"]["cuts1"] = 0
event_numbers["MC"]["pe"]["11977"]["cuts1"] = 379
event_numbers["MC"]["pe"]["9456"]["cuts1"] = 3
event_numbers["MC"]["pe"]["9457"]["cuts1"] = 853388
event_numbers["MC"]["pe"]["1235"]["cuts1"] = 15
event_numbers["MC"]["pe"]["1237"]["cuts1"] = 15
event_numbers["MC"]["pe"]["1005"]["cuts1"] = 2283
event_numbers["MC"]["pe"]["3429"]["cuts1"] = 833
event_numbers["MC"]["pe"]["998"]["cuts1"] = 8035
event_numbers["DATA"]["pe"]["Run1"]["cuts1"] = 2499
event_numbers["DATA"]["pe"]["Run2"]["cuts1"] = 7433
event_numbers["DATA"]["pe"]["Run3"]["cuts1"] = 3981
event_numbers["DATA"]["pe"]["Run4"]["cuts1"] = 12197
event_numbers["DATA"]["pe"]["Run5"]["cuts1"] = 16084
event_numbers["DATA"]["pe"]["Run6"]["cuts1"] = 9961
# pnu
event_numbers["MC"]["pnu"]["11975"]["cuts1"] = 1163125
event_numbers["MC"]["pnu"]["11976"]["cuts1"] = 1211
event_numbers["MC"]["pnu"]["11977"]["cuts1"] = 5993
event_numbers["MC"]["pnu"]["9456"]["cuts1"] = 58762
event_numbers["MC"]["pnu"]["9457"]["cuts1"] = 190830
event_numbers["MC"]["pnu"]["1235"]["cuts1"] = 140295
event_numbers["MC"]["pnu"]["1237"]["cuts1"] = 110916
event_numbers["MC"]["pnu"]["1005"]["cuts1"] = 2491114
event_numbers["MC"]["pnu"]["3429"]["cuts1"] = 599900
event_numbers["MC"]["pnu"]["998"]["cuts1"] = 22139039
event_numbers["DATA"]["pnu"]["Run1"]["cuts1"] = 1175225
event_numbers["DATA"]["pnu"]["Run2"]["cuts1"] = 3454029
event_numbers["DATA"]["pnu"]["Run3"]["cuts1"] = 1803069
event_numbers["DATA"]["pnu"]["Run4"]["cuts1"] = 5486570
event_numbers["DATA"]["pnu"]["Run5"]["cuts1"] = 7341398
event_numbers["DATA"]["pnu"]["Run6"]["cuts1"] = 4443902
# nmu
event_numbers["MC"]["nmu"]["11975"]["cuts1"] = 30311
event_numbers["MC"]["nmu"]["11976"]["cuts1"] = 1211064
event_numbers["MC"]["nmu"]["11977"]["cuts1"] = 471
event_numbers["MC"]["nmu"]["9456"]["cuts1"] = 95168
event_numbers["MC"]["nmu"]["9457"]["cuts1"] = 5673
event_numbers["MC"]["nmu"]["1235"]["cuts1"] = 531495
event_numbers["MC"]["nmu"]["1237"]["cuts1"] = 387059
event_numbers["MC"]["nmu"]["1005"]["cuts1"] = 4461530
event_numbers["MC"]["nmu"]["3429"]["cuts1"] = 6831321
event_numbers["MC"]["nmu"]["998"]["cuts1"] = 13404987
event_numbers["DATA"]["nmu"]["Run1"]["cuts1"] = 1193280
event_numbers["DATA"]["nmu"]["Run2"]["cuts1"] = 3597486
event_numbers["DATA"]["nmu"]["Run3"]["cuts1"] = 2000074
event_numbers["DATA"]["nmu"]["Run4"]["cuts1"] = 6054158
event_numbers["DATA"]["nmu"]["Run5"]["cuts1"] = 7946008
event_numbers["DATA"]["nmu"]["Run6"]["cuts1"] = 4695801
# ne
event_numbers["MC"]["ne"]["11975"]["cuts1"] = 50
event_numbers["MC"]["ne"]["11976"]["cuts1"] = 18
event_numbers["MC"]["ne"]["11977"]["cuts1"] = 1010383
event_numbers["MC"]["ne"]["9456"]["cuts1"] = 9
event_numbers["MC"]["ne"]["9457"]["cuts1"] = 59637
event_numbers["MC"]["ne"]["1235"]["cuts1"] = 166293
event_numbers["MC"]["ne"]["1237"]["cuts1"] = 148667
event_numbers["MC"]["ne"]["1005"]["cuts1"] = 1409404
event_numbers["MC"]["ne"]["3429"]["cuts1"] = 4797187
event_numbers["MC"]["ne"]["998"]["cuts1"] = 1247404
event_numbers["DATA"]["ne"]["Run1"]["cuts1"] = 1827695
event_numbers["DATA"]["ne"]["Run2"]["cuts1"] = 5632005
event_numbers["DATA"]["ne"]["Run3"]["cuts1"] = 3242649
event_numbers["DATA"]["ne"]["Run4"]["cuts1"] = 9656281
event_numbers["DATA"]["ne"]["Run5"]["cuts1"] = 12790650
event_numbers["DATA"]["ne"]["Run6"]["cuts1"] = 7672053

