from raw_event_numbers_and_cross_section import raw_event_numbers
from COUNTS_SIGNAL_REMAINING import event_numbers

nBB = 470.89e6
nBpBm = nBB * 51.6e-2
nB0B0bar = nBB * 48.4e-2



dc = ['pmu', 'pe', 'pnu', 'nmu', 'ne']
signal_events = [500, 500, 140, 2130, 1000]
nbb_for_each_channel = [nB0B0bar, nB0B0bar, nBpBm, nBpBm, nBpBm]

for i,sp in enumerate(['9456','9457','11975','11976','11977']):

    raw = raw_event_numbers['MC'][sp]['raw']
    n = event_numbers['MC'][dc[i]][sp]['selection_cuts_TESTING'] 
    eff = n/raw
    sig = signal_events[i]
    nbb = nbb_for_each_channel[i]

    B = sig/(eff*nbb)

    print(f"{dc[i]:4} {raw:10d}  {n:10d}     {eff:0.4f}   {sig:0.1f}   {nbb:.2e} {B:0.2e}")


