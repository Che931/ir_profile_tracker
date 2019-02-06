[![Build Status](https://travis-ci.com/Che931/ir_profile_tracker.svg?branch=master)](https://travis-ci.com/Che931/ir_profile_tracker)
# IR-Profile-Tracker

This python script makes your life easier because you will get an updated SR/irating file of your teammates.
You won't need to waste time visiting all profiles and updating a document. At this moment SR and iRating info is exported 
to a CSV file but other formats should be available #soon.

## Usage

### Installation

I recommend you to create a virtual environment and install all dependencies there. As soon as it's ready and activated,
you can install all dependencies:

```bash
pip install -r requirements.txt
```

If you want to run tests, you have to install requirements-test.txt because they use nose and coverage.

```bash
pip install -r requirements-text.txt
```

And then:
```bash
 nosetests -v
```

## Application

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
   /* More memebers */
  ]
}
```
The name can be different to the real one used on iR (useful if your mates have +4 names and you want a short version) but 
the id must be right or you will get stats from other guy.

### Run
Main.py is the only executable file. The behaviour can be changed using some commandline params that you can see below:

|Arg|Optional|Description|
|-------|-------|------|
|-f --file|No|Json file with drivers' info - can be a path|
|-o --output|Yes|Output csv file - can be a path|

__Examples:__

drivers.json as input file and default output filename.
> main.py -f drivers.json

drivers.json(inside files folder) as input file and info will be exported to stats.csv.
> main.py -f files/drivers.json -o stats.csv

Error because no input file was given.
> main.py  -o stats.csv

## FAQ

1. Do I have to put my iRacing credentials?

> Yes. iRacing doesn't have any API so the only valid method is using your account. It's fair you don't trust me but you can check 
my code

2. Have you used it?

> I've tested it and a modified version of this script is running on my Raspberry Pi every morning. 

3. Where can I find the customerid from my mate?

> If visit his profile, his id is at the end of the url after ?custid= .

4. I only care about <insert road/oval/dirt licence here>
> At this moment all licences are exported but in the future you might be able to filter those you don't care. 

5. I would love having the csv file on my Dropbox/GDrive folder or Discord channel automatically.
   
> Sync feature is on my TODO list and #soon. Discord and Dropbox could be the first services supported.

6. Can I modify/copy it?
> Of course!. It's under MIT Licence so feel free to do whatever you want. If you make an awesome feature, you can create a
PR.


*Thanks to Juri, his laziness made this script possible ;).*


 

