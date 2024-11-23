# Django Posts and Ratings Application
This application is a Django project that allows users to view a list of posts and rate them. 
Each post consists of a title and text. Users can rate posts with a value between 0 and 5. 
The application is designed to handle high performance under heavy load and includes mechanisms to mitigate the impact of sudden influxes of manipulative ratings.

## Installation
1. Clone the repository.
```bash
git clone https://github.com/yourusername/bitpin-task.git
cd django-posts-ratings
```
## Testing the EMA Method:
There is a file in the root directory named `simulate_ratings.py`. with this file you can see that if EMA method actually works
or not, and how it can affect the ratings of the users, if so many users start rating in the short period of time.   

To run the file:   
1- you need to change the Debug mode in the Django app. Go to `settings.py` file in the `app` directory and change the `DEBUG` variable to `True`.   
2- Also change the `ALLOWED_HOSTS` variable to `['*']`.   
3- Run the project first, to have the database ready.   
4- make sure that the post you want to test is already created, if it's not, you can create a new post using Django admin.   
5- write the id of the post in the `post_id` variable in the file.   
6- you can change the number of reviewers using `num_ratings` variable.   
7- you can choose between the EMA method and Dynamic EMA method using the `method` variable.
8- run the file using `python simulate_ratings.py` command, in separate terminal.   
9- you can see the results in the terminal.    