import calendar
import datetime
year = datetime.datetime.now().year
month = datetime.datetime.now().month
import json

def load_entries():
    '''Loads entries from json file.'''
    with open('filename.json') as f:
        data = json.load(f) 
    return data['entries']

def save_entry(entries):
    '''Saves entries and stores them in a json file. '''
    with open('filename.json','w') as file:
        json.dump({"entries":entries},file,indent=4)

def display_current_month():
    '''Calculates and displays the current month. '''                                      
    print()
    print(calendar.month(year,month))

def display_current_year():
    '''Calculates and displays the current year. '''                               
    print()
    print(calendar.calendar(year))

def add_entry(data,type,name_or_description,date):
    '''Assigns the data of new entries and stores them in a specific dictionary (json file).'''
    if type == 'b':                                    
        data["birthdays"].update({name_or_description : date})               
    elif type == 'm':
        data["meetings"].update({name_or_description : date})
    elif type == 'e':
        data["events"].update({name_or_description : date})   
    save_entry(data)
    load_entries()
    print("Entry saved!")  
                                                             
def get_entry(data,type,name_or_description):
    '''Searches a specific entry in the dictionary's (within the json file).'''
    if type == 'b': 
        dict_birth = data["birthdays"]
        for key,value in dict_birth.items():
            if key == name_or_description:
                return key,value
        else:
            return 'No entry found.'
    if type == 'm':
        dict_meet = data["meetings"] 
        for key,value in dict_meet.items():
            if key == name_or_description:
                return key,value
        else:
            return 'No entry found.'
    if type == 'e': 
        dict_event = data["events"]
        for key,value in dict_event.items():
            if key == name_or_description:
                return key,value
        else:
            return 'No entry found.'
        
def display_entry(data,type,name_or_description):  
    '''Displays specific entry (which the user is searching for).'''
    entry = get_entry(data,type,name_or_description)
    if type == 'b': 
        dict_birth = data["birthdays"]
        if name_or_description in dict_birth:
            print(f'{name_or_description} : {entry[1]}') 
        else:
            print("No entry found.")    
    if type == 'm': 
        dict_meet = data["meetings"]
        if name_or_description in dict_meet:
            print(f'{name_or_description} : {entry[1]}') 
        else:
            print("No entry found.")           
    if type == 'e': 
        dict_event = data["events"]
        if name_or_description in dict_event:
            print(f'{name_or_description} : {entry[1]}') 
        else:
            print("No entry found.")                   
    
def delete_entry(data,type,name_or_description):
    '''Deletes a selected entry from the dictionary (within the json file).'''
    entry = get_entry(data,type,name_or_description)
    if entry[0] in data["birthdays"]:
        del data["birthdays"][entry[0]] 
        print("Entry deleted!")
    elif entry[0] in data["meetings"]:
        del data["meetings"][entry[0]]
        print("Entry deleted!")
    elif entry[0] in data["events"]:
        del data["events"][entry[0]]
        print("Entry deleted!")
    elif entry[0] not in data:
        print('No entry found.')    
    save_entry(data) 
    load_entries()       
    
def change_entry(data,type,name_or_description,new_date):
    '''Allows the user to change the date/time (value) of an entry.'''
    entry = get_entry(data,type,name_or_description)  
    if entry[0] in data["birthdays"]:
        data["birthdays"].update({entry[0] : new_date})  
        print("Entry successfully changed!") 
    elif entry[0] in data["meetings"]:
        data["meetings"].update({entry[0] : new_date})
        print("Entry successfully changed!") 
    elif entry[0] in data["events"]:
        data["events"].update({entry[0] : new_date}) 
        print("Entry successfully changed!") 
    elif entry[0] not in data:
        print('No entry found.')       
    save_entry(data)      
    load_entries()
    
def show_all(data,type):
    '''Lists all entries of a type.'''
    if type == 'b': 
        dict_birth = data["birthdays"]
        for key,value in dict_birth.items():
            print(key,value)
    elif type == 'm':
        dict_meet = data["meetings"]
        for key,value in dict_meet.items():
            print(key,value)
    elif type == 'e':
        dict_event = data["events"]
        for key,value in dict_event.items():
            print(key,value)    
    
    
