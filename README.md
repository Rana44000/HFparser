# HFparser
Code to find and output large hyperfine values from OUTCAR file.

The OUTCAR file is from running the VASP program.

For more information on OUTCAR, see: https://www.vasp.at/wiki/index.php/OUTCAR

For more information on VASP, see: https://www.vasp.at/wiki/index.php/The_VASP_Manual

reads OUTCAR file for hyperfine tensor values. 

Searches for the large values using the HF cutoff. The default cutoff value is 8. The user can change this. 

Finds the atoms of the large values and outputs the atom numbers and hyperfine tensor values into new file HFvalues.txt.

Additionally:

can find all HF values and averages for a user defined atom using -md and atom number

can print out dipolar matrix values and large isotropic hyperfine values using -matrix and True as well as default HFvalues

can print out isotropic hyperfine values if user chooses into HFisoAll.txt and HFisoLarge.txt using -iso and True

Input files: OUTCAR

Output files: HFvalues.txt, HFisoAll.txt, HFisoLarge.txt, HFmatrix.txt

Sample output in HFvalues.txt with SiH3 OUTCAR file:
default: HFvalues(md=0).txt
-iso True: HFvalues(md=0).txt, HFisoAll.txt, HFisoLarge.txt
-matrix True: HFvalues(md=0).txt, HFisoAll.txt, HFisoLarge.txt, HFmatrix.txt
-md 1: HFvalues(md=1).txt
