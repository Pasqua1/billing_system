insert into transaction_statuses (status_name) values('New');
insert into transaction_statuses (status_name) values('Completed');
insert into transaction_statuses (status_name) values('Rejected');

insert into currency_types (currency_type_name) values('RUB');
insert into currency_types (currency_type_name) values('USD');

insert into companies (company_name) values('Yandex');
insert into companies (company_name) values('Google');

insert into customers (customer_name, balance, company_id, currency_type_id) values('Alex',1000,1,1);

insert into products (product_name, price, quantity, company_id, currency_type_id) values('Cake',10,1000,2,1);
