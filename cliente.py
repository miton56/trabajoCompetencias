
class Cliente:
    def __init__(self, nombre: str, correo: str, direccion: str, telefono: int, rut: str):
        self.nombre = str(nombre)
        self.correo = str(correo)
        self.direccion = str(direccion)
        self.telefono = int(telefono)
        self.rut = str(rut)
    
    def get_nombre(self):
        return self.nombre
    
    def get_correo(self):
        return self.correo
    
    def get_direccion(self):
        return self.direccion
    
    def get_telefono(self):
        return self.telefono
    
    def get_rut(self):
        return self.rut
        
    def informacion(self):
        return f"nombre: {self.nombre} \n contacto: {self.correo}"
    
    hola="1"
    


    




