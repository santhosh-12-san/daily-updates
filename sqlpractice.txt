SELECT * FROM employees
WHERE department = 'IT';




SELECT * FROM employees
WHERE department = 'IT' AND salary > 50000;




SELECT * FROM employees
WHERE department = 'IT' OR department = 'HR';




SELECT * FROM employees
 WHERE NOT department = 'Finance';




SELECT * FROM students
WHERE course IN ('BCA', 'MCA', 'BSc');



SELECT * FROM customers
WHERE name LIKE 'S%';





 SELECT * FROM orders
    WHERE delivery_date IS NULL;





SELECT * FROM orders
    WHERE delivery_date IS NOT NULL;




mysql> SELECT * FROM products
    WHERE price BETWEEN 100 AND 500;


    