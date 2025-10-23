#input files: OUTCAR file
#output files: HFvalues.txt, if chosen: HFisoAll.txt, HFisoLarge.txt
#This code is to find and print the coordinates of the large Hyperfine values. 
import argparse
import os

parser = argparse.ArgumentParser(description="Arguments for vasp output file ",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-outcar", nargs='?', default = "./OUTCAR", help="outcar file location")
parser.add_argument("-hfcutoff", nargs='?', type=float, default = 8.0, help="cuttoff HF value")
parser.add_argument("-iso", nargs='?', type=bool, default = False, help="output HFisoAll.txt and HFisoLarge.txt")
args = parser.parse_args()
config = vars(args)
def skip_ahead(it, elems):
    assert elems >= 1, "can only skip positive integer number of elements"
    for i in range(elems):
        value = next(it)
    return value
count=0
count2=0
count3=0
num=0
count4=0
compare=config['hfcutoff']
print("To learn more about features, use HFparser.py -h")
print("Running code to calculate HF values")
#Reads OUTCAR file and outputs coupling parameters into new file HFcouplingAll.txt
print("Input files are: OUTCAR")
ISiso=config['iso']
if ISiso==True:
    #Reads OUTCAR file and outputs Fermi contact (isotropic) hyperfine coupling parameter (MHz) into new file; HFisoAll.txt
    with open(config["outcar"], 'r') as f:
         for line in f:
             if 'Fermi contact (isotropic) hyperfine coupling parameter (MHz)' in line:
                count4=count4+1
    with open(config["outcar"], 'r') as f:
             always_print=False
             for line in f:
                 if 'Fermi contact (isotropic) hyperfine coupling parameter (MHz)' in line:
                     num=num+1
                     if num==count4:
                        with open("HFisoAll.txt", "w") as y:
                             print (line, file=y, end='')
                             line = skip_ahead(f, 3)
                             always_print=True
                             num=0
                 if always_print:
                    with open("HFisoAll.txt", "a") as y:
                         print(line, file=y,end='')
                    if '-------------------------------------------------------------' in line:
                       count3=count3 +1
                 if count3==2:
                    always_print=False
    
    #reads HFisoAll.txt file and outputs the large values into HFisoLarge.txt
    #compare=float(input("HF input: "))
    with open("HFisoAll.txt", 'r') as t:
         with open("HFisoLarge.txt", "w") as x:
            for i, line in enumerate(t):
                count2 = count2 + 1
                if '-------------------------------------------------------------' in line and count2>2:
                    break
                if count2 > 2: #and i%2==0:
                       temp = line.split()
                       floatTemp=[float(i) for i in temp[1:]]
                       if floatTemp[4]>=compare or floatTemp[4]<=-compare:
                          print(temp[0], floatTemp[4], file=x)
                    
    print("Output files are: HFisoAll.txt, HFisoLarge.txt")
#reads outcar for Total hyperfine coupling parameters after diagonalization (MHz) and outputs into HFcouplingAll.txt
num=0
count4=0
count3=0
num2=5
with open(config["outcar"], 'r') as f:
         for line in f:
              if 'Total hyperfine coupling parameters after diagonalization (MHz)' in line:
                 count4=count4+1
         always_print=False
with open(config["outcar"], 'r') as f:
         for line in f:
             if 'Total hyperfine coupling parameters after diagonalization (MHz)' in line:
                 num=num+1
                 num2=num2-1
                 if num==count4:
                    with open("HFcouplingAll.txt", "w") as y:
                         print (line, file=y, end='')
                         line = skip_ahead(f, 4)
                         always_print=True
                         num=0
                 if num2==count4:
                     print("no hyperfine coupling found in OUTCAR")
             if always_print:
                with open("HFcouplingAll.txt", "a") as y:
                     print(line, file=y, end='')
                if '-------------------------------------------------------------' in line:
                   count3=count3 +1
             if count3==2:
                always_print=False
#reads HFcouplingAll file and finds the large values of Azz and outputs into HFvalues.txt
count4=0
count2=0
with open("HFvalues.txt", 'w') as z:
     print("HF_Large coordinates", file=z)
     print("Atom  Axx       Ayy       Azz", file=z)
with open("HFcouplingAll.txt", 'r') as x:
     for line in x:
        count4 = count4+ 1
        if '-------------------------------------------------------------' in line and count4 > 2:
            break
        if count4 > 2 and '-------------------------------------------------------------' not in line:
           compx = line.split()
           floatcomp=[float(i) for i in compx]
           if floatcomp[3]>=compare or floatcomp[3]<=(-compare):
              with open("HFvalues.txt", 'a') as zz:
                   print(floatcomp[0], ' ', floatcomp[1],' ', floatcomp[2],' ',floatcomp[3], file=zz)

os.remove("HFcouplingAll.txt")
#removes HFcouplingAll.txt file
print("Output files: HFvalues.txt")
