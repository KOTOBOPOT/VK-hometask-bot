import vk_api
import time
import random
print("Bot Vkontakte v2.0 start working... ")
token = ""#input your own VK token (you can get it in settings of your VK community)
subjects = {"общество":0,"физика":1,"алгебра":2,"геометрия":3,"литра":4,"русский":5,"география":6,"биология":7,"англ":8,"информатика":10,"история":11,"химия":12,"обж":13,"литра(род)":14,"астрономия":15,"русегэ":16}
vk = vk_api.VkApi(token=token)
vk._auth_token()
days=['пн','вт','ср','чт','пт','сб']
#[['пн','понедельник'],['вт','вторник'],['ср','среда'],['чт','четверг'],['пт','пятница'],['сб','суббота',]]
instruction="Инструкция. Основные функции:\n 1.ДЗ на день недели (первые 2 согласные дня), примеры запроса: пн ; вт.\n 2.Дз по конкретному предмету, пример: дз алгебра. \n 3.Запись дз, пример: общество стр10 №1 (можно прикреплять фотографии)\n 4.Прошлое дз по предмету: пр алгебра .\n    Предметы : русегэ,общество, физика, алгебра, геометрия, литра, русский, география, биология, англ, астрономия, информатика, история, химия, обж, литра(род)."
zapr= "Запрос не опознан. Для получения инструкции введите \"инструкция\" (писать без ковычек)"
peremennaya_dlya_isklyucheniya=0
spec = "Специальные возможности. Получение домашки на определенный день недели, примеры запросов: пн ; вт"
day_lesson = {"пн": ["алгебра","геометрия","астрономия","география","русский","химия"], "вт": ["общество","физика","информатика","русегэ"],"ср": ["алгебра","обж","физика","биология"],"чт": ["информатика","история","литра","англ"],"пт": ["геометрия","литра","англ"],"сб": ["физика","алгебра","англ"]}
def files_send(subject_name,files_name):
  print("Из файла достаем id")
  hometask_file = open(files_name, "r",encoding="utf-8")
  hometask_lines = hometask_file.readlines()
  hometask = hometask_lines[subjects[subject_name]]
  hometask_file.close()
  return hometask
def file_change(subject_name, hmtsk,files_name):
    print("Запись в файл")
    hometask_file = open(files_name, "r", encoding="utf-8")
    hometask_lines = hometask_file.readlines()
    hometask_file.close()
    hometask_file = open(files_name, "w", encoding="utf-8")
    old_hmtsk = hometask_lines[subjects[subject_name]]
    hometask_lines[subjects[subject_name]] = hmtsk + " \n"
    for i in range(len(hometask_lines)):
        hometask_file.write(hometask_lines[i])
    hometask_file.close()
    return old_hmtsk.strip()
def day_send(day):# функция отправки домашки по дням
 print("Отправка домашки по дням")
 message = ""
 for i in range(len(day_lesson[day])):
   message=files_send(day_lesson[day][i],'hometask.txt')
   vk.method("messages.send",{"peer_id": id, "message": "", "random_id": random.randint(1, 2147483647),"forward_messages":message})
def join1(p):
    k = " "
    for i in range(len(p)):
        k +=p[i]
        k+= ' '
    return k
def message_in(pl):
    peremennaya_dlya_isklyucheniya = 0
    if pl[0] in subjects:
        file_change(pl[0],file_change(pl[0],str(id_message),'hometask.txt'),'hmtsk_last.txt')
        vk.method("messages.send",{"peer_id": id, "message": "дз получено", "random_id": random.randint(1, 2147483647)})
        peremennaya_dlya_isklyucheniya = 1
        print("Дз записано")
    if len(pl)>1:
     print('3')
     if pl[0]=="пр" and pl[1] in subjects:
       peremennaya_dlya_isklyucheniya = 1
       vk.method("messages.send",{"peer_id": id, "message": "Распишитесь", "random_id": random.randint(1, 2147483647),"forward_messages":files_send(pl[1],'hmtsk_last.txt')})
     if pl[0]=="дз" and pl[1] in subjects:
        vk.method("messages.send",{"peer_id": id, "message": "Распишитесь", "random_id": random.randint(1, 2147483647),"forward_messages":files_send(pl[1],'hometask.txt')})
        peremennaya_dlya_isklyucheniya = 1
        print("Дз отправлено")
    if pl[0] in days:
         peremennaya_dlya_isklyucheniya = 1
         day_send(pl[0])
         print(pl[0])
    return peremennaya_dlya_isklyucheniya
while True:
    try:
        peremennaya_dlya_isklyucheniya = 0
        messages = vk.method("messages.getConversations", {"offset": 0, "count": 200, "filter": "unanswered"})
        if messages["count"] >= 1:
            id = messages["items"][0]["last_message"]["from_id"]
            id_message = messages["items"][0]["last_message"]["id"]
            body = messages["items"][0]["last_message"]["text"]
            k=body.lower().split()
            peremennaya_dlya_isklyucheniya =  message_in(body.lower().split())
            if body.lower() == "инструкция":
               vk.method("messages.send", {"peer_id": id, "message": instruction, "random_id": random.randint(1, 2147483647)})
               peremennaya_dlya_isklyucheniya=1
               print("Отправка инструкции")
            if peremennaya_dlya_isklyucheniya == 0:
                print("неизвестный запрос")
                vk.method("messages.send", {"peer_id": id, "message": zapr, "random_id": random.randint(1, 2147483647)})
            print("cycle's end")
    except Exception as E:
        print(E)
        time.sleep(1)
