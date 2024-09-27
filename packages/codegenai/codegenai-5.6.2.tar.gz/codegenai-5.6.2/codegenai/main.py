from codegenai.aids import *
from codegenai.cn import *
from codegenai.special import *
import os
import sys
import subprocess
import shutil
import time

available = {'AIDS' : "",
             '0   ' : "All",
             '1   ' : "Breadth First Search",
             '2   ' : "Depth First Search",
             '3   ' : "Uniform Cost Search",
             '4   ' : "Depth Limited Search", 
             '5   ' : "Iterative Deepening Search(IDDFS)", 
             '6   ' : "A*", 
             '7   ' : "Iterative Deepening A*", 
             '8   ' : "Simplified Memory Bounded A*",
             '9   ' : "Genetic Algorithm", 
             '10  ' : "Simulated Annealing",
             '11  ' : "Solving Sudoku(Simulated Annealing)",
             '12  ' : "Alpha-Beta Pruning",
             '13  ' : "Map Coloring(Constraint Satisfaction Problem)",
             '14  ' : "House Allocation(Constraint Satisfaction Problem)",
             '    ' : "",
             'CN  ' : "",
             '15  ' : "Chat Application",
             '16  ' : "File Transfer",
             '17  ' : "RMI(Remote Method Invocation)",
             '18  ' : "Wired Network TCL Script",
             '19  ' : "Wired Network AWK File",
             '20  ' : "Wireless Network TCL Script",
             '21  ' : "Wireless Network AWK File",
             }

def display(name = ""):
    try:
        name = str(name)
        if   name in ['1']      :   print(bfs)
        elif name in ['2']      :   print(dfs)
        elif name in ['3']      :   print(ucs)
        elif name in ['4']      :   print(dls)
        elif name in ['5']      :   print(ids)
        elif name in ['6']      :   print(astar)
        elif name in ['7']      :   print(idastar)
        elif name in ['8']      :   print(smastar)
        elif name in ['9']      :   print(genetic)
        elif name in ['10']     :   print(sa)
        elif name in ['11']     :   print(sudoku)
        elif name in ['12']     :   print(alphabeta)
        elif name in ['13']     :   print(csp_map)
        elif name in ['14']     :   print(csp_house)
        elif name in ['15']     :   print(chat)
        elif name in ['16']     :   print(file_transfer)
        elif name in ['17']     :   print(rmi)
        elif name in ['18']     :   print(wired_tcl)
        elif name in ['19']     :   print(wired_awk)
        elif name in ['20']     :   print(wireless_tcl)
        elif name in ['21']     :   print(wireless_awk)
        elif name in ["",'0']   :   print(code)
        else:
            for k, v in available.items():
                sep = " : " if v else ""
                print(k,v,sep = sep)
    except:
        pass

def get(name = ""):
    try:
        name = str(name)
        if   name in ['1']      :   print("Not Available Yet")
        elif name in ['2']      :   print("Not Available Yet")
        elif name in ['3']      :   print("Not Available Yet")
        elif name in ['4']      :   print("Not Available Yet")
        elif name in ['5']      :   print("Not Available Yet")
        elif name in ['6']      :   print("Not Available Yet")
        elif name in ['7']      :   print("Not Available Yet")
        elif name in ['8']      :   print("Not Available Yet")
        elif name in ['9']      :   print("Not Available Yet")
        elif name in ['10']     :   print("Not Available Yet")
        elif name in ['11']     :   print("Not Available Yet")
        elif name in ['12']     :   print("Not Available Yet")
        elif name in ['13']     :   print("Not Available Yet")
        elif name in ['14']     :   print("Not Available Yet")
        elif name in ['15']     :   print("Not Available Yet")
        elif name in ['16']     :   print("Not Available Yet")
        elif name in ['17']     :   print("Not Available Yet")
        elif name in ['18']     :   print("Not Available Yet")
        elif name in ['19']     :   print("Not Available Yet")
        elif name in ['20']     :   print("Not Available Yet")
        elif name in ['21']     :   print("Not Available Yet")
        elif name in ["",'0']   :   get_ipynb('All')
        else:
            for k, v in available.items():
                sep = " : " if v else ""
                print(k,v,sep = sep)
    except:
        pass

def get_ipynb(file_name):
    try:
        if file_name != 'All':
            return
        p = os.path.realpath(__file__)[:-7]+"\\Notebooks\\"+file_name+".ipynb"
        shutil.copy(f'{p}', f'{os.getcwd()}\\AllinOne.ipynb')
        subprocess.Popen(f'jupyter notebook {os.getcwd()}\\AllinOne.ipynb')

        total_iterations = 100
        for i in range(total_iterations + 1):
            time.sleep(0.05)
            percentage_complete = (i / total_iterations) * 100 
            if i == total_iterations:percentage_complete -= 0.01
            print("Loading: {:.2f}%".format(percentage_complete), end='\r')
            sys.stdout.flush()
        print()
        print("Please Wait")
    except:
        pass
    

def ghost(key = None, what = ""):
    if key and isinstance(key,str) and key == "r690z4t13x":
        available = {'101  or  sudoku   ' : "Solving Sudoku(Loading Bar)"}
        try:
            if isinstance(what,str):
                what =  what.lower()
            if what in ["sudoku", 101]   :   print(sudoku_lb)
            else:
                print("Invalid Value! Refer Below Table")
                for k, v in available.items():
                    print(k,v,sep = " : ")
        except:
            pass