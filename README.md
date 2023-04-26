# Mr Beast Youtube Channel Analysis

![](https://ichef.bbci.co.uk/news/976/cpsprodpb/16621/production/_122718619_maxresdefault1.jpg.webp)

This GitHub repository contains an analysis of the "Mr Beast" YouTube channel using the YouTube API. The analysis includes information such as video ID, title, description, like count, view count, comment count, and duration for each video on the channel.

## Project Description

The "Mr Beast" YouTube channel is known for its philanthropic content, where the creator, Jimmy Donaldson, known as "Mr Beast," creates and uploads videos that often involve giving away large sums of money to individuals or charities. The purpose of this project is to analyze the video data from the channel using the YouTube API to gain insights into the channel's content and engagement metrics.

## Data Collection

The YouTube API was used to collect video data from the "Mr Beast" YouTube channel. The API allows access to a variety of information related to videos, including video ID, title, description, like count, view count, comment count, and duration. The data was collected using Python and the google-api-python-client library, which provides a convenient way to interact with the YouTube API.

## Repository Structure

**The repository contains the following files:**

+ main.py: Python script used to collect video data from the YouTube API.
+ analysis.rmd: R Markdown file that contains the analysis of the collected video data.
+ presentation.html: Slidy HTML presentation of the analysis.
+ MrBeastYoutube.csv: CSV file that contains the raw video data collected from the YouTube API.
+ README.md: The current file, which provides documentation about the project.

## Data Analysis

The collected video data was analyzed using Python and popular data analysis libraries such as Pandas, NumPy, and Matplotlib. The analysis includes various visualizations and statistical measures to gain insights into the channel's video metrics, such as like count, view count, comment count, and duration. The analysis aims to provide a comprehensive overview of the "Mr Beast" YouTube channel's performance and engagement.

## Usage

To run the data collection script main.py, you will need to have Python installed on your machine, along with the google-api-python-client library. You will also need to create a project in the Google Cloud Console, enable the YouTube API, and obtain an API key to authenticate your requests. Replace the API_KEY variable in the script with your own API key before running the script.

The collected video data will be stored in the data.csv file, which can then be used for further analysis in the Jupyter notebook analysis.ipynb. The notebook contains step-by-step instructions and code to load and analyze the data, and visualize the results using various plots and charts.

## Conclusion

This project provides an analysis of the "Mr Beast" YouTube channel using the YouTube API. The collected video data can be used to gain insights into the channel's content and engagement metrics, and the analysis can be further extended to perform more in-depth analyses or create custom visualizations. The project can serve as a reference for anyone interested in analyzing YouTube channels or working with the YouTube API.





