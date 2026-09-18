# **CREACIÓN BASE DE DATOS PUNTO STOCK**

## 1.MySQL

1.1 Creación de la base de datos en dbeaver

``` mysql
CREATE DATABASE puntostock;
```

![](images/clipboard-2791081486.png)

1.2creación de tabla branch

``` mysql
CREATE TABLE branch (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    description VARCHAR(255),
    is_active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
```

![](images/clipboard-2963322324.png)

1.2 creación de tabla product

``` mysql
CREATE TABLE product (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sku VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    description VARCHAR(255),
    price DECIMAL(12,2) NOT NULL,
    is_active TINYINT(1) DEFAULT 1
);
```

![](images/clipboard-197680292.png)

1.2 creación de tabla supplier

``` mysql
CREATE TABLE supplier (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tax_id VARCHAR(30) NOT NULL UNIQUE, -- Representa el NIT / Documento Fiscal
    company_name VARCHAR(150) NOT NULL,
    contact_person VARCHAR(100),
    phone VARCHAR(30),
    email VARCHAR(150),
    is_active TINYINT(1) DEFAULT 1
);
```

![](images/clipboard-2230667923.png)

1.2 creación de tabla customer

``` mysql
CREATE TABLE customer (
    id INT AUTO_INCREMENT PRIMARY KEY,
    document_type VARCHAR(20) NOT NULL,
    document_number VARCHAR(30) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    phone VARCHAR(30),
    email VARCHAR(150),
    is_active TINYINT(1) DEFAULT 1
);
```

![](images/clipboard-750168348.png)

1.2 creación de tabla inventory

``` mysql
CREATE TABLE inventory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    location_id INT NOT NULL, -- FK Branch
    item_id INT NOT NULL,     -- FK Product
    quantity INT NOT NULL DEFAULT 0,
    min_stock INT NOT NULL DEFAULT 0,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (location_id) REFERENCES branch(id),
    FOREIGN KEY (item_id) REFERENCES product(id),
    UNIQUE (location_id, item_id)
);
```

![](images/clipboard-2030942465.png)

1.2 creación de tabla purchase

``` mysql

CREATE TABLE purchase (
    id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_id INT NOT NULL,
    purchase_date DATETIME NOT NULL,
    subtotal DECIMAL(12,2) NOT NULL,
    tax DECIMAL(12,2) NOT NULL,
    total DECIMAL(12,2) NOT NULL,
    status VARCHAR(30) NOT NULL,
    FOREIGN KEY (supplier_id) REFERENCES supplier(id)
);
```

![](images/clipboard-3420156374.png)

1.2 creación de tabla purchase_detail

``` mysql
CREATE TABLE purchase_detail (
    id INT AUTO_INCREMENT PRIMARY KEY,
    header_id INT NOT NULL, -- FK Purchase
    item_id INT NOT NULL,   -- FK Product
    quantity INT NOT NULL,
    unit_price DECIMAL(12,2) NOT NULL,
    total DECIMAL(12,2) NOT NULL,
    notes TEXT,
    FOREIGN KEY (header_id) REFERENCES purchase(id),
    FOREIGN KEY (item_id) REFERENCES product(id)
);
```

![](images/clipboard-1729828930.png)

1.2 creación de tabla sale

``` mysql
CREATE TABLE sale (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    branch_id INT NOT NULL,
    sale_date DATETIME NOT NULL,
    subtotal DECIMAL(12,2) NOT NULL,
    tax DECIMAL(12,2) NOT NULL,
    total DECIMAL(12,2) NOT NULL,
    status VARCHAR(30) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customer(id),
    FOREIGN KEY (branch_id) REFERENCES branch(id)
);
```

![](images/clipboard-1244666756.png)

1.2 creación de tabla sale_detail

``` mysql
CREATE TABLE sale_detail (
    id INT AUTO_INCREMENT PRIMARY KEY,
    header_id INT NOT NULL, -- FK Sale
    item_id INT NOT NULL,   -- FK Product
    quantity INT NOT NULL,
    unit_price DECIMAL(12,2) NOT NULL,
    total DECIMAL(12,2) NOT NULL,
    notes TEXT,
    FOREIGN KEY (header_id) REFERENCES sale(id),
    FOREIGN KEY (item_id) REFERENCES product(id)
);
```

![](images/clipboard-762830443.png)

1.2 creación de tabla payment

``` mysql
CREATE TABLE payment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reference_type VARCHAR(50) NOT NULL, -- Ej: 'SALE', 'PURCHASE'
    reference_id INT NOT NULL,           -- ID de la Venta/Compra
    payment_method VARCHAR(50) NOT NULL,  -- Cash, Credit Card, Bank Transfer, etc.
    amount DECIMAL(12,2) NOT NULL,
    payment_date DATETIME NOT NULL,
    status VARCHAR(30) NOT NULL
);
```

