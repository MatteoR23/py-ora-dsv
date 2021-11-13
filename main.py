from settings import config
import csv
import cx_Oracle

connString = f'{config["user"]}/{config["password"]}@{config["host"]}:{config["port"]}/{config["service"]}'

def getSqlFileContent(conf):
    with open(conf["source_sql"], "r") as f:
        return f.readlines()

def generateCsvFromOracle(conf):
    import os
    sql = getSqlFileContent(conf)

    con = cx_Oracle.connect(connString)
    cursor = con.cursor()
    csv_file = open(os.path.join(conf["path"], conf["outputfile"]), "w")
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