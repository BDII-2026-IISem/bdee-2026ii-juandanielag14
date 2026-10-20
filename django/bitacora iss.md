## ISS-00 - Entorno y proyecto Django

En este ISS preparé el entorno aislado y creé el proyecto Django `config`, sin modelos todavía. Los pasos siguen la guía de Django del curso (ISS-00 · Entorno y proyecto Django).

### Paso 1 - Verificación de requisitos

Verifiqué que tengo Python 3.12 y que el directorio del proyecto está vacío antes de crear el entorno.

``` bash
python3 --version
ls -la
```

![EVI-00-04 - Versión de Python y directorio vacío](./trazabilidad/EVI-00-04-requisitos.png)

**Retroalimentación de la evidencia:** En la captura observé la versión `[3.12.x]` impresa por `python3 --version` y el directorio sin archivos previos [o con solo los archivos de carpeta oculta].

**Conclusión y aprendizaje:** Aprendí que el ISS exige una versión concreta de Python, porque Django 5.2 y sus dependencias se prueban sobre esa versión. Verificar el requisito antes de instalar evita errores difíciles de diagnosticar más adelante.

### Paso 2 - Creación del entorno virtual e instalación de Django

Creé el entorno virtual `.venv`, lo activé, instalé Django 5.2.17 con `python -m pip` y guardé las dependencias en `requirements.txt`. Uso `python -m pip` para asegurar que la instalación va al entorno activo.

``` bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install "Django==5.2.17"
python -m pip freeze > requirements.txt
python -m django --version
```

![](trazabilidad/EVI-00-01.png)

**Retroalimentación de la evidencia:** En la captura observé el prompt con `(.venv)` activo, la instalación de Django 5.2.17 sin errores y la versión `5.2.17` impresa al final.

**Conclusión y aprendizaje:** Aprendí que `.venv` aísla las dependencias del proyecto del Python del sistema. `requirements.txt` permite reproducir el mismo entorno en otra máquina.

### Paso 3 - Creación del proyecto `config`

Generé el proyecto con la CLI de Django en el directorio actual, para que `manage.py` quede en la raíz y el paquete de configuración se llame `config`.

``` bash
django-admin startproject config .
ls config
```

![EVI-00-02 - Árbol config y manage.py generados](trazabilidad/EVI-00-02.png)

**Retroalimentación de la evidencia:** En la captura observé `manage.py` en la raíz y, dentro de `config/`, los archivos `settings.py`, `urls.py`, `wsgi.py` y h`asgi.py`.

**Conclusión y aprendizaje:** Aprendí que `startproject config .` no crea una carpeta doble `proyecto/proyecto/`. `urls.py` es el punto de entrada de todas las peticiones; en este ISS solo contiene la ruta `admin/`.

### Paso 4 - Creación del archivo `.gitignore`

Creé `.gitignore` en la raíz para excluir del control de versiones el entorno virtual, cachés, archivos de configuración local y archivos generados. Django no lo genera, así que lo creé manualmente.

``` bash
cat > .gitignore <<'EOF'
.venv/
__pycache__/
*.py[cod]
.env
db.sqlite3
*.log
.idea/
.vscode/
staticfiles/
media/
.pytest_cache/
htmlcov/
.coverage
EOF
cat .gitignore
```

![](trazabilidad/EVI-00-03.jpg)

**Retroalimentación de la evidencia:** En la captura observé el contenido del archivo impreso por `cat`, con las reglas `.venv/` y `.env` entre las líneas.

**Conclusión y aprendizaje:** Aprendí que `.gitignore` debe estar en la raíz del proyecto. Excluir `.venv/` y `.env` evita subir el entorno local y las credenciales al repositorio.

### Paso 5 - Verificación del ISS

Comprobé la versión de Django y ejecuté la verificación del sistema de Django.

``` bash
python -m django --version
python manage.py check
```

![EVI-00-05 - Verificación de Django y check sin errores](trazabilidad/EVI-00-05.png)

**Retroalimentación de la evidencia:** En la captura observé la versión `5.2.17` y el mensaje `System check identified no issues (0 silenced).`

**Conclusión y aprendizaje:** Aprendí que `manage.py check` valida la configuración del proyecto sin necesidad de tener modelos. Confirma que el entorno está listo para el ISS-01.

## ISS-01 - Settings y selección del motor

En este ISS separé la configuración en el paquete `config/settings/`, instalé los drivers de los cuatro motores de base de datos (PostgreSQL, MySQL, SQL Server y Oracle) y elegí el motor activo desde `.env` mediante `DB_ENGINE`. No escribí SQL: el ORM recibe un único alias `default` por ejecución. Las pruebas con cada motor se realizan a partir del ISS-03, cuando se aplican migraciones.

### Paso 1 - Confirmación del entorno y dependencias del sistema

Verifiqué que `python` apunta al intérprete de `.venv` y que las herramientas de compilación están instaladas para `mysqlclient`.

```bash
source .venv/bin/activate
which python
python --version
sudo apt update
sudo apt install -y build-essential pkg-config default-libmysqlclient-dev python3.14-dev
```

![EVI-01-01 - Entorno virtual activo y dependencias del sistema](trazabilidad/EVI-01-01.png)

**Retroalimentación de la evidencia:** En la captura observé el prompt con `(.venv)`, la ruta `[ruta exacta]/.venv/bin/python`, la versión `Python [3.14.x]` y la instalación de las dependencias del sistema sin errores.

**Conclusión y aprendizaje:** Aprendí que `pip` y `python` deben apuntar al mismo entorno; de lo contrario, los drivers quedan instalados fuera del proyecto y `manage.py` no los encuentra.

