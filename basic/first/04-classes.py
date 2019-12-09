#  Created by Artem Manchenkov
#  artyom@manchenkoff.me
#
#  Copyright © 2019
#
#  Основы ООП, класс, объект, метод и атрибут
#

class User:
    first_name: str
    last_name: str


john = User()
john.first_name = "John"

print(john.first_name)
