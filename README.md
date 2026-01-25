# HFparser
Code to find and output large hyperfine values from OUTCAR file.

# Command Line Arguments
| Argument | Type | Default | Description |
| ---------- | ---------- | ---------- |
| -outcar |  | ./OUTCAR | outcar file location |
| -hfcutoff | float | 8.0 | cuttoff HF value |
| -iso | bool | False | output isotropic hyperfine values into HFisoAll.txt and HFisoLarge.txt |
| -md | float | 0 | atom number for HF values to output HF values and averages of this atom |
| -matrix | bool | False | read the dipolar matrix elements |

# Features
- find all HF values and averages for a user defined atom
- print out dipolar matrix values and large isotropic hyperfine values as well as default HFvalues
- print out isotropic hyperfine values if user chooses into HFisoAll.txt and HFisoLarge.txt


The OUTCAR file is from running the VASP program.

For more information on OUTCAR, see: https://www.vasp.at/wiki/index.php/OUTCAR

For more information on VASP, see: https://www.vasp.at/wiki/index.php/The_VASP_Manual

reads OUTCAR file for hyperfine tensor values. 

Searches for the large values using the HF cutoff. The default cutoff value is 8. The user can change this. 

Finds the atoms of the large values and outputs the atom numbers and hyperfine tensor values into new file HFvalues.txt.


Input files: OUTCAR

Output files: HFvalues.txt, HFisoAll.txt, HFisoLarge.txt, HFmatrix.txt

Sample output in HFvalues.txt with SiH3 OUTCAR file:
default: HFvalues(md=0).txt
-iso True: HFvalues(md=0).txt, HFisoAll.txt, HFisoLarge.txt
-matrix True: HFvalues(md=0).txt, HFisoAll.txt, HFisoLarge.txt, HFmatrix.txt
-md 1: HFvalues(md=1).txt
