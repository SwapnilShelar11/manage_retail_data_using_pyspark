from main_use_cases.start_session import spark


def readData(fileFormat,readPath,name):
    df = spark\
        .read \
        .format(fileFormat) \
        .option("header", True) \
        .option("inferSchema", True) \
        .load(f"{readPath}{name}")
    return df







