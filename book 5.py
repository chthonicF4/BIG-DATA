import uproot , numpy as np , pickle , matplotlib.pyplot as plt , hist ,loading_bars as ldbr ,time,datetime
from TLorentzVector import TLorentzVector
from hist import Hist
from crochet import crochet

# get selected events

sel_events_out_name = "sel_events"
selected_keys = ["lep_n", "lep_charge", "lep_type", "lep_pt", "lep_eta", "lep_phi", "lep_E"]
server_url = "https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/MC/mc_363490.llll.4lep.root:mini"

def get_data_from_server():
    events = uproot.open(server_url)
    print("recived .root file ! , getting selected events ... ")
    sel_events = events.arrays(selected_keys)
    return sel_events

def save_data(file_name,data):
    out = open(f"{file_name}.json","wb")
    pickle.dump(data,out)


try : # get previously loaded events
    past_sel_events = open(f"{sel_events_out_name}.json","rb")

except IOError : # if cant load data
    print("no previous selected data exists , getting data from server")
    sel_events = get_data_from_server()
    print("saving data...")
    save_data(sel_events_out_name,sel_events)
    print("saved new data!")


else:

    load_past_choice = str(input(f"past data found in {sel_events_out_name}.json , load data ? [y/n] :")).lower()

    while True :
        
        if load_past_choice in ["y","yes"]: # use old data

            print("loading past data ...")
            try:
                sel_events = pickle.load(past_sel_events)
            except :
                print("error loading past data , reverting to server's data")
                load_past_choice = "n"
                continue
            print("data loaded successfully !")
            break
        
        elif load_past_choice in ["n","no"]: # make new data

            print("ignoring past data , getting data from server ...")
            sel_events = get_data_from_server()
            print("saving data...")
            save_data(sel_events_out_name,sel_events)
            print("saved new data!")
            break
        
        else :
            print("invalid input :(")
            load_past_choice = str(input(f"past data found in {sel_events_out_name}.json , load data ? [y/n] :")).lower()



# --------------------------------------------------------------------------------------------------
#                                        ANILISE DATA
# --------------------------------------------------------------------------------------------------

firstLepton = TLorentzVector()
seccondLepton = TLorentzVector()
thirdLepton = TLorentzVector()
fourthLepton = TLorentzVector()

histagram = Hist(hist.axis.Regular(30,40,140, label = "Mass (GeV)"))
# loading feedback
prev_ldbr = -1
total_events = len(sel_events)
length_ldbr = 50

def eta(prev:float,current:float,time:float):
    if time == 0 : time = 0.00001
    completedPerSec = (current - prev)/time
    ammount_left = 1 - current
    time_left = ammount_left / completedPerSec
    return time_left

start = time.time()


def analise_event(event):

    lep_n      = event[  "lep_n"   ]

    if lep_n < 4 :
        return None

    lep_charge = event["lep_charge"]
    lep_type   = event[ "lep_type" ]
    lep_pt     = event[  "lep_pt"  ]
    lep_eta    = event[ "lep_eta"  ]
    lep_phi    = event[ "lep_phi"  ]
    lep_E      = event[   "lep_E"  ]


    combos = []

    out_bosons = []

    for x in range(lep_n):
        for y in range(lep_n):
            if x < y :
                combos.append((x,y))

    blacklist = []

    for combo in combos :

        for item in blacklist: 
            if item in combo : continue

        # cuts :
        if not(lep_charge[combo[0]]!=lep_charge[combo[1]]): # same charge
            continue
        elif not(lep_type[combo[0]]==lep_type[combo[1]]): # same type
            continue
        else:
            firstLepton.SetPtEtaPhiE(lep_pt[0]/1000., lep_eta[0], lep_phi[0], lep_E[0]/1000.)
            seccondLepton.SetPtEtaPhiE(lep_pt[1]/1000., lep_eta[1], lep_phi[1], lep_E[1]/1000.)
            Z0_boson_1 = firstLepton + seccondLepton
            
            if (80<Z0_boson_1.M()<100):
                out_bosons.append(Z0_boson_1)
                blacklist.append(combo[0])
                blacklist.append(combo[1])

    return out_bosons


pass

def loading(value):
    print(f"{100*(value):.2f}%\r",end="")

print("proccessing")

data_procceser = crochet(analise_event,sel_events,10,loading)
data_procceser.load_fraction = 10000
proccessed_data = data_procceser.run()

print("plotting")


for event in proccessed_data :
    if event == None :
        continue
    for boson in event :
        histagram.fill(boson.M())

print("presenting")

histagram.plot(histtype = "fill")
plt.show()