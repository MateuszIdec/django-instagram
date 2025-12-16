import os
import sys
import json
import django
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Django_Instagram.settings")
django.setup()

from django.contrib.auth import get_user_model
from authy.models import Profile
# from django.contrib.auth.models import User
from post.models import Follow, Post, User, Tag

User = get_user_model()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "data_json/users.json")



def get_data():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        users = json.load(f)
    return users


def add_users(users_number, users):
    firstNames = users["firstNames"]
    lastNames = users["lastNames"]
    bios = users["bios"]
    locations = users["locations"]


    for i in range(int(users_number)):
        firstName = random.choice(firstNames)
        lastName = random.choice(lastNames)
        bio = random.choice(bios)
        location = random.choice(locations)

        user, created = User.objects.get_or_create(
            username=firstName[:2]+lastName[:2],
            defaults={"email": firstName[:2]+lastName[:2]+"@example.com"}
        )

        if created:
            user.set_password("test")
            user.save()
            print(f"✔ User {user.username} created")

        profile, p_created = Profile.objects.get_or_create(user=user)

        url = firstName[:2]+lastName[:2]+".com"
        # Nadpisujemy losowymi danymi
        profile.first_name = firstName
        profile.last_name = lastName
        profile.bio = bio
        profile.location = location
        profile.url = url
        profile.save()

        if p_created:
            print(f"✔ Profile for {user.username} created")

    print("✅ JSON seed completed")
    return users

def add_follows(all_users, max_follows_per_user=10):
    for user in all_users:
        # Lista możliwych użytkowników do followowania (bez samego siebie)
        possible_to_follow = [u for u in all_users if u != user]
        
        # Losowa liczba followów dla danego użytkownika
        follow_count = random.randint(1, min(max_follows_per_user, len(possible_to_follow)))
        
        # Losowo wybieramy kogo followuje
        users_to_follow = random.sample(possible_to_follow, k=follow_count)
        
        for target_user in users_to_follow:
            # Tworzymy follow, jeśli jeszcze nie istnieje
            Follow.objects.get_or_create(follower=user, following=target_user)


def add_posts(users, data):
    images_folder = "images"
    posts_per_user=10
    # Pełna ścieżka do folderu images
    folder_path = os.path.join(django.conf.settings.MEDIA_ROOT, images_folder)

    try:
        # Lista wszystkich plików w folderze
        if os.path.exists(folder_path):
            image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        else:
            image_files = []

        if not image_files:
            print("❌ Brak obrazów w folderze", folder_path)
            return


        for user in users:
            num_posts = random.randint(1, posts_per_user)
            for _ in range(num_posts):
                image_name = random.choice(image_files)
                image_path = os.path.join(folder_path, image_name)

                caption = random.choice(data["captions"])

                # Tworzymy post
                with open(image_path, "rb") as f:
                    post = Post.objects.create(
                        user=user,
                        caption=caption,
                        picture=django.core.files.File(f, name=image_name),
                        likes=random.randint(0, 100)  # losowe polubienia
                    )

                    # Opcjonalnie przypisanie losowych tagów, jeśli masz Tag model
                    # tags = Tag.objects.all()
                    # selected_tags = random.sample(list(tags), k=random.randint(0, 3))
                    # post.tags.set(selected_tags)

                print(f"✔ Post created for {user.username} with image {image_name}")
    except Exception as e:
        print(e)
        return

def main():
    data = get_data()

    add_users(sys.argv[1], data)

    all_users = list(User.objects.all())
    
    add_follows(all_users)
    add_posts(all_users, data)



if __name__ == '__main__':
    main()