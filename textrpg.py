import random
from typing import List

ESCAPE_CHANCES = {'Разбойник': 0.55, 'Маг': 0.25, 'Воин': 0.25}
CRITICAL_HIT_CHANCE = 0.1
HEALTH_RESTORE = 30
DEFAULT_HEALTH = 100

class Character:
    def __init__(self, char_class: str):
        self.char_class: str = char_class
        self.health: int = DEFAULT_HEALTH
        self.attack_power: int = self.set_attack_power()

    def set_attack_power(self) -> int:
        if self.char_class == 'Воин':
            return random.randint(15, 20)
        elif self.char_class == 'Маг':
            return random.randint(8, 15)
        elif self.char_class == 'Разбойник':
            return random.randint(8, 15)
        return 0

    @property
    def is_alive(self) -> bool:
        return self.health > 0

    def attack(self, enemy) -> None:
        damage = self.attack_power
        if random.random() < CRITICAL_HIT_CHANCE:
            damage = int(damage * 1.5)
            print(f"Критический удар! Урон увеличен до {damage}.")
        enemy.health -= damage
        print(f"{self.char_class} атакует {enemy.name} и наносит {damage} урона!")

    def heal(self, target) -> None:
        if self.char_class == 'Маг':
            target.health = min(target.health + HEALTH_RESTORE, DEFAULT_HEALTH)
            print(f"{self.char_class} исцеляет {target.char_class}. Здоровье: {target.health}/{DEFAULT_HEALTH}.")

    def restore_health(self) -> None: 
        self.health = DEFAULT_HEALTH    #Восстановление здоровья до максимума
        print(f"{self.char_class} восстановил здоровье до {DEFAULT_HEALTH} HP.")


class Enemy:
    def __init__(self, name: str, health: int, attack_power: int):
        self.name: str = name
        self.health: int = health
        self.attack_power: int = attack_power

    @property
    def is_alive(self) -> bool:
        return self.health > 0

    def attack(self, target: Character) -> None:
        target.health -= self.attack_power
        print(f"{self.name} атакует {target.char_class} и наносит {self.attack_power} урона!")


ENEMY_LIST = [
    Enemy("Гоблин", 20, 10),
    Enemy("Ядовитый Паук", 30, 10),
    Enemy("Воин-Мечник", 60, 20),
    Enemy("Воин-Лучник", 60, 20),
    Enemy("Дракон", 100, 30)
]


def battle(team: List[Character], enemy: Enemy) -> bool:
    print(f"\nСражение с {enemy.name} началось! \nВраг имеет {enemy.health} HP.")

    while any(c.is_alive for c in team) and enemy.is_alive: #Пока кто-нибудь из команды жив и враг жив
        print("\nКоманда:")
        for i, char in enumerate(team):
            status = f"{char.health}/{DEFAULT_HEALTH}" if char.is_alive else "погиб"
            print(f"  {i + 1}. {char.char_class} (HP: {status})")

        try:
            choice = int(input("\nВыберите персонажа (1-3): ")) - 1
            if choice < 0 or choice >= len(team) or not team[choice].is_alive:
                raise ValueError
        except ValueError:
            print("Некорректный выбор.")
            continue    #Следущий цикл

        char = team[choice]
        action = input(f"Ход персонажа {char.char_class}. Выберите действие: (a) - атаковать, (h) - лечить , (q) - сбежать: ").lower()

        if action == 'a':
            char.attack(enemy)
            if not enemy.is_alive:
                print(f"{enemy.name} побежден!")
                return True  # Враг побежден

        elif action == 'h' and char.char_class == 'Маг':
            try:
                target_choice = int(input("Кого лечить? (Введите номер 1-3): ")) - 1
                if target_choice < 0 or target_choice >= len(team) or not team[target_choice].is_alive:
                    raise ValueError
                char.heal(team[target_choice])
            except ValueError:
                print("Некорректный выбор цели для лечения.")

        elif action == 'q':
            escape_chance = ESCAPE_CHANCES.get(char.char_class, 0.2) #Получаем шанс побега
            if random.random() < escape_chance:
                print(f"{char.char_class} сбежал с поля боя!")
                restore_team_health(team)  
                return False  
            else:
                print(f"{char.char_class} не смог сбежать!")

        if enemy.is_alive:
            target = random.choice([c for c in team if c.is_alive]) #Атака случайного союзника
            enemy.attack(target)

        for c in team:
            if not c.is_alive:
                print(f"{c.char_class} погиб!")

    return any(c.is_alive for c in team)  # Возврат true если кто-то из команды жив


def restore_team_health(team: List[Character]) -> None: 
    print("\nКоманда восстанавливает силы после побега!")
    for member in team:
        if member.is_alive:
            member.restore_health() #Восстановление здоровья команды после успешного побега


def game():
    print("Добро пожаловать в игру! \nВаш отряд, состоящий из Воина, Мага и Разбойника вступает в подземелье. Вашей задача - победить Дракона, находящегося на нижнем уровне подземелья, путь к которому преграждают различные монстры.\nВоин имеет повышенный урон. Маг может лечит себя либо члена команды один раз за ход. Разбойник может инициировать командный побег с поля боя.")
    team = [Character('Воин'), Character('Маг'), Character('Разбойник')]

    for enemy in ENEMY_LIST[:-1]: #Бой со всеми кроме дракона
        if not battle(team, enemy):
            print("Вы сбежали и избежали столкновения с врагом!")
            continue  

    
    print("\nБитва с Драконом")
    if battle(team, ENEMY_LIST[-1]):
        print("Вы победили Дракона! Игра завершена.")
    else:
        print("Команда пала в бою. Конец игры.")

if __name__ == "__main__":
    game()