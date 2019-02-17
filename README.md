[![Build Status](https://travis-ci.com/Che931/ir_profile_tracker.svg?branch=master)](https://travis-ci.com/Che931/ir_profile_tracker)
[![Maintainability](https://api.codeclimate.com/v1/badges/72db40f438c835176f06/maintainability)](https://codeclimate.com/github/Che931/ir_profile_tracker/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/72db40f438c835176f06/test_coverage)](https://codeclimate.com/github/Che931/ir_profile_tracker/test_coverage)

# IR-Profile-Tracker

This python script makes your life easier because you will get an updated SR/irating file of your teammates.
You won't need to waste time visiting all profiles and updating a document. SR and iRating info is exported to a CSV
file. 

This script has been tested in Python 3.5, 3.6 and 3.7.

## Installation

I recommend you to create a virtual environment and install all dependencies there. As soon as it's ready and activated,
you can install all dependencies:

```bash
pip install -r requirements.txt
```

If you want to run tests, you have to install requirements-test.txt because they use nose and coverage.

```bash
pip install -r requirements-text.txt
```

And then type:
```bash
 nosetests -v
```

## Configuration

### settings.py
You have to open settings.py and edit these two lines adding your iRacing email/password:
```python
IRACING_EMAIL = 'YOUR EMAIL'
IRACING_PASSWORD = 'YOUR PASSWORD'
```
__If you want to upload this script or share it, don't forget to remove your personal info from this file.__

### Input file
You need to create a .json file(name doesn't matter) and put the info of your teammates. You can have multiple files but 
you have to follow the following structure. (Note that names and ids are fictional)
```json
{
  "drivers":
  [
    {"name": "Archaon the Everchosen", "id":4012 },
    {"name": "Garrett Branko", "id":1540}
  ]
}
```
The name can be different to the real one used on iR (useful if your mates have +4 names and you want a short version) but 
the id must be right or you will get stats from other guy.

## Command-line arguments
Main.py is the only executable file and the behaviour can be changed using some commandline params:

### -h/--help

```
$ main.py -h 
$ main.py --help
```
This will show you a list of possible command-line flags.

### -f/ --file
```
$ main.py -f drivers.json 
$ main.py --file files/drivers.json
```

Indicates the input file tha the script will use. You can have this file in the same level that main.py or different folder.
It's a required flag so if you miss it you will get an error. In order to keep this tutorial simple, this flag is missing in the next explanations. 

### -o/ --output
```
$ main.py -o stats.csv 
$ main.py --file /output/stats.csv
```

By default stats are exported to a csv file named DriversStats.csv and you find it in the project root. With this flag,
you can change the name of the file and exported to a different folder.


### --ignore
```
$ main.py --ignore 2
$ $ main.py --ignore 3,4
```

By default it exports oval,road and both dirt licences but this flag lets you skip those you don't care. Values must be
between 1-4 and below you can see licence-number relation:

* 1: Oval
* 2: Road
* 3: Dirt-Oval
* 4: Dirt-Road

__Examples:__

Drivers.json file as input and both oval licences aren't exported. Output file will be DriversStats.csv.
```
$ main.py -f drivers.json --ignore 1,3
```

Drivers.json file (store in a folder) and info will be exported to a file named stats.csv.
```
$ main.py -f files/drivers.json -o stats.csv
```

Drivers.json (inside a folder) as input file, info will be exported to a file named stats.csv(inside a folder) and skip road info.
```
$ main.py -f files/drivers.json -o output/stats.csv --ignore 2
```


## FAQ

1. Do I have to put my iRacing credentials?

>Yes. iRacing doesn't have any API so the only valid method is using your account. It's fair you don't trust me but you can check my code.

2. Have you used it?

>It's running on my Raspberry Pi every morning. 

3. Where can I find the customerid?

>If visit your mate's profile, his id is at the end of the url after ?custid=.

4. I would love having the csv file on my Dropbox/GDrive folder or Discord channel automatically.

> I won't add sync to this script but I might write a small script for Dropbox/Discord.

5. Can I modify/copy it?

> Of course!. It's under MIT Licence so feel free to do whatever you want. If you make an awesome feature you can create a PR.


## Changelog

__V0.0.2 (17/02/2019)__

* Added ignore licence flag and it won't appear in the csv file. 

__V0.0.1 (06/02/2019)__

* Initial release.


*Thanks to Juri, his laziness made this script possible ;).*


 

