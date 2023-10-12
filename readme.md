# Cálculo de la velocidad media del sonido

Se calcula la velocidad media del sonido a partir de la grabación de un ruido impulsivo con dos micrófonos alejados, colocando la fuente junto a uno de ellos. Se calcula la diferencia de tiempo entre la detección de la fuente de cada micrófono y se evalúa la velocidad media y su error estadístico con la distancia entre los micrófonos y las diferencias de tiempo de grabaciones múltiples.

## Aclaraciones

- Los archivos mic1.wav y mic2.wav corresponden a las grabaciones de los micrófonos 1 y 2, respectivamente.
- El procesamiento se realiza en el archivo vsonido.py; en timetools.py únicamente se definen funciones.
- La velocidad media final y su error estadístico son expresadas redondeando sus valores a dos posiciones decimales.
- El código fue escrito para tratar archivos de audio con igual frecuencia de muestreo.
- El código fue escrito para tratar archivos de audio previamente procesados manualmente de modo que cada uno de los disparos se encuentre dentro de un sector de dos segundos de duración por sí solo (es decir, si se divide el audio en sectores de dos segundos no debería encontrarse más de un disparo en ninguno de ellos). No debe realizarse ningún otro procesamiento previo.