import re
import os
import sqlite3

conn = sqlite3.connect('mentions.db')  # создается база данных
c = conn.cursor()
c.execute("CREATE TABLE mentions( First_mention boolean, Именная группа text, Предложение text)")
for i in range(3987):
    firstmentionsid = []  # пустой список для будущих идентификаторов первых упоминаний
    secondmentionid = []  # пустой список для будущих идентификаторов вторых упоминаний
    thirdmentionid = []  # пустой список для будущих идентификаторов третьих упоминаний
    sent_list = [] #  пустой список, чтобы записывать каждое предложение в бд не более 1 раза
    pathchain = './ForTraining/Chains/book_%d.txt' % i  # путь к файлу с цепочкой упоминаний
    pathtext = './ForTraining/Texts/book_%d.txt' % i  #  путь к текстовому файлу
    if os.path.exists(pathchain):
        with open(pathchain, encoding='utf-8') as f:  # открывается документ с цепочкой упоминаний
            chainlayer = f.read()
        with open(pathtext, encoding='utf-8') as g:  # открывается сам текст
            text = g.read()
        sentences = text.splitlines()  #  текст делится на предожения
        for line in chainlayer.splitlines():
            chainid = line[-2:]  # для каждого упоминания достается номер цепочки
            if chainid not in firstmentionsid:  #  проверка на первое упоминание
                x = 1  # логическая переменная (первое упоминание - true)
                firstmentionsid.append(chainid)  # ID именной группы добавляется в список
                reg_offset = re.search(r'\d*?\s(\d*?)\s', line)  # поиск позиции данного вхождения в тексте
                offset = reg_offset.group(1)
                offset = int(offset)
                reg_length = re.search(r'\d*?\s\d*?\s(\d*?)\s', line)  # поиск длины данной именной группы
                length = reg_length.group(1)
                length = int(length)
                for sent in sentences:  #  ищется предложение, в которое входит рассматриваемая ИГ
                    sent_ind = text.index(sent)  # позиция предложения в целиковом тексте
                    if offset>=sent_ind and offset+length<=sent_ind+len(sent) and sent_ind not in sent_list:
                        c.execute('INSERT INTO mentions VALUES (?, ?, ?)', (x, text[offset:offset+length+1], sent))  # создание одной строчки файла в базе данных
                        conn.commit()
                        sent_list.append(sent_ind)  # пополнение списка с индексами уже использованных предложений

            elif chainid not in secondmentionid:  # все то же самое делается со вторыми и третьими упоминаниями
                x = 0  #  логическая переменная (первое упоминание - false)
                secondmentionid.append(chainid)
                reg_offset = re.search(r'\d*?\s(\d*?)\s', line)
                offset = reg_offset.group(1)
                offset = int(offset)
                reg_length = re.search(r'\d*?\s\d*?\s(\d*?)\s', line)
                length = reg_length.group(1)
                length = int(length)
                for sent in sentences:
                    sent_ind = text.index(sent)
                    if offset >= sent_ind and offset + length <= sent_ind + len(sent) and sent_ind not in sent_list:
                        c.execute('INSERT INTO mentions VALUES (?, ?, ?)', (x, text[offset:offset + length + 1], sent))
                        conn.commit()
                        sent_list.append(sent_ind)

            elif chainid not in thirdmentionid:
                x = 0 #  логическая переменная (первое упоминание - false)
                thirdmentionid.append(chainid)
                reg_offset = re.search(r'\d*?\s(\d*?)\s', line)
                offset = reg_offset.group(1)
                offset = int(offset)
                reg_length = re.search(r'\d*?\s\d*?\s(\d*?)\s', line)
                length = reg_length.group(1)
                length = int(length)
                for sent in sentences:
                    sent_ind = text.index(sent)
                    if offset >= sent_ind and offset + length <= sent_ind + len(sent) and sent_ind not in sent_list:
                        c.execute('INSERT INTO mentions VALUES (?, ?, ?)', (
                        x, text[offset:offset + length + 1], sent))  # создание одной строчки файла в базе данных
                        conn.commit()
                        sent_list.append(sent_ind)


conn.close()



