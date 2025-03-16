from deviceHA.config import HOME_ASSISTANT_TOKEN
from deviceHA.yeelinkLamp22Cad9Light import YeelinkLamp22Cad9Light

lamp = YeelinkLamp22Cad9Light(HOME_ASSISTANT_TOKEN)

res = lamp.toggle() 
print(res)