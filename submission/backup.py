import time
import tkinter as tk
import matplotlib.pyplot as plt
from csv import writer, reader

from gui import App

# ctrl + b, down button (to switch)

def convert_to_type(value):
    try:
        return float(value)
    except ValueError:
        try:
            return int(value)
        except ValueError:
            return value


def opif(i: int, o: int):
    if i == o:
        print(f"Option Pick mapper - {i}")
        return True
    else:
        return False


def op1(i: int, opif, file):
    if opif(i, 1):
       reader_obj = reader(file)
       
       data = list(reader_obj)
       
       del data[0] #delete the header from csv file
       header = ['No', 'Name', 'Capitalisation', 'QtyBought', 'Bought Price', 'Current Price']
       data.insert(0,header)
       
       num=1
       for row in data[1:]:     #insert the values for number column
           row.insert(0,num)
           num +=1


       num_columns = len(header)
       column_widths=[]
       formatted_header=[]
       for col_index in range (num_columns):
            max_column_width= len(str(data[0][col_index]))
            for row in data:
               if len(str(row[col_index]))>max_column_width:
                   max_column_width= len(str(row[col_index]))
            column_widths.append(max_column_width)
       
            header_item= header[col_index] #retrieve the header name for this column
            column_width=column_widths[col_index] #retrieve the max width for this column
            formatted_header.append('{:>{width}}'.format(header_item, width=column_width)) #format header to right align within the available space (width = max column width)
       
       header_row = ' | '.join(formatted_header)
       print(header_row)
       
       separator_line= '-' *(sum(column_widths) + len(column_widths) * 3 - 1)
       print(separator_line)
       
       formatted_rows=[]
       for row in data[1:]:
           formatted_row=[]
           for col_index in range(num_columns):
               row_item=row[col_index] #retrieve the item for this column
               column_width=column_widths[col_index] #retrieve the max width for this column
               formatted_row.append('{:>{width}}'.format(row_item, width=column_width))


           formatted_rows.append(' | '.join(formatted_row))
   
       for row in formatted_rows:
            print(row)
       
       print(separator_line)
           
def op2(i: int, opif, file, convert_to_type):
    if opif(i, 2):
        entries = []
        rows = list(reader(file))
        # CRYPTOCURRENCY NAME INPUT
        while True:
           name = input("Enter cryptocurrency Name or E to exit: ")
           if name.upper() == "E":
               print("Process Ended")
               break
           elif not any(row[0] == name for row in rows):
               entries.append(name)
           else:
               print("Cryptocurrency already exists!")
               continue


           #INITIALIZE BREAKER VARIABLE
           breaker = False


           while True:
               cap = input("Enter Market Cap of Crypto: High, Mid, Low or E to exit: ")
               match cap.lower().capitalize():
                   case "High" | "Mid" | "Low":
                       entries.append(cap.lower().capitalize())
                       break
                   case "E":
                       breaker = True
                       break
                   case _:
                       print("Try again mate!")
                       continue
           if breaker:
               print("Cryptocurrency not added because process ended!")
               break


           while True:
               qty = convert_to_type(input("Enter Quantity of Crypto bought: "))
               match qty:
                   case int() | float():
                       entries.append(qty)
                       break
                   case str():
                       if qty.lower().capitalize() == "E":
                           breaker = True
                           break
                       else:
                           continue
           if breaker:
               print("Cryptocurrency not added because process ended!")
               break


           while True:
               bip = convert_to_type(input("Enter buy-in price of Crypto bought: "))
               match bip:
                   case int() | float():
                       entries.append(bip)
                       break
                   case str():
                       if bip.lower().capitalize() == "E":
                           breaker = True
                           break
                       else:
                           continue
           if breaker:
               print("Cryptocurrency not added because process ended!")
               break


           while True:
               mkp = convert_to_type(input("Enter market price of Crypto bought: "))
               match mkp:
                   case int() | float():
                       entries.append(mkp)
                       break
                   case str():
                       if mkp.lower().capitalize() == "E":
                           breaker = True
                           break
                       else:
                           continue
           if breaker:
               print("Cryptocurrency not added becaused process ended!")
               break


           #Overwrite the list of rows inside cryptoProfile AMENDED.csv
           rows.append(entries)
           file.seek(0) #go to the first row in the csv
           write=writer(file,delimiter=',')
           write.writerows(rows)
           entries =[]
           
           print("Cryptocurrency now added to database!")


