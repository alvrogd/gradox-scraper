# gradox-scraper

## ¿Qué es?

El Grado de Ingeniería Informática de la Universidad de Santiago de Compostela cuenta con un repositorio no oficial para cada una de las asignaturas de las que se compone el grado: [gradox](https://www.gradox.es).

Su contenido ha sido esencialmente aportado por estudiantes del propio grado, y consiste principalmente en:
* Apuntes.
* Boletines y proyectos.
* Pruebas.

Este script escrito en Python se encarga de recorrer todo el contenido disponible en el repositorio, guardando en el almacenamiento local todos aquellos ficheros que todavía no se encuentren en él.

## ¿Por qué?

El repositorio presenta un gran problema: si el servidor que lo _hostea_ no responde, no existe ninguna otra vía de acceder a los ficheros alojados en él. A pesar de que esto pueda parecer un hecho poco recurrente, y efectivamente lo es, suele coincidir con fechas poco oportunas, como las semanas previas a exámenes.

Además, el sitio web del repositorio no se encuentra diseñado de modo que una persona pueda descargar rápidamente los ficheros presentes en él. Por otra parte, tampoco es posible realizar una búsqueda de ficheros, filtrándolos por ejemplo en base a una fecha de subida. 

Claramente, no hace falta destacar que además a nadie le apetece realizar una tarea tan repetitiva como descargar decenas de ficheros de un sitio web.

## ¿Cómo se usa?

1. Asegúrate de tener una instalación funcional de Python 3, así como el navegador _Chromium/Chrome_.
2. Asegúrate de tener el módulo ```selenium```, que se requiere para la ejecución, y no viene incluido por defecto en Python 3.
    2.1. Si no lo tienes instalado, es posible añadirlo a tu entorno de Python mediante ```pip3 install selenium```. 
3. Descarga el _script_: ```backup.py```.
4. Otorga permisos de ejecución al _script_; por ejemplo, ejecutando el comando ```chmod u+x ./backup.py```.
5. Ejecuta el _script_: ```./backup.py```.
6. Se abrirá una instancia del navegador; no la cierres, el _script_ la requiere para poder explorar el repositorio.
7. Cuando la descarga de todos los ficheros finalice, dicha instancia se cerrará, y el _script_ finalizará su ejecución.
