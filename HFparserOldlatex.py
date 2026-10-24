#input files: OUTCAR file
#output files: HFvalues.txt, if chosen: HFisoAll.txt, HFisoLarge.txt
#This code is to find and print the large Hyperfine values. 
import argparse
import os
#import csvtex 
import pandas as pd
#latex

parser = argparse.ArgumentParser(description="Arguments for vasp output file ",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-o", nargs='?',const="./OUTCAR", default = "./OUTCAR", help="outcar file location")
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
         print("HF values (MHz) of atom #", int(config['md']),"  (no core correction)", file=z)
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
            print("Atom  Axx     Ayy     Azz    Axy    Axz   Ayz       a_iso        a_iso with core corr", file=z)
        iso = {}
        with open("HFisoLarge.txt") as f:
            for line in f:
                if "Atom" in line:
                    continue
                parts = line.split()
                if parts:
                    atom = parts[0]
                    iso[atom] = parts
        
        with open("HFdipolarAll.txt") as f, open("HFmatrix.txt", "a") as out:
            for line in f:
                parts = line.split()
                if not parts:
                    continue
        
                atom = parts[0]
                if atom in iso:
                    iso_parts = iso[atom]
                    print(
                        atom,"  ", f"{float(parts[1]):.2f}", "   ",f"{float(parts[2]):.2f}","     ", f"{float(parts[3]):.2f}", "     ", f"{float(parts[4]):.2f}","       ", f"{float(parts[5]):.2f}","       ", f"{float(parts[6]):.2f}", "      ", f"{float(iso_parts[2]):.2f}", "       ", f"{float(iso_parts[3]):.2f}",
                        file=out
                    )

           
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
         print("HF Values (MHz) (no core correction", file=z)
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

#matrix wit h the eigenvalue stuff
import csv
import numpy as np
#import pandas as pd
import os

element_symbols = []
element_counts = []

with open(config["o"], 'r') as f:
    for line in f:
        if "POTCAR:" in line:
            parts = line.split()
            for p in parts:
                if p.isalpha() and len(p) <= 2:
                    element_symbols.append(p)
                    break
        if "ions per type" in line:
            nums = line.replace("=", " ").split()
            for n in nums:
                if n.isdigit():
                    element_counts.append(int(n))

atom_elements = []
for symbol, count in zip(element_symbols, element_counts):
    atom_elements.extend([symbol] * count)
A1c_map = {}

fc_block_count = 0
with open(config["o"], 'r') as f:
    for line in f:
        if "Fermi contact (isotropic) hyperfine coupling parameter" in line:
            fc_block_count += 1

with open(config["o"], 'r') as f:
    capture = False
    current_block = 0
    separator_seen = 0

    for line in f:
        if "Fermi contact (isotropic) hyperfine coupling parameter" in line:
            current_block += 1
            capture = (current_block == fc_block_count)
            separator_seen = 0
            continue

        if capture:
            if "-----" in line:
                separator_seen += 1
                if separator_seen >= 3:
                    capture = False
                continue
            if separator_seen < 2:
                continue

            parts = line.split()
            if len(parts) < 6:
                continue

            if not parts[0].isdigit():
                continue

            ion = int(parts[0])
            A1c_map[ion] = float(parts[4])

dipolar_count = 0
with open(config["o"], 'r') as f:
    for line in f:
        if 'Dipolar hyperfine coupling parameters (MHz)' in line:
            dipolar_count += 1

num = 0
count3 = 0
with open(config["o"], 'r') as f:
    always_print = False
    for line in f:
        if 'Dipolar hyperfine coupling parameters (MHz)' in line:
            num += 1
            if num == dipolar_count:
                with open("HFdipolarAll.txt", "w") as y:
                    print(line, file=y, end='')
                    line = skip_ahead(f, 4)
                    always_print = True

        if always_print:
            with open("HFdipolarAll.txt", "a") as y:
                print(line, file=y, end='')
            if '-------------------------------------------------------------' in line:
                count3 += 1
        if count3 == 1:
            always_print = False
            count3 = 0
with open("HFmatrix.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "Atom",
        "Axx_corr", "Ayy_corr", "Azz_corr",
        "Axy", "Axz", "Ayz",
        "Eigenvalue1", "Theta1", "Phi1",
        "Eigenvalue2", "Theta2", "Phi2",
        "Eigenvalue3", "Theta3", "Phi3",
        "aiso", "A1c"
    ])
iso = {}
with open("HFisoLarge.txt") as f:
    for line in f:
        if "Atom" in line:
            continue
        parts = line.split()
        if parts:
            atom = parts[0]
            iso[atom] = parts
#isovals={}
#with open("HFisoLarge.txt") as f:
#    for line in f:
#        if "Atom" not in line:
#            
#            isvals = line.split()
#            if isvals:
#                inums = isvals[3]
#                isovals[inums] = inums
isovals = {}
with open("HFisoLarge.txt") as f:
    for line in f:
        if "Atom" in line:
            continue
        fields = line.split()
        if not fields:
            continue
        atom_num = fields[0] #=atom index
        iso_val = float(fields[3])+float(fields[1]) #isotropic value
        isovals[atom_num] = iso_val
