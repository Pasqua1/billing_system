CREATE TABLE IF NOT EXISTS transaction_statuses (
  status_id SERIAL,
  status_name VARCHAR(250) NOT NULL UNIQUE,
  PRIMARY KEY (status_id)
);


CREATE TABLE IF NOT EXISTS currency_types (
  currency_type_id SERIAL,
  currency_type_name VARCHAR(250) NOT NULL UNIQUE,
  PRIMARY KEY (currency_type_id)
);


CREATE TABLE IF NOT EXISTS companies (
  company_id SERIAL,
  company_name VARCHAR(250) NOT NULL UNIQUE,
  PRIMARY KEY (company_id)
);


CREATE TABLE IF NOT EXISTS customers (
  customer_id SERIAL,
  customer_name VARCHAR(250) NOT NULL,
  company_id INT NOT NULL,
  balance DECIMAL(20,2) NOT NULL CHECK (balance >= 0),
  currency_type_id SMALLINT NOT NULL,
  PRIMARY KEY (customer_id),
  CONSTRAINT fk_company_id
    FOREIGN KEY(company_id) 
	    REFERENCES companies(company_id),
  CONSTRAINT fk_currency_type
    FOREIGN KEY(currency_type_id) 
	    REFERENCES currency_types(currency_type_id)
);


CREATE TABLE IF NOT EXISTS products (
  product_id SERIAL,
  product_name VARCHAR(250) NOT NULL,
  company_id INT NOT NULL,
  price DECIMAL(20,2) NOT NULL,
  quantity INT NOT NULL CHECK (quantity >= 0),
  currency_type_id SMALLINT NOT NULL,
  PRIMARY KEY (product_id),
  CONSTRAINT fk_company_id
    FOREIGN KEY(company_id) 
	    REFERENCES companies(company_id),
  CONSTRAINT fk_currency_type
    FOREIGN KEY(currency_type_id) 
	    REFERENCES currency_types(currency_type_id),
  UNIQUE (company_id, product_name)
);


CREATE TABLE IF NOT EXISTS transactions (
  transaction_id SERIAL,
  date_create TIMESTAMP NOT NULL,
  amount DECIMAL(20,2) NOT NULL,
  status_id SMALLINT NOT NULL,
  currency_type_id SMALLINT NOT NULL,
  customer_id INT NOT NULL,
  product_id INT NOT NULL, 
  number_of_products INT NOT NULL,
  PRIMARY KEY (transaction_id),
  CONSTRAINT fk_status
    FOREIGN KEY(status_id) 
	    REFERENCES transaction_statuses(status_id),
  CONSTRAINT fk_currency_type
    FOREIGN KEY(currency_type_id) 
	    REFERENCES currency_types(currency_type_id),
  CONSTRAINT fk_customer
    FOREIGN KEY(customer_id) 
	    REFERENCES customers(customer_id),
  CONSTRAINT fk_product
    FOREIGN KEY(product_id) 
	    REFERENCES products(product_id)
);
