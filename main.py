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
import pandas as pd
import fnmatch

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

            regex_line = fnmatch.filter([current_line], '*' + test_instance + '*')
            if len(regex_line) == 1:
                if (regex_line[0] == current_line) and ('DUTFlowItem' not in current_line) and ('{' in mtpl_lines[line_i+1]):
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

            regex_line = fnmatch.filter([current_line], '*' + test_instance + '*')
            if len(regex_line) == 1:
                if (regex_line[0] == current_line) and ('@EDC' in current_line) and ('{' in mtpl_lines[line_i+1]):
                    on_line = line_i+2
                    parameter = mtpl_lines[on_line]
                    if E_to_C_var.get() == "EDC to KILL":
                        mtpl_lines[line_i] = mtpl_lines[line_i].replace(' @EDC', '')
                        while 'DUTFlowItem' not in parameter:
                            if ('##EDC##' in parameter):
                                print('Moved to KILL', parameter)
                                mtpl_lines[on_line] = parameter.replace('##EDC## ', '')
                            on_line += 1
                            parameter = mtpl_lines[on_line]
                elif (regex_line[0] == current_line)and ('{' in mtpl_lines[line_i+1]):
                    on_line = line_i+2
                    parameter = mtpl_lines[on_line]
                    if E_to_C_var.get() == "KILL to EDC":
                        mtpl_lines[line_i] = mtpl_lines[line_i].replace('\n',' @EDC\n')
                        while 'DUTFlowItem' not in parameter:
                            if ('SetBin SoftBins' in parameter) and ('SetBin SoftBins.b90999901_fail_FAIL_DPS_ALARM' not in parameter) and ('SetBin SoftBins.b90989801_fail_FAIL_SYSTEM_SOFTWARE' not in parameter):
                                # print('updating test instance values', parameter)
                                mtpl_lines[on_line] = '\t\t\t' + param_to_update[1] + ' ' + mtpl_lines[on_line].replace('\t\t\t','') + '\n'
                            on_line += 1
                            parameter = mtpl_lines[on_line]

    with open(filename + '_new', 'w') as file:
        for line in mtpl_lines:
            print(line, end="", file=file)

def status(filename):
    # Open mtpl to search
    with open(filename, 'r') as fh:
        mtpl_lines = [str(line) for line in fh]

    mtpl_length = len(mtpl_lines)

    kill_stat = ['Test Instance,Status']
    
    #to remove do this

    # loop for individual search
    for line_i in range(mtpl_length):
        # Grabbing current line as string
        current_line = mtpl_lines[line_i]

        if ('DUTFlowItem' in current_line) and ('@EDC' in current_line) and ('{' in mtpl_lines[line_i+1]):
            temp = current_line.split(' ')
            kill_stat.append(temp[2] + ', E')
        elif ('DUTFlowItem' in current_line) and ('{' in mtpl_lines[line_i+1]):
            temp = current_line.split(' ')
            kill_stat.append(temp[1] + ', K')


    with open(filename.replace(".mtpl","") + '_status_audit.csv', 'w') as file:
        for line in kill_stat:
            print(line + '\n', end="", file=file)

def audit_mtpl(filename):
    # Open mtpl to search
    with open(filename, 'r') as fh:
        mtpl_lines = [str(line) for line in fh]

    mtpl_length = len(mtpl_lines)
    
    test_to_search = ['Test iC']
    instances = ['Test Instance Name']
    
    audit_param = [param_to_update[0] +'\n']

    # loop for individual search
    for test_instance in test_to_search:
        for line_i in range(mtpl_length):
            # Grabbing current line as string
            current_line = mtpl_lines[line_i]


            regex_line = fnmatch.filter([current_line], '*' + test_instance + '*')
            if len(regex_line) == 1:
                if (regex_line[0] == current_line) and ('DUTFlowItem' not in current_line) and ('{' in mtpl_lines[line_i+1]):
                    on_line = line_i+2
                    parameter = mtpl_lines[on_line]
                    for j in range(0,len(param_to_update)):
                        while '}' not in parameter:
                            if param_to_update[j] in parameter:
                                t_inst = current_line.split(" ")
                                instances.append(t_inst[2])
                                audit_param.append(parameter)
                            on_line += 1
                            parameter = mtpl_lines[on_line]

    with open(filename.replace(".mtpl","") + '_audit.csv', 'w') as file:
        for line_no in range(0,len(instances)):
            print(instances[line_no].strip('\n') + ',' + audit_param[line_no], end="", file=file)

