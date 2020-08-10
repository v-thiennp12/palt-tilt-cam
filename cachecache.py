import numpy

class cachecache:
    def __init__(self):
        self.alltext = ['je suis fatigué là ..', 'je me cache', '', 'approches-toi', 'bella ciao', 'allez, je décolle', 'j"ai faim', 'on fait une pause ?']
        
    def saysomething(self):
        x = numpy.random.randint(len(self.alltext))
        text_rand = self.alltext[x]        
        return text_rand