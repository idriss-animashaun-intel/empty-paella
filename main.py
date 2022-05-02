from tkinter import Tk
from tkinter import Button
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter import *
import webbrowser
import os
from pathlib import Path
import inspect

current_directory = os.getcwd()
print('Working Directory:', current_directory)


path = Path(current_directory)
repo_path = str(path.parent.absolute())
print('path to repo:', repo_path)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    caller_path = inspect.stack()[1].filename
    path = Path(caller_path).parent / relative_path
    return str(path)

def parse_mtpl(filename):
    # Open mtpl to search
    with open(filename, 'r') as fh:
        mtpl_lines = [str(line) for line in fh]


    mtpl_length = len(mtpl_lines)
    update = []
    for k in range(0, len(param_to_update)):
        update.append(param_to_update[k] + ' = ' + param_val[k])
    
    #to remove do this
    removal_update = ""

    # loop for individual search
    for test_instance in test_to_search:
        for line_i in range(mtpl_length):
            # Grabbing current line as string
            current_line = mtpl_lines[line_i]

            if (test_instance in current_line) and ('DUTFlowItem' not in current_line) and ('{' in mtpl_lines[line_i+1]):
                # block = [[current_line]]
                on_line = line_i+2
                parameter = mtpl_lines[on_line]
                flag = 0
                if removal == 1:
                    for j in range(0,len(param_to_update)):
                        while '}' not in parameter:
                            if param_to_update[j] in parameter:
                                flag = 1
                                print('update this', parameter)
                                mtpl_lines[on_line] = '\t' + removal_update
                            on_line += 1
                            parameter = mtpl_lines[on_line]
                        if flag == 0:
                            mtpl_lines[on_line - 1] = mtpl_lines[on_line - 1] + '\t' + removal_update
                else:
                    for j in range(0,len(param_to_update)):
                        while '}' not in parameter:
                            if update[j] in parameter:
                                flag = 1
                            elif param_to_update[j] in parameter:
                                if do_not_update_value == 1:
                                    flag = 1
                                    print('parameter already populated please review manually', parameter)
                                else:
                                    flag = 1
                                    # print('updating test instance values', parameter)
                                    mtpl_lines[on_line] = '\t' + update[j] + ';\n'
                            on_line += 1
                            parameter = mtpl_lines[on_line]
                        if flag == 0:
                            # print('adding test instance values', parameter)
                            mtpl_lines[on_line - 1] = mtpl_lines[on_line - 1] + '\t' + update[j] + ';\n'

    with open(filename + '_new', 'w') as file:
        for line in mtpl_lines:
            print(line, end="", file=file)

def e_k(filename):
    # Open mtpl to search
    with open(filename, 'r') as fh:
        mtpl_lines = [str(line) for line in fh]

    param_to_update = ['@EDC', '##EDC##']

    mtpl_length = len(mtpl_lines)
    
    #to remove do this

    # loop for individual search
    for test_instance in test_to_search:
        for line_i in range(mtpl_length):
            # Grabbing current line as string
            current_line = mtpl_lines[line_i]

            if (test_instance in current_line) and ('@EDC' in current_line) and ('{' in mtpl_lines[line_i+1]):
                on_line = line_i+2
                parameter = mtpl_lines[on_line]
                if E_to_C_var.get() == "EDC to KILL":
                    while '}' not in parameter and '}' not in mtpl_lines[on_line+1]:
                        if param_to_update[1] in parameter:
                            print('Moved to KILL', parameter)
                            mtpl_lines[on_line] = parameter.replace('##EDC## ', '')
                        on_line += 1
                        parameter = mtpl_lines[on_line]
                else:
                    while '}' not in parameter and '}' not in mtpl_lines[on_line+1]:
                        if 'SetBin SoftBins' in parameter:
                            # print('updating test instance values', parameter)
                            mtpl_lines[on_line] = param_to_update[1] + mtpl_lines[on_line] + '\n'
                        on_line += 1
                        parameter = mtpl_lines[on_line]

    with open(filename + '_new', 'w') as file:
        for line in mtpl_lines:
            print(line, end="", file=file)
   
