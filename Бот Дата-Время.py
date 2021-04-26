from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api
import random
from datetime import datetime
import pytz


TOKEN = 'a2d5ab8ff0620607f37970f89a3d6605e09c543da8a6cc48e223ac1126305654c6741f81aec1825807bce'
# Ссылка на группу-бота (писать в лс ему) - https://vk.com/club203903187

vk_sess = vk_api.VkApi(token=TOKEN)
vk = vk_sess.get_api()
longpoll = VkLongPoll(vk_sess)


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.from_user and event.to_me:
            if any([m in event.text.lower() for m in ['время', 'число', 'дата', 'день']]):
                tz_moscow = pytz.timezone('Europe/Moscow')
                dt_moscow = datetime.now(tz_moscow)
                string_date = dt_moscow.strftime('Дата: %d-%m-%Y\nВремя: '
                                                 '%H:%M:%S\nДень недели: %A')

                vk.messages.send(user_id=event.user_id,
                                 message=string_date,
                                 random_id=random.randint(0, 2 ** 64))
            else:
                vk.messages.send(user_id=event.user_id,
                                 message='Вы можете узнать дату и время, если'
                                         'в вашем сообщении будут слова: "время",'
                                         '"число", "дата", "день"!',
                                 random_id=random.randint(0, 2 ** 64))