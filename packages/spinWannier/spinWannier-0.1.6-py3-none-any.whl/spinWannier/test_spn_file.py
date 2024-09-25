import pickle
import numpy as np
from scipy.io import FortranFile

def spn_to_dict(model_dir='./', fwin="wannier90.win", fin="wannier90.spn", formatted=False, fout="spn_dict.pickle", save_as_text=False):
    """Convert wannier90.spn file to a dictionary object and save as pickle. 
    If 'text_file' == True, then save as a human-readable text file."""

    if formatted is True and fin.split('.')[-1] != 'formatted':
        raise Warning(f"Are you sure {fin} is a formatted (human-readable) file and not a binary FortranFile?")
    if formatted is False and fin.split('.')[-1] == 'formatted':
        raise Warning(f"Are you sure {fin} is a binary FortranFile and not a human-readable file?")

    fwin = model_dir + fwin
    fin = model_dir + fin
    fout = model_dir + fout

    if formatted is True:
        # human-readable spn file ("wannier90.spn_formatted")
        with open(fin, 'r') as fr:
            fr.readline()
            # get number of bands and kpoints
            NB = int(float(fr.readline()))
            NK = int(float(fr.readline()))
        with open(fin, 'r') as fr:
            # get the spin-projection matrices
            Sskmn = np.loadtxt(fr, dtype=np.complex64, skiprows=3)
    else:
        # FortranFile spn file ("wannier90.spn")
        with FortranFile(fin, 'r') as fr:
            header = fr.read_record(dtype='c')
            NB, NK = fr.read_record(dtype=np.int32)
            Sskmn = []
            for i in range(NK):
                Sskmn.append(fr.read_record(dtype=np.complex128))
            Sskmn = np.array(Sskmn)
    return Sskmn


if __name__ == "__main__":
    model_dir = 'C:/Users/lv268562/Documents/PhD work/Scripts/spinWannier/examples/CrSTe/2_wannier/'
    Sskmn_formatted = spn_to_dict(formatted=True, model_dir=model_dir)
    Sskmn = spn_to_dict(formatted=False, model_dir=model_dir, fin="wannier90.spn")
    print(np.allclose(Sskmn, Sskmn_formatted))
    print(np.max(np.abs(Sskmn - Sskmn_formatted)))