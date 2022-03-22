from pyspark.sql.functions import col, count

""" 
   Usecase 1 - Customer order count
          Get order count per customer for the month of 2014 January.
          * Tables - orders and customers.
          * Data should be sorted in descending order by count and ascending order by customer id.
          * Output should contain customer_id, customer_first_name, customer_last_name and customer_order_count.
  """

def custOrdersCount(ordersData,customersData,writePath):
    resultOrdersCount = ordersData \
        .join(customersData, ordersData.order_customer_id == customersData.customer_id, "inner") \
        .filter("order_date like '2014-01%'") \
        .groupBy(col("customer_id"), col("customer_fname"), col("customer_lname")) \
        .agg(count("order_id").alias("customer_order_count")) \
        .orderBy(col("customer_order_count").desc(), col("customer_id").cast("int"))
    resultOrdersCount.show()
    resultOrdersCount.repartition(1).write.option("header", "true").mode("overwrite")\
                .csv(f"{writePath}customers_orders_count")


"""
   Usecase 2 - Dormant Customers
         Get the customer details who have not placed any order for the month of 2014 January.
         * Tables - orders and customers
         * Data should be sorted in ascending order by customer_id
         * Output should contain all the fields from customers
"""
def dormantCustomers(ordersData,customersData,writePath):
    newOrdersData = ordersData.filter("order_date like '2014-01%'")
    resultDormant = newOrdersData \
        .join(customersData, newOrdersData.order_customer_id == customersData.customer_id, "right_outer") \
        .filter("order_date is null") \
        .orderBy(col("customer_id").cast("int")) \
        .select(col("customer_id"), col("customer_fname"), col("customer_lname"), col("customer_email"),
                col("customer_password"), col("customer_street"), col("customer_city"), col("customer_state"),
                col("customer_zipcode"))
    resultDormant.show()
    resultDormant.repartition(1).write.option("header", "true").mode("overwrite") \
        .csv(f"{writePath}dormantCustomers")