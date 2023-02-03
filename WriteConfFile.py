from agilepy.api.AGAnalysis import AGAnalysis

import pathlib
import argparse
import os
import yaml

def GetTarget(TargetsFile, TargetNumber):
    """
    Read the YAML file with the targets and return the dict of the requested Target,
    identified by its progressivenumber.
    
    Parameters
    ----------
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
    
    # Argument
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", help="Number of the target source", type=int)
    args = parser.parse_args()
    
    # Set the path of the Directories and files to use.
    CurrentDirectory = pathlib.Path(__file__).absolute().parent
    TargetsFile = CurrentDirectory.joinpath("Targets.yml")
    
    # Make Directory to store the Agilepy Configuration Files
    ConfFileDire = CurrentDirectory.joinpath(f"ConfigurationFiles")
    make_directory(ConfFileDire)
    
    # Get Target Name
    Target = GetTarget(TargetsFile, args.target)
    ConfFilePath = str(ConfFileDire.joinpath(f"Download_{Target['SourceName']}.yml"))
    
    # Make Directory to store Downloaded Data
    DataFilePath = str(CurrentDirectory.joinpath(f"DataFiles/{args.target}_{Target['SourceName']}"))
    make_directory(DataFilePath)
    
    # Write the Configuration YAML file for Downloading Data
    AGAnalysis.getConfiguration(
        confFilePath = ConfFilePath,

        # 1 - Input
        evtfile=None,
        logfile=None,
        userestapi=True,
        datapath=DataFilePath,

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
    
    # Write the Configuration YAML file for Analysis
    ConfFilePath = str(ConfFileDire.joinpath(f"Analysis_{Target['SourceName']}.yml"))
    AGAnalysis.getConfiguration(
        confFilePath = ConfFilePath,

        # 1 - Input
        evtfile=f"{DataFilePath}/EVT.index",
        logfile=f"{DataFilePath}/LOG.index",
        userestapi=False,
        datapath=DataFilePath,

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