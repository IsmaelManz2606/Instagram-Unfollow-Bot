# Instagram Unfollow Bot

## Descripción

Este proyecto es un bot automatizado que interactúa con tu cuenta de Instagram para gestionar la lista de cuentas a las que sigues. El bot realiza las siguientes tareas:

- Abre el perfil de Instagram usando Selenium y un perfil configurado de Chrome.
- Accede a la sección "Siguiendo" y despliega el modal con las cuentas que sigues.
- Realiza scroll dinámico en el modal para cargar todas las cuentas disponibles.
- Procesa cada cuenta:
  - Accede al perfil y obtiene la cantidad de seguidores.
  - Si la cuenta tiene 10,000 (o más) seguidores, se considera "famosa" y se omite.
  - Para el resto, comprueba en el modal de "Seguidos" de esa cuenta si te siguen.
  - Si la cuenta no te sigue, se procede a dejar de seguirla.
- Repite el proceso hasta no encontrar cuentas nuevas para procesar.

## Requisitos

- Python 3.x
- Selenium
- WebDriver Manager
- Python-Dotenv
- Un perfil configurado de Chrome para evitar problemas con el login.

## Instalación

1. Clona el repositorio:

   ```sh
   git clone <URL-del-repositorio>
   ```

2. Navega al directorio del proyecto:

   ```sh
   cd instagram-unfollow-bot
   ```

3. Crea y activa el entorno virtual:

   ```sh
   python -m venv env
   env\Scripts\activate  # en Windows
   ```

4. Instala las dependencias:
   ```sh
   pip install selenium webdriver_manager python-dotenv
   ```

## Configuración

1. Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

   ```env
   // filepath: c:\Users\USUARIOPERSONAL\Desktop\Automatizacion-dejardeseguir\.env
   INSTAGRAM_USERNAME=tu_usuario
   INSTAGRAM_PASSWORD=tu_contraseña
   ```

   Reemplaza `tu_usuario` y `tu_contraseña` con tus credenciales de Instagram.

2. Asegúrate de que la ruta del perfil de Chrome en `bot.py` esté correctamente configurada en la línea:
   ```python
   options.add_argument("user-data-dir=C:/Users/USUARIOPERSONAL/AppData/Local/Google/Chrome/User Data/Profile 1")
   ```

## Uso

Para ejecutar el bot, simplemente corre:

```sh
python bot.py
```

El bot abrirá el navegador, accederá a tu perfil de Instagram y ejecutará el proceso de dejar de seguir según los criterios definidos.

## Advertencia

- **Uso bajo responsabilidad:** Automatizar acciones en Instagram puede violar los términos de servicio de la plataforma y acarrear sanciones a tu cuenta.
- **Cuenta secundaria:** Se recomienda probar este bot con una cuenta secundaria antes de usarlo en tu cuenta principal.
- Asegúrate de comprender los riesgos antes de ejecutar el script.

## Contribuciones

Si deseas aportar mejoras o corregir errores, realiza un fork del repositorio y envía un pull request.

## Licencia

La licencia de este proyecto es de Ismael Manzano Reinoso. Todos los derechos reservados.
