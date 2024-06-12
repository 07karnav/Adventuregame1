import sys

class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.connected_rooms = {}
        self.items = []
        self.visited = False

    def connect(self, direction, room):
        self.connected_rooms[direction] = room

    def describe(self):
        return self.description

class Game:
    def __init__(self):
        self.rooms = self.setup_rooms()
        self.current_room = self.rooms['Entrance']
        self.inventory = []
        self.game_over = False

    def setup_rooms(self):
        entrance = Room("Entrance", "You're at the entrance of a spooky cave. A path leads north.")
        hall = Room("Hall", "You're in a hall with flickering torches. Paths lead north and south.")
        armory = Room("Armory", "You're in an old armory. Paths lead east and west.")
        treasure_room = Room("Treasure Room", "You've found the treasure room! There's a chest here.")
        exit_room = Room("Exit", "You see a door leading out of the cave to the east. It's locked.")

        entrance.connect('north', hall)
        hall.connect('south', entrance)
        hall.connect('north', armory)
        armory.connect('south', hall)
        armory.connect('east', treasure_room)
        treasure_room.connect('west', armory)
        armory.connect('west', exit_room)
        exit_room.connect('east', armory)

        armory.items.append('key')
        treasure_room.items.append('treasure')

        return {
            'Entrance': entrance,
            'Hall': hall,
            'Armory': armory,
            'Treasure Room': treasure_room,
            'Exit': exit_room
        }

    def play(self):
        print("Welcome to the Adventure Game!")
        print("Type 'help' if you need a list of commands.")
        while not self.game_over:
            print("\n" + self.current_room.describe())
            command = input("> ").strip().lower()
            self.process_command(command)

    def process_command(self, command):
        if command in ["north", "south", "east", "west"]:
            self.move(command)
        elif command == "look":
            self.look()
        elif command.startswith("take "):
            item = command.split("take ", 1)[1]
            self.take(item)
        elif command == "inventory":
            self.show_inventory()
        elif command.startswith("use "):
            item = command.split("use ", 1)[1]
            self.use(item)
        elif command == "help":
            self.show_help()
        else:
            print("I don't understand that command.")

    def move(self, direction):
        if direction in self.current_room.connected_rooms:
            self.current_room = self.current_room.connected_rooms[direction]
            if not self.current_room.visited:
                self.current_room.visited = True
                if self.current_room.name == "Treasure Room" and 'key' in self.inventory:
                    print("You use the key to open the chest and find the treasure! You win!")
                    self.inventory.append('treasure')
                    self.game_over = True
                elif self.current_room.name == "Exit" and 'treasure' in self.inventory:
                    print("You unlock the door with the treasure and escape the cave! You win!")
                    self.game_over = True
        else:
            print("You can't go that way.")

    def look(self):
        if self.current_room.items:
            print("You see the following items: " + ", ".join(self.current_room.items))
        else:
            print("There's nothing here.")

    def take(self, item):
        if item in self.current_room.items:
            self.inventory.append(item)
            self.current_room.items.remove(item)
            print(f"You took the {item}.")
        else:
            print(f"There is no {item} here.")

    def show_inventory(self):
        if self.inventory:
            print("You have: " + ", ".join(self.inventory))
        else:
            print("You're not carrying anything.")

    def use(self, item):
        if item in self.inventory:
            if item == "key" and self.current_room.name == "Treasure Room":
                print("You use the key to open the chest and find the treasure! You win!")
                self.inventory.append('treasure')
                self.inventory.remove('key')
                self.game_over = True
            elif item == "treasure" and self.current_room.name == "Exit":
                print("You unlock the door with the treasure and escape the cave! You win!")
                self.game_over = True
            else:
                print("You can't use that here.")
        else:
            print("You don't have that item.")

    def show_help(self):
        print("Commands:")
        print("  north, south, east, west - Move in a direction")
        print("  look - Look around the room")
        print("  take [item] - Take an item")
        print("  inventory - Show your inventory")
        print("  use [item] - Use an item from your inventory")
        print("  help - Show this help message")

if __name__ == "__main__":
    game = Game()
    game.play()