### Paso 2 - Instalación de los drivers de los cuatro motores

Instalé `python-dotenv` para leer `.env` y un driver por motor. Django no incluye drivers, así que sin ellos la conexión a cualquier base de datos falla al importar el backend.

```bash
python -m pip install "python-dotenv==1.2.3"
python -m pip install "psycopg[binary]==3.3.6"
python -m pip install "mysqlclient==2.3.0"
python -m pip install "mssql-django==2.0.0"
python -m pip install "oracledb==26.0.1"
python -m pip freeze > requirements.txt
cat requirements.txt
```

![EVI-01-02 - Instalación de los cuatro drivers](trazabilidad/EVI-01-02.png)

![EVI-01-03 - requirements.txt con los drivers](trazabilidad/EVI-01-03.png)

**Retroalimentación de las evidencias:** En la primera captura observé [la última línea de la instalación de `oracledb 26.0.1` sin errores]. En la segunda observé [las versiones registradas: python-dotenv 1.2.3, psycopg 3.3.6, mysqlclient 2.3.0, mssql-django 2.0.0 y oracledb 26.0.1].

**Conclusión y aprendizaje:** Aprendí que cada motor necesita su propio driver. `psycopg` sirve a PostgreSQL, `mysqlclient` a MySQL, `mssql-django` registra el motor `mssql` y necesita pyodbc y el driver ODBC del sistema para conectarse, y `oracledb` en modo thin conecta a Oracle sin Instant Client. `requirements.txt` deja constancia de las versiones exactas para reproducir el entorno.

### Paso 3 - Conversión de settings.py en paquete

`startproject` generó `config/settings.py`. Lo eliminé y creé la carpeta `config/settings/`, que se convierte en el único punto de configuración.

```bash
rm config/settings.py
mkdir -p config/settings
ls config
```

![EVI-01-04 - Carpeta config tras reemplazar settings.py](./trazabilidad/EVI-01-04.png)
**Retroalimentación de la evidencia:** En la captura observé [el listado de `config/` con `settings/` y sin `settings.py`].

**Conclusión y aprendizaje:** Aprendí que la configuración debe vivir en un solo lugar. Tener `settings.py` y un paquete `settings/` a la vez generaría dudas sobre cuál se carga.

### Paso 4 - Plantilla `.env.example` y archivo `.env`

Creé `.env.example` como plantilla sin secretos, con las variables de los cuatro motores, y copié la plantilla a `.env`. `.env` contiene credenciales, así que debe estar en `.gitignore`.

```bash
cat > .env.example <<'EOF'
# Copie este archivo a .env y complete los valores.
# .env no se versiona.

DJANGO_SECRET_KEY=
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,testserver

# Motor activo. Uno solo por ejecución: postgresql | mysql | mssql | oracle
DB_ENGINE=postgresql

POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432

MYSQL_DB=
MYSQL_USER=
MYSQL_PASSWORD=
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306

MSSQL_DB=
MSSQL_USER=
MSSQL_PASSWORD=
MSSQL_HOST=127.0.0.1
MSSQL_PORT=1433

ORACLE_DB=
ORACLE_USER=
ORACLE_PASSWORD=
ORACLE_HOST=127.0.0.1
ORACLE_PORT=1521
ORACLE_SERVICE_NAME=

CORS_ALLOW_ALL_ORIGINS=True
EOF

cp .env.example .env
```

Para generar la clave secreta usé:

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

y la pegué en `DJANGO_SECRET_KEY` dentro de `.env`.

![EVI-01-05 - .env.example y .env](trazabilidad/EVI-01-05.png)
**Retroalimentación de la evidencia:** En la captura observé [los dos archivos en el listado] y el contenido de `.env.example`, que solo tiene nombres de variables y valores vacíos. Los valores reales de `.env` no aparecen en la captura.

**Conclusión y aprendizaje:** Aprendí a separar la plantilla, que sí se versiona, del archivo con credenciales reales, que no se versiona. Así el repositorio documenta qué variables se necesitan sin exponer contraseñas.

### Paso 5 - Selector de motor en `config/database.py`

Creé `config/database.py`. No es una aplicación: traduce `DB_ENGINE` a un único diccionario `DATABASES["default"]`. Cada motor exige sus variables y define su `ENGINE`. Para Oracle armo el DSN con `SERVICE_NAME` y dejo `PORT` vacío porque Django lo toma del DSN.

