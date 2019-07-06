# PURPOSE:  SEARCH SCA USING KEY WORD



# IMPORT MODULES
import mysql.connector
import pandas as pd
import Module_0_utility_functions as m0
from datetime import datetime


# INSTANTIATE MYSQL CONNECTION
mydb = mysql.connector.connect(
                host="localhost",
                user="ccirelli2",
                passwd="Work4starr",
                database='SCA_SCRAPER')


# OUTPUT DIRECTORY
output_dir = '/home/ccirelli2/Desktop/repositories/sca_scraper_azure_server/Output'

# FUNCTION----------------------------------------------------------------
def keywordsearch(mydb, table, password):

	# Create Cursor
	mycursor = mydb.cursor()

	# Sys Datetime
	sys_datetime = str(datetime.now()).replace(' ', '')[0:14]

	# Key Word
	print('Enter your key word')
	keyword = input()

	# Query
	sql_query = '''
	SELECT 	filling_date, 
		close_date, 
		case_status, 
		defendant_name, 
		Symbol, 
		Headquarters, 
		Industry, 
		Sector, 
		Docket,
		court,  
		Judge, 
		case_summary
		

	FROM {}
	WHERE case_summary LIKE '%{}%'
	'''.format(table, keyword)

	# Get Data
	df = pd.read_sql(sql_query, mydb)
	
	# User Interaction 
	print('Your search has returned {} number of results\n'.format(len(df.index)))
	print('Do you want to further refine your search (Yes/No)?')
	resp = input()
	
	if resp == 'Yes':
		print('Fuck you.  Proceeding to write data')
	
	elif resp == 'No':
		print('\nOk.  Proceeding to write data for the original query\n')

		# Generate Excel File & Write 2 File
		m0.write_to_excel(df, 'keywordsearchresults_'+ keyword, output_dir, sys_datetime)
		
		# Email Attachment
		print('\n Ready to send you the data via email.  Please input your email address')
		toaddr = input()
		subject = 'SCA Database Query Results for {}'.format(keyword)
		body = 'The results for your query can be found in the attached excel file'
		attachment_filename = 'keywordsearchresults_' + keyword + '.xlsx'
		m0.email_with_attachments(password, toaddr, subject, body, attachment_filename)

	else:
		print('Sorry you did not enter Yes or No.  Proceeding to write data')
		
		# Generate Excel File & Write 2 File
		m0.write_to_excel(df, 'keywordsearchresults_'+ keyword, output_dir, sys_datetime)

		# Email Attachment
		print('Generating email.  Please input your email address')
		toaddr = input()
		subject = 'SCA Database Query Results for {}'.format(keyword)
		body = 'The results for your query can be found in the attachment to this email'
		attachment_filename = 'keywordsearchresults_' + keyword + '.xlsx'
		m0.email_with_attachments(password, toaddr, subject, body, attachment_filename)



keywordsearch(	mydb, 
		table = 'SCA_DATA_2', 
		password = 'Work4starr')



