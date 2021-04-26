import vk_api


LOGIN, PASSWORD = '', ''
# Айди группы обязательно с минусом в начале (пример: -203903187)
ALBUM_ID, GROUP_ID = '277755574', '-203903187'
# Ссылка на группу для проверки - https://vk.com/club203903187


def main():
    vk_session = vk_api.VkApi(login=LOGIN, password=PASSWORD)
    vk = vk_session.get_api()

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as e:
        print(e)
        return

    photos = vk.photos.get(owner_id=GROUP_ID, album_id=ALBUM_ID, fields='width,height')['items']
    for photo in photos:
        vk_photo_url = f"https://vk.com/photo{photo['owner_id']}_{photo['id']}"
        data = photo['sizes'][-1]
        size = f"{data['width']}x{data['width']}"
        print('URL ВК: ' + vk_photo_url)
        print('URL оригинала: ' + data['url'])
        print('Размер оригинала: ' + size, end='\n\n')


if __name__ == '__main__':
    main()

