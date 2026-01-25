# HFparser
## Overview
  Code to find and output large hyperfine values from OUTCAR file. It reads OUTCAR file for hyperfine tensor values and searches for the large values using the HF cutoff. The default cutoff value is 8. The user can change this. It finds the atoms of the large values and outputs the atom numbers and hyperfine tensor values into new file HFvalues.txt. Additionally, it can find and output all HF values and averages for a single user defined atom, output isotropic hyperfine values, and read dipolar matrix elements. These command line arguments are detailed below. 

## Command Line Arguments
| Argument | Type | Default | Description |
| :------: | :---: | :----: | :---------: |
| -outcar |  | ./OUTCAR | outcar file location |
| -hfcutoff | float | 8.0 | HF cuttoff value |
| -iso | bool | False | output isotropic hyperfine values into HFisoAll.txt and HFisoLarge.txt |
| -md | float | 0 | atom number for HF values to output HF values and averages of this atom |
| -matrix | bool | False | read the dipolar matrix elements |

## Features
- Find large hyperfine tensor values
- Find all HF values and averages for a user defined atom
- Print out dipolar matrix values and large isotropic hyperfine values as well as default HFvalues
- Print out isotropic hyperfine values if user chooses into HFisoAll.txt and HFisoLarge.txt

## VASP
The OUTCAR file is from running the VASP program.

For more information on OUTCAR, see: https://www.vasp.at/wiki/index.php/OUTCAR

For more information on VASP, see: https://www.vasp.at/wiki/index.php/The_VASP_Manual


## Input files:
- OUTCAR

## Output files: 
- HFvalues.txt
- HFisoAll.txt
- HFisoLarge.txt
- HFmatrix.txt

## Sample output in HFvalues.txt with SiH3 OUTCAR file:
- HFvalues(md=0).txt
- iso True: HFvalues(md=0).txt, HFisoAll.txt, HFisoLarge.txt
- matrix True: HFvalues(md=0).txt, HFisoAll.txt, HFisoLarge.txt, HFmatrix.txt
- md 1: HFvalues(md=1).txt
