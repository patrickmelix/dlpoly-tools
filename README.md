# dlpoly-tools
This Repository offers some of the codes that I use to handle DL_POLY Classic calculations. Feel free to contribute yours.

- history2xyz: Converts a HISTORY trajectory from DL_Poly into a xyz-trajectory. The xyz file is of the extended format used by ASE and includes cell vectors. Can be used as a script or module.
- statisreader: Reads the information from a STATIS file and returns a dictionary conatining the meta-information as well as a list containing all values for every simulation step present in the STATIS file. Also contains an easy way ('statisNames()') to name the values just retrieved by providing an ordered list of descriptions according to the Manual.
