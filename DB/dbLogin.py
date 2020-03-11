'''
Created on May 17, 2017

This is now to create DB login info; subject to change later on

'''
def initialDBLogin( schema_name ):
    
    hostip  = '127.0.0.1'
    dbname  = schema_name
    pwd     = 'dsl911023'
    userid  = 'root'
    dblogin = { 
                'ip':hostip, 
                'userid':userid, 
                'dbname':dbname, 
                'pw':pwd
              }
    
    return dblogin




