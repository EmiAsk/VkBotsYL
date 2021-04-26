from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api
import random
import wikipedia


TOKEN = ''


vk_sess = vk_api.VkApi(token=TOKEN)
vk = vk_sess.get_api()
longpoll = VkLongPoll(vk_sess)

wikipedia.set_lang('ru')

questioned = False
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.from_user and event.to_me:
            if not questioned:
                vk.messages.send(user_id=event.user_id,
                                 message='О чём вы хотите узнать из Википедии?',
                                 random_id=random.randint(0, 2 ** 64))
                questioned = True
            else:
                try:
                    msg = wikipedia.summary(event.text, sentences=20)
                    vk.messages.send(user_id=event.user_id,
                                     message=msg,
                                     random_id=random.randint(0, 2 ** 64))
                except wikipedia.WikipediaException:
                    vk.messages.send(user_id=event.user_id,
                                     message='Упс, что-то пошло не так...',
                                     random_id=random.randint(0, 2 ** 64))
                questioned = False


TOKEN = 'a2d5ab8ff0620607f37970f89a3d6605e09c543da8a6cc48e223ac1126305654c6741f81aec1825807bce'