![](images/clipboard-3443556344.png)\
1.2 creación de tabla product return

``` mysql
CREATE TABLE product_return (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reference_id INT NOT NULL, -- FK Sale
    return_date DATETIME NOT NULL,
    reason VARCHAR(255) NOT NULL,
    total DECIMAL(12,2) NOT NULL,
    status VARCHAR(30) NOT NULL,
    FOREIGN KEY (reference_id) REFERENCES sale(id)
);
```

![](images/clipboard-2112997086.png)

## 2. creación de bases de datos de forma visual usando schema de mysql

2.1 creamos la base de datos de forma visual

![](images/clipboard-1367574375.png)

2.2 creamos la tabla branch

![![](images/clipboard-2229580873.png)](images/clipboard-3641326226.png)

2.3 creación de tabla product

![](images/clipboard-3109283960.png)

![](images/clipboard-1191321758.png)

2.4 creación tabla supplier

![](images/clipboard-2249857333.png)

![](images/clipboard-1776148279.png)

2.5 creación de tabla customer

![![](images/clipboard-1021869525.png)](images/clipboard-4023966206.png)

2.6 creación de tabla inventory

![](images/clipboard-569443150.png)

![](images/clipboard-2527317293.png)

2.7 creación de tabla purchase

![](images/clipboard-1090408564.png)

![](images/clipboard-1434895428.png)\
2.8 creación de tabla purchase_detail

![](images/clipboard-1968045535.png)

![](images/clipboard-198337554.png)\
2.9 creación de tabla sale

![](images/clipboard-2322428466.png)![](images/clipboard-2455467515.png)\
2.10 creación de tabla sale_detail

![](images/clipboard-790227375.png)

![](images/clipboard-2453214024.png)

2.11 creación de tabla product payment

![](images/clipboard-3237886333.png)

![](images/clipboard-1987021007.png)2.12 creación de tabla product_return

![](images/clipboard-1401515965.png)

![](images/clipboard-61319437.png)

2.13 confirmación de la creación de las tablas

![](images/clipboard-3563478895.png)

2.14 diagrama de ingeniería reversa

![](images/clipboard-3478515421.png)

## 2. postgresql

2.1 creación tabla branch

