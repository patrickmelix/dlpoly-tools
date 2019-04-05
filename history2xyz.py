#!/usr/bin/python3
#
# Script to convert a DL_POLY HISTORY file to a XYZ-trajectory without loosing information
# Cell Vectors are put in the comment line in an ASE compatible form
# by Patrick Melix
# 2017/07/08
#
# You can import the module and use the functions or call it as a script
import os, sys, argparse



def main(inFile='HISTORY', outFile='traj.xyz', samePath=False, verbose=False):
    print('Welcome.')
    atomNames = {}
    atomNames['ca'] = 'C'
    atomNames['cb'] = 'C'
    atomNames['cc'] = 'C'
    atomNames['cd'] = 'C'
    atomNames['ce'] = 'C'
    atomNames['c1'] = 'C'
    atomNames['cn'] = 'C'
    atomNames['co'] = 'C'
    atomNames['o1'] = 'O'
    atomNames['oc'] = 'O'
    atomNames['n1'] = 'N'
    atomNames['ns'] = 'N'
    atomNames['ni'] = 'Ni'
    atomNames['cu'] = 'Cu'
    atomNames['h1'] = 'H'
    atomNames['ha'] = 'H'
    atomNames['ho'] = 'H'
    atomNames['hn'] = 'H'

    if os.path.isdir(inFile):
        inFile = os.path.join(inFile,'HISTORY')
    if samePath:
        outFile = os.path.join(os.path.split(inFile)[0],outFile)
        print("Writing to {:}".format(outFile))

    convertHistory2XYZ(inFile, outFile, atomNames, verbose)
    if verbose: print('Done!')

def convertHistory2XYZ(inFile, outFile, atomNames, verbose=False):
    bunchsize = 1000000     # Experiment with different sizes 1000000
    bunch = []
    if verbose: print('Processing...')
    with open(inFile, "r", bunchsize) as r, open(outFile, "w", bunchsize) as w:
        #skip header line
        next(r)
        line = r.readline().strip().split()
        levcfg,imcon,nAtoms = [int(x) for x in line[0:3]]
        if verbose:
            print('levcfg: '+str(levcfg))
            print('imcon: '+str(imcon))
            print('nAtoms: '+str(nAtoms))
            print('Frame: 0...', end='\r')
        nItems = (levcfg+1)*3
        if imcon == 6:
            latticeBool = 'pbc="T T F"'
        elif imcon > 0:
            latticeBool = 'pbc="T T T"'
        properties = 'Properties=species:S:1:pos:R:3 '
        if levcfg == 1:
            properties = 'Properties=species:S:1:pos:R:3:vel:R:3 '
        elif levcfg == 2:
            properties = 'Properties=species:S:1:pos:R:3:vel:R:3:forces:R:3 '
        iLine = 0
        iFrame = 0
        for line in r:
            split = line.split()
            if split[0].lower() == 'timestep':
                bunch.append(str(nAtoms)+'\n')
                iFrame += 1
                if verbose: print('Frame: '+str(iFrame)+'...', end='\r')
                tmp = []
                #timestep value
                #tmp.append(split[0])
                #tmp.append(split[1])
                if imcon > 0:
                    #three vectors
                    tmp.append('Lattice="')
                    for i in range(0,3):
                        tmp.append(("{:} "*3).format(*[float(x) for x in r.readline().strip().split()]))
                    tmp.append('" '+properties+latticeBool)
                tmp.append('\n')
                bunch.append(''.join(tmp))
            else:
                tmp = []
                for i in range(0,levcfg+1):
                    tmp.extend([float(x) for x in r.readline().strip().split()])
                name = atomNames[split[0].lower()]
                bunch.append(("{:4}"+("{:16f}")*nItems+'\n').format(name,*tmp))

            if len(bunch) == bunchsize:
                w.writelines(bunch)
                iLine += bunchsize
                bunch = []
        w.writelines(bunch)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert HISTORY file to ASE extxyz')
    parser.add_argument('-i', '--input', type=str, help='input file or folder', default='HISTORY')
    parser.add_argument('-o', '--output', type=str, help='output file', default="traj.xyz")
    parser.add_argument('--samepath', action='store_true', help='output file in same dir as input')
    parser.add_argument('-v', '--verbose', action='store_true', help='print progress info')
    args = parser.parse_args()

    main(args.input, args.output, args.samepath, args.verbose)


