import  matplotlib.pyplot as plt , hist ,loading_bars as ldbr ,time , numpy as np , multiprocessing , pickle
from TLorentzVector import TLorentzVector
from hist import Hist
from crochet import crochet
from rootFile import data_files


real_data_links = ["https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/2lep/Data/data_A.2lep.root",
                   "https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/2lep/Data/data_B.2lep.root",
                   "https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/2lep/Data/data_C.2lep.root",
                   "https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/2lep/Data/data_D.2lep.root" 
                  ]

simulated_data = ["https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/2lep/MC/mc_363492.llvv.2lep.root"
                 ]

selected_events = ["lep_ptcone30",
                   "lep_etcone20",
                   "lep_isTightID",
                   "lep_eta",
                   "photon_phi",
                   "lep_type",
                   "lep_n",
                   "photon_E",
                   "lep_E",
                   "lep_pt",
                   "trigP",
                   "XSection",
                   "SumWeights",
                   "trigE",
                   "trigM",
                   "scaleFactor_ELE",
                   "scaleFactor_MUON",
                   "scaleFactor_PILEUP",
                   "scaleFactor_LepTRIGGER",
                   "mcWeight",
                   "lep_charge",
                   "lep_phi",
                   "met_et",
                   "met_phi"
                   ]

# ---------------------------------------------------------------------------------------------------------
#                                        data analisis functions.
# ---------------------------------------------------------------------------------------------------------

def mcWeights(data,lumi=10):
    """
    When MC simulation is compared to data the contribution of each simulated event needs to be
    scaled ('reweighted') to account for differences in how some objects behave in simulation
    vs in data, as well as the fact that there are different numbers of events in the MC tree than 
    in the data tree.
    
    Parameters
    ----------
    tree : TTree entry for this event
    """
    
    XSection = data["XSection"]
    SumWeights = data["SumWeights"]
    #These values don't change from event to event
    norm = lumi*(XSection*1000)/SumWeights
    
    scaleFactor_ELE = data["scaleFactor_ELE"]
    scaleFactor_MUON = data["scaleFactor_MUON"]
    scaleFactor_LepTRIGGER = data["scaleFactor_LepTRIGGER"]
    scaleFactor_PILEUP = data["scaleFactor_PILEUP"]
    mcWeight = data["mcWeight"]
    #These values do change from event to event
    scale_factors = scaleFactor_ELE*scaleFactor_MUON*scaleFactor_LepTRIGGER*scaleFactor_PILEUP*mcWeight
    
    weight = norm*scale_factors
    return weight

def goodLeptons(data):
    """
    A function to return the indices of 'good leptons' (electrons or muons) in an event. This follows 
    many of the same steps as locateGoodPhotons() and photonIsolation() in Notebook 6.
    
    Parameters
    ----------
    tree : TTree entry for this event
    """
    
    #Initialise (set up) the variables we want to return
    goodlepton_index = [] #Indices (position in list of event's leptons) of our good leptons
    
    lep_n = data["lep_n"]
    ##Loop through all the leptons in the event
    for j in range(0,lep_n):
        lep_isTightID = data["lep_isTightID"][j]    
        ##Check lepton ID
        if(lep_isTightID):
            lep_ptcone30 = data["lep_ptcone30"][j]
            lep_pt = data["lep_pt"][j]
            lep_etcone20 = data["lep_etcone20"][j]
            #Check lepton isolation
            #Similar to photonIsolation() above, different thresholds
            if((lep_ptcone30 / lep_pt < 0.1) and 
               (lep_etcone20 / lep_pt < 0.1)):

                #Only central leptons 
                #Electrons and muons have slightly different eta requirements
                lep_type = data["lep_type"][j]
                lep_eta = data["lep_eta"][j]
                #Electrons: 'Particle type code' = 11
                if lep_type == 11:
                    #Check lepton eta is in the 'central' region and not in "transition region" 
                    if (np.abs(lep_eta) < 2.37) and\
                       (np.abs(lep_eta) < 1.37 or np.abs(lep_eta) > 1.52): 

                        goodlepton_index.append(j) #Store lepton's index

                #Muons: 'Particle type code' = 13
                elif (lep_type == 13) and (np.abs(lep_eta) < 2.5): #Check'central' region

                        goodlepton_index.append(j) #Store lepton's index


    return goodlepton_index #return list of good lepton indices