```bash
cat > config/database.py <<'EOF'
"""Selección del motor de base de datos a partir del entorno.

Un solo alias, default, queda activo en cada ejecución.
"""

from django.core.exceptions import ImproperlyConfigured

ALLOWED_ENGINES = ("postgresql", "mysql", "mssql", "oracle")


def database_from_environ(env):
    engine = str(env.get("DB_ENGINE", "postgresql")).strip().lower()
    if engine not in ALLOWED_ENGINES:
        allowed = ", ".join(ALLOWED_ENGINES)
        raise ImproperlyConfigured(
            f"DB_ENGINE='{engine}' no es válido. Valores permitidos: {allowed}."
        )
    builders = {
        "postgresql": _postgresql,
        "mysql": _mysql,
        "mssql": _mssql,
        "oracle": _oracle,
    }
    return {"default": builders[engine](env)}


def _required(env, key):
    value = env.get(key)
    if value is None or str(value).strip() == "":
        raise ImproperlyConfigured(
            f"Falta la variable de entorno {key} para DB_ENGINE={env.get('DB_ENGINE')}."
        )
    return str(value).strip()


def _postgresql(env):
    return {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": _required(env, "POSTGRES_DB"),
        "USER": _required(env, "POSTGRES_USER"),
        "PASSWORD": _required(env, "POSTGRES_PASSWORD"),
        "HOST": _required(env, "POSTGRES_HOST"),
        "PORT": _required(env, "POSTGRES_PORT"),
    }


def _mysql(env):
    return {
        "ENGINE": "django.db.backends.mysql",
        "NAME": _required(env, "MYSQL_DB"),
        "USER": _required(env, "MYSQL_USER"),
        "PASSWORD": _required(env, "MYSQL_PASSWORD"),
        "HOST": _required(env, "MYSQL_HOST"),
        "PORT": _required(env, "MYSQL_PORT"),
        "OPTIONS": {"charset": "utf8mb4"},
    }


def _mssql(env):
    return {
        "ENGINE": "mssql",
        "NAME": _required(env, "MSSQL_DB"),
        "USER": _required(env, "MSSQL_USER"),
        "PASSWORD": _required(env, "MSSQL_PASSWORD"),
        "HOST": _required(env, "MSSQL_HOST"),
        "PORT": _required(env, "MSSQL_PORT"),
        "OPTIONS": {
            "driver": "ODBC Driver 18 for SQL Server",
            "extra_params": "TrustServerCertificate=yes",
        },
    }


def _oracle(env):
    host = _required(env, "ORACLE_HOST")
    port = _required(env, "ORACLE_PORT")
    service = _required(env, "ORACLE_SERVICE_NAME")
    dsn = (
        f"(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST={host})(PORT={port}))"
        f"(CONNECT_DATA=(SERVICE_NAME={service})))"
    )
    return {
        "ENGINE": "django.db.backends.oracle",
        "NAME": dsn,
        "USER": _required(env, "ORACLE_USER"),
        "PASSWORD": _required(env, "ORACLE_PASSWORD"),
        "HOST": host,
        "PORT": "",
    }
EOF
```

![EVI-01-06 - config/database.py](trazabilidad/EVI-01-06.png)

**Retroalimentación de la evidencia:** En la captura observé [la función `database_from_environ` y la lista `ALLOWED_ENGINES` con los cuatro motores].

**Conclusión y aprendizaje:** Aprendí que el ORM no conoce el motor real: solo ve el alias `default`. La elección ocurre antes, con una función que puedo probar sin conectarme a ningún servidor.

### Paso 6 - Configuración principal en `config/settings/__init__.py`

Este archivo reemplaza al `settings.py` generado. Carga `.env` antes de leer la clave secreta y la base de datos, y define idioma, zona horaria y el modelo de llave primaria. Las aplicaciones de negocio y el usuario personalizado se agregan en los ISS siguientes.

```bash
cat > config/settings/__init__.py <<'EOF'
"""Configuración del proyecto PuntoStock.

El paquete sustituye al settings.py generado por startproject.
DJANGO_SETTINGS_MODULE sigue siendo config.settings.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from django.core.exceptions import ImproperlyConfigured

from config.database import database_from_environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "").strip()
if not SECRET_KEY:
    raise ImproperlyConfigured("Defina DJANGO_SECRET_KEY en el archivo .env.")

DEBUG = os.environ.get("DJANGO_DEBUG", "False").strip().lower() in {"1", "true", "yes", "on"}

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    if host.strip()
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

DATABASES = database_from_environ(os.environ)

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "es"
TIME_ZONE = "America/Bogota"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
EOF
```

![EVI-01-07 - config/settings/__init__.py](trazabilidad/EVI-01-07.png)

**Retroalimentación de la evidencia:** En la captura observé [los imports de `dotenv` y `database_from_environ`, y la línea `DATABASES = database_from_environ(os.environ)`].

**Conclusión y aprendizaje:** Aprendí que el orden importa: `load_dotenv` debe ejecutarse antes de leer `SECRET_KEY` y `DATABASES`. Si no, Django arranca con valores vacíos.

### Paso 7 - Intérprete del proyecto en `config/project_python.py`

Este módulo usa solo la biblioteca estándar. Si `manage.py` arranca con el Python del sistema, vuelve a lanzar el mismo comando con `.venv/bin/python`, donde están Django y los drivers.

```bash
cat > config/project_python.py <<'EOF'
"""Intérprete del proyecto.

Los paquetes se instalan dentro de .venv. Si python3 manage.py usa el
Python del sistema, no ve esos paquetes. use_project_python() vuelve a
lanzar el mismo comando con .venv/bin/python.
"""

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def use_project_python():
    """Reejecuta el proceso con el Python de .venv si aún no es ese intérprete."""
    venv_root = PROJECT_ROOT / ".venv"
    venv_python = venv_root / "bin" / "python"
    if not venv_python.is_file():
        return
    try:
        if Path(sys.prefix).resolve() == venv_root.resolve():
            return
    except OSError:
        return
    os.execv(venv_python, [str(venv_python), *sys.argv])
EOF
```

![EVI-01-08 - config/project_python.py](trazabilidad/EVI-01-08.png)

**Retroalimentación de la evidencia:** En la captura observé [el archivo creado y la función `use_project_python`].

**Conclusión y aprendizaje:** Aprendí que `sys.prefix` identifica el entorno activo. Por eso comparo esa ruta y no la del ejecutable, que en `.venv` es un enlace al Python del sistema.

### Paso 8 - Reescritura de `manage.py`, `wsgi.py` y `asgi.py`

Reescribí estos tres archivos completos con `cat`, para que carguen `.env` y usen el intérprete del proyecto antes de que Django lea la configuración. Los archivos generados por `startproject` se sustituyeron; no se editaron línea por línea.

