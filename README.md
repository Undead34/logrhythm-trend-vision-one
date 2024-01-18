## General Description:
Este es un script para la recoleccion de logs desde Trend Vision One
Utilizando una la API públida de Trend Micro.

## Obteniendo el inicio
Lo primero es crear un archiv __.env__ este archivo se utilizara para cargar las configuraciones
Para sabes que tiene que tener el __.env__ archivo. Lo que debe hacer es crear un copia  de __.env.example__
Y Rellenar los campos vamos a ver la aquí algunos de los valores posibles.

Se necesita un token de api, y la fecha de vencimiento del token API, en un caso extraño de que el token nunca se vensa se debe poner el EXPIRATION_TOKEN="INFINITY", en caso de no saber cuando el token vensa dejar en blanco.

El EMAIL_REPORT es la direccion de correo electronico para la cual se pueden recibir alert sobre el comportamiento del script. lo mismo para ALTERNATIVE_EMAIL_REPORT

Email y EMAIL_PASSWORD son las credenciales SMPT que se usaran para enviar los correos

Max file size se utiliza para determinar el tamaño maximo por archivo de log
Max num files es el numero maximo de archivos de logs.

LOG_SOURCE_ID="0"