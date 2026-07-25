-- ==========================================
-- Primary Keys for Bronze Layer
-- ==========================================

-- Aisles
ALTER TABLE bronze.aisles
ADD CONSTRAINT pk_aisles
PRIMARY KEY (aisle_id);

-- Departments
ALTER TABLE bronze.departments
ADD CONSTRAINT pk_departments
PRIMARY KEY (department_id);

-- Products
ALTER TABLE bronze.products
ADD CONSTRAINT pk_products
PRIMARY KEY (product_id);

-- Orders
ALTER TABLE bronze.orders
ADD CONSTRAINT pk_orders
PRIMARY KEY (order_id);

-- Order Products Prior
ALTER TABLE bronze.order_products__prior
ADD CONSTRAINT pk_order_products_prior
PRIMARY KEY (order_id, product_id);

-- Order Products Train
ALTER TABLE bronze.order_products__train
ADD CONSTRAINT pk_order_products_train
PRIMARY KEY (order_id, product_id);