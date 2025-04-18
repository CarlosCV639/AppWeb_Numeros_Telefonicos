# Background del Proyecto
Aplicación web desarrollada en Python con las librerías Streamlit, Pandas y SQLite con el objetivo de poder realizar búsquedas de teléfonos asociados a un suministro de luz, con control de la autenticación y estableciendo un límite diario de consultas por usuario. La aplicación fue desplegada internamente en la red de la empresa con previa autorización, por lo que fue utilizada activamente como herramienta de consulta diaria.

## Ventana de Autenticación

<img width="958" alt="image" src="https://github.com/user-attachments/assets/9cdf0d14-b6ec-4920-a770-2f07715d3725" />

Permite el login de los usuarios que tengan el usuario y contraseña establecidos.

## Ventana de Consulta

<img width="960" alt="image" src="https://github.com/user-attachments/assets/cdee2135-f92d-47ee-a170-32d33d5efbb7" />

- Permite ingresar el número de suministro del que se quiere obtener los teléfonos registrados en la bd.
- Muestra la cantidad de búsquedas hecha por usuario, permitiendo realizar 50 diariamente.
- Genera un registro de cada búsqueda realizada en la aplicación con fecha y hora.

# Conclusión
La aplicación permitió eliminar las solicitudes manuales y reducir tiempos de respuesta para solicitar el número celular de un cliente (antes se solicitaba por WhatsApp). Además, caba mencionar que este tipo de apliación es altamente escalable de requerir otras funcionalidades.