**`manage.py`**

```bash
cat > manage.py <<'EOF'
#!/usr/bin/env python
"""Run administrative tasks."""

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from config.project_python import use_project_python

use_project_python()

import os

from dotenv import load_dotenv


def main():
    """Run administrative tasks."""
    load_dotenv()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "No se pudo importar Django. ¿Está activado el entorno virtual?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
EOF
```

**`config/wsgi.py`**

```bash
cat > config/wsgi.py <<'EOF'
import os

from dotenv import load_dotenv

from django.core.wsgi import get_wsgi_application

load_dotenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()
EOF
```

**`config/asgi.py`**

```bash
cat > config/asgi.py <<'EOF'
import os

from dotenv import load_dotenv

from django.core.asgi import get_asgi_application

load_dotenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_asgi_application()
EOF
```

![EVI-01-09 - manage.py, wsgi.py y asgi.py reescritos](trazabilidad/EVI-01-09.png)

**Retroalimentación de la evidencia:** En la captura observé [`use_project_python()` y `load_dotenv()` en `manage.py`, y `load_dotenv()` antes de `get_wsgi_application()` y `get_asgi_application()`].

**Conclusión y aprendizaje:** Aprendí que `load_dotenv()` debe ejecutarse antes de que Django lea la configuración. Reescribir los archivos completos evita dejar restos de código generado que no coincidan con el resto del proyecto.

### Paso 9 - Verificación del ISS

Ejecuté la verificación del sistema de Django:

```bash
python manage.py check
```

![EVI-01-10 - check sin errores](trazabilidad/EVI-01-10.png)
**Retroalimentación de la evidencia:** En la captura observé `System check identified no issues (0 silenced).`

Como el test automatizado de selección de motor llega en ISS-03, comprobé los errores esperados con dos ejecuciones. Primero, un motor inválido:

```bash
DB_ENGINE=motor_falso python manage.py check
```

![EVI-01-11 - Error por motor inválido](trazabilidad/EVI-01-11.png)
Después, una variable obligatoria vacía. La variable del entorno tiene prioridad sobre `.env`, así que la vacía reemplaza el valor del archivo:

```bash
DB_ENGINE=mysql MYSQL_DB= python manage.py check
```

![EVI-01-12 - Error por variable vacía](trazabilidad/EVI-01-12.png)
**Retroalimentación de las evidencias:** En la primera captura observé el `ImproperlyConfigured` con el mensaje `DB_ENGINE='motor_falso' no es válido`. En la segunda observé el mensaje `Falta la variable de entorno MYSQL_DB`.

**Conclusión y aprendizaje:** Aprendí que la configuración falla al arrancar, antes de intentar conectarse a una base de datos. Así el error aparece de inmediato y no durante una petición.

### Criterios de aceptación y GATE

| AC | Criterio | Verificación | Evidencia | Resultado |
|:---|:---|:---|:---|:---|
| AC-01-01 | Cada motor produce su `ENGINE` documentado | Inspección de `database.py`; prueba automatizada desde ISS-03 | EVI-01-06 | [PASS ] |
| AC-01-02 | Un motor desconocido falla con `ImproperlyConfigured` | `DB_ENGINE=motor_falso python manage.py check` | EVI-01-11 | [PASS] |
| AC-01-03 | Una variable obligatoria vacía falla antes de conectar | `DB_ENGINE=mysql MYSQL_DB= python manage.py check` | EVI-01-12 | [PASS] |
| AC-01-04 | El DSN de Oracle contiene `SERVICE_NAME` | Inspección de `_oracle` en `database.py` | EVI-01-06 | [PASS] |

El GATE del ISS-01 queda cumplido cuando `python manage.py check` pasa con el motor activo y las dos pruebas negativas producen el error esperado.

## ISS-02 - Apps client, product y sale

En este ISS creé las tres aplicaciones de negocio base (`client`, `product` y `sale`) dentro del paquete `apps/`, con su `AppConfig` apuntando a `apps.<nombre>` y su etiqueta corta, y las registré en `INSTALLED_APPS`. Todavía no escribí modelos ni ejecuté migraciones: eso corresponde a los ISS siguientes, después del usuario personalizado del ISS-03.

### Paso 1 - Creación de las aplicaciones con la CLI

Creé los directorios de destino y generé las tres aplicaciones con `startapp`. `startapp` exige que el directorio exista antes de ejecutarse.

```bash

mkdir -p apps/client apps/product apps/sale
python manage.py startapp client apps/client
python manage.py startapp product apps/product
python manage.py startapp sale apps/sale
ls apps
```

Después creé `apps/__init__.py` vacío para que `apps` sea un paquete:

```bash
mkdir -p apps
cat > apps/__init__.py <<'EOF'
EOF
```

![EVI-02-02 - Estructura de apps generada con startapp](trazabilidad/EVI-02-02.png)

**Retroalimentación de la evidencia:** En la captura observé [los directorios `client`, `product` y `sale` dentro de `apps/`, con `__init__.py`, `apps.py`, `models.py`, `admin.py` y `views.py`].

**Conclusión y aprendizaje:** Aprendí que `startapp` genera el esqueleto de cada aplicación. `urls.py` no aparece porque todavía no hay endpoints.

### Paso 2 - Parche de `name` y `label` en cada `apps.py`

`startapp` genera `name = "client"`, pero como las apps viven dentro de `apps/`, Django necesita el nombre completo del paquete. Reemplacé esa línea en cada archivo y agregué `label` para que las migraciones usen solo el nombre corto. El nombre de la clase no cambia.

