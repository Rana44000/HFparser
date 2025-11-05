# HFparser
Code to find and output large hyperfine values from OUTCAR file.

reads OUTCAR file for hyperfine tensor values. 

Searches for the large values using the HF cutoff. The default cutoff value is 8. The user can change this. 

Finds the atoms of the large values and outputs the atom numbers and hyperfine tensor values into new file HFvalues.txt.

Additionally:

can find all HF values and averages for a user defined atom using -md and atom number

can print out isotropic hyperfine values if user chooses into HFisoAll.txt and HFisoLarge.txt using -iso and True

Input files: OUTCAR

Output files: HFvalues.txt, HFisoAll.txt, HFisoLarge.txt

Sample output in HFvalues.txt with SiH3:


HF_Large coordinates

Atom  Axx       Ayy       Azz

1.0   362.917   362.833   621.1

2.0   -23.614   -10.418   -28.168

3.0   -23.051   -9.906   -27.658

4.0   -23.877   -10.821   -28.479
