# Informe de Despliegue: Infraestructura de Bases de Datos en WSL con Docker (PuntoStock)

En este documento detallo el proceso técnico que seguí para estructurar y levantar los motores de bases de datos mediante contenedores en mi entorno local. La infraestructura está diseñada para soportar PuntoStock, un sistema que comercializa productos de consumo y requiere consolidar de forma eficiente compras, inventarios, ventas y devoluciones[cite: 2]. El entorno integra MySQL, PostgreSQL, SQL Server y Oracle XE, organizados bajo el directorio `~/ia-lab/services/motores-bd/`.

---

## 1. Verificación del Entorno y Estructura de Directorios

Antes de configurar los servicios, aseguré que el daemon de Docker estuviera activo en mi distribución sobre WSL.

```bash
sudo systemctl is-active docker
docker compose version
```
![alt text](imagenes/image-21.png)


## 2.Creación de directorios y estructura
A continuación, construí el árbol de directorios necesario para separar las configuraciones (services) de la persistencia de datos (data) de los cuatro motores.

```bash
mkdir -p ~/ia-lab/services/motores-bd/{mysql,postgres,mssql,oracle}
mkdir -p ~/ia-lab/data/{mysql,postgres,mssql,oracle}
tree ~/ia-lab/
```
La estructura obtenida es:

~/ia-lab/
├── services/
│   └── motores-bd/
│       ├── mysql/
│       ├── postgres/
│       ├── mssql/
│       └── oracle/
└── data/
    ├── mysql/
    ├── postgres/
    ├── mssql/
    └── oracle


![alt text](/imagenes/image.png)


## 3. Creación de la red Docker compartida
Para garantizar que todos los contenedores se comuniquen bajo el mismo segmento, creé la red compartida

```bash
docker network inspect ia-lab-network >/dev/null 2>&1 || docker network create ia-lab-network
docker network ls | grep ia-lab
```

![alt text](/imagenes/image3.png)

## 4. Implementación de MySQL 8.0

### 4.1 Creación del archivo docker-compose.yml

Creé el archivo docker-compose.yml utilizando la imagen mysql:8.0. Modifiqué el mapeo al puerto 3307:3306 para evitar conflictos con mi instalación local de Workbench.

```bash
cat > ~/ia-lab/services/motores-bd/mysql/docker-compose.yml << 'EOF'
services:
  mysql:
    image: mysql:8.0
    container_name: mysql-server
    restart: unless-stopped
    env_file:
      - .env
    ports:
      - "3307:3306"
    volumes:
      - ../../../data/mysql:/var/lib/mysql
    command: >
      --character-set-server=utf8mb4
      --collation-server=utf8mb4_unicode_ci
      --bind-address=0.0.0.0
    networks:
      - ia-lab-network
EOF
```

![alt text](image.png)

## 4.2 Creación del archivo .env

Para proteger las credenciales, definí el archivo .env con la contraseña raíz 123456 y le puse el nombre de mi proyecto

```bash
cat > ~/ia-lab/services/motores-bd/mysql/.env << 'EOF'
TZ=America/Bogota
MYSQL_ROOT_PASSWORD=123456
EOF
```

![alt text](image-1.png)


## 4.3 Puesta en marcha de MySQL

Me ubiqué en la carpeta del servicio y levanté el contenedor en segundo plano:

```bash
cd ~/ia-lab/services/motores-bd/mysql
docker compose up -d
docker ps | grep mysql-server
```

