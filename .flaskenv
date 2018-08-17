# This file is meant to store non sensitive environment variables. For sensitive environment
# variables just use a separate '.env' file that is not pushed to github. The new Flask version will automatically load them for you
# but only if you use the `flask run` command. To allow any command to load the .env values, please
# look at the top of the config file in the andela societies project lines 7-8 for a usage example. The library is called python-dotenv and I've added it to your project as well.
# I've included examples of how you'd declare these environment variables.


FLASK_ENV='development'