########################################
# # of charged cuts
# BNV child p 2.3-2.8 GeV/c
# # of high-p tracks is 1 or 2
# # of BNV tracks is 1
########################################
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
#event_numbers["DATA"]["pmu"]["All runs"]["tighterPID_childmomentum"] = 6663
event_numbers["DATA"]["pmu"]["Run1"]["tighterPID_childmomentum"] = 309
event_numbers["DATA"]["pmu"]["Run2"]["tighterPID_childmomentum"] = 940
event_numbers["DATA"]["pmu"]["Run3"]["tighterPID_childmomentum"] = 514
event_numbers["DATA"]["pmu"]["Run4"]["tighterPID_childmomentum"] = 1512
event_numbers["DATA"]["pmu"]["Run5"]["tighterPID_childmomentum"] = 2140
event_numbers["DATA"]["pmu"]["Run6"]["tighterPID_childmomentum"] = 1248
event_numbers["MC"]["pmu"]["1005"]["tighterPID_childmomentum"] = 3268
event_numbers["MC"]["pmu"]["11975"]["tighterPID_childmomentum"] = 77
event_numbers["MC"]["pmu"]["11976"]["tighterPID_childmomentum"] = 318
event_numbers["MC"]["pmu"]["11977"]["tighterPID_childmomentum"] = 0
event_numbers["MC"]["pmu"]["1235"]["tighterPID_childmomentum"] = 40
event_numbers["MC"]["pmu"]["1237"]["tighterPID_childmomentum"] = 34
event_numbers["MC"]["pmu"]["3429"]["tighterPID_childmomentum"] = 593
event_numbers["MC"]["pmu"]["9456"]["tighterPID_childmomentum"] = 847396
event_numbers["MC"]["pmu"]["9457"]["tighterPID_childmomentum"] = 3
event_numbers["MC"]["pmu"]["998"]["tighterPID_childmomentum"] = 30920
# pe
#event_numbers["DATA"]["pe"]["All runs"]["tighterPID_childmomentum"] = 3443
event_numbers["DATA"]["pe"]["Run1"]["tighterPID_childmomentum"] = 158
event_numbers["DATA"]["pe"]["Run2"]["tighterPID_childmomentum"] = 457
event_numbers["DATA"]["pe"]["Run3"]["tighterPID_childmomentum"] = 267
event_numbers["DATA"]["pe"]["Run4"]["tighterPID_childmomentum"] = 820
event_numbers["DATA"]["pe"]["Run5"]["tighterPID_childmomentum"] = 1094
event_numbers["DATA"]["pe"]["Run6"]["tighterPID_childmomentum"] = 647
event_numbers["MC"]["pe"]["1005"]["tighterPID_childmomentum"] = 1920
event_numbers["MC"]["pe"]["11975"]["tighterPID_childmomentum"] = 19
event_numbers["MC"]["pe"]["11976"]["tighterPID_childmomentum"] = 0
event_numbers["MC"]["pe"]["11977"]["tighterPID_childmomentum"] = 295
event_numbers["MC"]["pe"]["1235"]["tighterPID_childmomentum"] = 7
event_numbers["MC"]["pe"]["1237"]["tighterPID_childmomentum"] = 8
event_numbers["MC"]["pe"]["3429"]["tighterPID_childmomentum"] = 592
event_numbers["MC"]["pe"]["9456"]["tighterPID_childmomentum"] = 1
event_numbers["MC"]["pe"]["9457"]["tighterPID_childmomentum"] = 816170
event_numbers["MC"]["pe"]["998"]["tighterPID_childmomentum"] = 6862
# pnu
#event_numbers["DATA"]["pnu"]["All runs"]["tighterPID_childmomentum"] = 1896981
event_numbers["DATA"]["pnu"]["Run1"]["tighterPID_childmomentum"] = 96451
event_numbers["DATA"]["pnu"]["Run2"]["tighterPID_childmomentum"] = 279146
event_numbers["DATA"]["pnu"]["Run3"]["tighterPID_childmomentum"] = 145720
event_numbers["DATA"]["pnu"]["Run4"]["tighterPID_childmomentum"] = 436657
event_numbers["DATA"]["pnu"]["Run5"]["tighterPID_childmomentum"] = 582295
event_numbers["DATA"]["pnu"]["Run6"]["tighterPID_childmomentum"] = 356712
event_numbers["MC"]["pnu"]["1005"]["tighterPID_childmomentum"] = 565676
event_numbers["MC"]["pnu"]["11975"]["tighterPID_childmomentum"] = 1104535
event_numbers["MC"]["pnu"]["11976"]["tighterPID_childmomentum"] = 405
event_numbers["MC"]["pnu"]["11977"]["tighterPID_childmomentum"] = 2277
event_numbers["MC"]["pnu"]["1235"]["tighterPID_childmomentum"] = 40267
event_numbers["MC"]["pnu"]["1237"]["tighterPID_childmomentum"] = 36825
event_numbers["MC"]["pnu"]["3429"]["tighterPID_childmomentum"] = 261799
event_numbers["MC"]["pnu"]["9456"]["tighterPID_childmomentum"] = 43776
event_numbers["MC"]["pnu"]["9457"]["tighterPID_childmomentum"] = 62258
event_numbers["MC"]["pnu"]["980"]["tighterPID_childmomentum"] = 0
event_numbers["MC"]["pnu"]["998"]["tighterPID_childmomentum"] = 5184487
# nmu
#event_numbers["DATA"]["nmu"]["All runs"]["tighterPID_childmomentum"] = 2975422
event_numbers["DATA"]["nmu"]["Run1"]["tighterPID_childmomentum"] = 143201
event_numbers["DATA"]["nmu"]["Run2"]["tighterPID_childmomentum"] = 422932
event_numbers["DATA"]["nmu"]["Run3"]["tighterPID_childmomentum"] = 222248
event_numbers["DATA"]["nmu"]["Run4"]["tighterPID_childmomentum"] = 678860
event_numbers["DATA"]["nmu"]["Run5"]["tighterPID_childmomentum"] = 922838
event_numbers["DATA"]["nmu"]["Run6"]["tighterPID_childmomentum"] = 585343
event_numbers["MC"]["nmu"]["1005"]["tighterPID_childmomentum"] = 2286828
event_numbers["MC"]["nmu"]["11975"]["tighterPID_childmomentum"] = 1048
event_numbers["MC"]["nmu"]["11976"]["tighterPID_childmomentum"] = 1024700
event_numbers["MC"]["nmu"]["11977"]["tighterPID_childmomentum"] = 119
event_numbers["MC"]["nmu"]["1235"]["tighterPID_childmomentum"] = 308944
event_numbers["MC"]["nmu"]["1237"]["tighterPID_childmomentum"] = 243589
event_numbers["MC"]["nmu"]["3429"]["tighterPID_childmomentum"] = 4684926
event_numbers["MC"]["nmu"]["9456"]["tighterPID_childmomentum"] = 72071
event_numbers["MC"]["nmu"]["9457"]["tighterPID_childmomentum"] = 175
event_numbers["MC"]["nmu"]["980"]["tighterPID_childmomentum"] = 0
event_numbers["MC"]["nmu"]["998"]["tighterPID_childmomentum"] = 4703989
# ne
#event_numbers["DATA"]["ne"]["All runs"]["tighterPID_childmomentum"] = 4143932
event_numbers["DATA"]["ne"]["Run1"]["tighterPID_childmomentum"] = 187023
event_numbers["DATA"]["ne"]["Run2"]["tighterPID_childmomentum"] = 595134
event_numbers["DATA"]["ne"]["Run3"]["tighterPID_childmomentum"] = 327955
event_numbers["DATA"]["ne"]["Run4"]["tighterPID_childmomentum"] = 979470
event_numbers["DATA"]["ne"]["Run5"]["tighterPID_childmomentum"] = 1279455
event_numbers["DATA"]["ne"]["Run6"]["tighterPID_childmomentum"] = 774895
event_numbers["MC"]["ne"]["1005"]["tighterPID_childmomentum"] = 1379846
event_numbers["MC"]["ne"]["11975"]["tighterPID_childmomentum"] = 39
event_numbers["MC"]["ne"]["11976"]["tighterPID_childmomentum"] = 16
event_numbers["MC"]["ne"]["11977"]["tighterPID_childmomentum"] = 990269
event_numbers["MC"]["ne"]["1235"]["tighterPID_childmomentum"] = 163451
event_numbers["MC"]["ne"]["1237"]["tighterPID_childmomentum"] = 146235
event_numbers["MC"]["ne"]["3429"]["tighterPID_childmomentum"] = 4652171
event_numbers["MC"]["ne"]["9456"]["tighterPID_childmomentum"] = 8
event_numbers["MC"]["ne"]["9457"]["tighterPID_childmomentum"] = 57029
event_numbers["MC"]["ne"]["980"]["tighterPID_childmomentum"] = 0
event_numbers["MC"]["ne"]["998"]["tighterPID_childmomentum"] = 1170358
