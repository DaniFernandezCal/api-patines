# Api-Uvigo

Api desarrollada para proyecto UVigo de la asignatura Laboratio de Proyectos del Grado de Teleco.

# Breve descripción

El proyecto UVigo consiste en un sistema de alquiler de patines eléctricos. Para ello se desarrollo:
- Api REST para la gestión de usuarios y patines (código en este repositorio)
- Aplicación Android para poder registrarse, alquilar patines.
- Hardware para carga de patines y poder devolver los patines alquilados. 

# Arquitectura
El api se comunica con una base de datos de Mongodb para persistencia de información y con un Rabbitmq para la comunicación con la placa encargada de abrir o cerrar la cerradura del patin.
