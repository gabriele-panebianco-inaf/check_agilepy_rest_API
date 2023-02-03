# REPORT: Check if agilepy REST API allows to download data.

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
    There are two versions of configuration files: one used to download the data only (`Download_*.yml`), one used for the scientific analysis (`Analysis_*.yml`).
- [DownloadData.py](./DownloadData.py): Read the Agilepy Configuration file created for a given target and tries to download the data with the REST API.
It can be run as
    ```
    python DownloadData.py -t 0
    ```
    Change `0` with the progressive number of the Target you are interested in.
    Data are downloaded in [DataFiles](./DataFiles/), though the `.gz` fits files are ignored in this repository to keep it light.
Download is performed when calling `AGAnalysis.generateMaps()`.
Logs of program executions are stored in [Logs](./Logs/).

- [DataAnalysis](./DataAnalysis.py) Read the Agilepy Configuration file for data already downloaded and performs a MLE analysis with free position and flux in a single energy bin 100-50000 MeV.

**Summary results on each analysis target**

0. Try requesting Vela: 2022-04-01 - 2022-12-31.
    - Error: Maximum Download period allowed: 3 months.
1. Try requesting Vela inside restricted period: 2022-03-10 - 2022-03-20.
    - Error: No Data Found, as expected.
2. Try requesting Vela across restricted period: 2022-03-20 - 2022-04-10.
    - Data Downloaded only in the non-restricted period, as expected.
    EVT files were downloaded in OBT 575812732.0 - 577108732.0, see [EVT.index](./DataFiles/2_Vela_across_restricted_period/EVT.index), i.e. 2022-03-31 11:58:52.0 - 2022-04-15 11:58:52.0.
    LOG files were downloaded in OBT 575812732.0 - 576676731.9, see [LOG.index](./DataFiles/2_Vela_across_restricted_period/LOG.index), i.e. 2022-03-31 11:58:52.0 - 2022-04-10 11:58:51.9.
3. Try requesting Vela: 2022-04-01 - 2022-06-30.
    - Data Downloaded, as expected.
    EVT files were downloaded in OBT 575812732.0 - 583675132.0, see [EVT.index](./DataFiles/3_Vela/EVT.index), i.e. 2022-03-31 11:58:52.0 - 2022-06-30 11:58:52.0.
    LOG files were downloaded in OBT 575812732.0 - 583675131.9, see [LOG.index](./DataFiles/3_Vela/LOG.index), i.e. 2022-03-31 11:58:52.0 - 2022-06-30 11:58:51.9.
    Analysis was performed, main results can be seen in [Results/Gabriele_Vela_20230203-174142/](./Results/Gabriele_Vela_20230203-174142/)
4. Try replicate ATel https://www.astronomerstelegram.org/?read=15782 on 3C454.3.
    - Data Downloaded as expected, ATel results confirmed, see [Results/Gabriele_3C454.3_20230203-191611/](./Results/Gabriele_3C454.3_20230203-191611/).
5. Same as case 4, but inside Docker container, not conda environment.
    - It works, with some caveats, see below. Results in see [Results/Gabriele_3C454.3_Docker_20230203-184016/](./Results/Gabriele_3C454.3_Docker_20230203-184016/).

**Extra Notes**
- All cases were tested inside anaconda environment.
- Note: I installed the conda environment after the release of `agilepy 1.6.3`, but when I check the packages version I get:
    ```
    $ conda list agile
    # packages in environment at /home/gabriele/anaconda3/envs/agilepy-1.6.3:
    # Name                    Version                   Build  Channel
    agilepy                   1.6.1                    py38_0    agilescience
    agilepy-dataset           BUILD25ag                     0    agilescience
    agiletools                BUILD25b3                py38_0    agilescience
    ```
    We need to check if the conda environment is built with the latest releases.
- I tried to run case 4 inside Docker container.
If I run the container as shown in documentation data cannot be downloaded, as the container does not share the internet connectin of the host.
    ```
    urllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='tools.ssdc.asi.it', port=443): Max retries exceeded with url: /AgileData/rest/publicdatacoverage (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x7fcb3c59d8e0>: Failed to establish a new connection: [Errno -2] Name or service not known'))
    ```
- If I run the container with the `--network host` option then the following warning is displayed when running:
    ```
    WARNING: Published ports are discarded when using host network mode
    ```
    But then it works, the results of case 5 and case 4 are consistent.