#with open(HFisoLarge.txt)
with open("HFdipolarAll.txt") as f, open("HFmatrix.csv", "a", newline="") as csvfile:
    writer = csv.writer(csvfile)

    for line in f:
        parts = line.split()
        if not parts or not parts[0].isdigit():
            continue

        ion = int(parts[0])
        atom_index = ion - 1
        element = atom_elements[atom_index]

        atom = parts[0]
        if atom in iso:
            iso_val = float(isovals[atom])
            Axx_orig = float(parts[1])+ float(iso_val) # should add new isolarge value here from HFisoLarge.txt file 
            Ayy_orig = float(parts[2]) + float(iso_val)
            Azz_orig = float(parts[3]) + float(iso_val)
            Axy = float(parts[4])
            Axz = float(parts[5])
            Ayz = float(parts[6])

            a_iso = float(iso[atom][2])

            A1c = A1c_map[ion]

            Axx_corr = Axx_orig - A1c
            Ayy_corr = Ayy_orig - A1c
            Azz_corr = Azz_orig - A1c

            HF_tensor = np.array([
                [Axx_corr, Axy,      Axz],
                [Axy,      Ayy_corr, Ayz],
                [Axz,      Ayz,      Azz_corr]
            ])

            eigvals, eigvecs = np.linalg.eigh(HF_tensor)

            polar_coords = []
            for i in range(3):
                v = eigvecs[:, i] / np.linalg.norm(eigvecs[:, i])
                x, y, z = v
                theta = np.degrees(np.arccos(z))
                phi = np.degrees(np.arctan2(y, x))
                polar_coords.append((theta, phi))

            writer.writerow([
                element,
                round(Axx_corr, 1), round(Ayy_corr, 1), round(Azz_corr, 1),
                round(Axy, 1), round(Axz, 1), round(Ayz, 1),
                round(eigvals[0], 1), round(polar_coords[0][0], 1), round(polar_coords[0][1], 1),
                round(eigvals[1], 1), round(polar_coords[1][0], 1), round(polar_coords[1][1], 1),
                round(eigvals[2], 1), round(polar_coords[2][0], 1), round(polar_coords[2][1], 1),
                round(a_iso, 1), round(A1c, 1)
            ])

os.remove("HFdipolarAll.txt")
#latex table stuff
df = pd.read_csv("HFmatrix.csv")

for col in df.columns:
    if df[col].dtype in ["float64", "int64"]:
        df[col] = df[col].map(lambda x: f"{x:.1f}")

rows = []

for _, row in df.iterrows():
    
    atom = row["Atom"]
    
    eigs = [
        float(row["Eigenvalue1"]),
        float(row["Eigenvalue2"]),
        float(row["Eigenvalue3"])
    ]
    thetas = [
        float(row["Theta1"]),
        float(row["Theta2"]),
        float(row["Theta3"])
    ]
    phis = [
        float(row["Phi1"]),
        float(row["Phi2"]),
        float(row["Phi3"])
    ]

    Axx = float(row["Axx_corr"])
    Ayy = float(row["Ayy_corr"])
    Azz = float(row["Azz_corr"])
    Axz = float(row["Axz"])
    Ayz = float(row["Ayz"])
    Axy = float(row["Axy"])
    
    thetaR1= np.radians(thetas[0])
    thetaR2= np.radians(thetas[1])
    thetaR3 =np.radians(thetas[2])
    phiR1= np.radians(phis[0])
    phiR2 = np.radians(phis[1])
    phiR3 = np.radians(phis[2])

    A_par_c = (
    Axz + Ayz + Azz
    )

    A_par_a = (
    Axx+Axy+Axz
    )
    A_isoNEW=(Axx+Ayy+Azz)/3
    
    rows.append([atom, r"$A_{1}$", f"{Axx:.1f}", f"{eigs[0]:.1f}", f"{thetas[0]:.1f}", f"{phis[0]:.1f}"])
    rows.append(["", r"$A_{2}$", f"{Ayy:.1f}", f"{eigs[1]:.1f}", f"{thetas[1]:.1f}", f"{phis[1]:.1f}"])
    rows.append(["", r"$A_{3}$", f"{Azz:.1f}", f"{eigs[2]:.1f}", f"{thetas[2]:.1f}", f"{phis[2]:.1f}"])
    
    rows.append(["", r"$A_{iso}$", "", f"{A_isoNEW:.1f}", "", ""])
    rows.append(["", r"$A_{\parallel c}$", "", f"{A_par_c:.1f}", "", ""])
    rows.append(["", r"$A_{\parallel a}$","", f"{A_par_a:.1f}", "", ""])

    
df2 = pd.DataFrame(rows, columns=["Nucleus", "Parameter", "oldValue", "A (MHz)", r"$\theta$$^\circ$", r"$\phi$$^\circ$"])
lat_new = df2.drop('oldValue', axis=1)
#latex_table2 = lat_new.to_latex(index=False, escape=False)

latex_table2 = lat_new.to_latex(index=False, escape=False, column_format="rrrrrr")

with open("HFtable.tex", "w") as texfile:
    texfile.write(r"\documentclass{article}" "\n")
    texfile.write(r"\usepackage{booktabs}" "\n")
    texfile.write(r"\usepackage{amsmath}" "\n")
    texfile.write(r"\usepackage[margin=1in]{geometry}" "\n")
    texfile.write(r"\begin{document}" "\n\n")
    
    texfile.write(latex_table2)
    texfile.write("\n" + r"\end{document}" + "\n")


####################################################
    # latex table stuff
   
# test code for gyromagnetic table for superscripts
#with open("GyroTable.csv", 'r') as table:
    #for line in table:
        #maybe make it so this info is transferred into the csv then to latex instead of just latex
    
   # fix so that
    #os.remove("HFdipolarAll.txt")