def conflicts():
    
    searchstring = '<<<<<<< HEAD'
    tp_conflicts = []
    skipped_files = []

    for dirpath, dirnames, filenames in os.walk(repo_path + '//Modules'):
        for filename in filenames:
            try:
                # Full path
                f = open(os.path.join(dirpath, filename))

                if searchstring in f.read():
                    tp_conflicts.append(filename)
                f.close()
            except:
                skipped_files.append(filename)
                f.close()

    # print('Skipped files as I can not parse these:')
    # print(skipped_files)
    if tp_conflicts == []:
        print('No Unresolved conflicts found')
    else:
        print('Unresolved conflict found in:')
        print(tp_conflicts)

def bulk_fnr(filename):
    # Open mtpl to search
    with open(filename, 'r') as fh:
        mtpl_lines = [str(line) for line in fh]


    mtpl_length = len(mtpl_lines)
    # loop for individual search
    for i in range(0,len(test_to_search)):
        for line_i in range(mtpl_length):
            # Grabbing current line as string
            current_line = mtpl_lines[line_i]
            if test_to_search[i] in current_line:
                mtpl_lines[line_i] = current_line.replace(test_to_search[i], test_to_replace[i])

    with open(filename + '_new', 'w') as file:
        for line in mtpl_lines:
            print(line, end="", file=file)

def get_test_list(filename):
    # Open mtpl to search
    with open(filename, 'r') as fh:
        mtpl_lines = [str(line) for line in fh]

    test_to_search = ['Test iC']

    list_tests = ['Old Name\n']
    mtpl_length = len(mtpl_lines)
    # loop for individual search
    for line_i in range(mtpl_length):
        # Grabbing current line as string
        current_line = mtpl_lines[line_i]
        if test_to_search[0] in current_line:
            t_inst = current_line.split(" ")
            list_tests.append(t_inst[2])

    with open(filename.replace(".mtpl","") + '_test_names.csv', 'w') as file:
        for line in list_tests:
            print(line, end="", file=file)

def test_list():
    global TP_path
    global list_of_mtpls

    TP_path = r"\Modules"

    list_of_mtpls = list_of_mod_t5.get().split(",")

    print(list_of_mtpls)

    #if parameter value already taken then do not update

    for i in list_of_mtpls:
        get_test_list(repo_path + TP_path+'\\'+i+'\\'+i+'.mtpl')
        print(repo_path + TP_path+'\\'+i+'\\'+i+'_test_names.csv has been generated')

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

def audit_params():

    global TP_path
    global list_of_mtpls
    global param_to_update
    global param_val

    TP_path = r"\Modules"

    list_of_mtpls = list_of_mod_t6.get().split(",")
    param_to_update = test_param_t6.get().split(",")

    print(list_of_mtpls,param_to_update)

    for i in list_of_mtpls:
        audit_mtpl(repo_path + TP_path+'\\'+i+'\\'+i+'.mtpl')
        print(repo_path + TP_path+'\\'+i+'\\'+i+'_audit.csv has been generated')

def Kill_status():

    global TP_path
    global list_of_mtpls
    global param_to_update
    global param_val

    TP_path = r"\Modules"

    list_of_mtpls = list_of_mod_t8.get().split(",")

    print(list_of_mtpls)

    for i in list_of_mtpls:
        status(repo_path + TP_path+'\\'+i+'\\'+i+'.mtpl')
        print(repo_path + TP_path+'\\'+i+'\\'+i+'_status_audit.csv has been generated')

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

