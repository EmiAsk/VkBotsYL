from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api
import random


TOKEN = 'a2d5ab8ff0620607f37970f89a3d6605e09c543da8a6cc48e223ac1126305654c6741f81aec1825807bce'

# ссылка на группу-бота (писать ему в лс) - https://vk.com/club203903187
# Айди группы обязательно с минусом в начале (пример: -203903187)
GROUP_ID, ALBUM_ID = '-132868814', '237593538'
LOGIN, PASSWORD = '', ''


def get_photos():
    vk_session = vk_api.VkApi(login=LOGIN, password=PASSWORD)
    vk = vk_session.get_api()

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as e:
        print(e)
        return

    photos = vk.photos.get(owner_id=GROUP_ID, album_id=ALBUM_ID)['items']

    urls = [f"photo{p['owner_id']}_{p['id']}" for p in photos]

    return urls


def main():
    vk_sess = vk_api.VkApi(token=TOKEN)
    vk = vk_sess.get_api()
    longpoll = VkLongPoll(vk_sess)

    photos = get_photos()

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me and event.from_user:
                photo = random.sample(photos, 1)

                data = vk.users.get(user_ids=[event.user_id])[0]
                vk.messages.send(user_id=event.user_id,
                                 message=f'Привет, {data["first_name"]}',
                                 random_id=random.randint(0, 2 ** 64), attachment=photo)


if __name__ == '__main__':
    main()