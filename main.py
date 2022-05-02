from tkinter import Tk
from tkinter import Button
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter import *
import webbrowser
import os
from pathlib import Path

current_directory = os.getcwd()
print('Working Directory:', current_directory)


path = Path(current_directory)
repo_path = str(path.parent.absolute())
print('path to repo:', repo_path)


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

            if just_tests == 1:
                condition = (test_instance in current_line) and ('DUTFlowItem' not in current_line) and ('{' in mtpl_lines[line_i+1])
            elif just_flow == 1:
                condition = (test_instance in current_line) and ('Test iC' not in current_line) and ('{' in mtpl_lines[line_i+1])
            else:
                condition = (test_instance in current_line) and ('{' in mtpl_lines[line_i+1])

            if condition:
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
                
def run_tool():

    global TP_path
    global list_of_mtpls
    global test_to_search
    global param_to_update
    global param_val
    global removal
    global just_flow
    global just_tests
    global do_not_update_value

    TP_path = r"\Modules"

    list_of_mtpls = list_of_mod.get().split(",")

    test_to_search = test_inst.get().split(",")

    param_to_update = test_param.get().split(",")
    param_val = param_value.get().split(",")

    if len(param_to_update) != param_val:
        print('One or more of your parameters/values has a comma in the string, this is used as a dilimiter and may cause errors, parse a list instead to avoid potential errors')

    print(list_of_mtpls,test_to_search,param_to_update)
    removal = 0

    just_tests = 1
    just_flow = 0

    #if parameter value already taken then do not update
    do_not_update_value = 1

    for i in list_of_mtpls:
        parse_mtpl(repo_path + TP_path+'\\'+i+'\\'+i+'.mtpl')
        print(repo_path + TP_path+'\\'+i+'\\'+i+'.mtpl_new has been generated')


### Main Root
root = Tk()
root.title('Empty-Paella v1.00 [Beta]')

tab_parent = ttk.Notebook(root)

tab1 = ttk.Frame(tab_parent, padding="20 30 20 50")
tab2 = ttk.Frame(tab_parent, padding="60 50 60 50")

tab_parent.add(tab1, text='Modify Test Instance')
tab_parent.add(tab2, text='Find & Replace')
tab_parent.grid(sticky=('news'))

def callback(url):
    webbrowser.open_new(url)

link1 = Label(tab1, text="Wiki: https://goto/emptypaella", fg="blue", cursor="hand2")
link1.grid(row = 0,column = 0, sticky=W, columnspan = 2)
link1.bind("<Button-1>", lambda e: callback("https://gitlab.devtools.intel.com/ianimash/supercpg/-/wikis/Need4Seed"))

link2 = Label(tab1, text="IT support contact: idriss.animashaun@intel.com", fg="blue", cursor="hand2")
link2.grid(row = 1,column = 0, sticky=W, columnspan = 2)
link2.bind("<Button-1>", lambda e: callback("https://outlook.com"))

#### Tab 1
var1 = IntVar(value=1)
Checkbutton(tab1, text="Match exactly", variable=var1).grid(row=3, column = 1, sticky=W)

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

# button_0 = Button(tab1, text="Add", height = 1, width = 20, command = run_tool, bg = 'green', fg = 'white', font = '-family "SF Espresso Shack" -size 12')
# button_0.grid(row = 6, column = 0, sticky=E )

button_0 = Button(tab1, text="Update MTPL's", height = 1, width = 20, command = run_tool, bg = 'green', fg = 'white', font = '-family "SF Espresso Shack" -size 12')
button_0.grid(row = 7, column = 0, sticky=E )

# #### Tab 2
link2 = Label(tab2, text="MTPL updater", fg="blue", cursor="hand2")
link2.grid(row = 0,column = 0, sticky=W, columnspan = 2)
link2.bind("<Button-1>", lambda e: callback("https://gitlab.devtools.intel.com/tcathcar/mtplupdater"))

### Main loop
root.mainloop()