def analise_event_mc(event):
    """
    Function which executes the analysis flow for the Higgs production cross-section measurement in the H->WW
    decay channel.
    
    Fills a histogram with mT(llvv) of events which pass the full set of cuts 
    
    Parameters
    ----------
    data : A Ttree containing data / background information
    
    hist : The name of the histogram to be filled with mT(llvv) values
    
    mode : A flag to tell the function if it is looping over 'data' or 'mc'
    """
        
    #############################
    ### Event-level requirements
    #############################
    
    #If event is MC: Reweight it
    weight = mcWeights(event)
        
    trigE = event["trigE"]
    trigM = event["trigM"]
    #If the event passes either the electron or muon trigger
    if trigE or trigM:
        
        ####Lepton preselections
        goodLeps = goodLeptons(event) #If the datafiles were not already filtered by number of leptons

        ###################################
        ### Individual lepton requirements
        ###################################

        if len(goodLeps) == 2: #Exactly two good leptons...
            lep1 = goodLeps[0] #INDICES of the good leptons
            lep2 = goodLeps[1]
            
            lep_type = event["lep_type"]
            if lep_type[lep1] != lep_type[lep2]: #... with different flavour
                
                lep_charge = event["lep_charge"]
                if lep_charge[lep1] != lep_charge[lep2]: #... and opposite charge...
                    
                    lep_pt = event["lep_pt"]
                    if (lep_pt[lep1] > 22000) and (lep_pt[lep2] > 15000): #pT requirements
                        #Note: TTrees always sort objects in descending pT order
                        
                        lep_phi = event["lep_phi"]
                        if abs(lep_phi[lep1] - lep_phi[lep2]) < 1.8: #lepton separtion in phi 

                            #################################
                            ### Dilepton system requirements
                            #################################

                            #Initialse (set up) an empty 4 vector for dilepton system
                            dilep_four_mmtm = TLorentzVector()

                            #Loop through our list of lepton indices
                            for i in goodLeps:

                                #Initialse (set up) an empty 4 vector for each lepton
                                lep_i = TLorentzVector()
                                
                                lep_pt = event["lep_pt"][i]
                                lep_eta = event["lep_eta"][i]
                                lep_phi = event["lep_phi"][i]
                                lep_E = event["lep_E"][i]
                                #Retrieve the lepton's 4 momentum components from the tree
                                lep_i.SetPtEtaPhiE(lep_pt, lep_eta, lep_phi, lep_E)

                                #Store lepton's 4 momentum
                                dilep_four_mmtm += lep_i
                                
                            # Dilepton system pT > 30 GeV
                            if dilep_four_mmtm.Pt() > 30000:

                                if (dilep_four_mmtm.M() > 10000) and (dilep_four_mmtm.M() < 55000):

                                    #####################
                                    ### MET requirements
                                    #####################
                                    
                                    met_et = event["met_et"]
                                    met_phi = event["met_phi"]
                                    #Initialse (set up) an empty 4 vector for the event's MET and fill from tree
                                    met_four_mom = TLorentzVector()
                                    met_four_mom.SetPtEtaPhiE(met_et,0,met_phi,met_et)

                                    #MET > 30 GeV
                                    if met_four_mom.Pt() > 30000:

                                        #Diffence in phi between the dilepton system and the MET < pi/2
                                        if abs(dilep_four_mmtm.Phi()-met_four_mom.Phi()) < 1.571:

                                            #####################
                                            ### Full llvv system
                                            #####################
                                            system_four_mom = dilep_four_mmtm + met_four_mom
                                            
                                            #Use the keyword weight to specify the weight of the evwnt
                                            return (system_four_mom.Mt()/1000, weight)

