from Tkinter import *
from ttk import *
import datetime
import calendar
import tkMessageBox

root = Tk()                           # Create instance      
root.title("Prostate Cancer Clinical Trial")                 # Add a title
root.geometry("490x290") #size of root (canvas)
tabControl = Notebook(root)          # Create Tab Control
nccn_risk_tab = Frame(tabControl)            # Create a tab:NCCN Risk
tabControl.add(nccn_risk_tab, text='NCCN risk')      # Add the tabtab:NCCN Risk

date_cal_tab = Frame(tabControl)            # Create a tab: Date Calculation
tabControl.add(date_cal_tab, text='Date Calculation')      # Add the tab: Date Calculation


#creating psa entry box
psa = Entry(nccn_risk_tab)
psa.insert(0, "0.02")
psa.grid(row=2, column=1, pady=8)

#creating psa label
psa_lb = Label(nccn_risk_tab, text="PSA Level:")
psa_lb.grid(row=2, column=0, pady=8)

#creating cT Staging box
ct = StringVar(nccn_risk_tab)
ct.set("T0")

#creating cT Staging Options
ct_options = OptionMenu(nccn_risk_tab, ct, "T1", "T1a", "T1b", "T1c", "T2", "T2a",
                        "T2b", "T2c", "T3", "T3a", "T3b", "T4")
ct_options.grid(row = 0, column = 1)

#creating cT Staging label
ct_label = Label(nccn_risk_tab, text = "cT Staging")
ct_label.grid(row = 0, column = 0)

#creating Gleason Score entry box
Gleason_score = StringVar(nccn_risk_tab)
Gleason_score.set("3+3")

#creating Gleason Score Options
gs_options = OptionMenu(nccn_risk_tab, Gleason_score, "3+3", "3+4", "3+5", "4+3",
                        "4+4", "4+5", "5+3", "5+4", "5+5")
gs_options.grid(row = 1, column = 1)

#creating Gleason Score label
gs_label = Label(nccn_risk_tab, text = "Gleason Score")
gs_label.grid(row = 1, column = 0)

#creating Core involvement entry box
core_involvement = Entry(nccn_risk_tab)
core_involvement.insert(0, "0")
core_involvement.grid(row=4, column=1)

#Creating Core involvement label
core_involvement_lbl = Label(nccn_risk_tab, text = 'Core Involvement (%):')
core_involvement_lbl.grid(row=4, column=0, pady=4)

#Function for risk classification
def risk_classify():
    risk = ""
    if Gleason_score.get() in ["3+5", "4+4", "5+3", "4+5", "5+4", "5+5"]:
        risk = "High"
    elif ct.get() in ["T3", "T3a", "T3b", "T4"]:
        risk = "High"
    elif float(psa.get()) > 20:
        risk = "High"
    elif Gleason_score.get() in ["3+4", "4+3"]:
        risk = "Intermediate"
    elif ct.get() in ["T2b", "T2c"]:
        risk = "Intermediate"
    elif float(psa.get()) >= 10 and float(psa.get()) <= 20:
        risk = "Intermediate"
    elif Gleason_score.get() in ["3+3"]:
        risk = "Low"
    elif ct.get() in ["T1", "T1a", "T1b", "T1c", "T2", "T2a"]:
        risk = "Low"    
    elif float(psa.get()) < 10:
        risk = "Low"
    else:
        risk = "Unknown"
    return risk


#function to classify favorable or infavorable intermediate risk using risk count
def risk_count(count):
    intermediate_risk = ""
    if int(count) == -1:
        intermediate_risk = "N.A."
    elif int(count) < 2:
        intermediate_risk = "Favorable"
    elif int(count) >= 2:
        intermediate_risk = "Unfavorable"
    else:
        intermediate_risk = "Unknown"
    return intermediate_risk
        
#function to determine favorable or infavorable intermediate risk using risk count from previous function
def intermediate_risk(risk):
    count = 0
    if risk == "Intermediate":
        if float(core_involvement.get()) > 50:
            count += 1
        if Gleason_score.get() in ["4+4", "4+3", "4+5"]:
            count += 1
        if ct.get() in ["T2", "T2a", "T2b", "T2c"]:
            count += 0.5
        if Gleason_score.get() in ["3+4", "4+3"]:
            count += 0.5
        if float(psa.get()) >= 10 and float(psa.get()) <= 20:
            count += 0.5
    else:
        count = -1
    return (risk_count(count), count)


