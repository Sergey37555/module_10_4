from queue import Queue
from random import randint
from threading import Thread
from time import sleep


class Table:

    def __init__(self, number):
        self.number = number
        self.guest = None


class Guest(Thread):

    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        sleep(randint(3, 10))


class Cafe:

    def __init__(self, *tables):
        self.queue = Queue()
        self.tables = tables

    def guest_arrival(self, *guests):
        list_guests = list(guests)
        for table in self.tables:
            if len(list_guests) > 0:
                table.guest = list_guests.pop(0)
                table.guest.start()
                print(f'{table.guest.name} сел(-а) за стол номер {table.number}')
        for guest in list_guests:
            self.queue.put(guest)
            print(f'{guest.name} в очереди')

    def discuss_guests(self):
        is_guest = True
        while not self.queue.empty() or is_guest:
            is_guest = False
            for table in self.tables:
                if table.guest is None:
                    if not self.queue.empty():
                        table.guest = self.queue.get()
                        table.guest.start()
                        print(f'{table.guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}')
                elif not table.guest.is_alive():
                    print(f'{table.guest.name} покушал(-а) и ушёл (ушла)')
                    print(f'Стол номер {table.number} свободен')
                    table.guest = None
                if table.guest is not None:
                    is_guest = True


# Создание столов
tables = [Table(number) for number in range(1, 6)]

# Имена гостей
guests_names = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
    'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]

# Создание гостей
guests = [Guest(name) for name in guests_names]

# Заполнение кафе столами
cafe = Cafe(*tables)

# Приём гостей
cafe.guest_arrival(*guests)

# Обслуживание гостей
cafe.discuss_guests()