from pyspark.sql.functions import col, when, sum

"""
Usecase 3 - Revenue Per Customer
       Get the revenue generated by each customer for the month of 2014 January
       * Tables - orders, order_items and customers
       * Data should be sorted in descending order by revenue and then ascending order by customer_id
       * Output should contain customer_id, customer_first_name, customer_last_name, customer_revenue.
       * If there are no orders placed by customer, then the corresponding revenue for a give customer should be 0.
       * Consider only COMPLETE and CLOSED orders.
"""
def revenuePerCust(ordersData,orderItemsData,customersData,writePath):
    newOrdersData = ordersData.filter("order_date like '2014-01%'")
    resultRevenueCust = newOrdersData \
        .join(customersData, newOrdersData.order_customer_id == customersData.customer_id, "right_outer") \
        .join(orderItemsData, newOrdersData.order_id == orderItemsData.order_item_order_id, "inner") \
        .groupBy(col("customer_id"), col("customer_fname"), col("customer_lname")) \
        .agg(sum("order_item_subtotal").alias("customerRevenue")) \
        .select(col("customer_id"), col("customer_fname"), col("customer_lname"),
                when(col("customerRevenue").isNotNull(), col("customerRevenue"))
                .otherwise(0).alias("revenue_per_customer")) \
        .orderBy(col("revenue_per_customer").desc(), col("customer_id"))
    resultRevenueCust.show()
    resultRevenueCust.repartition(1).write.option("header", "true").mode("overwrite") \
        .csv(f"{writePath}revenuePerCust")


"""
Usecase 4 - Revenue Per Category
         Get the revenue generated for each category for the month of 2014 January
         * Tables - orders, order_items, products and categories
         * Data should be sorted in ascending order by category_id.
         * Output should contain all the fields from category along with the revenue as category_revenue.
         * Consider only COMPLETE and CLOSED orders
"""
def revenuePerCategory(ordersData,orderItemsData,productsData,categoriesData,writePath):
    resultRevenueCategory = ordersData \
        .join(orderItemsData, ordersData.order_id == orderItemsData.order_item_order_id, "inner") \
        .join(productsData, productsData.product_id == orderItemsData.order_item_product_id, "inner") \
        .join(categoriesData, categoriesData.category_id == productsData.product_category_id, "inner") \
        .filter("order_date like '2014-01%' AND order_status in ('COMPLETE','CLOSED')") \
        .groupBy(col("category_Id"), col("category_department_id"), col("category_name")) \
        .agg(sum(orderItemsData.order_item_subtotal.cast("int")).alias("revenue_per_category")) \
        .orderBy(col("category_Id").cast("int"))
    resultRevenueCategory.show()
    resultRevenueCategory.repartition(1).write.option("header", "true").mode("overwrite") \
        .csv(f"{writePath}revenuePerCategory")

