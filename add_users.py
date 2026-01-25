import os
import sys
import json
import django
import random

from image_master import convertImage

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Django_Instagram.settings")
django.setup()

random.seed(42)

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


def add_test_user():
    firstName = "testUser"
    lastName = "testUser"
    bio = "testUser"
    location = "testUser"

    user, created = User.objects.get_or_create(
            username=firstName,
            email=firstName[:2]+lastName[:2]+"@example.com",
            password="test",
        )
    print(f"User {user.username} created")
    url = firstName[:2]+lastName[:2]+".com"
    profile = Profile.objects.create(
        user=user,
        first_name = firstName,
        last_name = lastName,
        bio = bio,
        location = location,
        url = url
    )

    print(f"\n\n\nProfile for {user.username} created")

def add_users(users_number, users):
    firstNames = users["firstNames"]
    lastNames = users["lastNames"]
    bios = users["bios"]
    locations = users["locations"]


    for i in range(users_number):
        firstName = random.choice(firstNames)
        lastName = random.choice(lastNames)
        bio = random.choice(bios)
        location = random.choice(locations)

        user, created = User.objects.get_or_create(
                username=firstName[:2]+lastName[:2],
                email=firstName[:2]+lastName[:2]+"@example.com",
                password="test",
            )
        print(f"User {user.username} created")
        url = firstName[:2]+lastName[:2]+".com"
        profile = Profile.objects.create(
            user=user,
            first_name = firstName,
            last_name = lastName,
            bio = bio,
            location = location,
            url = url
        )

        print(f"Profile for {user.username} created")

    add_test_user()

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


def add_posts(users, data, posts_per_user=10):
    images_folder = "images"
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
                    #najmniejszy, średni, największy
                    image1, image2, image3 = convertImage(f)
                    post = Post.objects.create(
                        user=user,
                        caption=caption,
                        picture=django.core.files.File(f, name=image1),
                        likes=random.randint(0, 100)  # losowe polubienia
                    )

                    post.picture.save(
                        image_name,          # nazwa pliku
                        image1,       # ContentFile
                        save=True
                    )
                
                    post.picture1.save(
                        image_name,          # nazwa pliku
                        image2,       # ContentFile
                        save=True
                    )
                    post.picture2.save(
                        image_name,          # nazwa pliku
                        image3,       # ContentFile
                        save=True
                    )


                    # Opcjonalnie przypisanie losowych tagów, jeśli masz Tag model
                    # tags = Tag.objects.all()
                    # selected_tags = random.sample(list(tags), k=random.randint(0, 3))
                    # post.tags.set(selected_tags)
                    tag_count = random.randint(0, 5)

                    # losujemy stringi
                    tag_names = random.sample(data["tags"], k=tag_count)
                    
                    # zamieniamy stringi na obiekty Tag
                    tag_objects = []
                    for name in tag_names:
                        tag, _ = Tag.objects.get_or_create(title=name)
                        tag_objects.append(tag)

                    # przypisujemy do posta
                    post.tags.set(tag_objects)

                print(f"Post created for {user.username} with image {image_name}")

#################################################
                print(f"✔ Post created for {user.username} with image {image_name}")
    except Exception as e:
        print(e)
        return

def delete_users():
    Follow.objects.all().delete()
    Post.objects.all().delete()
    Profile.objects.all().delete()

    users = User.objects.all()
    count = users.count()
    users.delete()

    print(f"Deleted {count} users and all related data")

def make_admin():
    username = "admin"
    password = "admin"

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(
            username=username,
            email="admin@example.com",
            password=password
        )
        print("Admin user created (admin / admin)")
    else:
        print("Admin user already exists")

def main():

    return
    random.seed(42)
    delete_users()
    make_admin()

    data = get_data()

    add_users(int(sys.argv[1]), data)

    all_users = list(User.objects.all())
    
    
    add_follows(all_users)
    add_posts(all_users, data)



if __name__ == '__main__':
    main()