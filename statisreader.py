#!/usr/bin/python3
#
# Module to load the results of a DL_POLY calculation from a STATIS file.
# Add to your $PYTHONPATH or copy code to your script
#
# by Patrick Melix
# 2017/10/18

__all__ = ['readSTATIS', 'statisNames']
  
try:
    import os
    import errno
except ModuleNotFoundError:
    __all__ = []

def readSTATIS(statis='STATIS', path='./',chunkSize=1024):
    """
    Reads a DL_POLY STATIS file given as statis (default="STATIS") from path in pieces of chunkSize.
    Returns metaInfo, data:

        -metaInfo: Dictionary that contains the system name, energy units, number of steps, number of data points per step.
                   Contains keys: 'systemName', 'units', 'nSteps', 'nPoints'.

        -data: The Energies from every step in the statis file are returned as a list inside a list.
               The information of the first step is therefore found in the 0th element of the returned list.

    """
    #filepath
    filePath = os.path.join(path,statis)
    if not os.path.isfile(filePath):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filename)
    if not type(chunkSize) == int:
        raise ValueError('chunkSize must be of type integer')

    #initiate return list and dict
    data = [[]]
    metaInfo = {}

    #read file in chunkSizes to avoid I/O
    with open(filePath, "r", chunkSize) as read:

        #read header
        metaInfo['systemName'] = read.readline().strip()
        metaInfo['units'] = read.readline().strip().split('=')[-1]
        metaInfo['nPoints'] = int(read.readline().strip().split()[-1])

        #read the data
        for line in read:

            l = line.strip().split()

            #if this is a line that ends with the number of points, go to the next step
            if l[-1] == str(metaInfo['nPoints']):
                data.append([])

            #save data
            data[-1].extend([float(x) for x in l])
 
        #length of data gives nSteps
        metaInfo['nSteps'] = len(data)

        #check length of each data set
        if not set([len(dataSet) for dataSet in data]) == set([metaInfo['nPoints']]):
            raise RuntimeError('Not all lengths of data sets are equal to '+str(metaInfo['nPoints'])+', is your STATIS file valid?')

    return metaInfo,data



def statisNames():
    """
        Returns a list of descriptions (strings) that define the values printed in a STATIS file in the right ordering.
        Stops at 'pressure', all values after the pressure are system-dependent (forces etc.).
        Usefull for labelling purposes of data obtained by readSTATIS().
    """
    names = ['total extended system energy',
            'system temperature',
            'configurational energy',
            'VdW/metal/Tersoff energy',
            'electrostatic energy',
            'chemical bond energy',
            'valence angle/3-body potential energy',
            'dihedral/inversion/four body energy',
            'tethering energy',
            'enthalpy (total energy + PV)',
            'rotational temperature',
            'total virial',
            'VdW/metal/Tersoff virial',
            'electrostatic virial',
            'bond virial',
            'valence angle/3-body virial',
            'constraint virial',
            'tethering virial',
            'volume',
            'core-shell temperature',
            'core-shell potential energy',
            'core-shell virial',
            'MD cell angle α','MD cell angle β','MD cell angle γ',
            'Potential of Mean Force virial',
            'pressure']
    return names
