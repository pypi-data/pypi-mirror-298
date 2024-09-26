import calendar
import datetime
from calendar_functions import *

year = datetime.datetime.now().year
month = datetime.datetime.now().month
data = load_entries()

def main():
    while True:
        print("\n1. Show current month")
        print("2. Show current year")
        print("3. Add entry")
        print("4. Show entry")
        print("5. Delete entry")
        print("6. Change entry")
        print("7. Show all birthdays/events or meetings")
        print("q. Exit")
        
        option = input("\nSelect an option: ")
        if option == '1':
          display_current_month()
        elif option == '2':
          display_current_year()  
        elif option == '3':
          type = input('Choose a type (b=birthday, e=event or m=meeting): ')
          name_or_description = input('Please enter a name (if type=birthday) or description (if type=event/meeting): ')
          date = (input('Enter the date: '))
          add_entry(data,type,name_or_description,date)   
        elif option == '4':
          type = input('Choose a type (b=birthday, e=event or m=meeting): ')
          name_or_description = (input('Enter the name/description of the entry you want to display: '))
          display_entry(data,type,name_or_description)                                                        
        elif option == '5':
          type = input('Choose a type (b=birthday, e=event or m=meeting): ')
          name_or_description = (input('Enter the name/description of the entry you want to delete: '))
          delete_entry(data,type,name_or_description)  
        elif option == '6':
          type = input('Choose a type (b=birthday, e=event or m=meeting): ')
          name_or_description = (input('Enter the name/description of the entry you want to change: ')) 
          display_entry(data,type,name_or_description)
          new_date = (input('Enter the new date: '))
          change_entry(data,type,name_or_description,new_date)
        elif option == '7':
          type = input('Select the type of entries do you want to display (b=birthdays, e=events or m=meetings): ')
          show_all(data,type)
        elif option == 'q':
            break
        else:
            print("Invalid option. Please try again.")    
main() 
