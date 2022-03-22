from pyspark.sql.functions import col, count

"""
Usecase 5 - Product Count Per Department
          Get the products for each department.
          * Tables - departments, categories, products.
          * Data should be sorted in ascending order by department_id
          * Output should contain all the fields from department and the product count as product_count
"""
def productCountPerDept(productsData,categoriesData,departmentsData,writePath):
    resultprodCount = productsData \
        .join(categoriesData, categoriesData.category_id == productsData.product_category_id, "inner") \
        .join(departmentsData, departmentsData.department_id == categoriesData.category_department_id, "inner") \
        .groupBy(col("department_id"), col("department_name")) \
        .agg(count(col("product_id")).alias("product_count")) \
        .orderBy(col("department_id"))
    resultprodCount.show()
    resultprodCount.repartition(1).write.option("header", "true").mode("overwrite") \
        .csv(f"{writePath}productCountPerDept")