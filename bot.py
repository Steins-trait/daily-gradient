import os
import random
from datetime import datetime
from PIL import Image, ImageOps
import tweepy

def random_color():
    return tuple(random.randint(0, 255) for _ in range(3))

def rgb_to_hex(rgb):
    return f"{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"

def create_gradient_image():
    start = random_color()
    end = random_color()
    width, height = 800, 400
    img = Image.new("RGB", (width, height))
    
    for x in range(width):
        r = int(start[0] + (end[0] - start[0]) * x / width)
        g = int(start[1] + (end[1] - start[1]) * x / width)
        b = int(start[2] + (end[2] - start[2]) * x / width)
        for y in range(height):
            img.putpixel((x, y), (r, g, b))
    

    date = datetime.now().strftime("%Y-%m-%d")
    filename = f"gradient_{date}_{rgb_to_hex(start)}_{rgb_to_hex(end)}.png"
    image_dir = "gradients/"
    image_path = f"{image_dir}/{filename}"
    img.save(image_path)
    image = Image.open(image_path)
    bordered = ImageOps.expand(image, border=40, fill=(0, 0, 0))
    bordered.save(image_path)
    return image_path, rgb_to_hex(start), rgb_to_hex(end)

def tweet_image():
    filename, start_hex, end_hex = create_gradient_image()
    tweet = f"#{start_hex} → #{end_hex}"

    # OAuth 1.0a for media upload
    auth = tweepy.OAuth1UserHandler(
        os.getenv("TWITTER_API_KEY"),
        os.getenv("TWITTER_API_SECRET"),
        os.getenv("TWITTER_ACCESS_TOKEN"),
        os.getenv("TWITTER_ACCESS_SECRET")
    )
    api = tweepy.API(auth)
    media = api.media_upload(filename)

    # OAuth 2.0 Client for tweet creation (with user_auth=True)
    client = tweepy.Client(
        consumer_key=os.getenv("TWITTER_API_KEY"),
        consumer_secret=os.getenv("TWITTER_API_SECRET"),
        access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
        access_token_secret=os.getenv("TWITTER_ACCESS_SECRET")
    )

    client.create_tweet(
        text=tweet,
        media_ids=[media.media_id_string],
        user_auth=True
    )

if __name__ == "__main__":
    #tweet_image()