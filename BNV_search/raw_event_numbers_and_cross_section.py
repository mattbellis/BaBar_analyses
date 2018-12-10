raw_event_numbers = {}
raw_event_numbers["data"] = {}
raw_event_numbers["MC"] = {}

for i in range(1,7):
        key = "Run{0}".format(i)
        raw_event_numbers["data"][key] = {"raw":100000, "xsec":0}

for i in [1235, 1237, 1005, 998, 3429, 3981, 2400, 11975, 11976, 11977, 9456, 9457]:
        key = "{0}".format(i)
        raw_event_numbers["MC"][key] = {"raw":100000, "xsec":0}

raw_event_numbers["data"]["Run1"]["raw"] *= 2929
raw_event_numbers["data"]["Run2"]["raw"] *= 9590
raw_event_numbers["data"]["Run3"]["raw"] *= 5014
raw_event_numbers["data"]["Run4"]["raw"] *= 15936
raw_event_numbers["data"]["Run5"]["raw"] *= 21045
raw_event_numbers["data"]["Run6"]["raw"] *= 12629

raw_event_numbers["MC"]["1005"]["raw"] *= 11338
raw_event_numbers["MC"]["11975"]["raw"] *= 12
raw_event_numbers["MC"]["11976"]["raw"] *= 12
raw_event_numbers["MC"]["11977"]["raw"] *= 12
raw_event_numbers["MC"]["1235"]["raw"] *= 7105
raw_event_numbers["MC"]["1237"]["raw"] *= 7201
raw_event_numbers["MC"]["2400"]["raw"] *= 4729
raw_event_numbers["MC"]["3429"]["raw"] *= 16202
raw_event_numbers["MC"]["3981"]["raw"] *= 6224
raw_event_numbers["MC"]["9456"]["raw"] *= 23
raw_event_numbers["MC"]["9457"]["raw"] *= 23
raw_event_numbers["MC"]["998"]["raw"] *= 35959

raw_event_numbers["MC"]["1235"]["xsec"] = 0.54
raw_event_numbers["MC"]["1237"]["xsec"] = 0.54
raw_event_numbers["MC"]["1005"]["xsec"] = 1.30
raw_event_numbers["MC"]["998"]["xsec"] = 2.09
raw_event_numbers["MC"]["3429"]["xsec"] = 0.94
raw_event_numbers["MC"]["3981"]["xsec"] = 1.16
raw_event_numbers["MC"]["2400"]["xsec"] = 40

intlumi = 424.18

