from agilepy.api.AGAnalysis import AGAnalysis

import pathlib
import argparse
import os

def GetTarget(targetnumber):
    
    if targetnumber==0:
        Target={'SourceName':'Vela',
                'TimeType':'MJD',
                'tmin': 59670, # 2022-04-01 00:00:00 UTC
                'tmax': 59944, # 2022-12-31 00:00:00 UTC
                'glon': 263.59,
                'glat': -2.84
                }
    elif targetnumber==1:
        Target={'SourceName':'Vela_restricted_period',
                'TimeType':'MJD',
                'tmin': 59648, # 2022-03-10 00:00:00 UTC
                'tmax': 59658, # 2022-03-20 00:00:00 UTC
                'glon': 263.59,
                'glat': -2.84
                }
    elif targetnumber==2:
        Target={'SourceName':'Vela_across_restricted_period',
                'TimeType':'MJD',
                'tmin': 59658, # 2022-03-20 00:00:00 UTC
                'tmax': 59679, # 2022-04-10 00:00:00 UTC
                'glon': 263.59,
                'glat': -2.84
                }
    else:
        raise ValueError(f"Target number {targetnumber} not valid.")
    
    return Target

def make_directory(path):
    "Create directory if it does not exist"
    if not os.path.exists(path):
        os.makedirs(path)
    return None

if __name__=="__main__":
    
    # Set the path of the Directories to use.
    CurrentDirectory = pathlib.Path(__file__).absolute().parent
    DataFilePath = CurrentDirectory.joinpath(f"DataFiles/")
    ConfFileDire = CurrentDirectory.joinpath(f"ConfigurationFiles")
    make_directory(DataFilePath)
    make_directory(ConfFileDire)

    # Argument
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", help="Number of the target source", type=int)
    args = parser.parse_args()

    # Get Target Name
    Target = GetTarget(args.target)
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
        verboselvl = 0,

        # 3 - Selection
        tmin = Target['tmin'],
        tmax = Target['tmax'],
        timetype = Target['TimeType'],
        glon = Target['glon'],
        glat = Target['glat'],
    )