```text
ARCHIVO: apps/client/apps.py

UBICAR:
    name = "client"

REEMPLAZAR POR:
    name = "apps.client"
    label = "client"
```

El mismo parche se aplica a `apps/product/apps.py` (`name = "apps.product"`, `label = "product"`) y a `apps/sale/apps.py` (`name = "apps.sale"`, `label = "sale"`).

![EVI-02-03 - apps.py de client, product y sale](./trazabilidad/EVI-02-03.png)
**Retroalimentación de la evidencia:** En la captura observé `name = "apps.<nombre>"` y `label = "<nombre>"` en cada `apps.py`.

**Conclusión y aprendizaje:** Aprendí que, sin `name = "apps.client"`, Django busca `client` en la raíz del proyecto y no encuentra la aplicación.

### Paso 3 - Registro en INSTALLED_APPS

En `config/settings/__init__.py` agregué las tres aplicaciones al final de `INSTALLED_APPS`, sin tocar las de Django. No agregué `security` todavía: esa app llega en el ISS-03.

```text
ARCHIVO: config/settings/__init__.py

DEBAJO DE:
    "django.contrib.staticfiles",

AGREGAR:
    "apps.client.apps.ClientConfig",
    "apps.product.apps.ProductConfig",
    "apps.sale.apps.SaleConfig",
```

![EVI-02-04 - INSTALLED_APPS con las tres aplicaciones](trazabilidad/EVI-02-04.png)

**Retroalimentación de la evidencia:** En la captura observé las tres entradas `apps.client.apps.ClientConfig`, `apps.product.apps.ProductConfig` y `apps.sale.apps.SaleConfig` debajo de `django.contrib.staticfiles`.

**Conclusión y aprendizaje:** Aprendí que crear la carpeta de una aplicación no basta: Django solo carga las aplicaciones listadas en `INSTALLED_APPS`.

### Paso 4 - Verificación del ISS

```bash
python manage.py check
```

![EVI-02-01 - check sin errores con las tres apps registradas](trazabilidad/EVI-02-01.png)
**Retroalimentación de la evidencia:** En la captura observé `System check identified no issues (0 silenced).`

**Conclusión y aprendizaje:** Aprendí que `check` detecta errores de registro, como una ruta de `name` incorrecta, antes de que se intente crear cualquier tabla.

### Criterios de aceptación y GATE

| AC | Criterio | Verificación | Evidencia | Resultado |
|:---|:---|:---|:---|:---|
| AC-02-01 | Las tres apps fueron creadas con `startapp` | Árbol de `apps/` | EVI-02-02 | [PASS] |
| AC-02-02 | `check` no reporta apps mal registradas | `python manage.py check` | EVI-02-01 | [PASS] |
| AC-02-03 | En este ISS no hay modelos de negocio | Revisión de `models.py` (vacíos) | EVI-02-02 | [PASS] |

El GATE del ISS-02 queda cumplido cuando las tres apps existen, están registradas y `check` pasa sin errores.

## ISS-03 - Custom User antes de la primera migración

En este ISS definí el usuario del proyecto sobre `django.contrib.auth` con `AbstractUser`, y fijé `AUTH_USER_MODEL = "security.User"` antes de ejecutar cualquier migración. Así Django crea la tabla de usuarios con el modelo propio desde el principio. También escribí las pruebas de selección de motor que quedaron pendientes en el ISS-01.

### Paso 1 - Paquete `apps/common` y `RecordStatus`

`apps/common` no es una aplicación: no se registra en `INSTALLED_APPS` ni se crea con `startapp`. Contiene `RecordStatus`, que usa el usuario y, desde el ISS-04, el negocio.

```bash
mkdir -p apps/common
cat > apps/common/__init__.py <<'EOF'
EOF
cat > apps/common/status.py <<'EOF'
from django.db import models


class RecordStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
EOF
```

![EVI-03-01 - apps/common/status.py](./trazabilidad/EVI-03-01.png)

**Retroalimentación de la evidencia:** En la captura observé [el contenido de `status.py` con las clases `ACTIVE` e `INACTIVE`].

**Conclusión y aprendizaje:** Aprendí que `TextChoices` guarda el valor en la base de datos y el nombre legible en el formulario, así `status` tiene valores controlados desde el principio.

### Paso 2 - Aplicación `security`

Creé la aplicación con la CLI y reescribí `apps.py` para que su `name` sea `apps.security`, como en las demás apps del ISS-02.

```bash
mkdir -p apps/security
python manage.py startapp security apps/security
cat > apps/security/apps.py <<'EOF'
from django.apps import AppConfig


class SecurityConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.security"
    label = "security"
EOF
```
![EVI-03-02 - apps.py de security](trazabilidad/EVI-03-02.png)
**Retroalimentación de la evidencia:** En la captura observé [`name = "apps.security"` y `label = "security"` en `apps.py`].

**Conclusión y aprendizaje:** Aprendí que el `label` es el nombre que usa `AUTH_USER_MODEL` (`security.User`), así que debe coincidir.

### Paso 3 - Modelo `User`

Escribí `apps/security/models.py` con `StoreUserManager` y `User`. `User` hereda de `AbstractUser`, que ya trae el hash de contraseñas, los validadores, `set_password()`, `check_password()` y el admin. Agregué `email` único, `status`, las marcas de tiempo y una restricción de base de datos sobre `status`.

