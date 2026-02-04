#input files: OUTCAR file
#output files: HFvalues.txt, if chosen: HFisoAll.txt, HFisoLarge.txt
#This code is to find and print the large Hyperfine values. 
import argparse
import os

parser = argparse.ArgumentParser(description="Arguments for vasp output file ",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-o", nargs='?', default = "./OUTCAR", help="outcar file location")
parser.add_argument("-cut", nargs='?', type=float, default = 8.0, help="cuttoff HF value")
parser.add_argument("-iso", nargs='?', type=bool, default = True, help="output HFisoAll.txt and HFisoLarge.txt")
parser.add_argument("-md", nargs='?', type=float, default=0, help="atom number for HF values to output HF values of this atom")
parser.add_argument("-matrix", nargs='?', type=bool, default=True, help="read the dipolar matrix elements")

args = parser.parse_args()
config = vars(args)
def skip_ahead(it, elems):
    assert elems >= 1, "can only skip positive integer number of elements"
    for i in range(elems):
        value = next(it)
    return value
print("To learn more about features, use HFparser.py -h")

if config['md']!=0:
    #reads outcar for Total hyperfine coupling parameters after diagonalization (MHz) and outputs into HFcouplingAll.txt
    num=0
    count4=0
    count3=0
    num2=5
    with open(config["o"], 'r') as f:
             for line in f:
                  if 'Total hyperfine coupling parameters after diagonalization (MHz)' in line:
                     count4=count4+1
             always_print=False
    with open("HFcouplingAll.txt", "w") as y:
         print ('Total hyperfine coupling parameters', file=y, end='')
    with open(config["o"], 'r') as f:
             for line in f:
                 if 'Total hyperfine coupling parameters after diagonalization (MHz)' in line:
                     with open("HFcouplingAll.txt", "a") as y:
                          print (line, file=y, end='')
                          line = skip_ahead(f, 4)
                          always_print=True
                          num=0
                 if always_print:
                    with open("HFcouplingAll.txt", "a") as y:
                         print(line, file=y, end='')
                    if '----------------------------------------------------------------------' in line:
                       count3=count3 +1
                    if count3==2:
                       always_print=False
                       count3=0
                 
    #reads HFcouplingAll file and finds the large values of Azz and outputs into HFvalues.txt
    totalX=0
    totalY=0
    totalZ=0
    with open("HFvalues.txt", 'w') as z:
         print("HF values (MHz) of atom #", int(config['md']),file=z)
         print("Axx       Ayy       Azz", file=z)
    with open("HFcouplingAll.txt", 'r') as x:
         for line in x:
            count4 = count4+ 1
            if any(char.isdigit() for char in line):
               compx = line.split()
               floatcomp=[float(i) for i in compx]
               if floatcomp[0]==config['md']:
                  with open("HFvalues.txt", 'a') as zz:
                       print(floatcomp[1],' ', floatcomp[2],' ',floatcomp[3], file=zz)
    count4=0
    lineNum=0
    with open("HFvalues.txt", 'r') as zzz:
         for line in zzz:
             lineNum=lineNum+1
             if any(char.isdigit() for char in line) and lineNum>=2:
                 count4=count4+1
                 comp=line.split()
                 floatcomp=[float(i)for i in comp]
                 totalX=totalX+(floatcomp[0])
                 totalY=totalY+(floatcomp[1])
                 totalZ=totalZ+(floatcomp[2])
    with open("HFvalues.txt", 'a') as zz:
         avgX=totalX/count4
         avgX=round(avgX,3)
         avgY=totalY/count4
         avgY=round(avgY,3)
         avgZ=totalZ/count4
         avgZ=round(avgZ,3)
         print(" ", file=zz)
         print("Averages:   Axx       Ayy       Azz", file=zz)
         print("        ", avgX, "  ", avgY, "   ", avgZ, file=zz)
    os.remove("HFcouplingAll.txt")
    print("Output files: HFvalues.txt")
count=0
count2=0
count3=0
num=0
count4=0
compare=config['cut']

if config['md']==0 or config['matrix']==True:
    print("Running code to calculate HF values")
    #Reads OUTCAR file and outputs coupling parameters into new file HFcouplingAll.txt
    print("Input files are: OUTCAR")
    ISiso=config['iso']
    if ISiso==True or config['matrix']==True:
        #Reads OUTCAR file and outputs Fermi contact (isotropic) hyperfine coupling parameter (MHz) into new file; HFisoAll.txt
        with open(config["o"], 'r') as f:
             for line in f:
                 if 'Fermi contact (isotropic) hyperfine coupling parameter (MHz)' in line:
                    count4=count4+1
        with open(config["o"], 'r') as f:
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
        with open("HFisoAll.txt", 'r') as t:
             with open("HFisoLarge.txt", "w") as x:
                print( "Atom #    A1c   Atotal    A1c+Atotal", file=x)
                for i, line in enumerate(t):
                    count2 = count2 + 1
                    if '-------------------------------------------------------------' in line and count2>2:
                        break
                    if count2 > 2: #and i%2==0:
                           temp = line.split()
                           floatTemp=[float(i) for i in temp[1:]]
                           if floatTemp[4]>=compare or floatTemp[4]<=-compare:
                              Atotal=floatTemp[3]+floatTemp[4]
                              print(temp[0],"  ", floatTemp[3], "  ",floatTemp[4], "  ",Atotal, file=x)
        
        num=0
        count4=0
        count3=0
        num2=5
        with open(config["o"], 'r') as f:
                 for line in f:
                      if 'Total hyperfine coupling parameters after diagonalization (MHz)' in line:
                         count4=count4+1
                 always_print=False            
        with open(config["o"], 'r') as f:
                 for line in f:
                     if ' Dipolar hyperfine coupling parameters (MHz)' in line:
                         num=num+1
                         num2=num2-1
                         if num==count4:
                            with open("HFdipolarAll.txt", "w") as y:
                                 print (line, file=y, end='')
                                 line = skip_ahead(f, 4)
                                 always_print=True
                                 num=0
                     if always_print:
                        with open("HFdipolarAll.txt", "a") as y:
                             print(line, file=y, end='')
                        if '-------------------------------------------------------------' in line:
                           count3=count3 +1
                     if count3==1:
                        always_print=False
        with open("HFmatrix.txt", 'w') as z:
            print("HF_Large matrix values (MHz)", file=z)
            print("Atom  Axx     Ayy     Azz    Axy    Axz   Ayz", file=z)
        with open("HFisoLarge.txt", 'r') as y:
            lines_y = y.readlines()
        values_y = []
        for line in lines_y:
            count2 += 1
            if '-------------------------------------------------------------' in line and count2 > 3:
                break
            compy = line.split()
            values_y.append(compy[0])
        with open("HFdipolarAll.txt", 'r') as x:
            count5=0
            for line in x:
                count5 += 1
                if '-------------------------------------------------------------' in line and count4 > 5:
                    break
                compx = line.split()
                if compx and compx[0] in values_y:
                    with open("HFmatrix.txt", 'a') as z:
                         print(int(compx[0]), ' ', f"{float(compx[1]):.2f}" ,' ', f"{float(compx[2]):.2f}",' ',f"{float(compx[3]):.2f}", ' ', f"{float(compx[4]):.2f}",' ', f"{float(compx[5]):.2f}",' ',f"{float(compx[6]):.2f}", file=z)
                        
        os.remove("HFdipolarAll.txt")
        #removes HFdipolarAll.txt file
        if config["matrix"]==True and config["iso"]==False:
           print("Running code to calculate matrix of large hyperfine values and large isotropic hyperfine values")
           print("Output files: HFisoAll.txt, HFisoLarge.txt, HFmatrix.txt, HFvalues.txt")
    
    if (config["matrix"])==False and config["iso"]==True:
        print("Running code to calculate large isotropic hyperfine values")
        print("Output files are: HFisoAll.txt, HFisoLarge.txt, HFvalues.txt")
        os.remove("HFmatrix.txt")
    #reads outcar for Total hyperfine coupling parameters after diagonalization (MHz) and outputs into HFcouplingAll.txt
    num=0
    count4=0
    count3=0
    num2=5
    with open(config["o"], 'r') as f:
             for line in f:
                  if 'Total hyperfine coupling parameters after diagonalization (MHz)' in line:
                     count4=count4+1
             always_print=False
    with open(config["o"], 'r') as f:
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
         print("HF Values (MHz)", file=z)
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
                       print(int(floatcomp[0]), ' ', floatcomp[1],' ', floatcomp[2],' ',floatcomp[3], file=zz)
    
    os.remove("HFcouplingAll.txt")
    #removes HFcouplingAll.txt file
    if config['matrix']==False and config['iso']==False:
       print("Output files: HFvalues.txt")