def op3(i: int, opif, checker, file, convert_to_type):
   if opif(i, 3):
       rows = list(reader(file))


       # SELECT CRYPTOCURRENCY TO EDIT


       while True:
           print("No - CryptoCurrency")
           print("---------------------------")
           for row in rows[1:]:
               if row[0] != '' and row[0] != 'Name':
                   print(f"{rows.index(row)} - {row[0]}")
           print("---------------------------")
           option = input(f"Enter 1 to {rows.__len__()-1}, E to exit: ")


           try:
               while True:
                 
                   # SELECT HEADER TO EDIT


                   print("---------------------------")
                   headers = ["Name", "Market Cap", "Quantity", "Buy-In", "Market Price"]
                   i1_option = int(option)
                   edit_list = rows[i1_option][0:5]
                   mix_iter = zip(headers, edit_list)


                   for (header, to_edit) in mix_iter:
                       print(f"{headers.index(header)}. {header} - {to_edit}")


                   h_option = input(f"Enter 0 to {headers.__len__()-1}, E to break: ")
               
                   try:
                       i_option = int(h_option)


                       # Edit Schema
                       match i_option:
                           case 0:
                               while True:
                                   edit = input(f"Input the value you want to edit for {headers[i_option]}: ")
                                   names = []


                                   for row in rows:
                                       names.append(row[0].lower())


                                   if edit.lower() in names:
                                       print("Cryptocurrency already exists!")
                                       continue
                                   elif edit.lower().capitalize() == "E":
                                       print("Ended editing name!")
                                       break
                                   else:
                                       print(f"Cryptocurrency name edited to {edit}")
                                       rows[i1_option][i_option] = edit
                                       break
                                 
                           case 1:
                               while True:
                                   edit = input(f"Input the value you want to edit for {headers[i_option]}: ")
                                   cap_list = ["High", "Mid", "Low"]
                                   if edit in cap_list:
                                       rows[i1_option][i_option] = edit
                                       break
                                   else:
                                       print("Option not part of the Market Cap!")
                                       continue


                           case 2 | 3 | 4:
                               while True:
                                   edit = convert_to_type(input(f"Input the value you want to edit for {headers[i_option]}: "))
                                   match edit:
                                       case int() | float():
                                           rows[i1_option][i_option] = edit
                                           print(f"{headers[i_option]} has been edited!")
                                           break
                                       case str():
                                           if edit.lower().capitalize() == "E":
                                               print(f"{edit_list[i_option]} process has been stopped!")
                                               break
                                           else:
                                               print("Try again!")
                                               continue


                       print(rows[i1_option])
                       print("---------------------------")


                   except ValueError:
                       str(h_option)
                       match h_option.capitalize():
                           case "E":
                               print(f"Editing {edit_list[0]} Ended!")
                               print("---------------------------")
                               break
                           case _:
                               print("Try again!")
                               continue


                   except IndexError:
                       print("Index Out of Range!")
                       continue


           except ValueError:
               try:
                   str(option)
                   match option.capitalize():
                       case "E":
                           print("Amending Process Ended!")
                           break
                       case _:
                           print("Try again!")
               except:
                   print("Wrong input type!")
                   continue
               
        #overwrite to cryptoProfile_AMENDED.csv
       file.seek(0) #go to the first row in the csv
       write=writer(file,delimiter=',')
       write.writerows(rows)
       