#Function for output
def output_risk():
    output_entry.delete("1.0",END)
    try:
        risk = str(risk_classify())
        intermed_risk = str(intermediate_risk(risk))
        output = "\n" + "PSA Level:" + psa.get()  + "\n" + \
                 "Gleason Score:" + Gleason_score.get() + "\n" + \
                 "cT Staging:" + ct.get() + "\n" +\
                 "Core Involvement: " + core_involvement.get() + "%" +  "\n" +\
                 "Risk Classification: " + risk + "\n" +\
                 "Intermed Risk: " + intermed_risk
        output_entry.insert(END, output)
    except ValueError:
        output_error = "\n" + "Please enter PSA and Core " + "\n" + \
                      "Involvement as 0 if N.A." 
        output_entry.insert(END, output_error)


#Function for reset cT, GS, PSA and Output
def reset_nccn():
    ct.set("T1")
    Gleason_score.set("3+3")
    psa.delete(0,END)
    psa.insert(0, "0.02")
    core_involvement.delete(0,END)
    core_involvement.insert(0, "0")
    output_entry.delete("1.0",END)

#Creating buttons commanding printing output to output box    
b = Button(nccn_risk_tab, text="Stratify Risk", command=output_risk)
b.grid(row=0, column=3,sticky=W)

#Creating buttons commanding reset to all data fields  
b_1 = Button(nccn_risk_tab, text="Reset", command=reset_nccn)
b_1.grid(row=2, column=3,sticky=W)

#Creating output label
output = Label(nccn_risk_tab, text = 'Output:')
output.grid(row=5, column=0, sticky=S, pady=4)

#Creating output textbox
output_entry = Text(nccn_risk_tab, height=7, width=35)
output_entry.grid(row=5, column=1)

#creating Start Date entry box
start_date = Entry(date_cal_tab)
start_date.insert(0, "01-01-2018")
start_date.grid(row=1, column=1, pady=8)

#creating Start Date label
start_date_lb = Label(date_cal_tab, text="Start Date: ")
start_date_lb.grid(row=1, column=0, pady=8)

#creating End Date entry box
end_date = Entry(date_cal_tab)
end_date.insert(0, "01-01-2018")
end_date.grid(row=2, column=1, pady=8)

#creating End Date label
end_date_lb = Label(date_cal_tab, text="End Date: ")
end_date_lb.grid(row=2, column=0, pady=8)

#creating Durarion Number entry box
no_days = Entry(date_cal_tab)
no_days.configure(state = "disabled")
no_days.grid(row=4, column=1, pady=8)

#creating Durarion Number of days label
no_days_lb = Label(date_cal_tab, text="Duration Number: ")
no_days_lb.grid(row=4, column=0, pady=8)

#creating day, month, year entry box
dmy = StringVar(date_cal_tab)
dmy.set("Days")

#creating day, month, year label
dmy_label = Label(date_cal_tab, text = "Duration: ")
dmy_label.grid(row = 3, column = 0)

#creating day, month, year Options
dmy_options = OptionMenu(date_cal_tab, dmy, "", "Days", "Months", "Years")
dmy_options.grid(row = 3, column = 1)

#Create error label
error = Label(date_cal_tab, text = '')
error.grid(row=5, column=1, pady=4)

#Create function to calculate between two dates based on Days, Months, Years
def date_calculation():
    """
    """
    no_days.configure(state = "normal")
    no_days.delete(0,END)
    error.config(text = "")
    try: 
        start = datetime.datetime.strptime(start_date.get(), '%d-%m-%Y')
        end = datetime.datetime.strptime(end_date.get(), '%d-%m-%Y')
        difference = end - start
        if dmy.get() == "Days":
            difference_1 = str(difference.days) + " days"
        elif dmy.get() == "Months":
            difference_1 = str(difference.days/30) + " months"
        elif dmy.get() == "Years":
            difference_1 = str(difference.days/365.25) + " years"
        else:
            difference_1 = "Undefined"
        no_days.insert(END, difference_1)
        no_days.configure(state = "disabled")
    except ValueError:
        no_days.insert(END, "Undefined")
        error.config(text = "Date not in" + "\n" + "dd-mm-yyyy format")
        no_days.configure(state = "disabled")


#Create function to reset start date, end date, duration and duration number
def reset():
    no_days.configure(state = "normal")
    no_days.delete(0,END)
    no_days.configure(state = "disabled")
    error.config(text = "")
    dmy.set("Days")
    start_date.delete(0,END)
    end_date.delete(0,END)

#Creating buttons commanding printing Duration Number to output box    
calculate = Button(date_cal_tab, text="Calculate", command=date_calculation)
calculate .grid(row=4, column=4,sticky=W)

#Creating buttons commanding reset all data fields
reset_button = Button(date_cal_tab, text="Reset", command=reset)
reset_button .grid(row=4, column=5,sticky=W)



tabControl.pack(expand=1, fill="both")  # Pack to make visible
root.mainloop()
