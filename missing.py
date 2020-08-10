import numpy

class missing:
    def __init__(self):
        self.alltext = ['ne pars pas', 'what do you mean ?', 'on est en agile là !', 'approches-toi ^ ^', 'un café ?', 'qu"est-ce qu"il fait beau aujourd"hui !', 'il est trop froid ?']
        
    def saysomething(self):
        x = numpy.random.randint(len(self.alltext))
        text_rand = self.alltext[x]        
        return text_rand