def op4(i: int, opif, file):
   if opif(i, 4):
       reader_obj = reader(file)
       
       data = list(reader_obj)
           
       while True:
           for row in data[1:]:
               if row[0] != '' and row[0] != 'Name':
                   print(f"{data.index(row)} - {row[0]}")
           print("---------------------------")
           option = input(f"Enter 1 to {data.__len__()-1} to delete!, E to exit: ")


           try:
               i_option = int(option)
               if i_option == 0:
                   print("You can't delete the first row!")
                   continue
               else:
                   for_string = data[i_option][0]
                   data.pop(i_option)
                   print(f"You removed the {for_string} cryptocurrency!")
               
           except ValueError:
               str(option)
               match option.capitalize():
                   case "E":
                       print("Removing cryptocurrencies process ended!")
                       print("---------------------------")
                       break
                   case _:
                       print("Try again!")
                       continue
        #overwrite to cryptoProfile_AMENDED.csv
       file.seek(0) #go to the first row in the csv
       write=writer(file,delimiter=',')
       write.writerows(data)
       file.truncate()
       
'''
'''
def op5(i: int, opif, file, convert_to_type):
    if opif(i, 5):
        rows = list(reader(file))
       
        #append the headers
        additional_headers=['Total Invested', 'Invested Portfolio Size','Total Current Value','Profit/Loss','Current Portfolio Size']
        for header in additional_headers:
            rows[0].append(header)
           
        #calculate & append Total Invested
        total_total_i= 0
        for item in rows[1:]:
            currenttotal_i= round(convert_to_type(item[2])*convert_to_type(item[3]))
            item.append(currenttotal_i)
            total_total_i+=currenttotal_i
       
        #calculate & append Invested Portfolio Size
        for item in rows[1:]:
            currentinvested_p_s=str(round((convert_to_type(item[5])/total_total_i)*100,2))+'%'
            item.append(currentinvested_p_s)
       
        #calculate & append Total Current Value, Profit/Loss
        total_total_c_v=0
        total_pl=0
        for item in rows[1:]:
            current_total_c_v=round(convert_to_type(item[2])*convert_to_type(item[4]))
            total_total_c_v+=current_total_c_v
            current_pl=current_total_c_v-convert_to_type(item[5])
            total_pl+=current_pl
            item.append(current_total_c_v)
            item.append(current_pl)
       
        #calculate & append Current Portfolio Size
        for item in rows[1:]:
            current_current_p_s=str(round((convert_to_type(item[7])/total_total_c_v)*100,2))+'%'
            item.append(current_current_p_s)
       
        #append sum row
        sum_row=['','','','','SUM',total_total_i,'100%',total_total_c_v,total_pl,'100%']
        rows.append(sum_row)


        #delete market cap from the 2D list
        for row in rows:
            del row[1]
       
        #add numbering in the first column for the 2D list
        rows[0].insert(0,"No.")
        rows[-1].insert(0,'')
        num=1
        for row  in rows[1:-1]:
            row.insert(0,num)
            num +=1
         
        #print the portfolio statement
        num_columns = len(rows[0])
        column_widths=[]
        formatted_header=[]
        for col_index in range (num_columns):
            max_column_width= len(str(rows[0][col_index]))
            for row in rows:
               if len(str(row[col_index]))>max_column_width:
                   max_column_width= len(str(row[col_index]))
            column_widths.append(max_column_width)
       
            header_item= rows[0][col_index] #retrieve the header name for this column
            column_width=column_widths[col_index] #retrieve the max width for this column
            formatted_header.append('{:>{width}}'.format(header_item, width=column_width)) #format header to right align within the available space (width = max column width)
       
        header_row = ' | '.join(formatted_header)
        print(header_row)
       
        separator_line= '-' *(sum(column_widths) + len(column_widths) * 3 - 1)
        print(separator_line)
       
        formatted_rows=[]
        for row in rows[1:]:
           formatted_row=[]
           for col_index in range(num_columns):
               row_item=row[col_index] #retrieve the item for this column
               column_width=column_widths[col_index] #retrieve the max width for this column
               formatted_row.append('{:>{width}}'.format(row_item, width=column_width))


           formatted_rows.append(' | '.join(formatted_row))
   
        for row in formatted_rows:
            print(row)
       
        print(separator_line)
       
