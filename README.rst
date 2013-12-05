========================
Punto de venta 2013
========================

Punto de venta para medianas empresas con pantallas touch, calcula las ventas diarias, lleva un control de inventarios, control de caja en tiempo real

*nota: Se ira actualizando segun los impuestos que marca la ley*

Demo
---------------
www.puntodeventa.grupodms.com

usuario: Administrador, contraseña: 123 (Lleva control de todo el sistema)

usuario: Autorizado, contraseña: 123 (Vendedor autorizado para cobrar a un cliente)

usuario: Caja. contraseña: 123 (Cobra los tickets que emite un vendedor)

usuario: Vendedor, contraseña: 123 (Vendedor que emite tickets para ser cobrados posteriormente)

Requisitos
---------------

Python2.7 (vease documentacion) http://www.python.org/

PIP (vease documentacion) http://www.pip-installer.org/en/latest/

Node.js (vease documentacion) http://nodejs.org/

Instalacion
---------------

Primero, tu debes asegurarte de contar con un ambiente virtual (http://www.virtualenv.org). Para ello ejecutamos:

    $ pip install virtualenv 

Clonamos el repositorio

    $ git clone https://github.com/flipjack/punto_de_venta.git

Renombramos el proyecto

    $ mv punto_de_venta nombre_del_proyecto

Instalamos el ambiente virtual en el ordenador:

    $ virtualenv nombre_del_proyecto

Activamos el ambiente virtual

    $ cd nombre_del_proyecto

    $ source bin/activate

Instalamos las dependencias

    $ pip install -r requeriments.txt

Corremos el servidor de Django

    $ mv punto_de_venta project

    $ cd project

    $ python manage.py runserver

Corremos el servidor de Node

	$ node node.js/app.js

Documentacion del proyecto
--------------------------
Podras encontrar toda la documentacion del proyecto en:

Agradecimientos
--------------------------
Gustavo Castellanos 

*www.gustavo-castellanos.com*
