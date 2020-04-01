class Comanche:
  def __init__(self, name = 'Comanche'):
    self.name = name

class Luminary:
  def __init__(self, name = 'Luminary'):
    self.name = name
 
sep = "============================"
server_rack_init = "Initializing server rack: {}"
welcome = "Welcome to Server Rack Initializer!"
init_server_before = "Initializing server rack..."
print(sep)
print(welcome)
# Start by initializing the main server rack, Comanche
comanche = Comanche()
print(server_rack_init.format(comanche.name))
print(sep)
luminary = Luminary()
print(server_rack_init.format(luminary.name))
