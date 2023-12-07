from enum import Enum


class HomeInfo(Enum):
    floor: int = 0
    unit: int = 1
    price: int = 2
    status: int = 3
    address: int = 4


class Home:
    def __init__(self, floor: HomeInfo, unit: HomeInfo, price: HomeInfo, status: HomeInfo, address: HomeInfo) -> None:
        self.floor = floor
        self.unit = unit
        self.price = price
        self.status = status
        self.address = address

    def __str__(self) -> str:
        return f"Home: The floor is " \
               f"{self.floor}, the unit is {self.unit}, the price is {self.price}, " \
               f"the status is {self.status}, the address is {self.address}"

    class Rooms:
        @staticmethod
        def func():
            print()
            print("Hello world")


# print(Home(HomeInfo.floor, HomeInfo.unit, HomeInfo.price, HomeInfo.status, HomeInfo.address))
#
# Home.Rooms().func()
exec("for i in range(10): print(i) if i % 2 == 0 else print('odd') if i % 3 == 0 else print('even')")


class HHome:
    def __init__(self, name: str) -> None:
        self.name = name


obj = HHome("John")
print(getattr(obj, "name"))
setattr(obj, "name", "Jack")
print(getattr(obj, "name"))

iterable = [1, 2, 3, 4, 5]
iterator = iter(iterable)
print(next(iterator))
print(next(iterator))