def bypass():
    global TP_path
    global list_of_mtpls
    global test_to_search
    global removal
    global param_to_update
    global param_val

    TP_path = r"\Modules"

    list_of_mtpls = list_of_mod_t3.get().split(",")
    test_to_search = test_inst_t3.get().split(",")
    param_to_update = ['bypass_global']
    param_val = ['"1"']

    if bypass_var.get() == "Un-Bypass":
        removal = 1
    else:
        removal =0

    print(list_of_mtpls,test_to_search)

    #if parameter value already taken then do not update

    for i in list_of_mtpls:
        parse_mtpl(repo_path + TP_path+'\\'+i+'\\'+i+'.mtpl')
        print(repo_path + TP_path+'\\'+i+'\\'+i+'.mtpl_new has been generated')

def bulk_replace():
    global bindef_flag
    global TP_path
    global list_of_mtpls
    global test_to_search
    global removal
    global test_to_replace

    TP_path = r"\Modules"

    test_instance_to_update = pd.read_csv(filename)
    test_to_search = test_instance_to_update['Old Name']
    test_to_replace = test_instance_to_update['New Name']

    list_of_mtpls = list_of_mod_t4.get().split(",")
    # bindef_flag = 1
    if bindef_flag == 1:
        bulk_fnr(repo_path + "\Shared\Common\BinDefinitions.bdefs")
        print(repo_path + "\Shared\Common\BinDefinitions.bdefs_new has been generated")

    #if parameter value already taken then do not update

    for i in list_of_mtpls:
        print('Please be patient')
        bulk_fnr(repo_path + TP_path+'\\'+i+'\\'+i+'.mtpl')
        print(repo_path + TP_path+'\\'+i+'\\'+i+'.mtpl_new has been generated')
    bindef_flag = 0

def bindef():
    global bindef_flag
    bindef_flag = 1
    bulk_replace()

def callback(url):
    webbrowser.open_new(url)

