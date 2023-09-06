# 1. Import Statements
import sqlite3


# 2. Create a connection to DB
s_con = sqlite3.connect("northwind_small.sqlite3")


# 3. Create cursor object
s_cur = s_con.cursor()


# 4. Execute Queries
expensive_items = s_cur.execute(
    """SELECT * FROM Product ORDER BY UnitPrice DESC LIMIT 10""").fetchall()

avg_hire_age = s_cur.execute(
    """ SELECT AVG(Hiredate - Birthdate) FROM Employee""").fetchall()

ten_most_expensive = s_cur.execute("""
    SELECT Product.ProductName, Product.UnitPrice, Supplier.CompanyName
    FROM Product
    LEFT JOIN Supplier
    ON Product.SupplierId = Supplier.Id
    ORDER BY UnitPrice DESC
    LIMIT 10 """).fetchall()

largest_category = s_cur.execute("""
    SELECT Category.CategoryName, COUNT(DISTINCT Product.Id)
    FROM Category, Product
    WHERE Category.Id = Product.CategoryId
    GROUP BY 1
    ORDER BY 2 DESC
    LIMIT 1""").fetchall()
# STRETCH GOALS
avg_age_by_city = s_cur.execute(
    """ SELECT DISTINCT(City), AVG(Hiredate - Birthdate)
    FROM Employee GROUP BY City""").fetchall()

most_territories = s_cur.execute("""
    SELECT *, COUNT(EmployeeTerritory.TerritoryId)
    FROM Employee
    LEFT JOIN EmployeeTerritory
    ON Employee.Id = EmployeeTerritory.EmployeeId
    ORDER BY COUNT(EmployeeTerritory.TerritoryId) DESC
    LIMIT 1""").fetchall()

if __name__ == '__main__':
    print(expensive_items)
    print(avg_hire_age)
    print(avg_age_by_city)
    print(ten_most_expensive)
    print(largest_category)
    print(most_territories)
