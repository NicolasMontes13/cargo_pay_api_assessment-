def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class UFE():
    def __init__(self):
        self.resultado = 0
    
    def calculate_ufe(self, ufe, new_ufe):
        self.resultado = ufe * new_ufe
        print(self.resultado)
        return self.resultado

    