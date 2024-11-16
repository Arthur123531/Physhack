
BLACK = (0,0,0)

class BlackHole: 
    #global vars 
    G = 6.6743*10**(-11)
    c = 299792458  

    def __init__(self, radius, mass):
        self.radius = radius 
        self.mass = mass 

        



def child_rad(M):
    G = 6.6743*10**(-11)
    c = 299792458          
    return 2*G*M/c**2

def check_radius(R, M):
    max_rad = child_rad(M)
    if R == max_rad:
        return (black hole)
    else:
        continue 

