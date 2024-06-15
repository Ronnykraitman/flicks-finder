# flicks-finder

## Before you start:
- Make sure you use Python 3.10 or above
- run the init script
```bash
init.sh
```

## Start by simply running
```bash
python3 flicks.py
```
Wait a second or two, and go to the address you see on your screen, usually its: http://127.0.0.1:8000/

## How it works:

1. A data set of thousands of imdb rated movies (the data has been already cleaned for you)
2. Using TF-IDF model + linear kernel function to calculate similarities between movies, based on their plot
3. All you need to do is select a movie from the list, and any other condition if you'd like
4. And voilà - you got your self similar movies based on your filtering

![Alt text](./static/thiller.gif)
