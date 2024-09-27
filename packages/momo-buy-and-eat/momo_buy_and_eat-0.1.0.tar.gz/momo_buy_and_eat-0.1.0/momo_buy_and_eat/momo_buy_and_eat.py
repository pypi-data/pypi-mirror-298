import random


class Momo:
    def __init__(self):
        self.price = random.randint(100, 5000)
        self.message = " ".join(random.choices(["Yummy!", "momo", "Tasty!", ":)", "peach"], k=random.randint(1, 10)))
        
    def smile(self):
        print(self.message)


class MomoEater:
    def __init__(self, username) -> None:
        self.username = username
        self.momo_list = []
        self.total_price = 0
        self.total_momo_eaten = 0
        
    def __str__(self):
        return f"MomoEater {self.username}; living with {len(self.momo_list)} momo(s)."
        
    def _clear(self):
        self.momo_list = []
        self.total_price = 0
        self.total_momo_eaten = 0
    
    def buy_momo(self):
        new_momo = Momo()
        self.momo_list.append(new_momo)
        self.total_price += new_momo.price
        print(f"{self.username} is buying momo for {new_momo.price} yen.")
    
    def eat_momo(self):
        if len(self.momo_list) == 0:
            print(f"{self.username} has no momo to eat.")
            return
        momo = random.choice(self.momo_list)
        self.momo_list.remove(momo)
        self.total_momo_eaten += 1
        print(f"{self.username} is eating momo that costs {momo.price} yen.")
        
    def play_with_momo(self):
        if len(self.momo_list) == 0:
            print(f"{self.username} has no momo to play with.")
            return
        print(f"You have {len(self.momo_list)} momo(s) to play with.")
        print("Playing with one of them...")
        momo = random.choice(self.momo_list)
        momo.smile()
        
    def finish_game(self):
        print(f"{self.username} has eaten {self.total_momo_eaten} momo(s) with total price of {self.total_price} yen.")
        if len(self.momo_list) == 0:
            print(f"But {self.username} has no momo living together :-(")
        else:
            print(f"{self.username} has {len(self.momo_list)} momo(s) living together :)")
        print(f"Goodbye, {self.username}!")
        self._clear()
