from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api
import random


TOKEN = 'a2d5ab8ff0620607f37970f89a3d6605e09c543da8a6cc48e223ac1126305654c6741f81aec1825807bce'


vk_sess = vk_api.VkApi(token=TOKEN)
vk = vk_sess.get_api()
longpoll = VkLongPoll(vk_sess)


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.from_user and event.to_me:
            data = vk.users.get(user_ids=[event.user_id], fields=['first_name', 'city'])[0]
            vk.messages.send(user_id=event.user_id,
                             message=f'Привет, {data["first_name"]}',
                             random_id=random.randint(0, 2 ** 64))
            if 'city' in data:
                vk.messages.send(user_id=event.user_id,
                                 message=f'Как поживает {data["city"]["title"]}?',
                                 random_id=random.randint(0, 2 ** 64))