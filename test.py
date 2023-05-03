import uproot , numpy as np

def root_get(links:list,selected_events:list):
    out = []
    for index,link in enumerate(links) :
        print(f"proccesing {index}")
        events = uproot.open(f"{link}:mini")
        sel_events = events.arrays(selected_events)
        out.append(sel_events)
        print(len(sel_events))
    return out

links = ["https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/Data/data_A.4lep.root",
         "https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/Data/data_B.4lep.root",
         "https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/Data/data_C.4lep.root",
         "https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/Data/data_D.4lep.root",
         ]

selected_events = ["lep_n", "lep_charge", "lep_type", "lep_pt", "lep_eta", "lep_phi", "lep_E"]
out_1 = root_get(links,selected_events)

print(out_1)


out_1
out = np.concatenate(out_1)

print("\n",out,len(out))