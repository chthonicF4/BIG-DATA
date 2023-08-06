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

    out_bosons = []

    combos = []

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
            firstLepton.SetPtEtaPhiE(lep_pt[combo[0]]/1000., lep_eta[combo[0]], lep_phi[combo[0]], lep_E[combo[0]]/1000.)
            seccondLepton.SetPtEtaPhiE(lep_pt[combo[1]]/1000., lep_eta[combo[1]], lep_phi[combo[1]], lep_E[combo[1]]/1000.)
            Z0_boson_1 = firstLepton + seccondLepton
            
            if True or (90<Z0_boson_1.M()<92):
                out_bosons.append((lep_type[combo[0]],Z0_boson_1))
                blacklist.append(combo[0])
                blacklist.append(combo[1])
    return out_bosons


pass


# loading feedback
global prev_loading , current_loading , start ,average_list
start = time.time()
prev_loading = 0
current_loading = 0
average_list = []

def eta(prev:float,current:float,time:float):
    if time == 0 : time = 0.0001
    completedPerSec = (current - prev)/time
    if completedPerSec == 0 :
        return 0
    ammount_left = 1 - current
    time_left = ammount_left / completedPerSec
    return time_left

def loading(value):
    global prev_loading , current_loading , start,average_list
    prev_loading = current_loading
    current_loading = value
    time_left = eta(prev_loading,current_loading,time.time()-start)
    average_list.append(time_left)
    if len(average_list) > 50 :
        average_list.pop(0)
    time_left = 0
    for x in average_list :
        time_left += x
    time_left = time_left/len(average_list)
    time_left = time.strftime("%H:%M:%S",time.gmtime(time_left))
    print(f"{100*(value):.2f}% eta:{time_left}\r",end="")
    start = time.time()

print("proccessing")

data_procceser = crochet(analise_event,sel_events,12,loading)
data_procceser.load_fraction = 10000
proccessed_data = data_procceser.run()
print(f"\nDone!")

print("plotting")

start = time.time()
prev_loading = 0
current_loading = 0
average_list = []
total = len(proccessed_data)

#histagrams
histagram_electrons = Hist(hist.axis.Regular(200,102,80, label = "Mass (GeV)"))
histagram_muons = Hist(hist.axis.Regular(200,102,80, label = "Mass (GeV)"))

for index,event in enumerate(proccessed_data) :
    if event == None :
        continue
    for type,boson in event :
        if type == 11 :
            histagram_electrons.fill(boson.M())
        elif type == 13 :
            histagram_muons.fill(boson.M())
    loading(index/total)

print("presenting")

histagram_electrons.plot(histtype = "fill")
plt.show()

histagram_muons.plot(histtype = "fill")
plt.show()