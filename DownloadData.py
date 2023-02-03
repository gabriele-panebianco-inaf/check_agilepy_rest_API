from time import time
START=time()

from agilepy.api.AGAnalysis import AGAnalysis
import argparse
import pathlib
import os
import yaml


def GetTargetYAML(TargetNumber):
    """
    Get the Agilepy Configuration YAML File through the TargetNumber.
    
    Parameters
    ----------
    TargetNumber : int
        Progressive Number of the chosen target.
        
    Returns
    -------
    path : str
        Path of the Agilepy Configuration File.    
    """
    
    # Set the path of the Directories to use.
    CurrentDirectory = pathlib.Path(__file__).absolute().parent
    ConfFileDire = CurrentDirectory.joinpath(f"ConfigurationFiles")
    TargetsFile = CurrentDirectory.joinpath("Targets.yml")
    
    # Read Target Source Name
    with open(TargetsFile, 'r') as file:
        Targets = yaml.safe_load(file)
            
    SourceName=Targets[f'Target_{TargetNumber}']['SourceName']
    
    # Set File path
    path=str(ConfFileDire.joinpath(f"Download_{SourceName}.yml"))
    
    # Check if it exists
    if not os.path.exists(path):
        raise FileNotFoundError(f"File does not exists: {path}")
    
    return path
    

def RunDownloadData(ConfFilePath):
    
    # Load AGAnalysis object
    ag = AGAnalysis(ConfFilePath)
    ag.setOptions(binsize=0.5)
    
    # DownLoad Data
    try:
        ag.generateMaps()
    except Exception as e:
        ag.deleteAnalysisDir()
        raise e
    
    # Clear up Analysis Directory
    ag.deleteAnalysisDir()
    
    return None



if __name__=="__main__":

    # Argument
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", help="Number of the target source", type=int)
    args = parser.parse_args()
        
    # Get Target Name
    ConfFilePath = GetTargetYAML(args.target)
    print(f"Configuration File: {ConfFilePath}")
    
    # Run Analysis
    RunDownloadData(ConfFilePath)
    
    # RunTime
    print(f"TOTAL RUNTIME = {float(time()-START):.3f} s.")
    
    