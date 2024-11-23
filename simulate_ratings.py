import requests

# Base URLs
EMA_URL = 'http://127.0.0.1:8000/rate/'
DYNAMIC_EMA_URL = 'http://127.0.0.1:8000/rate_dynamic/'
SIMPLE_URL = 'http://127.0.0.1:8000/rate_simple/'
POST_LIST_URL = 'http://127.0.0.1:8000/posts/'
POST_RESET_URL = 'http://127.0.0.1:8000/reset_post/'

# ------------ Edit these values as needed -------------
post_id = 1  # assuming a post with this ID exists
num_ratings = 20  # Number of people that rating
ratings_values = [1, 5]  # Ratings values to simulate
method = EMA_URL  # Choose between EMA_URL, DYNAMIC_EMA_URL to compare it to Simple Average

def submit_rating(url, user_id, value):
    data = {
        'user_id': f'user{user_id}',
        'post': post_id,
        'value': value
    }
    try:
        response = requests.post(url, json=data)
        if response.status_code != 200:
            print(f'Error submitting rating by user{user_id}: {response.status_code} - {response.text}')
        else:
            print(f'Successfully submitted rating by user{user_id}')
    except Exception as e:
        print(f'Exception occurred while submitting rating by user{user_id}: {e}')


def simulate_ratings(url, version_name):
    threads = []
    for i in range(1, num_ratings + 1):
        value = ratings_values[i % 2]
        submit_rating(url, i, value)

    for t in threads:
        t.join()

    response = requests.get(POST_LIST_URL)
    posts = response.json()
    for post in posts:
        if post['id'] == post_id:
            print(f"[{version_name}] Average Rating: {post['average_rating']}, Total Ratings: {post['total_ratings']}")
            break

if __name__ == '__main__':
    # Simulate ratings with EMA
    print("Simulating ratings with EMA...")
    simulate_ratings(method, 'EMA')

    # Reset the post's average rating and total ratings
    print("Resetting post...")
    data = {'post': post_id}
    response = requests.post(POST_RESET_URL, json=data)

    # Simulate ratings with Simple Average
    print("Simulating ratings with Simple Average...")
    simulate_ratings(SIMPLE_URL, 'Simple Average')