def update_params():

    global TP_path
    global list_of_mtpls
    global test_to_search
    global param_to_update
    global param_val
    global removal
    global do_not_update_value

    TP_path = r"\Modules"

    list_of_mtpls = list_of_mod.get().split(",")

    test_to_search = test_inst.get().split(",")

    param_to_update = test_param.get().split(",")
    param_val = param_value.get().split(",")

    if len(param_to_update) != param_val:
        print('One or more of your parameters/values has a comma in the string, this is used as a dilimiter and may cause errors, parse a list instead to avoid potential errors')

    print(list_of_mtpls,test_to_search,param_to_update)
    removal = removal_var.get()

    #if parameter value already taken then do not update
    do_not_update_value = overwrite.get()

    for i in list_of_mtpls:
        parse_mtpl(repo_path + TP_path+'\\'+i+'\\'+i+'.mtpl')
        print(repo_path + TP_path+'\\'+i+'\\'+i+'.mtpl_new has been generated')

def edc_to_kill():
    global TP_path
    global list_of_mtpls
    global test_to_search

    TP_path = r"\Modules"

    list_of_mtpls = list_of_mod_t2.get().split(",")
    test_to_search = test_inst_t2.get().split(",")

    print(list_of_mtpls,test_to_search)

    #if parameter value already taken then do not update

    for i in list_of_mtpls:
        e_k(repo_path + TP_path+'\\'+i+'\\'+i+'.mtpl')
        print(repo_path + TP_path+'\\'+i+'\\'+i+'.mtpl_new has been generated')

def callback(url):
    webbrowser.open_new(url)

# def gui():
### Main Root
root = Tk()
root.title('Empty-Paella v1.00 [Beta]')
icon = resource_path("logo.ico")
root.iconbitmap(icon)

tab_parent = ttk.Notebook(root)

tab1 = ttk.Frame(tab_parent, padding="20 30 20 50")
tab2 = ttk.Frame(tab_parent, padding="20 30 20 50")
tab3 = ttk.Frame(tab_parent, padding="20 30 20 50")
tab4 = ttk.Frame(tab_parent, padding="20 30 20 50")
tab5 = ttk.Frame(tab_parent, padding="20 30 20 50")
tab6 = ttk.Frame(tab_parent, padding="20 30 20 50")
tab7 = ttk.Frame(tab_parent, padding="60 50 60 50")

tab_parent.add(tab1, text='Update Test Parameters')
tab_parent.add(tab2, text='EDC to KILL/KILL to EDC')
tab_parent.add(tab3, text='Bypass/Unbypass')
tab_parent.add(tab4, text='Find & Replace')
tab_parent.add(tab5, text='Test Instance Rename')
tab_parent.add(tab6, text='TP Audit')
tab_parent.add(tab7, text='Additional Tools')
tab_parent.grid(sticky=('news'))

#### Tab 1
link1 = Label(tab1, text="Wiki: https://goto/emptypaella", fg="blue", cursor="hand2")
link1.grid(row = 0,column = 0, sticky=W, columnspan = 2)
link1.bind("<Button-1>", lambda e: callback("https://gitlab.devtools.intel.com/ianimash/Empty-Paella/-/wikis/Empty-Paella"))

link2 = Label(tab1, text="IT support contact: idriss.animashaun@intel.com", fg="blue", cursor="hand2")
link2.grid(row = 1,column = 0, sticky=W, columnspan = 2)
link2.bind("<Button-1>", lambda e: callback("https://outlook.com"))

removal_var = IntVar(value=0)
Checkbutton(tab1, text="Remove Parameters", variable=removal_var).grid(row=4, column = 2, sticky=W)

overwrite = IntVar(value=1)
Checkbutton(tab1, text="Do not overwrite Existing Parameter Values", variable=overwrite).grid(row=5, column = 2, sticky=W)

label_0 = Label(tab1, text = 'Enter Modules to Modify: ', bg  ='black', fg = 'white')
label_0.grid(row = 2, sticky=E)
list_of_mod = Entry(tab1, width=50, relief = FLAT)
list_of_mod.insert(2,"SCN_CCF,SCN_SOC")
list_of_mod.grid(row = 2, column = 1)