```bash
cat > apps/security/models.py <<'EOF'
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from apps.common.status import RecordStatus


class StoreUserManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("status", RecordStatus.INACTIVE)
        return super().create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("status", RecordStatus.ACTIVE)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField("correo electrónico", max_length=150, unique=True)
    status = models.CharField(
        max_length=8,
        choices=RecordStatus.choices,
        default=RecordStatus.INACTIVE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = StoreUserManager()

    class Meta:
        db_table = "users"
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(status__in=RecordStatus.values),
                name="users_status_valid",
            )
        ]

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.strip().lower()
        self.is_active = self.status == RecordStatus.ACTIVE
        super().save(*args, **kwargs)
EOF
```

![EVI-03-03 - models.py con User](./trazabilidad/EVI-03-03.png)
**Retroalimentación de la evidencia:** En la captura observé [la clase `User(AbstractUser)`, `email` con `unique=True` y el `save()` que sincroniza `is_active` con `status`].

**Conclusión y aprendizaje:** Aprendí que `status` manda sobre `is_active`. Mantengo `is_active` porque Django y las autenticaciones lo consultan para decidir si una cuenta puede entrar. `create_superuser` fuerza `status = active` para que `save()` no desactive al superusuario.

### Paso 4 - Settings: registro de la app y `AUTH_USER_MODEL`

Agregué `apps.security` encima de las apps de negocio en `INSTALLED_APPS` y declaré `AUTH_USER_MODEL` después de `DATABASES`.

```text
ARCHIVO: config/settings/__init__.py

ENCIMA DE:
    "apps.client.apps.ClientConfig",

AGREGAR:
    "apps.security.apps.SecurityConfig",

DEBAJO DE:
DATABASES = database_from_environ(os.environ)

AGREGAR:

AUTH_USER_MODEL = "security.User"
```

![EVI-03-04 - INSTALLED_APPS y AUTH_USER_MODEL](./trazabilidad/EVI-03-04.png)
**Retroalimentación de la evidencia:** En la captura observé [`apps.security.apps.SecurityConfig` en `INSTALLED_APPS` y `AUTH_USER_MODEL = "security.User"` debajo de `DATABASES`].

**Conclusión y aprendizaje:** Aprendí que `AUTH_USER_MODEL` debe declararse antes de la primera migración. Si se cambia después, Django no puede reemplazar la tabla de usuarios sin rehacer la base.

### Paso 5 - Pruebas de selección de motor

Escribí `apps/security/tests.py` con las pruebas de selección de motor que el ISS-01 dejó pendientes. Usan `SimpleTestCase`, así que no abren ninguna conexión.

```bash
cat > apps/security/tests.py <<'EOF'
from django.core.exceptions import ImproperlyConfigured
from django.test import SimpleTestCase

from config.database import database_from_environ


class DatabaseSelectionTests(SimpleTestCase):
    def _env(self, engine):
        return {
            "DB_ENGINE": engine,
            "POSTGRES_DB": "storelab",
            "POSTGRES_USER": "storelab",
            "POSTGRES_PASSWORD": "storelab",
            "POSTGRES_HOST": "127.0.0.1",
            "POSTGRES_PORT": "5432",
            "MYSQL_DB": "storelab",
            "MYSQL_USER": "storelab",
            "MYSQL_PASSWORD": "storelab",
            "MYSQL_HOST": "127.0.0.1",
            "MYSQL_PORT": "3306",
            "MSSQL_DB": "storelab",
            "MSSQL_USER": "storelab",
            "MSSQL_PASSWORD": "storelab",
            "MSSQL_HOST": "127.0.0.1",
            "MSSQL_PORT": "1433",
            "ORACLE_DB": "storelab",
            "ORACLE_USER": "storelab",
            "ORACLE_PASSWORD": "storelab",
            "ORACLE_HOST": "127.0.0.1",
            "ORACLE_PORT": "1521",
            "ORACLE_SERVICE_NAME": "FREEPDB1",
        }

    def test_postgresql_engine(self):
        config = database_from_environ(self._env("postgresql"))
        self.assertEqual(config["default"]["ENGINE"], "django.db.backends.postgresql")

    def test_mysql_engine(self):
        config = database_from_environ(self._env("mysql"))
        self.assertEqual(config["default"]["ENGINE"], "django.db.backends.mysql")
        self.assertEqual(config["default"]["OPTIONS"]["charset"], "utf8mb4")

    def test_mssql_engine(self):
        config = database_from_environ(self._env("mssql"))
        self.assertEqual(config["default"]["ENGINE"], "mssql")

    def test_oracle_uses_service_name(self):
        config = database_from_environ(self._env("oracle"))
        self.assertIn("SERVICE_NAME=FREEPDB1", config["default"]["NAME"])
        self.assertEqual(config["default"]["PORT"], "")

    def test_invalid_engine(self):
        with self.assertRaises(ImproperlyConfigured):
            database_from_environ({"DB_ENGINE": "sqlite"})

    def test_missing_variable(self):
        env = self._env("postgresql")
        env["POSTGRES_DB"] = ""
        with self.assertRaises(ImproperlyConfigured):
            database_from_environ(env)
EOF
```
![EVI-03-05](./trazabilidad/EVI-03-05.png)
**Retroalimentación de la evidencia:** Aún no hay captura de esta prueba; la EVI-03-02 corresponde a la ejecución del paso 6.

**Conclusión y aprendizaje:** Aprendí que una prueba de configuración puede verificar cada motor sin abrir una conexión. Por eso `SimpleTestCase` basta.

### Paso 6 - Migración inicial y ejecución de pruebas

Generé la migración con la CLI, la apliqué y ejecuté las pruebas de selección de motor.

