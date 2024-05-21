#!/usr/bin/env python3
import os
import pickle
from dataclasses import dataclass

os.system('clear')
data_file = 'address.data'


@dataclass
class Record:
  first_name: str
  last_name: str = ''
  nick_name: str = ''
  age: str = ''
  phone: str = ''


class InputController:
  def __init__(self, callbacks = None):
    self.message = None
    self.callbacks = callbacks if callbacks else {}

  def start(self):
    if self.message:
      print(self.message)

    self.message = None
    print('----------------')
    command = input('Enter command: ')
    os.system('clear')
    self.run_command(command)

  def run_command(self, string):
    command, *args = string.split()

    if not command in self.callbacks:
      self.message = f'Wrong command: {command}'
    else:
      callbacks = self.callbacks[command]

      for cb in callbacks:
        if callable(cb):
          cb(*args)

    if command != 'end':
      self.start()
    else:
      os.system('clear')
      print('END')

  def end(self):
    self.run_command('end')

  def add_command(self, command, callback):
    if not command in self.callbacks:
      self.callbacks[command] = []

    self.callbacks[command].append(callback)


class DataController:
  def __init__(self, filename = None):
    self.filename = filename
    self.data = self.get_data()

  def get_data(self):
    result = None

    with open(self.filename, 'rb') as data:
      try:
        result = pickle.load(data)
      except:
        result = {}

    return result

  def set_data(self, data):
    with open(self.filename, 'wb') as file:
      try:
        pickle.dump(data, file)
        return True
      except:
        print("Can't save data")
        return False


class AddressBook(InputController, DataController):
  __changed = False

  def __init__(self, filename):
    DataController.__init__(self, filename)
    InputController.__init__(self)
    self.add_command('list', self.list)
    self.add_command('add', self.add)
    self.add_command('delete', self.delete)
    self.add_command('edit', self.edit)
    self.add_command('save', self.save)

  def list(self):
    # print(self.data)
    for name, data in self.data.items():
      print(f'---------[{name}]---------')
      print(f'  First name: {data.first_name}')
      print(f'  Last name: {data.last_name}')
      print(f'  Nick name: {data.nick_name}')
      print(f'  Age: {data.age}')
      print(f'  Phone: {data.phone}')
      print('')

  def __get_info(self, check = False):
    first_name = input('Enter first name*: ')

    if len(first_name) == 0:
      print('First name is required!')
      return self.__get_info(check)

    if first_name in self.data and check:
      print(f'{first_name} already exists in your address book!')
      return self.__get_info(check)

    last_name = input('Enter last name: ')
    nick_name = input('Enter nick name: ')
    age = input('Enter age: ')
    phone = input('Enter phone: ')

    return first_name, last_name, nick_name, age, phone

  def add(self):
    print('----------[add]-----------')
    first_name, last_name, nick_name, age, phone = self.__get_info(True)
    self.__create(first_name, last_name, nick_name, age, phone)

  def delete(self, name):
    print('------------[delete]----------')
    result = self.__remove(name)

    if result:
      print(f'{name} deleted successfully!')

  def __remove(self, name):
    if not name in self.data:
      print(f'No such user in your address book: {name}')
      return False
    else:
      del self.data[name]
      self.__changed = True
      return True

  def edit(self, name):
    if not name in self.data:
      print(f'No such user in your address book: {name}')
    else:
      first_name, last_name, nick_name, age, phone = self.__get_info()
      self.__remove(name)
      self.__create(first_name, last_name, nick_name, age, phone)

  def __create(self, first_name, last_name, nick_name, age, phone):
    self.data[first_name] = Record(
      first_name,
      last_name,
      nick_name,
      age,
      phone,
    )
    self.__changed = True

  def save(self):
    print('----------[saving data]----------')

    if (self.__changed):
      result = self.set_data(self.data)

      if result:
        print('Data saved!')
        self.__changed = False
    else:
      print('Data has not changed')

  def run_command(self, string):
    command = string.split()[0]

    if command == 'end' and self.__changed:
      confirm = input('Do you want to save changes? (print "yes") ')

      if confirm == 'yes':
        self.save()

    return super().run_command(string)



def main():
  book = AddressBook(filename = 'address.data')
  book.start()


if __name__ == '__main__':
  main()