label_1 = Label(tab1, text = 'Enter Test Instance/Test Template to Modify: ', bg  ='black', fg = 'white')
label_1.grid(row = 3, sticky=E)
test_inst = Entry(tab1, width=50, relief = FLAT)
test_inst.insert(4,'iCVminTest,iCAuxiliaryTest')
test_inst.grid(row = 3, column = 1)

label_2 = Label(tab1, text = 'Enter Parameter to Add/Update Modify: ', bg  ='black', fg = 'white')
label_2.grid(row = 4, sticky=E)
test_param = Entry(tab1, width=50, relief = FLAT)
test_param.insert(4,"preplist,postinstance")
test_param.grid(row = 4, column = 1)

label_3 = Label(tab1, text = 'Enter Parameter value: ', bg  ='black', fg = 'white')
label_3.grid(row = 5, sticky=E)
param_value = Entry(tab1, width=50, relief = FLAT)
param_value.insert(4,'"CPD_DEBUG!EnableDMEMCapture TDO","CPD_DEBUG!ProcessDTS TDO,9"')
param_value.grid(row = 5, column = 1)

button_0 = Button(tab1, text="Update MTPL's", height = 1, width = 20, command = update_params, bg = 'green', fg = 'white', font = '-family "SF Espresso Shack" -size 12')
button_0.grid(row = 7, column = 0, sticky=E )


#### Tab 2
link1 = Label(tab2, text="Wiki: https://goto/emptypaella", fg="blue", cursor="hand2")
link1.grid(row = 0,column = 0, sticky=W, columnspan = 2)
link1.bind("<Button-1>", lambda e: callback("https://gitlab.devtools.intel.com/ianimash/Empty-Paella/-/wikis/Empty-Paella"))

link2 = Label(tab2, text="IT support contact: idriss.animashaun@intel.com", fg="blue", cursor="hand2")
link2.grid(row = 1,column = 0, sticky=W, columnspan = 2)
link2.bind("<Button-1>", lambda e: callback("https://outlook.com"))

var2 = IntVar(value=0)
Checkbutton(tab2, text="Match exactly", variable=var2).grid(row=3, column = 2, sticky=W)

label_0 = Label(tab2, text = 'Enter Modules to Modify: ', bg  ='black', fg = 'white')
label_0.grid(row = 2, sticky=E)
list_of_mod_t2 = Entry(tab2, width=50, relief = FLAT)
list_of_mod_t2.insert(2,"SCN_SOC")
list_of_mod_t2.grid(row = 2, column = 1)

label_1 = Label(tab2, text = 'Enter Test Instances: ', bg  ='black', fg = 'white')
label_1.grid(row = 3, sticky=E)
test_inst_t2 = Entry(tab2, width=50, relief = FLAT)
test_inst_t2.insert(4,'ATSPEED_SOC_VMIN_E_SDTEND_STF_SAPF_NOM_LFM_1100_SACENTRAL1,ATSPEED_SOC_VMIN_E_SDTEND_STF_SAQ_NOM_LFM_1100_ASTROMID')
test_inst_t2.grid(row = 3, column = 1)

button_0 = Button(tab2, text="Update MTPL's", height = 1, width = 20, command = edc_to_kill, bg = 'green', fg = 'white', font = '-family "SF Espresso Shack" -size 12')
button_0.grid(row = 4, column = 0, sticky=E )

E_to_C_var = StringVar(tab2)
E_to_C_var.set("EDC to KILL") # default value

sel_prod = OptionMenu(tab2, E_to_C_var, "EDC to KILL", "KILL to EDC")
sel_prod.grid(row = 4, column = 1, sticky=W)




# #### Tab 7
link7 = Label(tab7, text="MTPL updater", fg="blue", cursor="hand2")
link7.grid(row = 0,column = 0, sticky=W, columnspan = 2)
link7.bind("<Button-1>", lambda e: callback("https://gitlab.devtools.intel.com/tcathcar/mtplupdater"))

### Main loop
root.mainloop()

# gui()