```bash
python manage.py makemigrations security
python manage.py migrate
python manage.py test apps.security.tests.DatabaseSelectionTests
```

![EVI-03-06 - makemigrations y migrate](./trazabilidad/EVI-03-06.png)

![EVI-03-07 - Pruebas de selección de motor en PASS](./trazabilidad/EVI-03-07.png)
**Retroalimentación de las evidencias:** En la primera captura observé [`Create model User` y la aplicación de `security.0001_initial`]. En la segunda observé [`Ran 6 tests` y `OK`].

**Conclusión y aprendizaje:** Aprendí que la migración la genera Django a partir del modelo, así que el archivo refleja `AUTH_USER_MODEL`. Si hubiera migrado antes de fijar `AUTH_USER_MODEL`, esta tabla no habría sido la del usuario personalizado.

### Criterios de aceptación y GATE

| AC | Criterio | Verificación | Evidencia | Resultado |
|:---|:---|:---|:---|:---|
| AC-03-01 | `AUTH_USER_MODEL` apunta a `security.User` antes de migrar | Inspección de settings y orden de comandos | EVI-03-03, EVI-03-04 | [PASS] |
| AC-03-02 | `Client` no tiene campo de contraseña | Revisión de `models.py` | EVI-03-02 | [PASS] |
| AC-03-03 | Un usuario `inactive` no puede iniciar sesión | Prueba de login (pendiente) | — | [PENDIENTE] |
| AC-03-04 | Una clave incorrecta no autentica | `check_password` (pendiente) | — | [PENDIENTE] |

Los criterios AC-03-03 y AC-03-04 requieren pruebas de autenticación que la guía del ISS-03 menciona pero no incluye. Se verifican cuando se implemente el login.

El GATE del ISS-03 queda cumplido cuando AC-03-01 y AC-03-02 están en PASS y las pruebas de selección de motor pasan.

## ISS-04 - Modelo Client (Cliente de PuntoStock)

En este ISS creé el modelo base con marcas de tiempo y el modelo `Client`, que corresponde a la entidad Cliente de PuntoStock: `tipo_documento`, `numero_documento` único, `nombre`, `telefono`, `email` e `is_active`.

### Paso 1 - Modelo base con marcas de tiempo

`TimeStampedModel` agrega `created_at` y `updated_at`. Es abstracto, así que no crea tabla.

```bash
cat > apps/common/models.py <<'EOF'
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
EOF
```

![EVI-04-01 - apps/common/models.py](./trazabilidad/EVI-04-01.png)
**Retroalimentación de la evidencia:** En la captura observé [`TimeStampedModel` con `created_at`, `updated_at` y `abstract = True`].

**Conclusión y aprendizaje:** Aprendí que un modelo abstracto sirve para repetir campos comunes sin crear una tabla propia.

### Paso 2 - Modelo `Client`

`startapp` generó `apps/client/models.py` vacío. Lo reescribí completo con los campos de la especificación.

```bash
cat > apps/client/models.py <<'EOF'
from django.core.validators import MinLengthValidator
from django.db import models

from apps.common.models import TimeStampedModel


class Client(TimeStampedModel):
    class DocumentType(models.TextChoices):
        CC = "CC", "Cédula de ciudadanía"
        NIT = "NIT", "NIT"
        CE = "CE", "Cédula de extranjería"
        PASAPORTE = "PASAPORTE", "Pasaporte"

    tipo_documento = models.CharField(max_length=10, choices=DocumentType.choices)
    numero_documento = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=150, validators=[MinLengthValidator(2)])
    telefono = models.CharField(max_length=30, blank=True)
    email = models.EmailField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "clientes"
        verbose_name = "cliente"
        verbose_name_plural = "clientes"
        ordering = ["nombre", "id"]

    def __str__(self):
        return f"{self.nombre} ({self.numero_documento})"

    def save(self, *args, **kwargs):
        self.numero_documento = self.numero_documento.strip()
        if self.email:
            self.email = self.email.strip().lower()
        super().save(*args, **kwargs)
EOF
```

![EVI-04-02 - apps/client/models.py](./trazabilidad/EVI-04-02.png)
**Retroalimentación de la evidencia:** En la captura observé [los campos de la especificación, `numero_documento` con `unique=True` y `db_table = "clientes"`].

**Conclusión y aprendizaje:** Aprendí que `choices` restringe los valores permitidos en Django y que la unicidad de `numero_documento` la impone la base de datos.

### Paso 3 - Migración de `client`

```bash
python manage.py makemigrations client
python manage.py migrate client
```

![EVI-04-03 - makemigrations y migrate de client](./trazabilidad/EVI-04-03.png)

**Retroalimentación de la evidencia:** En la captura observé [`Create model Client` y `Applying client.0001_initial... OK`].

**Conclusión y aprendizaje:** Aprendí que la migración la genera Django a partir del modelo, así que el archivo refleja los campos y el nombre de tabla definidos.

### Paso 4 - Verificación en el shell

```bash
python manage.py shell
```

Bloque 1: crear un cliente sin enviar `is_active`.

```python
from django.db import IntegrityError
from apps.client.models import Client
c = Client.objects.create(tipo_documento="CC", numero_documento="1001", nombre="Ana", email="ANA@EJEMPLO.COM")
print(c.is_active, c.created_at, c.email)
```

Bloque 2: intentar crear otro cliente con el mismo número de documento.

```python
try:
    Client.objects.create(tipo_documento="CC", numero_documento="1001", nombre="Luis")
except IntegrityError as e:
    print("rechazado:", e)
```

Escribe `exit()` al terminar.

