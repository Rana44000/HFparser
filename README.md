# HFparser
## Overview
  Code to find and output large hyperfine values from OUTCAR file from a VASP simulation. It reads OUTCAR file and searches for hyperfine tensor values. It can find the hyperfine values for select atoms of interest. The code can print out the isotropic parameter, the hyperfine matrix elements, and the core corrections. The code can print output for the final results of the relaxation or follow the results during a molecular dynamic simulation. Several command line arguments are availble for the user to select the desired output. 

## Command Line Arguments
| Argument | Type | Default | Description |
| :------: | :---: | :----: | :---------: |
| -o |  | ./OUTCAR | outcar file location and name |
| -c | float | 8.0 | hyperfine cutoff value |
| -iso | bool | True | output isotropic hyperfine values into HFisoAll.txt and HFisoLarge.txt |
| -md | float | 0 | atom number for HF values to output HF values and averages of this atom |
| -m | bool | True | read the dipolar matrix elements |

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
