from time import time
START=time()

from agilepy.api.AGAnalysis import AGAnalysis
import argparse
import pathlib
import os


def GetTargetYAML(targetnumber):
    
    # Set the path of the Directories to use.
    CurrentDirectory = pathlib.Path(__file__).absolute().parent
    ConfFileDire = CurrentDirectory.joinpath(f"ConfigurationFiles")
    
    # Choose Target
    if targetnumber==0:
        SourceName='Vela_Long'
    elif targetnumber==1:
        SourceName='Vela_restricted_period'
    elif targetnumber==2:
        SourceName='Vela_across_restricted_period'
    elif targetnumber==3:
        SourceName='Vela'
    else:
        raise ValueError(f"Target number {targetnumber} not valid.")
    
    # Set File path
    path=ConfFileDire.joinpath(f"AgilepyConf_{SourceName}.yml")
    
    # Check if it exists
    if not os.path.exists(path):
        raise FileNotFoundError(f"File does not exists: {path}")
    
    return str(path)
    

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
    
    