``` postgres
CREATE TABLE branch (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    description VARCHAR(255),
    is_active SMALLINT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

![](images/clipboard-2198650756.png)

2.2 creación de tabla product

``` postgres
CREATE TABLE product (
    id SERIAL PRIMARY KEY,
    sku VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    description VARCHAR(255),
    price NUMERIC(12,2) NOT NULL,
    is_active SMALLINT DEFAULT 1
);
```

![](images/clipboard-89114991.png)

2.3 creación de tabla supplier

``` postgres
CREATE TABLE supplier (
    id SERIAL PRIMARY KEY,
    tax_id VARCHAR(30) NOT NULL UNIQUE,
    company_name VARCHAR(150) NOT NULL,
    contact_person VARCHAR(100),
    phone VARCHAR(30),
    email VARCHAR(150),
    is_active SMALLINT DEFAULT 1
);
```

![](images/clipboard-1512469523.png)

2.4 creación de tabla customer

``` postgres
CREATE TABLE customer (
    id SERIAL PRIMARY KEY,
    document_type VARCHAR(20) NOT NULL,
    document_number VARCHAR(30) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    phone VARCHAR(30),
    email VARCHAR(150),
    is_active SMALLINT DEFAULT 1
);
```

![](images/clipboard-631419892.png)

2.5 creación de tabla inventory

``` postgres
CREATE TABLE inventory (
    id SERIAL PRIMARY KEY,
    location_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 0,
    min_stock INT NOT NULL DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_inventory_branch FOREIGN KEY (location_id) REFERENCES branch(id),
    CONSTRAINT fk_inventory_product FOREIGN KEY (item_id) REFERENCES product(id),
    CONSTRAINT unique_location_item UNIQUE (location_id, item_id)
);
```

![](images/clipboard-2776121234.png)

2.6 creación de tabla purchase

``` postgres
CREATE TABLE purchase (
    id SERIAL PRIMARY KEY,
    supplier_id INT NOT NULL,
    purchase_date TIMESTAMP NOT NULL,
    subtotal NUMERIC(12,2) NOT NULL,
    tax NUMERIC(12,2) NOT NULL,
    total NUMERIC(12,2) NOT NULL,
    status VARCHAR(30) NOT NULL,
    CONSTRAINT fk_purchase_supplier FOREIGN KEY (supplier_id) REFERENCES supplier(id)
);
```

![](images/clipboard-3135367773.png)

2.7 creación de tabla purchase_detail

``` postgres
CREATE TABLE purchase_detail (
    id SERIAL PRIMARY KEY,
    header_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price NUMERIC(12,2) NOT NULL,
    total NUMERIC(12,2) NOT NULL,
    notes TEXT,
    CONSTRAINT fk_purchase_detail_header FOREIGN KEY (header_id) REFERENCES purchase(id),
    CONSTRAINT fk_purchase_detail_product FOREIGN KEY (item_id) REFERENCES product(id)
);
```

![](images/clipboard-764998832.png)

2.8 creacíon de tabla sale

``` postgres
CREATE TABLE sale (
    id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    branch_id INT NOT NULL,
    sale_date TIMESTAMP NOT NULL,
    subtotal NUMERIC(12,2) NOT NULL,
    tax NUMERIC(12,2) NOT NULL,
    total NUMERIC(12,2) NOT NULL,
    status VARCHAR(30) NOT NULL,
    CONSTRAINT fk_sale_customer FOREIGN KEY (customer_id) REFERENCES customer(id),
    CONSTRAINT fk_sale_branch FOREIGN KEY (branch_id) REFERENCES branch(id)
);
```

![](images/clipboard-2191328325.png)

2.10 creación de tabla sale_detail

``` postgres
CREATE TABLE sale_detail (
    id SERIAL PRIMARY KEY,
    header_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price NUMERIC(12,2) NOT NULL,
    total NUMERIC(12,2) NOT NULL,
    notes TEXT,
    CONSTRAINT fk_sale_detail_header FOREIGN KEY (header_id) REFERENCES sale(id),
    CONSTRAINT fk_sale_detail_product FOREIGN KEY (item_id) REFERENCES product(id)
);
```

![](images/clipboard-4289856468.png)

2.11 creación de tabla payment

``` postgres
CREATE TABLE payment (
    id SERIAL PRIMARY KEY,
    reference_type VARCHAR(50) NOT NULL,
    reference_id INT NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    amount NUMERIC(12,2) NOT NULL,
    payment_date TIMESTAMP NOT NULL,
    status VARCHAR(30) NOT NULL
);
```

![](images/clipboard-3862813475.png)

2.12 creación de tabla product return

``` postgres
CREATE TABLE product_return (
    id SERIAL PRIMARY KEY,
    reference_id INT NOT NULL,
    return_date TIMESTAMP NOT NULL,
    reason VARCHAR(255) NOT NULL,
    total NUMERIC(12,2) NOT NULL,
    status VARCHAR(30) NOT NULL,
    CONSTRAINT fk_return_sale FOREIGN KEY (reference_id) REFERENCES sale(id)
);
```

![](images/clipboard-1389159992.png)

## 3. sqlserver

3.1 creación de tabla branch

``` sqlserver
CREATE TABLE branch (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    description VARCHAR(255),
    is_active TINYINT DEFAULT 1,
    created_at DATETIME2 DEFAULT GETDATE(),
    updated_at DATETIME2 DEFAULT GETDATE()
);
```

![](images/clipboard-149430895.png)

3.2 creación de tabla suppiler

``` sqlserver
CREATE TABLE supplier (
    id INT IDENTITY(1,1) PRIMARY KEY,
    tax_id VARCHAR(30) NOT NULL UNIQUE,
    company_name VARCHAR(150) NOT NULL,
    contact_person VARCHAR(100),
    phone VARCHAR(30),
    email VARCHAR(150),
    is_active TINYINT DEFAULT 1
);
```

![](images/clipboard-4021608513.png)

3.3 creación de tabla product

``` sqlserver
CREATE TABLE product (
    id INT IDENTITY(1,1) PRIMARY KEY,
    sku VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    description VARCHAR(255),
    price DECIMAL(12,2) NOT NULL,
    is_active TINYINT DEFAULT 1
);
```

![](images/clipboard-2630553333.png)

3.4 creación de tabla customer

``` sqlserver
CREATE TABLE customer (
    id INT IDENTITY(1,1) PRIMARY KEY,
    document_type VARCHAR(20) NOT NULL,
    document_number VARCHAR(30) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    phone VARCHAR(30),
    email VARCHAR(150),
    is_active TINYINT DEFAULT 1
);
```

![](images/clipboard-2504198360.png)

3.5 creación de tabla purchase

``` sqlserver
CREATE TABLE purchase (
    id INT IDENTITY(1,1) PRIMARY KEY,
    supplier_id INT NOT NULL,
    purchase_date DATETIME2 NOT NULL,
    subtotal DECIMAL(12,2) NOT NULL,
    tax DECIMAL(12,2) NOT NULL,
    total DECIMAL(12,2) NOT NULL,
    status VARCHAR(30) NOT NULL,
    CONSTRAINT fk_purchase_supplier FOREIGN KEY (supplier_id) REFERENCES supplier(id)
);
```

![](images/clipboard-4023359944.png)

3.6 creación de tabla purchase_detail

``` sqlserver
CREATE TABLE purchase_detail (
    id INT IDENTITY(1,1) PRIMARY KEY,
    header_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(12,2) NOT NULL,
    total DECIMAL(12,2) NOT NULL,
    notes VARCHAR(MAX),
    CONSTRAINT fk_purchase_detail_header FOREIGN KEY (header_id) REFERENCES purchase(id),
    CONSTRAINT fk_purchase_detail_product FOREIGN KEY (item_id) REFERENCES product(id)
);
```

![](images/clipboard-3833228528.png)

3.7 creación de tabla sale

``` sqlserver
CREATE TABLE sale (
    id INT IDENTITY(1,1) PRIMARY KEY,
    customer_id INT NOT NULL,
    branch_id INT NOT NULL,
    sale_date DATETIME2 NOT NULL,
    subtotal DECIMAL(12,2) NOT NULL,
    tax DECIMAL(12,2) NOT NULL,
    total DECIMAL(12,2) NOT NULL,
    status VARCHAR(30) NOT NULL,
    CONSTRAINT fk_sale_customer FOREIGN KEY (customer_id) REFERENCES customer(id),
    CONSTRAINT fk_sale_branch FOREIGN KEY (branch_id) REFERENCES branch(id)
);
```

![](images/clipboard-3616935477.png)

3.8 creación de tabla sale_detail

``` sqlserver
CREATE TABLE sale_detail (
    id INT IDENTITY(1,1) PRIMARY KEY,
    header_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(12,2) NOT NULL,
    total DECIMAL(12,2) NOT NULL,
    notes VARCHAR(MAX),
    CONSTRAINT fk_sale_detail_header FOREIGN KEY (header_id) REFERENCES sale(id),
    CONSTRAINT fk_sale_detail_product FOREIGN KEY (item_id) REFERENCES product(id)
);
```

![](images/clipboard-779691755.png)

3.9 creación de tabla payment

``` sqlserver
CREATE TABLE payment (
    id INT IDENTITY(1,1) PRIMARY KEY,
    reference_type VARCHAR(50) NOT NULL,
    reference_id INT NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    payment_date DATETIME2 NOT NULL,
    status VARCHAR(30) NOT NULL
);
```

![](images/clipboard-1719187105.png)

3.10 creación de tabla inventory

``` sqlserver
CREATE TABLE inventory (
    id INT IDENTITY(1,1) PRIMARY KEY,
    location_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 0,
    min_stock INT NOT NULL DEFAULT 0,
    updated_at DATETIME2 DEFAULT GETDATE(),
    CONSTRAINT fk_inventory_branch FOREIGN KEY (location_id) REFERENCES branch(id),
    CONSTRAINT fk_inventory_product FOREIGN KEY (item_id) REFERENCES product(id),
    CONSTRAINT unique_location_item UNIQUE (location_id, item_id)
);
```

![](images/clipboard-1284760146.png)

3.11 creación de tabla product_return

``` sqlserver
CREATE TABLE product_return (
    id INT IDENTITY(1,1) PRIMARY KEY,
    reference_id INT NOT NULL,
    return_date DATETIME2 NOT NULL,
    reason VARCHAR(255) NOT NULL,
    total DECIMAL(12,2) NOT NULL,
    status VARCHAR(30) NOT NULL,
    CONSTRAINT fk_return_sale FOREIGN KEY (reference_id) REFERENCES sale(id)
);
```

![](images/clipboard-172795436.png)

## 4. ORACLE XE

4.1 creación de tabla branch

![](images/clipboard-3565607012.png)

4.1 creación de tabla product

![](images/clipboard-3256994770.png)

4.1 creación de tabla supplier

![](images/clipboard-2795582306.png)

4.1 creación de tabla customer

![](images/clipboard-2287853797.png)

4.1 creación de tabla inventory

![](images/clipboard-3933857965.png)

4.1 creación de tabla purchase

![](images/clipboard-2176534204.png)

4.1 creación de tabla purchase_detail

![](images/clipboard-4191993210.png)

4.1 creación de tabla sale

![](images/clipboard-1273661332.png)

4.1 creación de tabla sale_detail

![](images/clipboard-3425325546.png)

4.1 creación de tabla payment

![](images/clipboard-2821276133.png)

4.1 creación de tabla product return

![](images/clipboard-108443274.png)
