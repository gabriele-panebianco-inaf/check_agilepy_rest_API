from agilepy.api.AGAnalysis import AGAnalysis

import pathlib
import argparse
import os
import yaml

def GetTarget(TargetsFile, TargetNumber):
    """
    Read the YAML file with the targets and return the dict of the requested Target,
    identified by its progressivenumber.
    
    Parameters:
    TargetsFile : str
        Path of the file with the Targets and their progressive number.
    TargetNumber : int
        Progressive Number of the chosen target.
    
    Returns
    -------
    Target : dict
        Dictionary with Target information to write the Agilepy Configuration File.
    """
    
    with open(TargetsFile, 'r') as file:
        Targets = yaml.safe_load(file)
        
    Target=Targets[f'Target_{TargetNumber}']

    return Target

def make_directory(path):
    """Create directory if it does not exist"""
    if not os.path.exists(path):
        os.makedirs(path)
    return None

if __name__=="__main__":
    
    # Set the path of the Directories and files to use.
    CurrentDirectory = pathlib.Path(__file__).absolute().parent
    DataFilePath = CurrentDirectory.joinpath(f"DataFiles/")
    ConfFileDire = CurrentDirectory.joinpath(f"ConfigurationFiles")
    make_directory(DataFilePath)
    make_directory(ConfFileDire)
    TargetsFile = CurrentDirectory.joinpath("Targets.yml")

    # Argument
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", help="Number of the target source", type=int)
    args = parser.parse_args()

    # Get Target Name
    Target = GetTarget(TargetsFile, args.target)
    ConfFilePath = ConfFileDire.joinpath(f"AgilepyConf_{Target['SourceName']}.yml")
    
    # Write the Configuration YAML file
    AGAnalysis.getConfiguration(
        confFilePath = str(ConfFilePath),

        # 1 - Input
        evtfile=None,
        logfile=None,
        userestapi=True,
        datapath=str(DataFilePath),

        # 2 - Output
        outputDir = str(CurrentDirectory.joinpath(f"Results/")),
        sourceName = Target['SourceName'],
        userName = "Gabriele",
        verboselvl = 2,

        # 3 - Selection
        tmin = Target['tmin'],
        tmax = Target['tmax'],
        timetype = Target['TimeType'],
        glon = Target['glon'],
        glat = Target['glat'],
    )