![EVI-04-04 - Shell con is_active, timestamps y documento duplicado](./trazabilidad/EVI-04-04.png)
**Retroalimentación de la evidencia:** En la captura observé [`True`, la fecha de creación y `ana@ejemplo.com` en el bloque 1; `rechazado:` con la violación de unicidad de `numero_documento` en el bloque 2].

**Conclusión y aprendizaje:** Aprendí que `is_active` toma `True` por defecto y que `save()` normaliza el email antes de guardarlo.

### Criterios de aceptación y GATE

| AC | Criterio | Verificación | Evidencia | Resultado |
|:---|:---|:---|:---|:---|
| AC-04-01 | La tabla física es `clientes` | Migración aplicada | EVI-04-03 | [PASS] |
| AC-04-02 | `numero_documento` es único | Bloque 2 del shell | EVI-04-04 | [PASS] |
| AC-04-03 | `is_active` vale `True` por defecto y `created_at` se genera | Bloque 1 del shell | EVI-04-04 | [PASS] |
| AC-04-04 | `tipo_documento` acepta solo los valores de la especificación | Revisión de `choices` | EVI-04-02 | [PASS] |

El GATE del ISS-04 queda cumplido cuando AC-04-01 a AC-04-03 están en PASS.

## ISS-05 - Modelo Product (Producto de PuntoStock)

En este ISS creé el modelo `Product`, que corresponde a la entidad Producto de PuntoStock: `sku` único, `nombre`, `descripcion`, `precio` no negativo e `is_active`. No incluí `ProductType` ni `stock`, porque la especificación no los define. El stock se modela en la entidad Inventario, que llega en un ISS posterior.

### Paso 1 - Modelo `Product`

`startapp` generó `apps/product/models.py` vacío. Lo reescribí completo.

```bash
cat > apps/product/models.py <<'EOF'
from decimal import Decimal

from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models

from apps.common.models import TimeStampedModel


class Product(TimeStampedModel):
    sku = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=120, validators=[MinLengthValidator(2)])
    descripcion = models.CharField(max_length=255, blank=True)
    precio = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0"))],
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "productos"
        verbose_name = "producto"
        verbose_name_plural = "productos"
        ordering = ["nombre", "id"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(precio__gte=0),
                name="producto_precio_no_negativo",
            ),
        ]

    def __str__(self):
        return f"{self.sku} - {self.nombre}"

    def save(self, *args, **kwargs):
        self.sku = self.sku.strip().upper()
        super().save(*args, **kwargs)
EOF
```

![EVI-05-01 - apps/product/models.py](./trazabilidad/EVI-05-01.png)

**Retroalimentación de la evidencia:** En la captura observé [el campo `sku` con `unique=True`, `precio` con `MinValueValidator` y la restricción `producto_precio_no_negativo`].

**Conclusión y aprendizaje:** Aprendí que la validación de Python protege los formularios, y la `CheckConstraint` impide precios negativos aunque alguien escriba directo en la base.

### Paso 2 - Migración de `product`

```bash
python manage.py makemigrations product
python manage.py migrate product
```

![EVI-05-02 - makemigrations y migrate de product](./trazabilidad/EVI-05-02.png)

**Retroalimentación de la evidencia:** En la captura observé [`Create model Product` y `Applying product.0001_initial... OK`].

**Conclusión y aprendizaje:** Aprendí que el nombre de la tabla `productos` queda definido en `Meta`, no en el nombre de la clase.

### Paso 3 - Verificación en el shell

```bash
python manage.py shell
```

Bloque 1: crear un producto sin enviar `is_active` y con el SKU en minúsculas.

```python
from django.db import IntegrityError
from apps.product.models import Product
p = Product.objects.create(sku="agua-600", nombre="Agua 600ml", precio=1500)
print(p.sku, p.is_active)
```

Bloque 2: intentar crear otro producto con el mismo SKU.

```python
try:
    Product.objects.create(sku="AGUA-600", nombre="Agua repetida", precio=1500)
except IntegrityError as e:
    print("sku duplicado:", e)
```

Bloque 3: intentar crear un producto con precio negativo.

```python
try:
    Product.objects.create(sku="JUGO-1", nombre="Jugo", precio=-5)
except IntegrityError as e:
    print("precio negativo:", e)
```

Escribe `exit()` al terminar.

![EVI-05-03 - Shell con SKU normalizado, duplicado y precio negativo](./trazabilidad/EVI-05-03.png)
**Retroalimentación de la evidencia:** En la captura observé [`AGUA-600 True` en el bloque 1, `sku duplicado:` en el bloque 2 y `precio negativo:` en el bloque 3].

**Conclusión y aprendizaje:** Aprendí que `save()` normaliza el SKU, que la unicidad y la restricción de precio las aplica la base de datos.

Si repites la prueba, borra primero los registros de prueba con `Product.objects.all().delete()`.

### Criterios de aceptación y GATE

| AC | Criterio | Verificación | Evidencia | Resultado |
|:---|:---|:---|:---|:---|
| AC-05-01 | La tabla física es `productos` | Migración aplicada | EVI-05-02 | [PASS] |
| AC-05-02 | `sku` es único y se guarda en mayúsculas | Bloques 1 y 2 del shell | EVI-05-03 | [PASS] |
| AC-05-03 | `precio` no admite valores negativos | Bloque 3 del shell | EVI-05-03 | [PASS] |
| AC-05-04 | `is_active` vale `True` por defecto | Bloque 1 del shell | EVI-05-03 | [PASS] |

El GATE del ISS-05 queda cumplido cuando AC-05-01 a AC-05-03 están en PASS.

