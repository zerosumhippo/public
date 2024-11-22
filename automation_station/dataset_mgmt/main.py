# Gotta take arguments that identify:
# # client
# # oneview
# # redshift cluster
# Then it would reach into github to grab the SQL
# Then update in Redshift
# Then run metadata generation

# import sqlite3
#
# db = sqlite3.connect("starship_agency.db")
# cursor = db.cursor()
# cursor.execute("CREATE TABLE table1 (field1 varchar(250), field2 FLOAT, field3 FLOAT, field4 FLOAT)")
# cursor.execute("INSERT INTO table1 VALUES('Your planet needs you!', '55.12', '1.25', '9.3')")
# db.commit()
# use sqlalchemy instead >> look at sqlite-databases project
