BEGIN;

CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS metadata;

CREATE TABLE IF NOT EXISTS bronze.aisles (
    aisle_id INTEGER PRIMARY KEY,
    aisle TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bronze.departments (
    department_id INTEGER PRIMARY KEY,
    department TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bronze.products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    aisle_id INTEGER NOT NULL,
    department_id INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS bronze.orders (
    order_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    eval_set TEXT NOT NULL,
    order_number INTEGER NOT NULL,
    order_dow SMALLINT NOT NULL,
    order_hour_of_day SMALLINT NOT NULL,
    days_since_prior_order NUMERIC(6,2)
);

CREATE TABLE IF NOT EXISTS bronze.order_products__prior (
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    add_to_cart_order INTEGER NOT NULL,
    reordered SMALLINT NOT NULL,
    PRIMARY KEY (order_id, product_id)
);

CREATE TABLE IF NOT EXISTS bronze.order_products__train (
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    add_to_cart_order INTEGER NOT NULL,
    reordered SMALLINT NOT NULL,
    PRIMARY KEY (order_id, product_id)
);

CREATE TABLE IF NOT EXISTS metadata.file_tracking (
    file_name TEXT PRIMARY KEY,
    last_modified TIMESTAMP,
    last_loaded TIMESTAMP,
    status TEXT NOT NULL DEFAULT 'PENDING',
    file_size BIGINT
);

COMMIT;