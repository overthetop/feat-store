# feat-store

It's a demo python project that reads data from a test .csv file and calculates different stats on top that could be
used to predict sales for a location. The result is saved into a PostgreSQL database.

## Get Started

Just hit ```docker compose up``` in the terminal and there will be two docker containers spun up for.
You can check out all the endpoints available here ```http://localhost:8000/docs```

![api](https://github.com/overthetop/feat-store/blob/main/api-screenshot.png?raw=true)

## TL;DR

Adding new features to the feature store is pretty simple. Just derive from ```BaseFeature``` class.
Then add a new instance of the feature to the rest of the features in the ```constants.py``` file.
Make sure you put a meaningful name because that name will end up as a column in the PosgreSQL database.
Once all the features are calculated a ```feat_tbl``` is automatically created in the database.
Initially just run a historic backfill ```POST /api/backfill/false```. 
For convenience there is a REST endpoint to fetch all features for a given location ```GET /api/features/{location}```.
At any give point of time, you can get a list of the active features in the database from ```GET /api/schema```.