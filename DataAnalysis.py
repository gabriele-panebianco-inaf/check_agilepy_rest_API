from time import time
START=time()

from agilepy.api.AGAnalysis import AGAnalysis
import argparse
import os
import pathlib
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
    path=str(ConfFileDire.joinpath(f"Analysis_{SourceName}.yml"))
    
    # Check if it exists
    if not os.path.exists(path):
        raise FileNotFoundError(f"File does not exists: {path}")
    
    return path



def RunDataAnalysis(ConfFilePath):
    
    # Load AGAnalysis object
    ag = AGAnalysis(ConfFilePath)
    
    # Set Options
    ag.setOptions(binsize=0.5)
    ag.setOptions(energybins=[[100, 50000]])
    
    # Print Analysis Options
    ag.printOptions()
    
    # Add sources for MLE
    sources = ag.loadSourcesFromCatalog("2AGL", rangeDist = (0, 5))
    sources = ag.selectSources("flux > 0", show = True)
    
    # Free Sources parameters
    name="2AGLJ0835-4514" # This is Vela
    sources = ag.freeSources(f'name == "{name}"', "pos", True)
    sources = ag.freeSources(f'name == "{name}"', "flux", True)
    
    
    
    # Generate Maps Data
    try:
        ag.generateMaps()
    except Exception as e:
        ag.deleteAnalysisDir()
        raise e
    
    # Run MLE
    ag.mle()
    
    # Print Results
    ag.selectSources("sqrtTS > 0", show=True)
    regFile = ag.writeSourcesOnFile("source_regions", "reg")
    
    # Save Plots
    ag.displayCtsSkyMaps(catalogRegions="2AGL", catalogRegionsColor="green",saveImage=True)
    ag.displayExpSkyMaps(saveImage=True)
    ag.displayGasSkyMaps(saveImage=True)
    ag.displayIntSkyMaps(smooth=True, regFiles=[regFile], regFileColors=["white"],
                         catalogRegions="2AGL", catalogRegionsColor="green",
                         saveImage=True
                         )




if __name__=="__main__":
    
    # Argument
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", help="Number of the target source", type=int)
    args = parser.parse_args()
    
    # Get Target Name
    ConfFilePath = GetTargetYAML(args.target)
    print(f"Configuration File: {ConfFilePath}")
    
    # Run Analysis
    RunDataAnalysis(ConfFilePath)
    
    # RunTime
    print(f"TOTAL RUNTIME = {float(time()-START):.3f} s.")
