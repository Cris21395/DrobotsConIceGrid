# Drobots

# 1. Introducción
CROBOTS es un juego basado en programación de computadores. A diferencia de los juegos tipo arcade que requiere interacción con 
un
humano para controlar algún objeto, toda la estrategia en CROBOTS está especificada antes del comienzo del juego. La estrategia
del juego está condensada en un programa C que tú diseñas y escribes. Tu programa controla un robot cuya misión es buscar,
perseguir y destruir otros robots, cada uno de ellos bajo el control de programas diferentes en ejecución. Cada robot está
igualmente equipado, y hasta un máximo de cuatro robots pueden competir a la vez. CROBOTS es mejor si lo juegan varias personas,
cada uno perfeccionando su propio programa, y después enfrentando a los programas entre sí. 

En DROBOTS, la arquitectura y la mecánica de la aplicación es muy diferente. El juego está orquestado por un servidor que crea
partidas a la que se conectan los jugadores. Los jugadores aportan controladores de robots y, opcionalmente, controladores de
detectores. Cuando la partida dispone del número de jugadores adecuado, crea robots y detectores para cada jugador y les solicita
los controladores para los mismos. Todos ellos: servidor, jugador, robot y controladores son objetos distribuidos. El detector no
se considera un objeto distribuido, ya que no dispone de ninguna funcionalidad que ofrecer de manera directa, y por tanto no 
tiene
interfaz. Después, el juego va indicando a cada controlador de robot un turno en el que puede interaccionar con el robot 
asociado.
En la modalidad más simple cada jugador tiene un único controlador y por tanto un único robot. Salvo por los aspectos de
comunicación entre programas, pasando de una máquina virtual y ejecución centralizada en CROBOTS, a un conjunto de programas que 
se comunican a través de la red.

En DROBOTS, el juego trata de respetar siempre que sea posible las reglas y funcionamiento del CROBOTS original.

# 2. Ejecución
Antes de comenzar con la ejecución, es importante destacar que se necesita tener instalado IceGrid, así como una versión de 
python superior a la 2.7.
Una vez tengamos instalado lo que se ha mencionado anteriormente, necesitaremos conectarnos con la vpn de la UCLM. En la 
siguiente dirección se especifican los pasos para la configuración de la vpn: https://www.google.es/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=0ahUKEwjhosbkmcLUAhXBbBoKHe76AfQQFggyMAA&url=http%3A%2F%2Fbiblioteca.uclm.es%2FArchivos%2FVPN_UCLM.pdf&usg=AFQjCNGMl5atqqyuG-DMPV8U4--RtKtFgw.
Después de haber realizado estos pasos, ejecutaremos el siguiente comando:
```
make all
```
Con este comando se desplegará la aplicación además de abrir la herramienta icegridgui, un entorno donde ejecutaremos la 
aplicación Drobots. Para ello, daremos clic en "log into an IceGrid Registry". Acto seguido, se abrirá una ventana para 
conectarnos al endpoint del registro icegrid. Pulsamos en connect y se abrirá la venta de "Live Deployment". Una vez estemos en 
la ventana, pulsamos la pestaña (+) de cada nodo para ejecutarlos. Dejamos para el final los players, por lo tanto, nos 
dirigimos a cualquiera que no sean los citados anteriormente y pulsamos botón derecho y ejecutar. Cuando queden por ejecutar 
player y player2, los ejecutamos y, acto seguido, botón derecho y abrimos la salida estándar para ver que está ocurriendo. Es 
importante resaltar, que si la aplicación no funciona, se debe a que el servidor de la unviersidad (UCLM) ha sido modificado 
para la realización de otra práctica diferente a ésta.

# 3. Descarga
Este repositorio puede ser descargado usando el siguiente comando:
```
git clone https://github.com/Cris21395/DrobotsConIceGrid.git
```
El repositorio se almacenará en el directorio donde ejecutemos el comando.
