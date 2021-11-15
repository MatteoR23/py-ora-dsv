from settings import config
import csv
import cx_Oracle
import os

connString = f'{config["user"]}/{config["password"]}@{config["host"]}:{config["port"]}/{config["service"]}'

def getSqlFileContent(conf):
    sourcePath = os.path.join(conf["source_path"], conf["source_sql"])
    with open(sourcePath, "r") as f:
        return f.read()

def generateCsvFromOracle(conf):
    import os
    sql = getSqlFileContent(conf)

    con = cx_Oracle.connect(connString)
    cursor = con.cursor()
    csv_file = open(os.path.join(conf["output_path"], conf["output_file"]), "w")
    writer = csv.writer(csv_file, delimiter=conf["separator"], lineterminator=conf["lineTerminator"], quoting=csv.QUOTE_NONNUMERIC)
    
    r = cursor.execute(sql)
    
    for row in cursor:
        writer.writerow(row)

    cursor.close()
    con.close()
    csv_file.close()

def main():
    confArray = config["conf"]

    for conf in confArray:
        generateCsvFromOracle(conf)

if __name__ == "__main__":
    main()