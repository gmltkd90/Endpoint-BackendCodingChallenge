'''TODO: A common method of organizing files on a computer is to store them in hierarchical directories. For instance:

 

```

photos/

  birthdays/

    joe/

    mary/

  vacations/

  weddings/

```

Input	                                    Output

CREATE fruits	                            CREATE fruits
CREATE vegetables	                        CREATE vegetables
CREATE grains	                            CREATE grains
CREATE fruits/apples	                    CREATE fruits/apples
CREATE fruits/apples/fuji	                CREATE fruits/apples/fuji
LIST	                                    LIST
                                                fruits
                                                    apples
                                                        fuji
                                                grains
                                                vegetables
CREATE grains/squash	                    CREATE grains/squash
MOVE grains/squash vegetables	            MOVE grains/squash vegetables
CREATE foods	                            CREATE foods
MOVE grains foods	                        MOVE grains foods
MOVE fruits foods	                        MOVE fruits foods
MOVE vegetables foods	                    MOVE vegetables foods
LIST	                                    LIST
                                                foods
                                                    fruits
                                                        apples
                                                        fuji
                                                grains
                                                vegetables
                                                    squash
DELETE fruits/apples	                    DELETE fruits/apples
                                            Cannot delete fruits/apples - fruits does not exist
DELETE foods/fruits/apples	                DELETE foods/fruits/apples
LIST	                                    LIST
                                                foods
                                                    fruits
                                                    grains
                                                    vegetables
                                                        squash

'''

# Setting the calss
class FileOrganizer:
    # Construcutor
    def __init__(self):
        self.directories_tree = {}

    # CREATE function - Create new node into the tree
    def create(self, path):
        try:
            dirs = path.split('/')
            node = self.directories_tree
            for d in dirs:
                # If the element does not exist, 
                if d not in node:
                    node[d] = {}
                node = node[d]
        except Exception as e:
            print("Error During CREATE: " + str(e))

    # Disply Function - Display full directory free 
    def display_list(self, node=None, indent=0):
        try:
            # node should be None for directories_tree only. If node is none, set it to directories_tree.
            if node is None:
                node = self.directories_tree
            for name in sorted(node.keys()):
                print("  " * indent + name)
                # Disply next line with higher level of indent
                self.display_list(node[name], indent + 1)
        except Exception as e:
            print("Error During LIST: " + str(e))

    # Move Function - Move the element to different location of the tree
    def move(self, src_path, dest_path):
        try:
            src_dirs = src_path.split('/')
            dest_dirs = dest_path.split('/')
            
            # Navigate to the source parent directory
            node = self.directories_tree
            for d in src_dirs[:-1]:
                if d not in node:
                    print("Cannot move " + src_path + " - " + '/'.join(src_dirs[:-1]) + " does not exist")
                    return
                node = node[d]
            
            # Remove the source item
            item_name = src_dirs[-1]
            if item_name not in node:
                print("Cannot move " + src_path + " - " + item_name + " does not exist")
                return
            item = node.pop(item_name)
            
            # Navigate to the destination directory
            node = self.directories_tree
            for d in dest_dirs:
                if d not in node:
                    node[d] = {}
                node = node[d]
            
            node[item_name] = item
        except KeyError as e:
            print("Error During MOVE: Missing Directory in Path - " + str(e))
        except Exception as e:
            print("Unexpected Rrror During MOVE: " + str(e))

    # Delete Function - Delete the element from the tree
    def delete(self, path):
        try:
            dirs = path.split('/')
            node = self.directories_tree
            for d in dirs[:-1]:
                if d not in node:
                    print("Cannot Delete " + path + " - " + '/'.join(dirs[:-1]) + " does not exist")
                    return
                node = node[d]
            
            # Attempt to delete the item
            item_name = dirs[-1]
            if item_name in node:
                del node[item_name]
            else:
                print("Cannot delete " + path + " - " + item_name + " does not exist")
        except KeyError as e:
            print("Error During DELETE: Missing Directory in Path - " + str(e))

    # Command Reader - Ready the command from input and route to correct functionality
    def command_reader(self, command):
        try:
            parts = command.split()
            action = parts[0]
            #Let user know if Command has any smallcases
            if action != action.upper():
                print("Error: Commands Must be in Uppercase.")
                return
            if action == "CREATE":
                self.create(parts[1])
            elif action == "LIST":
                self.display_list()
            elif action == "MOVE":
                self.move(parts[1], parts[2])
            elif action == "DELETE":
                self.delete(parts[1])
            else:
                print("Unknown Command: " + command)
        except IndexError:
            print("Error: Missing Command.")
        except Exception as e:
            print("Error While Processing Command '" + command + "': " + str(e))


# Interactive session
fs = FileOrganizer()
print("Please Enter Your Commands - CREATE, LIST, MOVE, DELETE (type 'QUIT' to quit):")
while True:
    try:
        command = input().strip()
        if command == "QUIT":
            break
        fs.command_reader(command)
    except KeyboardInterrupt:
        print("\nExiting Program.")
        break
    except Exception as e:
        print("Unexpected Error: " + str(e))

