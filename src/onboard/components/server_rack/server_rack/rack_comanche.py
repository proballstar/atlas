class ComancheRack():
    """
    Defines the Comanche server rack.
    """
    def __init__(self, wifi):
        self.name = 'Comanche'
        self.wifi = wifi
    
    def init():
        self.startup()
        # @TODO: Figure out a way for windows machine to connect to wifi remotely.
        self.connect_wifi()
    
    def connect_wifi():
        pass
    
    def startup():
        pass
    
    def delete_all():
        pass
    
    def shutdown(self):
        
        del self.wifi
