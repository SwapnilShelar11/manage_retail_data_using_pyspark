import configparser
import os

from main_use_cases.read import readData
from logic_use_cases.customer import custOrdersCount,dormantCustomers
from logic_use_cases.revenue import revenuePerCust,revenuePerCategory
from logic_use_cases.products_count import productCountPerDept

config = configparser.ConfigParser()
config.read(os.environ['CONFIGFILE'])

readPath=config.get('ReadSection','readPath')
writePath=config.get('WriteSection','writePath')
fileFormat=config.get('ReadSection','fileFormat')

orders=config.get('ReadSection','ordersFile')
customers=config.get('ReadSection','customersFile')
orderItems=config.get('ReadSection','order_itemsFile')
products=config.get('ReadSection','productsFile')
categories=config.get('ReadSection','categoriesFile')
departments=config.get('ReadSection','departmentsFile')

ordersData=readData(fileFormat,readPath,orders)
customersData=readData(fileFormat,readPath,customers)
orderItemsData=readData(fileFormat,readPath,orderItems)
productsData=readData(fileFormat,readPath,products)
categoriesData=readData(fileFormat,readPath,categories)
departmentsData=readData(fileFormat,readPath,departments)


custOrdersCount(ordersData,customersData,writePath)
#dormantCustomers(ordersData,customersData,writePath)
#revenuePerCust(ordersData,orderItemsData,customersData,writePath)
#revenuePerCategory(ordersData,orderItemsData,productsData,categoriesData,writePath)
#productCountPerDept(productsData,categoriesData,departmentsData,writePath)