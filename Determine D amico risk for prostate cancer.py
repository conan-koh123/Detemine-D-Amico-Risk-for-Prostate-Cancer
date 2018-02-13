from Tkinter import *

root = Tk()
root.wm_title("D Amico's Risk Classification for Prostate Cancer") #title of program
root.geometry("450x200") #size of root (canvas)

#creating psa entry box
psa = Entry(root)
psa.insert(0, "0.02")
psa.grid(row=0, column=1)

#creating psa label
psa_lb = Label(root, text="PSA Level")
psa_lb.grid(row=0, column=0)

#creating cT Staging box
ct = StringVar(root)
ct.set("T0")

#creating cT Staging Options
ct_options = OptionMenu(root, ct, "T0", "T1", "T1a", "T1b", "T1c", "T2", "T2a",
                        "T2b", "T2c", "T3", "T3a", "T3b", "T4")
ct_options.grid(row = 2, column = 1)

#creating cT Staging label
ct_label = Label(root, text = "cT Staging")
ct_label.grid(row = 2, column = 0)

#creating Gleason Score entry box
Gleason_score = StringVar(root)
Gleason_score.set("3+3")

#creating Gleason Score Options
gs_options = OptionMenu(root, Gleason_score, "3+3", "3+4", "3+5", "4+3",
                        "4+4", "4+5", "5+3", "5+4", "5+5")
gs_options.grid(row = 3, column = 1)

#creating Gleason Score label
gs_label = Label(root, text = "Gleason Score")
gs_label.grid(row = 3, column = 0)

#Function for risk classification
def risk_classify():
    risk = ""
    if Gleason_score.get() in ["3+5", "4+4", "5+3", "4+5", "5+4", "5+5"]:
        risk = "High"
    elif ct.get() in ["T2c", "T3", "T3a", "T3b", "T4"]:
        risk = "High"
    elif float(psa.get()) > 20:
        risk = "High"
    elif Gleason_score.get() in ["3+4", "4+3"]:
        risk = "Intermediate"
    elif ct.get() in ["T2b"]:
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

#Function for output
def output_risk():
    output_entry.delete("1.0",END)
    risk = str(risk_classify())
    output = "\n" + "PSA Level:" + psa.get()  + "\n" + \
             "Gleason Score:" + Gleason_score.get() + "\n" + \
             "cT Staging:" + ct.get() + "\n" + "Risk Classification: " + risk 
    output_entry.insert(END, output)


#Creating buttons commanding printing output to output box    
b = Button(root, text="Stratify Risk", command=output_risk)
b.grid(row=0, column=3,sticky=W)

#Creating output label
output = Label(root, text = 'Output:')
output.grid(row=5, column=0, sticky=S, pady=4)

#Creating output textbox
output_entry = Text(root, height=5, width=35)
output_entry.grid(row=5, column=1)
                  
mainloop()
