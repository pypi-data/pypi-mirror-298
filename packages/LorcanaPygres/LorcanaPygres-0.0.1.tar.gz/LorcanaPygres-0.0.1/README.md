# A PostgreSQL Database and Python Scripts for Lorcana


This database and subsequent python scripts leverages the Lorcana-API https://github.com/Dogloverblue/Lorcana-API.

I am not affiliated with the lorcana api.  And all copyrights beyond to their respective owners. i.e. Disney, Ravensburger, etc.  I am an enthusiast, just expanding the playability of the game.

# Update - 9-25-2024

The lorcana api uses a mysql database, with each entry held as a json.  I pulled a copy of all of its contents, and then created a postgres database with each piece of information in its own relational table.  I used my database visualizer to identify typos and data duplicates, which I subsequently cleaned up.

The card_images folder is empty, as I have that included in the .gitignore for now.  The script to pull down your own copy of all images is in this repo.

The current version of this database includes cards up through Shimmering Skies.  I am currently working on adding the upcoming Azurite Sea release.

### Known issues:
1) Starter deck info is incomplete
2) Azurite Sea incomplete

### Planned Additions:
1) Create requirements file and PIP Package
2) FastAPI scripts to host your own api.
2) Discord Bot script to show cards, and open random packs for fun.
3) Scripts to automate the adjustment of cards - i.e. resize, rotate, overlay, etc