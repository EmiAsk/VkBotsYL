from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api
import random
from datetime import datetime


TOKEN = 'a2d5ab8ff0620607f37970f89a3d6605e09c543da8a6cc48e223ac1126305654c6741f81aec1825807bce'

# ссылка на группу-бота (писать ему в лс) - https://vk.com/club203903187


def send_message(user_id, text):
    vk.messages.send(user_id=user_id,
                     message=text,
                     random_id=random.randint(0, 2 ** 64))


vk_sess = vk_api.VkApi(token=TOKEN)
vk = vk_sess.get_api()
longpoll = VkLongPoll(vk_sess)

answered = False

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me and event.from_user:
            if not answered:
                data = vk.users.get(user_ids=[event.user_id], fields=['first_name', 'city'])[0]
                msg = f'Привет, {data["first_name"]}! Напиши дату, а я отвечу, ' \
                      f'какой день недели был в этот день!'
                send_message(event.user_id, msg)

                answered = True
            else:
                try:
                    date = datetime.strptime(event.text, '%Y-%m-%d')
                    name = date.strftime('%A')
                    send_message(event.user_id, f'В эту дату был: {name}. '
                                                f'Спрашивайте меня дальше до бесконечности')

                except ValueError:
                    send_message(event.user_id, 'Неверный формат даты (YYYY-MM-DD)! Повторите ввод!')

