# OKN DECIDE PYTHON PACKAGE LIBRARY MANUAL
## Description
This program will read the given signal csv and extract the information about max chain length, unchained okn total and whether there is okn or not.

## Installation requirements and guide
### Anaconda
To install this program, `Anaconda python distributing program` and `Anaconda Powershell Prompt` are needed.  
If you do not have `Anaconda`, please use the following links to download and install:  
Download link: https://www.anaconda.com/products/distribution  
Installation guide link: https://docs.anaconda.com/anaconda/install/  
### PIP install
To install `okndecide`, you have to use `Anaconda Powershell Prompt`.  
After that, you can use the `okndecide` from any command prompt.  
In `Anaconda Powershell Prompt`:
```
pip install okndecide
```  
## Usage guide
### Example usage
```
okndecide -i (input file) -c (config file) -v
```
`-v` is optional.  
If `-v` is not mentioned, it will only generate only json string.  
If `-v` is mentioned, it will generate all info as comments and result json string.
 
If you want to test this program, you can clone this repository, install `okndecide`, open any command prompt or terminal.  
In the terminal, go to `../okndecide/development` then run the following command:
```
okndecide -i signal.csv -c decide.info.json -v > out_with_v.json
```
out_with_v.json will be created with all information(as comments) and result json string.
If you do not want to see all other information, then run the same command without `v`:
```
okndecide -i signal.csv -c decide.info.json > out_without_v.json
```
out_without_v.json will be created with just result json string.

### Rules
#### Before version 3.0.2
Before version 3.0.2, rule file (decide.info.json) must have 2 rules.  
Example  
```
{
  "rule": {"name": "main1", "min_chain_length": 2, "min_unchained_okn": 3}
}
```
They are **min_chain_length** (minimum length of chained okn) and **min_unchained_okn** (minimum number of un chained okn) which will determine a trial whether it has valid okn or not.  

#### From version 3.0.2
Rule file (decide.info.json) can have up to 3 rules.  
Example  
```
{
  "rule": {"name": "main1", "min_chain_length": 2, "min_unchained_okn": 3, "slow_phase_track": true}
}
```
They are **min_chain_length**, **min_unchained_okn** and **slow_phase_track** (checking whether there is slow phase track or not).  
**slow_phase_track** can be boolean (true or false) or could be integer.  
If it is boolean false, then it will be exluded from rules.  
If it is boolean true, minimum number of slow phase track will be 1.  
If it is integer, that integer number will be used as minimum number of slow phase track.


### To upgrade version  
In `Anaconda Powershell Prompt`,
```
pip install -U okndecide
```
or
```
pip install --upgrade okndecide
```

