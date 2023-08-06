import  uproot , matplotlib.pyplot as plt , hist ,loading_bars as ldbr ,pickle
from hist import Hist
from TLorentzVector import TLorentzVector


print(f"getting events from server")

events = uproot.open("https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/MC/mc_363490.llll.4lep.root:mini")

print(f"retreving required data")


sel_events = events.arrays(["lep_n", "lep_charge", "lep_type", "lep_pt", "lep_eta", "lep_phi", "lep_E"])
#read_file = open("out.json","rb")
#sel_events = pickle.load(read_file)
print("saving data")

out_file = open("sel_data.json","wb")

pickle.dump(sel_events,out_file)

print("data saved")

print(f"creating hist")

hist2 = Hist(hist.axis.Regular(30,40,140, label = "muon Mass (GeV)"))

print(f"starting data analisis")

total_events = len(sel_events)
prev_bar = ""
leadLepton  = TLorentzVector()
trailLepton = TLorentzVector()
num_of_muons = 0

for index , event in enumerate(sel_events) :
    if event["lep_n"] >= 2 :
        
        lep_charge = event["lep_charge"]
        if lep_charge[0] != lep_charge[1] :

            lep_type = event["lep_type"] 
            if lep_type[0] == lep_type[1] :
                
                lep_pt  = event["lep_pt"]
                lep_eta = event["lep_eta"]
                lep_phi = event["lep_phi"]
                lep_E   = event["lep_E"]

                leadLepton.SetPtEtaPhiE(lep_pt[0]/1000., lep_eta[0], lep_phi[0], lep_E[0]/1000.)
                trailLepton.SetPtEtaPhiE(lep_pt[1]/1000., lep_eta[1], lep_phi[1], lep_E[1]/1000.)

                Z0_boson = leadLepton + trailLepton
                if lep_type[0] == 11 == lep_type[1] :
                    hist2.fill(Z0_boson.M())
                    pass
                elif (lep_type[0]==13) & (lep_type[1]==13) :
                    #hist2.fill(Z0_boson.M())    
                    pass        

    new_bar = ldbr.loadingbar(name="PROGRESS",value=((index+1)/total_events),length=50)
    if new_bar != prev_bar :
        print(new_bar,end="\r")

hist2.plot(histtype = "fill")
plt.show()
    