def op6(i: int, opif, file):
    '''Name of function: Portfolio Overview with Visualisation - <Chrissandella - p2212476>
       Purpose         : To display a summary of the cryptocurrency portfolio using pie charts and bar chart
       Description     : This function allows user to choose from 3 options. The function will perform input validation
                         and display the appropriate charts according to user's option. The data is first read from the csv file into a 2D list
                         before calculations are performed and appended to the list. Thereafter, charts are constructed using matplotlib library.'''
    if opif(i, 6):
        rows=list(reader(file))
        while True:
        #allow user to choose
            print("---------------------------")
            print("Cryptocurrency Portfolio Overview")
            print("---------------------------")
            print("1. Display portfolio diversification according to invested amount")
            print("2. Display portfolio diversification according to asset value")
            print("3. Display profit or loss")
            print("E. Exit Menu")
            print("---------------------------")
            i = input("Select an option: ")
            print("---------------------------")
           
            if str(i).upper() =='E':
                print("Menu exited")
                print("---------------------------")
                break
           
            try:
                i = int(i)
               
                #append the headers
                additional_headers=['Total Invested', 'Invested Portfolio Size','Total Current Value','Profit/Loss','Current Portfolio Size']
                for header in additional_headers:
                    rows[0].append(header)
                   
                #calculate & append Total Invested
                total_total_i= 0
                for item in rows[1:]:
                    currenttotal_i= round(convert_to_type(item[2])*convert_to_type(item[3]))
                    item.append(currenttotal_i)
                    total_total_i+=currenttotal_i
               
                #calculate & append Invested Portfolio Size
                for item in rows[1:]:
                    currentinvested_p_s=str(round((convert_to_type(item[5])/total_total_i)*100,2))+'%'
                    item.append(currentinvested_p_s)
               
                #calculate & append Total Current Value, Profit/Loss
                total_total_c_v=0
                total_pl=0
                for item in rows[1:]:
                    current_total_c_v=round(convert_to_type(item[2])*convert_to_type(item[4]))
                    total_total_c_v+=current_total_c_v
                    current_pl=current_total_c_v-convert_to_type(item[5])
                    total_pl+=current_pl
                    item.append(current_total_c_v)
                    item.append(current_pl)
               
                #calculate & append Current Portfolio Size
                for item in rows[1:]:
                    current_current_p_s=str(round((convert_to_type(item[7])/total_total_c_v)*100,2))+'%'
                    item.append(current_current_p_s)
               
                # display portfolio diversification according to invested amount    
                if i==1:
                    labels=[]
                    value=[]
                    for i in rows[1:]:
                        labels.append(i[0] +" $"+ f'{i[5]:,}')
                        value.append(i[5])
                    plt.figure(figsize=(13,11))
                    pie= plt.pie(value,autopct='%1.1f%%',pctdistance=1.1, startangle=270)
                    plt.axis('equal')
                    plt.legend( loc = 'best', labels=labels)
                    plt.title("Portfolio Diversification According to Amount Invested")
                    plt.show()
                   
                # display portfolio diversification according to asset value
                elif i==2:
                    labels=[]
                    value=[]
                    for i in rows[1:]:
                        labels.append(i[0] +", $"+ f'{i[7]:,}')
                        value.append(i[7])
                    plt.figure(figsize=(13,11))
                    pie= plt.pie(value,autopct='%1.1f%%',pctdistance=1.1, startangle=270)
                    plt.axis('equal')
                    plt.legend( loc = 'best', labels=labels)
                    plt.title("Portfolio Diversification According to Total Current Value")
                    plt.show()
               
                # display profit/loss
                elif i==3:
                    labels=[]
                    value=[]
                    for i in rows[1:]:
                        labels.append(i[0])
                        value.append(i[8])
                    plt.bar(labels,value, color=["green" if v>0 else "red" for v in value])
                    plt.title('Profit or Loss')
                    plt.xticks(rotation=30)
                    for i, value in enumerate(value):
                        plt.text(
                            i,  # X position (bar index)
                            value + (1 if value > 0 else -1),  # Y position (slightly above/below the bar)
                            str(value),  # The text to display (the value)
                            ha="center",  # Horizontal alignment
                            va="bottom" if value > 0 else "top",  # Vertical alignment
                            fontsize=10
                            )
                    plt.show()
                   
                else:
                    print('Please select 1-3 or E to  exit.')    
                   
            except ValueError:
                print("Try again!")
                continue

