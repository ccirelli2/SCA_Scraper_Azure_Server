'''DOCUMENTATION

The purpose of this module is to house the functions that will automatically create
the SCA_SCRAPER database & SCA_Data table.  

The code is triggered upon the generation of the mysql.connector error
'''

### IMPORT MODULES_______________________________________________
import mysql.connector

	

def create_SCA_DATA_table(mydb):
	
	# Generate Cursor
	mycursor = mydb.cursor()
	
	# User Feedback
	print('Creating SCA_DATA_2 table in SCA_SCRAPER database')
	# SQL Command
	sql_command = '''
	CREATE TABLE SCA_DATA_2 (
	page_number smallint(6) NOT NULL,
	defendant_address mediumtext,
	defendant_name varchar(255) DEFAULT NULL,        
	case_status varchar(25) DEFAULT NULL,\n        
	filling_date date DEFAULT NULL,\n        
	close_date date DEFAULT NULL,\n        
	case_summary longblob,\n        
	Sector varchar(25) DEFAULT NULL,\n        
	Industry varchar(225) DEFAULT NULL,\n        
	Symbol varchar(25) DEFAULT NULL,\n        
	Status_2 varchar(25) DEFAULT NULL,\n        
	Headquarters varchar(225) DEFAULT NULL,\n        
	Company_market varchar(25) DEFAULT NULL,\n        
	Court varchar(25) DEFAULT NULL,\n        
	Docket varchar(25) DEFAULT NULL,\n        
	Judge varchar(255) DEFAULT NULL,\n        
	Date_Filed date DEFAULT NULL,\n        
	Class_Period_Start date DEFAULT NULL,\n        
	Class_Period_End date DEFAULT NULL,\n        
	Plaintiff_firm varchar(2225) DEFAULT NULL,\n        
	Ref_court varchar(255) DEFAULT NULL,\n        
	Ref_docket varchar(255) DEFAULT NULL,\n        
	Ref_judge varchar(255) DEFAULT NULL,\n        
	Ref_date_filed date DEFAULT NULL,\n        
	Ref_class_period_start date DEFAULT NULL,\n        
	Ref_class_period_end date DEFAULT NULL,\n        
	YEAR_FILED int(4) DEFAULT NULL,\n        
	Breach_Fiduciary_Duties smallint(6) DEFAULT NULL,\n        
	Merger smallint(6) DEFAULT NULL,\n        
	Proxy_violation smallint(6) DEFAULT NULL,\n        
	Related_parties smallint(6) DEFAULT NULL,\n        
	Stock_Drop smallint(6) DEFAULT NULL,\n        
	Cash_Flow smallint(6) DEFAULT NULL,\n        
	Revenue_Rec smallint(6) DEFAULT NULL,\n        
	Net_Income smallint(6) DEFAULT NULL,\n        
	Customers smallint(6) DEFAULT NULL,\n        
	Fourth_Quarter smallint(6) DEFAULT NULL, 
	Third_Quarter smallint(6) DEFAULT NULL,\n        
	Second_Quarter smallint(6) DEFAULT NULL,\n        
	Press_Release smallint(6) DEFAULT NULL,\n        
	10K_Filling smallint(6) DEFAULT NULL,\n        
	10Q_Filling smallint(6) DEFAULT NULL,\n        
	Corporate_Governance smallint(6) DEFAULT NULL,\n        
	Conflicts_Interest smallint(6) DEFAULT NULL,\n        
	Accounting smallint(6) DEFAULT NULL,\n        
	Fees smallint(6) DEFAULT NULL,\n        
	Failed_disclose smallint(6) DEFAULT NULL,\n        
	False_misleading smallint(6) DEFAULT NULL,\n        
	Commissions smallint(6) DEFAULT NULL,\n        
	Bankruptcy smallint(6) DEFAULT NULL,\n        
	Secondary_Offering smallint(6) DEFAULT NULL,\n        
	IPO smallint(6) DEFAULT NULL,\n        
	1934_Exchange_Act smallint(6) DEFAULT NULL,\n        
	Derivative smallint(6) DEFAULT NULL,\n        
	10b5 smallint(6) DEFAULT NULL,\n        
	1933_Act smallint(6) DEFAULT NULL,\n        
	Heavy_trading smallint(6) DEFAULT NULL
	Proxy smallint(6) DEFAULT NULL, 
	ERISA smallint(6) DEFAULT NULL, 
	FCPA smallint(6) DEFAULT NULL, 
	Sexual_Misconduct smallint(6) DEFAULT NULL, 
	Data_breach smallint(6) DEFAULT NULL);'''

	

	# Execute Sql Command	
	mycursor.execute(sql_command)
	
	# User Feedback
	print('SCA_DATA_2 table created successfully')
	
	# End
 
	

# DRIVER FUNCTION - CHECK FOR DB & TABLE - IF MISSING - CREATE_________________________
'''Purpose:  When the user first starts up the scraper, it is likely that they
	     did not manually create the database and table. 
	     This code will automatically create them if they are missing. '''

def driver_test_conn_db_table():
	# Step 1:  Test Connection to SCA_SCRAPER Database-----------------
	try:
		mydb = mysql.connector.connect(
		host="localhost",
		user="ccirelli2",	
		passwd="Work4starr",
		database='SCA_SCRAPER')
		# If Connection without errors - log & return mydb connection
		print('Connection to MySQL SCA_SCRAPER database successfully created')
		return mydb

	# If DB Missing - Create the Database
	except mysql.connector.errors.ProgrammingError as err:
        	# If Error = Missing DB
		if "Unknown database" in str(err):
			print('SCA_SCRAPER Database Not Found.  Creating Database')
			# Establish Connection
			mydb = mysql.connector.connect(
			host="localhost",
			user="ccirelli2",
			passwd="Work4starr")
			# Create Cursor
			mycursor = mydb.cursor()
			# SQL Command
			sql_command = 'CREATE DATABASE SCA_SCRAPER;'
			# Execute
			mycursor.execute(sql_command)
			# User Info
			print('SCA_SCRAPER database successfully created')

		# Return All other Errors to the user
		else:
			print('MySql Connector Error => {}'.format(err))
	
	# Step 2:  Test the connection to the SCA_DATA table---------------
	try:
		# Establish Connection
		mydb     = mysql.connector.connect(
		host     ="localhost",
		user     ="ccirelli2",
		passwd   ="Work4starr",
		database ='SCA_SCRAPER')
		
		# Test Query On SCA_DATA_2 Table
		print('Testing connection to SCA_DATA_2 table')
		mycursor = mydb.cursor()
		sql_command = 'SELECT * FROM SCA_DATA_2;'
		mycursor.execute(sql_command)
		
		# If No Error
		print('Connection to SCA_DATA_table successful')
		return mydb
	
	# If Error = Missing Table - Create the table
	except mysql.connector.errors.ProgrammingError as err:
		if 'SCA_SCRAPER.SCA_DATA_2' in str(err):
			print('SCA_DATA_table not found.')
			# Establish Connection
			mydb     = mysql.connector.connect(
			host     ="localhost",
			user     ="ccirelli2",
			passwd   ="Work4starr",
			database ='SCA_SCRAPER')
			mycursor = mydb.cursor()
			# Create Table
			create_SCA_DATA_table(mydb)
			# Return mydb
			return mydb
	
	# End of function
	pass
	