def select_file():
    global filename
    filetypes = (
        ('text files', '*.csv'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    showinfo(
        title='Selected File',
        message=filename
    )

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
tab7 = ttk.Frame(tab_parent, padding="20 30 20 50")
tab8 = ttk.Frame(tab_parent, padding="20 30 20 50")
tab12 = ttk.Frame(tab_parent, padding="60 50 60 50")

tab_parent.add(tab1, text='Update Test Parameters')
tab_parent.add(tab2, text='EDC to KILL/KILL to EDC')
tab_parent.add(tab3, text='Bypass/Unbypass')
tab_parent.add(tab4, text='Bulk Find & Replace')
tab_parent.add(tab5, text='Test Instance Rename')
tab_parent.add(tab6, text='TP Audit')
tab_parent.add(tab7, text='Check unresolved Conflicts')
tab_parent.add(tab8, text='Kill Status')
tab_parent.add(tab12, text='Additional Tools')
tab_parent.grid(sticky=('news'))

#### update params
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

label_1 = Label(tab1, text = 'Enter Test Instance/Test Template to Modify (Wildcard *): ', bg  ='black', fg = 'white')
label_1.grid(row = 3, sticky=E)
test_inst = Entry(tab1, width=50, relief = FLAT)
test_inst.insert(4,'iCVminTest,iCAuxiliaryTest')
test_inst.grid(row = 3, column = 1)

label_2 = Label(tab1, text = 'Enter Parameter to Add/Update: ', bg  ='black', fg = 'white')
label_2.grid(row = 4, sticky=E)
test_param = Entry(tab1, width=50, relief = FLAT)
test_param.insert(4,"preplist,bypass_global")
test_param.grid(row = 4, column = 1)

label_3 = Label(tab1, text = 'Enter Parameter value: ', bg  ='black', fg = 'white')
label_3.grid(row = 5, sticky=E)
param_value = Entry(tab1, width=50, relief = FLAT)
param_value.insert(4,'"CPD_DEBUG!EnableDMEMCapture TDO","1"')
param_value.grid(row = 5, column = 1)

button_0 = Button(tab1, text="Update MTPL's", height = 1, width = 20, command = update_params, bg = 'green', fg = 'white', font = '-family "SF Espresso Shack" -size 12')
button_0.grid(row = 7, column = 0, sticky=E )


#### EDC to KILL
link1 = Label(tab2, text="Wiki: https://goto/emptypaella", fg="blue", cursor="hand2")
link1.grid(row = 0,column = 0, sticky=W, columnspan = 2)
link1.bind("<Button-1>", lambda e: callback("https://gitlab.devtools.intel.com/ianimash/Empty-Paella/-/wikis/Empty-Paella"))

link2 = Label(tab2, text="IT support contact: idriss.animashaun@intel.com", fg="blue", cursor="hand2")
link2.grid(row = 1,column = 0, sticky=W, columnspan = 2)
link2.bind("<Button-1>", lambda e: callback("https://outlook.com"))

# var2 = IntVar(value=0)
# Checkbutton(tab2, text="Match exactly", variable=var2).grid(row=3, column = 2, sticky=W)

label_0 = Label(tab2, text = 'Enter Modules to Modify: ', bg  ='black', fg = 'white')
label_0.grid(row = 2, sticky=E)
list_of_mod_t2 = Entry(tab2, width=50, relief = FLAT)
list_of_mod_t2.insert(2,"SCN_SOC")
list_of_mod_t2.grid(row = 2, column = 1)

label_1 = Label(tab2, text = 'Enter Test Instances (Wildcard *): ', bg  ='black', fg = 'white')
label_1.grid(row = 3, sticky=E)
test_inst_t2 = Entry(tab2, width=50, relief = FLAT)
test_inst_t2.insert(4,'STUCKAT_SOC_SCANFI_E_*_STF_SAQ_NOM_LFM_1100_SHMOO_MC')
test_inst_t2.grid(row = 3, column = 1)

button_0 = Button(tab2, text="Update MTPL's", height = 1, width = 20, command = edc_to_kill, bg = 'green', fg = 'white', font = '-family "SF Espresso Shack" -size 12')
button_0.grid(row = 4, column = 0, sticky=E )

E_to_C_var = StringVar(tab2)
E_to_C_var.set("EDC to KILL") # default value

sel_op = OptionMenu(tab2, E_to_C_var, "EDC to KILL", "KILL to EDC")
sel_op.grid(row = 4, column = 1, sticky=W)

#### Bypass
link1 = Label(tab3, text="Wiki: https://goto/emptypaella", fg="blue", cursor="hand2")
link1.grid(row = 0,column = 0, sticky=W, columnspan = 2)
link1.bind("<Button-1>", lambda e: callback("https://gitlab.devtools.intel.com/ianimash/Empty-Paella/-/wikis/Empty-Paella"))

link2 = Label(tab3, text="IT support contact: idriss.animashaun@intel.com", fg="blue", cursor="hand2")
link2.grid(row = 1,column = 0, sticky=W, columnspan = 2)
link2.bind("<Button-1>", lambda e: callback("https://outlook.com"))

label_0 = Label(tab3, text = 'Enter Modules to Modify: ', bg  ='black', fg = 'white')
label_0.grid(row = 2, sticky=E)
list_of_mod_t3 = Entry(tab3, width=50, relief = FLAT)
list_of_mod_t3.insert(2,"SCN_CCF,SCN_SOC")
list_of_mod_t3.grid(row = 2, column = 1)

label_1 = Label(tab3, text = 'Enter Test Instance/Test Template to Modify (Wildcard *): ', bg  ='black', fg = 'white')
label_1.grid(row = 3, sticky=E)
test_inst_t3 = Entry(tab3, width=50, relief = FLAT)
test_inst_t3.insert(4,'iCVminTest,iCAuxiliaryTest')
test_inst_t3.grid(row = 3, column = 1)

button_0 = Button(tab3, text="Update MTPL's", height = 1, width = 20, command = bypass, bg = 'green', fg = 'white', font = '-family "SF Espresso Shack" -size 12')
button_0.grid(row = 4, column = 0, sticky=E )

bypass_var = StringVar(tab3)
bypass_var.set("Bypass") # default value

sel_op = OptionMenu(tab3, bypass_var, "Bypass", "Un-Bypass")
sel_op.grid(row = 4, column = 1, sticky=W)

#### Find & Replace
link1 = Label(tab4, text="Wiki: https://goto/emptypaella", fg="blue", cursor="hand2")
link1.grid(row = 0,column = 0, sticky=W, columnspan = 2)
link1.bind("<Button-1>", lambda e: callback("https://gitlab.devtools.intel.com/ianimash/Empty-Paella/-/wikis/Empty-Paella"))

link2 = Label(tab4, text="IT support contact: idriss.animashaun@intel.com", fg="blue", cursor="hand2")
link2.grid(row = 1,column = 0, sticky=W, columnspan = 2)
link2.bind("<Button-1>", lambda e: callback("https://outlook.com"))

label_0 = Label(tab4, text = 'Enter Modules to Modify: ', bg  ='black', fg = 'white')
label_0.grid(row = 2, sticky=E)
list_of_mod_t4 = Entry(tab4, width=50, relief = FLAT)
list_of_mod_t4.insert(2,"SCN_SOC")
list_of_mod_t4.grid(row = 2, column = 1)

open_button_1 = Button(
    tab4,
    text='Select Renamed csv',
    command=select_file,
    bg = 'blue', fg = 'white', font = '-family "SF Espresso Shack" -size 12'
)

open_button_1.grid(row = 3, column = 0)

button_0 = Button(tab4, text="Update MTPL's", height = 1, width = 20, command = bulk_replace, bg = 'green', fg = 'white', font = '-family "SF Espresso Shack" -size 12')
button_0.grid(row = 3, column = 1, sticky=E )

#### Test Rename
link1 = Label(tab5, text="Wiki: https://goto/emptypaella", fg="blue", cursor="hand2")
link1.grid(row = 0,column = 0, sticky=W, columnspan = 2)
link1.bind("<Button-1>", lambda e: callback("https://gitlab.devtools.intel.com/ianimash/Empty-Paella/-/wikis/Empty-Paella"))

link2 = Label(tab5, text="IT support contact: idriss.animashaun@intel.com", fg="blue", cursor="hand2")
link2.grid(row = 1,column = 0, sticky=W, columnspan = 2)
link2.bind("<Button-1>", lambda e: callback("https://outlook.com"))

label_0 = Label(tab5, text = 'Enter Modules to Modify: ', bg  ='black', fg = 'white')
label_0.grid(row = 2, sticky=E)
list_of_mod_t5 = Entry(tab5, width=50, relief = FLAT)
list_of_mod_t5.insert(2,"SCN_SOC")
list_of_mod_t5.grid(row = 2, column = 1)

button_0 = Button(tab5, text="Get Current Test Names", height = 1, width = 20, command = test_list, bg = 'green', fg = 'white', font = '-family "SF Espresso Shack" -size 12')
button_0.grid(row = 3, column = 0, sticky=E )

open_button_1 = Button(
    tab5,
    text='Select Renamed Tests csv',
    command=select_file,
    bg = 'blue', fg = 'white', font = '-family "SF Espresso Shack" -size 12'
)

open_button_1.grid(row = 3, column = 1)

button_2 = Button(tab5, text="Update MTPL's", height = 1, width = 20, command = bindef, bg = 'green', fg = 'white', font = '-family "SF Espresso Shack" -size 12')
button_2.grid(row = 3, column = 2, sticky=E )

#### Audit
link1 = Label(tab6, text="Wiki: https://goto/emptypaella", fg="blue", cursor="hand2")
link1.grid(row = 0,column = 0, sticky=W, columnspan = 2)
link1.bind("<Button-1>", lambda e: callback("https://gitlab.devtools.intel.com/ianimash/Empty-Paella/-/wikis/Empty-Paella"))

link2 = Label(tab6, text="IT support contact: idriss.animashaun@intel.com", fg="blue", cursor="hand2")
link2.grid(row = 1,column = 0, sticky=W, columnspan = 2)
link2.bind("<Button-1>", lambda e: callback("https://outlook.com"))

label_0 = Label(tab6, text = 'Enter Modules to Audit: ', bg  ='black', fg = 'white')
label_0.grid(row = 2, sticky=E)
list_of_mod_t6 = Entry(tab6, width=50, relief = FLAT)
list_of_mod_t6.insert(2,"SCN_SOC")
list_of_mod_t6.grid(row = 2, column = 1)

# label_1 = Label(tab6, text = 'Enter Test Instance/Test Template to Audit: ', bg  ='black', fg = 'white')
# label_1.grid(row = 3, sticky=E)
# test_inst = Entry(tab6, width=50, relief = FLAT)
# test_inst.insert(4,'iCVminTest,iCAuxiliaryTest')
# test_inst.grid(row = 3, column = 1)

label_2 = Label(tab6, text = 'Enter Parameter to Audit: ', bg  ='black', fg = 'white')
label_2.grid(row = 4, sticky=E)
test_param_t6 = Entry(tab6, width=50, relief = FLAT)
test_param_t6.insert(4,"preplist")
test_param_t6.grid(row = 4, column = 1)

button_0 = Button(tab6, text="Audit MTPL's", height = 1, width = 20, command = audit_params, bg = 'green', fg = 'white', font = '-family "SF Espresso Shack" -size 12')
button_0.grid(row = 7, column = 0, sticky=E )

#### Merge Conflicts
link1 = Label(tab7, text="Wiki: https://goto/emptypaella", fg="blue", cursor="hand2")
link1.grid(row = 0,column = 0, sticky=W, columnspan = 2)
link1.bind("<Button-1>", lambda e: callback("https://gitlab.devtools.intel.com/ianimash/Empty-Paella/-/wikis/Empty-Paella"))

link2 = Label(tab7, text="IT support contact: idriss.animashaun@intel.com", fg="blue", cursor="hand2")
link2.grid(row = 1,column = 0, sticky=W, columnspan = 2)
link2.bind("<Button-1>", lambda e: callback("https://outlook.com"))

button_0 = Button(tab7, text="Check For Conflicts", height = 1, width = 20, command = conflicts, bg = 'green', fg = 'white', font = '-family "SF Espresso Shack" -size 12')
button_0.grid(row = 2, column = 0, sticky=E )

#### KILL Status
link1 = Label(tab8, text="Wiki: https://goto/emptypaella", fg="blue", cursor="hand2")
link1.grid(row = 0,column = 0, sticky=W, columnspan = 2)
link1.bind("<Button-1>", lambda e: callback("https://gitlab.devtools.intel.com/ianimash/Empty-Paella/-/wikis/Empty-Paella"))

link2 = Label(tab8, text="IT support contact: idriss.animashaun@intel.com", fg="blue", cursor="hand2")
link2.grid(row = 1,column = 0, sticky=W, columnspan = 2)
link2.bind("<Button-1>", lambda e: callback("https://outlook.com"))

label_0 = Label(tab8, text = 'Enter Modules to Audit: ', bg  ='black', fg = 'white')
label_0.grid(row = 2, sticky=E)
list_of_mod_t8 = Entry(tab8, width=50, relief = FLAT)
list_of_mod_t8.insert(2,"SCN_SOC")
list_of_mod_t8.grid(row = 2, column = 1)

button_0 = Button(tab8, text="Pull Kill Status", height = 1, width = 20, command = Kill_status, bg = 'green', fg = 'white', font = '-family "SF Espresso Shack" -size 12')
button_0.grid(row = 4, column = 0, sticky=E )

#### Additional Tools
link7 = Label(tab12, text="MTPL updater", fg="blue", cursor="hand2")
link7.grid(row = 0,column = 0, sticky=W, columnspan = 2)
link7.bind("<Button-1>", lambda e: callback("https://gitlab.devtools.intel.com/tcathcar/mtplupdater"))

### Main loop
root.mainloop()

# gui()