import os
import random
from datetime import datetime
from PIL import Image
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
    img.save(filename)
    return filename, rgb_to_hex(start), rgb_to_hex(end)

def tweet_image():
    filename, start_hex, end_hex = create_gradient_image()
    tweet = f"Today's gradient: #{start_hex} → #{end_hex}"

    auth = tweepy.OAuth1UserHandler(
        os.getenv("TWITTER_API_KEY"),
        os.getenv("TWITTER_API_SECRET"),
        os.getenv("TWITTER_ACCESS_TOKEN"),
        os.getenv("TWITTER_ACCESS_SECRET")
    )
    api = tweepy.API(auth)

    # Upload image and get media ID
    media = api.media_upload(filename)

    # Post tweet with media
    api.update_status(status=tweet, media_ids=[media.media_id_string])

if __name__ == "__main__":
    tweet_image()
