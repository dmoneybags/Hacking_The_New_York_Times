# I don't have a New York Times subscription

https://user-images.githubusercontent.com/86892271/147376896-416402ab-e06a-43ba-a23b-a873426ca1f3.mp4

# How it works:
pretty simple code, broken down into attempts to get the article. The first attempt simply tries to download the html immeadiately on load before the javascript on the page can check whether or not Im authenticated and thus, give me the full article. However, if that doesnt work, we perform a depth-first tree search on the json linked in the html which contains the full article. By filtering for every end node labeled "text" we can get the full article in our terminal.
# Note
First option works 99% of the time, however sometimes it only gets the first paragraph.
