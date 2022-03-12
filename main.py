import pywebio
from pywebio import input
from pywebio import output
import time
import numpy
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import os


def sbros():
    df = pd.DataFrame(columns=['day', 'accuracy', 'time_word'])
    df.to_csv('stat.csv')

def list_words(len):
    with open('russian.txt', 'r', encoding='windows-1251') as file:
        words = file.readlines()
        words = [s.strip("\n") for s in words]
    return numpy.random.choice(words, size=len)


def time_reset():
    global time_i
    time_i = 0


def train():
    global time_i
    global df

    def check_l(p):
        if p < 0:
            return 'What?'

    output.clear()
    len = input.input("Введите количесвто слов", type='number', validate=check_l)
    time_word = input.input("Время на запоминание одного слова [сек]", type='number', validate=check_l)
    words = list_words(len)
    for j, i in enumerate(words):
        time_i = time_word
        output.clear()
        output.put_markdown('## Тренировка')
        output.put_row([
            output.put_column([
                output.put_text('\n\n')]),None,
            output.put_column([
                output.put_text('\n\n'),
                output.put_markdown(f'<font size = 10> {i} </font>')]),
            output.put_column([
                output.put_text('\n\n')]), None,
        ])

        for i in range(int(time_word), 0, -1):
            if i < 4:
                output.put_text(i)
            time.sleep(1)

    output.clear()
    output.put_markdown('## Проверка знаний')
    for j, i in enumerate(words):
        output.put_markdown(f'<font size = 5> {j+1} - {i} </font>')
        len_words = j+1
    true_words = input.input("Введите количесвто запомнившихся слов", type='number')
    accuracy = true_words/len_words
    new_row = {'day': datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S"),
               'accuracy': accuracy,
               'time_word': true_words}

    df = df.append(new_row, ignore_index=True)
    df[['day', 'accuracy', 'time_word']].to_csv('stat.csv')
    menu()


def stat():
    global df
    output.clear()
    plt.figure(figsize=[10, 5])
    plt.plot(df['day'], df['accuracy'])
    plt.xlabel('day')
    plt.ylabel('accuracy')
    plt.savefig('plot.png')
    output.put_image(src='plot.png')
    # os.remove('plot.png')
    time.sleep(15)
    main()
    pass


def menu():
    output.clear()
    output.put_markdown('# Mind Train')
    output.put_row([
        output.put_button("Тренировка",
                          onclick=lambda: train()),
        output.put_button("Статистика",
                          onclick=lambda: stat(),
                          disabled=True),
        output.put_button("Сброс статистики",
                          onclick=lambda: sbros())
    ])

df = pd.read_csv('stat.csv')
def main():
    global df
    menu()


if __name__ == '__main__':
    pywebio.start_server(main, debug=True, port=8070, cdn=False)