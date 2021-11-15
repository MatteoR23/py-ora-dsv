from settings import config
import csv
import cx_Oracle
print("cx_Oracle version: %s"%cx_Oracle.version)
import getpass
import os

user = ""
pwd = ""

def getSqlFileContent(conf):
    sourcePath = os.path.join(conf["source_path"], conf["source_sql"])
    with open(sourcePath, "r") as f:
        return f.read().replace("\n", "").replace(";", "")

def generateCsvFromOracle(conf):
    import os
    batchrowsize = 1000
    sql = getSqlFileContent(conf)
    print("Connecting to database...")
    tns_dsn = cx_Oracle.makedsn(config["host"],config["port"], service_name= config["service"])
    try:
        with cx_Oracle.connect(user, pwd, tns_dsn) as con:
            print("Connected!!")

            with con.cursor() as cursor:
                with open(os.path.join(conf["output_path"], conf["output_file"]), "w") as csv_file:
                    writer = csv.writer(csv_file, delimiter=conf["separator"], lineterminator=conf["lineTerminator"], quoting=csv.QUOTE_NONNUMERIC)
                    print("Executing SQL:")
                    print(sql)
                    r = cursor.execute(sql)
                    
                    writeheader = True
                    while True:
                        rows = cursor.fetchmany(batchrowsize)
                        if not rows: break
                        total_rows = len(rows)
                        print("Rows to write: " + str(total_rows))
                        #this takes the column names
                        if writeheader:
                            col_names = [row[0] for row in cursor.description]
                            writer.writerow(col_names)
                            writeheader = False
                        
                        r = 0
                        for row in rows:
                            writer.writerow(row)
                            r = r + 1
                            print(f"Wrote {r}/{total_rows}")
                            
                    print("Successfully exported to:")
                    print(csv_file.name)
                        
    except cx_Oracle.Error as error:
        print(error)

def main():
    global user
    global pwd

    confArray = config["conf"]
    
    user = os.getenv("PY_ORA_DSV_USER")
    if not user: user = input("Insert username:")
    
    pwd = os.getenv("PY_ORA_DSV_PASSWORD")
    if not pwd: pwd = getpass.getpass("Insert password:")
    
    for conf in confArray:
        try:
            generateCsvFromOracle(conf)
        except Exception as ex:
            print(ex)
        
    input("All done!! press any key to exit")

if __name__ == "__main__":
    main()