# Check if agilepy REST API allows to download data.

**Repository structure**
- [Targets.yml](./Targets.yml): YAML file with the different targets used for the analysis (target= source position + time intervals requested for download and scientific analysis).
Every target is associated with a progressive number from `0` onward.
- [WriteConfFile.py](./WriteConfFile.py): script used to create the Agilepy Configuration files necessary to start an analysis.
It can be run as
    ```
    python WriteConfFile.py -t 0
    ```
    Change `0` with the progressive number of the Target you are interested in.
    Configuration files are wirtten in [ConfigurationFiles](./ConfigurationFiles/).
- [DownloadData.py](./DownloadData.py): Read the Agilepy Configuration file created for a given target and tries to download the data with the REST API.
It can be run as
    ```
    python DownloadData.py -t 0
    ```
    Change `0` with the progressive number of the Target you are interested in.
    Data are downloaded in [DataFiles](./DataFiles/), though the `.gz` fits files are ignored in this repository to keep it light.
Download is performed when calling `AGAnalysis.generateMaps()`.

**Summary results on each analysis target**

0. Try requesting Vela: 2022-04-01 - 2022-12-31.
    - Error: Maximum Download period allowed: 3 months.
1. Try requesting Vela inside restricted period: 2022-03-10 - 2022-03-20.
    - Error: No Data Found.
2. Try requesting Vela across restricted period: 2022-03-20 - 2022-04-10.
    - Data Downloaded.
3. Try requesting Vela: 2022-04-01 - 2022-06-30.
    - Data Downloaded correctly.
- Try one or more ATels.
