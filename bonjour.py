import numpy

class bonjour:
    def __init__(self):
        self.bonjour_text = ['bonjour x_x', 'salut !!!', 'ça va ?', 'vas-y ^^', 'chica', 'on your mark', 'hallo', 'another day in paradise !']
        
    def saysomething(self):
        x = numpy.random.randint(len(self.bonjour_text))
        bonjour_rand = self.bonjour_text[x]        
        return bonjour_rand