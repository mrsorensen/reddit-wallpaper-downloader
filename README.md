# reddit-wallpaper-downloader
Downloads HD wallpapers from whichever subreddit you want

![Screenshot](https://github.com/mrsorensen/reddit-wallpaper-downloader/blob/master/screenshot.png "Screenshot")


## How to configure
Edit config in getWalls.py
```
# Where to store downloaded images
directory = '~/Pictures/Wallpapers/Reddit'
# Which subreddit to download from
subreddit = 'wallpapers'
# Minimum width of image
min_width = 1920
# Minimum height of image
min_height = 1080
# How many posts to loop through (max 100)
maxDownloads = 50
```
## How to run
You can run:
```
python ~/reddit-wallpaper-downloader/getWalls.py
```
or, to overwrite which subreddit you want to download from, run:
```
python ~/reddit-wallpaper-downloader/getWalls.py earthporn
```
