# check_agilepy_rest_API
Check if agilepy REST API allows to download data.

**Analysis targets chosen and respective codes:**
0. Try requesting Vela: 2022-04-01 - 2022-12-31.
    - Error: Maximum Download period allowed: 3 months.
1. Try requesting Vela inside restricted period: 2022-03-10 - 2022-03-20.
    - Error: No Data Found.
2. Try requesting Vela across restricted period: 2022-03-20 - 2022-04-10.
    - Data Downloaded.
3. Try requesting Vela: 2022-04-01 - 2022-06-30.
    - Data Downloaded correctly.
- Try one or more ATels.
