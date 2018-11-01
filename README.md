MathsJam Retweeter
==================

This repository contains Python code that makes the [@MathsJam](https://twitter.com/mathsjam) Twitter account
automatically retweet local MathsJams on the day of and the day before events.

Running this code
-----------------
Before running this code, you will need to:

1. Make a copy of `config.py.template` called `config.py` and fill in the Twitter API keys for the MathsJam account.
2. Install the required Python libraries by running
```bash
pip install -r requirements.txt
```

Once you've done this you can run the code using:
```bash
python tweet.py
```

If you want to test the code without actually sending and tweets, you can do this using:
```bash
python tweet.py test
```
