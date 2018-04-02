import datetime


def log(msg):
    date = str(datetime.date.today()).replace('-', '')
    filename = './logs/' + date + '.log'
    file = open(filename, 'a+', encoding="utf8")
    file.write(str(datetime.datetime.now()) + '\n' + str(msg) + '\n')
    file.close()

