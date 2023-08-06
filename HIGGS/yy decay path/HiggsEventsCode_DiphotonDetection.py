import  matplotlib.pyplot as plt , hist ,loading_bars as ldbr ,time ,pickle,multiprocessing
from TLorentzVector import TLorentzVector
from hist import Hist
from crochet import crochet
from rootFile import data_files

data_links = ["https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/GamGam/Data/data_A.GamGam.root",
              "https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/GamGam/Data/data_B.GamGam.root",
              "https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/GamGam/Data/data_C.GamGam.root",
              "https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/GamGam/Data/data_D.GamGam.root"              
              ] 

selected_events = ["photon_ptcone30",
                   "photon_etcone20",
                   "photon_isTightID",
                   "photon_eta",
                   "photon_phi",
                   "photon_n",
                   "photon_E",
                   "photon_pt", 
                   "trigP"
                   ]

def locateGoodPhotons(dat):
    """
    Function which returns the index of photons in the event which pass our quality requirements.
    These are:
        - Event passes photon trigger
        - Photon is identified as such, passing 'Tight' requirements 
            - This means we are very sure our photon is indeed a photon, but we might lose some photons that are 
              less obvious in the process. The opposite of this is the 'Loose' requirement, where we are less
              sure that our photon is a photon, but we are less likely to miss real ones .
        - Photon has pT > 25 GeV (or 25000 MeV)
        - Photon is in the 'central' region of ATLAS i.e. it has |eta| < 2.37
        - Photon does not fall in the 'transition region' between ATLAS's inner detector barrell
          and ECal endcap i.e. 1.37 <= |eta| <= 1.52
          
    Parameters
    ----------
    dat : array from TTree for this event
    
    """
    
    ## Checking the event passes the photon trigger
    #trigP = tree["trigP"]
    trigP = dat["trigP"]
    if trigP == True:
        
        # Initialise (set up) the variables we want to return
        goodphoton_index = [] #Indices (position in list of event's photons) of our good photons
            
        ## Loop through all the photons in the event
        photon_n = dat["photon_n"]
        for j in range(0,photon_n):
            
            ## Check photon ID
            photon_isTight = dat["photon_isTightID"][j]
            if(photon_isTight):
                photon_pt = dat["photon_pt"][j]
                # Check photon has a large enough pT
                if (j==0 and photon_pt > 35000) or (j==1 and photon_pt > 25000):
                    photon_eta = dat["photon_eta"][j]
                    # Check photon eta is in the 'central' region
                    if (abs(photon_eta) < 2.37):
                  
                      # Exclude "transition region" between ID barrell and ECal endcap
                      if (abs(photon_eta) < 1.37 or abs(photon_eta) > 1.52):

                        goodphoton_index.append(j) # Store photon's index
                    
        return goodphoton_index # Return list of good photon indices

def photonIsolation(dat,photon_indices):
    """
    Function which returns True if all photons are well-isolated, otherwise returns false.
    
    A photon is considered 'isolated' if the transverse momentum and transverse energy in the detector, within 
    a particular radius around the photon (variables called 'ptcone30' and 'etcone20'), is below a certain threshold compared to the photon's 
    transverse momentum (don't worry too much about the details!).
    
    Parameters
    ----------
    dat : array from TTree for this event
    
    photon_indices : List containing the indices in the TTree of our photons of interest
    
    """
    
    # Loop through our list of photon indices
    for i in photon_indices:
        photon_ptcone30 = dat["photon_ptcone30"][i]
        photon_pt = dat["photon_pt"][i]
        photon_etcone20 = dat["photon_etcone20"][i]
        
        # If each photon passes isolation requirements...
        if((photon_ptcone30 / photon_pt < 0.065) and 
           (photon_etcone20 / photon_pt < 0.065)):
            continue #...keep the loop going 
        
        # If any fail, break the loop and return False
        else: 
            return False
    
    # If the loop is able to finish, i.e. all photons are well-isolated, return True
    return True

def photonFourMomentum(dat, photon_indices):
    """
    Function which returns the 4 momenta of a list of photons in an event as a list of TLorentzVectors
    
    Parameters
    ----------
    dat : array from TTree for this event
    
    photon_indices : List containing the indices in the TTree of our photons of interest
    
    """
    
    photon_four_momenta = []
    
    # Loop through our list of photon indices
    for i in photon_indices:
    
        # Initialse (set up) an empty 4 vector for each photon
        Photon_i = TLorentzVector()
    
        photon_pt = dat["photon_pt"][i]
        photon_eta = dat["photon_eta"][i]
        photon_phi = dat["photon_phi"][i]
        photon_E = dat["photon_E"][i]
        # Retrieve the photon's 4 momentum components from the tree
        # Convert from MeV to GeV where needed by dividing by 1000
        Photon_i.SetPtEtaPhiE(photon_pt/1000., photon_eta, photon_phi, photon_E/1000.)
        
        # Store photon's 4 momentum
        photon_four_momenta.append(Photon_i)
        
        
    return photon_four_momenta

def sumFourMomentum(four_momenta):
    """
    Function which sums a list of four-momenta, and returns the resultant four-momentum of the system
    
    Parameters
    ----------
    four_momenta : List of TLorentzVectors containing the four-momentum of each object in the system
    
    """
    
    # Initialise (set up) TLorentzVector for our momentum sum
    four_mom_sum = TLorentzVector()
    for obj in four_momenta:
        four_mom_sum += obj
        
    return four_mom_sum
 
def anlise_data(event):
    
    #2) Identify exactly two 'good quality photons'
    goodphoton_indices = locateGoodPhotons(event)
    if len(goodphoton_indices) == 2:
        
        #3) Check our good quality photons are well-isolated
        photons_are_isolated = photonIsolation(event, goodphoton_indices)
        
        if photons_are_isolated:
        
            #4) Convert 4-momentum from MeV to GeV
            photon_four_momenta = photonFourMomentum(event, goodphoton_indices)
            
            #5) Add the 4-momenta together
            Photon_12 = sumFourMomentum(photon_four_momenta)
            
            #6) Calculate the diphoton invariant mass
            inv_mass = Photon_12.M() #Calculated invariant mass
            
            photon_pt = event["photon_pt"]
            #7) Check each photon makes up a minimum fraction of the diphoton system invariant mass
            if ((photon_pt[0]/inv_mass) > 0.35) and ((photon_pt[1]/inv_mass) > 0.25):
                
                #8) Fill histogram with invariant mass
                return inv_mass

def loading(value):
    percentage = f"{value*100:.2f}%"
    print(f"{percentage}\r",end="")

events = data_files(data_links,selected_events)

print(f"starting proccessing {len(events)} events ...")

threads = multiprocessing.cpu_count()

proccessed_data = crochet(anlise_data,events,threads,loading)
proccessed_data.load_fraction = 5000
proccessed_data = proccessed_data.run()

print("done proccessing! \n cleaning data...\r",end="")

clean_data = [i for i in proccessed_data if i is not None]

print("saving data...     ")

file_name = str(input("name of file :"))
file = open(f"{file_name}.json","wb")
pickle.dump(clean_data,file)

print("data saved!")









    