def analise_event_real(event):
    """
    Function which executes the analysis flow for the Higgs production cross-section measurement in the H->WW
    decay channel.
    
    Fills a histogram with mT(llvv) of events which pass the full set of cuts 
    
    Parameters
    ----------
    data : A Ttree containing data / background information
    
    hist : The name of the histogram to be filled with mT(llvv) values
    
    mode : A flag to tell the function if it is looping over 'data' or 'mc'
    """
        
    #############################
    ### Event-level requirements
    #############################
    
    #If event is MC: Reweight it
    weight = 1
        
    trigE = event["trigE"]
    trigM = event["trigM"]
    #If the event passes either the electron or muon trigger
    if trigE or trigM:
        
        ####Lepton preselections
        goodLeps = goodLeptons(event) #If the datafiles were not already filtered by number of leptons

        ###################################
        ### Individual lepton requirements
        ###################################

        if len(goodLeps) == 2: #Exactly two good leptons...
            lep1 = goodLeps[0] #INDICES of the good leptons
            lep2 = goodLeps[1]
            
            lep_type = event["lep_type"]
            if lep_type[lep1] != lep_type[lep2]: #... with different flavour
                
                lep_charge = event["lep_charge"]
                if lep_charge[lep1] != lep_charge[lep2]: #... and opposite charge...
                    
                    lep_pt = event["lep_pt"]
                    if (lep_pt[lep1] > 22000) and (lep_pt[lep2] > 15000): #pT requirements
                        #Note: TTrees always sort objects in descending pT order
                        
                        lep_phi = event["lep_phi"]
                        if abs(lep_phi[lep1] - lep_phi[lep2]) < 1.8: #lepton separtion in phi 

                            #################################
                            ### Dilepton system requirements
                            #################################

                            #Initialse (set up) an empty 4 vector for dilepton system
                            dilep_four_mmtm = TLorentzVector()

                            #Loop through our list of lepton indices
                            for i in goodLeps:

                                #Initialse (set up) an empty 4 vector for each lepton
                                lep_i = TLorentzVector()
                                
                                lep_pt = event["lep_pt"][i]
                                lep_eta = event["lep_eta"][i]
                                lep_phi = event["lep_phi"][i]
                                lep_E = event["lep_E"][i]
                                #Retrieve the lepton's 4 momentum components from the tree
                                lep_i.SetPtEtaPhiE(lep_pt, lep_eta, lep_phi, lep_E)

                                #Store lepton's 4 momentum
                                dilep_four_mmtm += lep_i
                                
                            # Dilepton system pT > 30 GeV
                            if dilep_four_mmtm.Pt() > 30000:

                                if (dilep_four_mmtm.M() > 10000) and (dilep_four_mmtm.M() < 55000):

                                    #####################
                                    ### MET requirements
                                    #####################
                                    
                                    met_et = event["met_et"]
                                    met_phi = event["met_phi"]
                                    #Initialse (set up) an empty 4 vector for the event's MET and fill from tree
                                    met_four_mom = TLorentzVector()
                                    met_four_mom.SetPtEtaPhiE(met_et,0,met_phi,met_et)

                                    #MET > 30 GeV
                                    if met_four_mom.Pt() > 30000:

                                        #Diffence in phi between the dilepton system and the MET < pi/2
                                        if abs(dilep_four_mmtm.Phi()-met_four_mom.Phi()) < 1.571:

                                            #####################
                                            ### Full llvv system
                                            #####################
                                            system_four_mom = dilep_four_mmtm + met_four_mom
                                            
                                            #Use the keyword weight to specify the weight of the evwnt
                                            return (system_four_mom.Mt()/1000, weight)





# get data 

print("getting real data")
real_data = data_files(real_data_links[:1],selected_events,"real_data")
print("getting mc data")
mc_data = data_files(simulated_data,selected_events,"mc_data")

print("DONE getting data!")
# proccess each set of data 

threads = multiprocessing.cpu_count()

def loading(value):
    percentage = f"{value*100:.2f}%"
    print(f"{percentage}\r",end="")

print("proccessing mc data")

proccessed_mc_data = crochet(analise_event_mc,mc_data,threads,loading)
proccessed_mc_data.load_fraction = 1
proccessed_mc_data = proccessed_mc_data.run()

print("done proccessing! \n cleaning data...\r",end="")

clean_mc_data = [i for i in proccessed_mc_data if i is not None]

print("saving data...     ")

file_name = str(input("name of file :"))
file = open(f"{file_name}.json","wb")
pickle.dump(clean_mc_data,file)

print("data saved!")

# clearing vars 

clean_mc_data = ""
mc_data = ""

print("starting next data set.. ")

proccessed_real_data = crochet(analise_event_real,real_data,threads,loading)
proccessed_real_data.load_fraction = 5000
proccessed_real_data = proccessed_real_data.run()

print("done proccessing! \n cleaning data...\r",end="")

clean_real_data = [i for i in proccessed_real_data if i is not None]

print("saving data...     ")

file_name = str(input("name of file :"))
file = open(f"{file_name}.json","wb")
pickle.dump(clean_real_data,file)

print("data saved!")