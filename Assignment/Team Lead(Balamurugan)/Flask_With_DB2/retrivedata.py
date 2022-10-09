import ibm_db;
conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=2d46b6b4-cbf6-40eb-bbce-6251e6ba0300.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=32328;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=bkj82229;PWD=KCwhio0Cb0XQmB5H",'','')

# To retrive all records from DB

sql="SELECT * FROM students"
stmt=ibm_db.exec_immediate(conn,sql);
dictionary= ibm_db.fetch_both(stmt);
while dictionary !=False:
    # print(dictionary)
    print("The name is:", dictionary)
    print("***************")
    dictionary=ibm_db.fetch_both(stmt);