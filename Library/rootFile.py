import uproot4 as uproot
import numpy as np
import pickle
#main body so far
def data_files(links: list, selected_data: list,cache_name:str):

  selected_events = None  # this is the variable we will store the combined arrrays in

  # check for previous data in BigData.json
  try:
    file = open(f"{cache_name}.json", "rb")
    selected_events = pickle.load(file)
  except FileNotFoundError: # if cant open file then just continue
    print("not past data found, ",end="")
  except EOFError :
    print("file cant be read, ",end="")
    pass
  else:  # if can open , ask user if they want to use this data or get new data
    while True:  # loop untill valid responce has been inputed
      load_choice = str(input("past data found , load data? [y/n] :")).lower()
      if load_choice in [
          "y", "yes"
      ]:  # if the awnser is yes then just return the loaded past data
        return selected_events
      elif load_choice in [
          "n", "no"
      ]:  # if awnser is no then break from loop and continue
        print("ignoring past data, ", end="")
        break
      else:  # if input is not yes or no
        print("invalid response >:(")

  # everything past this point will only run if no past data is found or if the user decided not to use past data

  print("loading data from sever...")

  files_out = []

  for index, link in enumerate(links):
    link += ":mini"  # specifies that the tree we are getting is mini , just speeds up downloads and also means we dont have to get the tree before we do anything
    print(f"downloading link {index+1}")  # print current link downloading
    try:
      
        file = uproot.open(link)  # opens link
        print(f"downloaded! ",end="")
    except:
        print("download timed out , Skipping link.")
        continue
    print("converting into array...",end="")
    file_selected_data = file.arrays(
        selected_data
    )  # gets selected events from file and puts them in an array
    print("done!")
    files_out.append(file_selected_data)  # add downloaded data to list
  print("done downloading")
  # now we need to combine the events into one array and then save it as a .json file
  print("combining data...")

  selected_events = np.concatenate(files_out)
  print("saving data...",end="")
  file = open(f"{cache_name}.json", "wb")
  pickle.dump(selected_events,file)
  print("done!")

  return selected_events

