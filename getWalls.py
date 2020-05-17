# ---------------------
# SCRIPT INFO ---------
# ---------------------
# This script downloads X amount of images from a
# selected subreddit. The subreddit can be specified
# in the user config section of this srcipt or as 
# a parameter in the script.
#
# Run example: python getWalls.py earthporn




# ---------------------
# USER CONFIG ---------
# ---------------------

# Where to store downloaded images
directory = '~/Pictures/Wallpapers/Reddit/'
# Which subreddit to download from
subreddit = 'wallpapers'
# Minimum width of image
min_width = 1920
# Minimum height of image
min_height = 1080
# How many posts to get for each request (Max 100)
jsonLimit = 100
# Increase this number if the number above (jsonLimit) isn't enough posts
loops = 5





# ---------------------
# IMPORTS -------------
# ---------------------
import os
from os.path import expanduser
import sys
import requests
import urllib
from PIL import ImageFile


# ---------------------
# FUNCTIONS -----------
# ---------------------

# Returns false on status code error
def validURL(URL):
    statusCode = requests.get(URL, headers = {'User-agent':'getWallpapers'}).status_code
    if statusCode == 404:
        return False
    else: return True

# Creates download directory if needed
def prepareDirectory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print('Created directory {}'.format(directory))

# Returns false if subreddit doesn't exist
def verifySubreddit(subreddit):
    URL = 'https://reddit.com/r/{}.json'.format(subreddit)
    result= requests.get(URL, headers = {'User-agent':'getWallpapers'}).json()
    try:
        result['error']
        return False
    except:
        return True

# Returns list of posts from subreddit as json
def getPosts(subreddit, loops, after):
    allPosts = []
    
    i = 0
    while i < loops:
        URL = 'https://reddit.com/r/{}/top/.json?t=all&limit={}&after={}'.format(subreddit, jsonLimit, after)
        posts = requests.get(URL, headers = {'User-agent':'getWallpapers'}).json()
        # allPosts.append(posts['data']['children'])
        for post in posts['data']['children']:
            allPosts.append(post)
        after = posts['data']['after']
        i += 1
    
    return allPosts

# Returns false if URL is not an image
def isImg(URL):
    if URL.endswith(('.png', '.jpeg', '.jpg')):
        return True
    else: return False

# Returns false if image from URL is not HD (Specified by min-/max_width)
def isHD(URL, min_widht, min_height):
    file = urllib.request.urlopen(URL)
    size = file.headers.get("content-length")
    if size: size = int(size)
    p = ImageFile.Parser()
    while 1:
        data = file.read(1024)
        if not data:
            break
        p.feed(data)
        if p.image:
            # return p.image.size
            if p.image.size[0] >= min_width and p.image.size[1] >= min_height:
                return True
                break
            else:
                return False
                break
    file.close()
    return False

# Returns false if image from URL is not landscape
def isLandscape(URL):
    file = urllib.request.urlopen(URL)
    size = file.headers.get("content-length")
    if size: size = int(size)
    p = ImageFile.Parser()
    while 1:
        data = file.read(1024)
        if not data:
            break
        p.feed(data)
        if p.image:
            # return p.image.size
            if p.image.size[0] >= p.image.size[1]:
                return True
                break
            else:
                return False
                break
    file.close()
    return False

# Returns true if image from URL is already downloaded
def alreadyDownloaded(URL):
    imgName = os.path.basename(URL)
    localFilePath = os.path.join(directory, imgName)
    if(os.path.isfile(localFilePath)):
        return True
    else: return False

# Returns false if image from post/URL is not from reddit or imgur domain
def knownURL(post):
    if post.lower().startswith('https://i.redd.it/') or post.lower().startswith('https://i.imgur.com/'):
        return True
    else: return False

# Returns true if image from post/URL is stored locally
def storeImg(post):
    if urllib.request.urlretrieve(post, os.path.join(directory, os.path.basename(post))):
        return True
    else: return False


# ---------------------
# COLORS --------------
# ---------------------
DARK = '\033[1;30m'
RED = '\033[1;31m'
GREEN = '\033[1;32m'
ORANGE = '\033[1;33m'
PURPLE = '\033[1;35m'
NC = '\033[0m'


# ---------------------
# START SCRIPT --------
# ---------------------

# Check if subreddit name is specified as parameter
try:
    subreddit = sys.argv[1]
except:
    pass

# Creates directory
directory = expanduser(directory)
directory = os.path.join(directory, subreddit)
prepareDirectory(directory)

# Exits if invalid subreddit name
if not verifySubreddit(subreddit):
    print('r/{} is not a valid subreddit'.format(subreddit))
    sys.exit()

# For reddit pagination (Leave empty)
after = ''

# Stores posts from function
posts = getPosts(subreddit, loops, after)

# For adding index numbers to loop
index = 1

# Counting amount of images downloaded
downloadCount = 0

# Print starting message
print()
print(DARK + '--------------------------------------------' + NC)
print(PURPLE + 'Downloading to      : ' + ORANGE + directory + NC)
print(PURPLE + 'From r/             : ' + ORANGE + subreddit + NC)
print(PURPLE + 'Minimum resolution  : ' + ORANGE + str(min_width) + 'x' + str(min_height) + NC)
print(PURPLE + 'Maximum downloads   : ' + ORANGE + str(jsonLimit*loops) + NC)
print(DARK + '--------------------------------------------' + NC)
print()


# Loops through all posts
for post in posts:
    
    # Shortening variable name
    post = post['data']['url']

    # Skip post on 404 error
    if not validURL(post):
        print(RED + '{}) 404 error'.format(index) + NC)
        index += 1
        continue

    # Skip unknown URLs
    elif not knownURL(post):
        print(RED + '{}) Skipping unknown URL'.format(index) + NC)
        index += 1
        continue

    # Skip post if not image
    elif not isImg(post):
        print(RED + '{}) No image in this post'.format(index) + NC + NC + NC + NC)
        index += 1
        continue

    # Skip post if not landscape
    elif not isLandscape(post):
        print(RED + '{}) Skipping protrait image'.format(index) + NC)
        index += 1
        continue
    
    # Skip post if not HD
    elif not isHD(post, min_width, min_height):
        print(RED + '{}) Skipping low resolution image'.format(index) + NC)
        index += 1
        continue

    # Skip already downloaded images
    elif alreadyDownloaded(post):
        print(RED + '{}) Skipping already downloaded image'.format(index) + NC)
        index += 1
        continue

    # All checks cleared, download image
    else:
        # Store image from post locally
        if storeImg(post):
            print(GREEN + '{}) Downloaded {}'.format(index, os.path.basename(post)) + NC)
            downloadCount += 1
            index += 1
        # For unexpected errors
        else:
            print(RED + 'Unexcepted error' + NC)
            index += 1


# Print info when loop is finished
print()
print(ORANGE + '{}'.format(downloadCount) + PURPLE + ' images was downloaded to ' + ORANGE + '{}'.format(directory) + NC)