def op7(i: int, opif, file):
    '''
    Name of function: Cryptocurrency Live & Historical Tracker with GUI - <Josh - p2110529>
    Purpose: To provide live and historical data of cryptocurrency coins with their market value,
            live value and other information with a graphical user interface for users to use the app
            with much comfort and convenience.
    Description: Pulls live and historical data of cryptocurrency from CoinGecko using the Demo API, utilising
                market and historical endpoints to get JSON data. Tkinter is used in this app for creating the gui
                for the user and also work with the API to present data into the interface. The Tkinter library also
                works with the matplotlib library to visualize the data pulled from the API.

    REQUIREMENTS -> CoinGecko API demo key

    DIRECTIONS: Inside api.py on line 8, a variable called key stores the API key you created by calling in the 
                os.environ.get("API) statement to retrieve the key from your environment variables but it can also
                be done with just a hardcoded api key

                First   : you must create your CoinGecko *DEMO* api from the website and retrieve the key
                    -it must be DEMO or PUBLIC or not the api wouldn't work

                Second  : set the API environment variable
                    Windows:
                        1. Open CMD
                        2. type in -> set API=**YOUR_API_KEY**
                        3. to see if it works -> echo %API%

                    Linux:
                        1. Open your terminal
                        2. type in -> export API=**YOUR_API_KEY**
                        3. to see if it works -> echo $API 

                            OR

                Second:
                    Set the key variable in line 8 of the api.py file to be the api key but hardcoded.
    '''
    if opif(i, 7):
        root = tk.Tk()
        app = App(root)
        root.mainloop()

def checker(i: int, s=1 ,e=7):
    if i < s or i > e:
        print("Option doesn't exist try again!")


def opexit(i: str):
    if i == "E":
        print("Program exited!")
        return True
    else:
        print("Try again!")
        return False


def main(op1, op2, op3, op4, op5, op6, op7, checker, opexit):
    with open('cryptoProfile AMENDED.csv', 'r+', newline='') as file:
       
        print("---------------------------")
        print("\rClass 02\r\n1. Edward Josh - p2110529\r\n2. Chrissandella - p2212476")
        print("---------------------------")
        print("Cryptocurrency Portfolio Application Main Menu")
        print("---------------------------")
        print("1. Display Cryptocurrency")
        print("2. Add Cryptocurrency")
        print("3. Amend Cryptocurrency")
        print("4. Remove Cryptocurrency")
        print("5. Cryptocurrency Portfolio Statement")
        print("6. Portfolio Overview with Visualization - <Chrissandella - p2212476>")
        print("7. Live & Historical Cryptocurrency Checker w/ GUI - <Josh - p2110529>")
        print("E. Exit Main Menu")
        print("---------------------------")
        i = input("Select an option: ")
        print("---------------------------")
       
        try:
            op1(int(i), opif, file)
            op2(int(i), opif, file, convert_to_type)
            op3(int(i), opif, checker, file, convert_to_type)
            op4(int(i), opif, file)
            op5(int(i), opif, file, convert_to_type)
            op6(int(i), opif, file)
            op7(int(i), opif, file)
            checker(int(i))
            return True
        except ValueError:
            r = opexit(i.upper())
            if r:
                return False
            else:
                return True
       


if __name__ == "__main__":
    while True:
        bin = main(op1, op2, op3, op4, op5, op6, op7, checker, opexit)
        time.sleep(2.5)
        if bin is False:
            break
