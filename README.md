# Mercedes Used Car Listing

Educational data analysis and programming project by Maksim Kuptsov,\
HSE FCS DSBA 27' group 231-1.

main.ipynb contains initial step-by-step analysis.\
Then there is a server written on Flask, which stores pictures of obtained graphs and tables.\
A Telegram bot is a user interface to view different parts of the analysis. It sends requests to the Flask server to get the images and their descriptions and displays them.

## Links:

- Dataset:\
    https://www.kaggle.com/datasets/mysarahmadbhat/mercedes-used-car-listing

- Streamlit:\
    https://mercedesusedcarlisting.streamlit.app

- Telegram Bot:\
    https://t.me/mercedes_project_bot


## To be done/fixed/clarified:

- Telegram Markdown interpretation
- Bot: passing a photo directly to bot.send_photo(photo=...) without saving them in 'temp' folder
- Replace long-polling with Webkook
