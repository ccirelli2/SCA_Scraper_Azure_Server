#!/usa/bin/python3
# -*- coding: utf-8 -*-




'''LOG - CHANGES / FIXES TO CODE

07.05.2019:
	Instead of inserting the Count object as the page number, we will insert the
	url.  This way we will always have an accurate link to the page from where
	we derived/retreived the data. 
'''


### IMPORT LIBRARIES___________________________________________________________
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
import string
from nltk.stem import *
stemmer = PorterStemmer()
from nltk import corpus
import nltk
from datetime import datetime
import mysql.connector
import logging

### IMPORT MODULES_____________________________________________________________
import Module_0_utility_functions as m0
import Module_1_Scraper_DataPoints as m1
import Module_2_Scraper_Scrape_CaseSummary as m2
import Module_3_Dict_Derived_Values as m3
import Module_4_Main_Scraper_Function as m4
import Module_5_Scraper_Automation as m5
import Module_9_Create_Database as m9

### TARGET OUTPUT DIR
target_output_dir  = r'/home/ccirelli2/Desktop/repositories/sca_scraper_azure_server/Output'
logging_output_dir = r'/home/ccirelli2/Desktop/repositories/sca_scraper_azure_server/logging'

### VERIFY DB & TABLE EXIST > CONNECT____________________________________________
mydb = m9.driver_test_conn_db_table()



### WEB PAGE OBJECTS____________________________________________________________ 
Url = 'http://securities.stanford.edu/filings-case.html?id='


### SCRAPER_______________________________________________________________________

def SCA_data_scraper(Url, add_pages, table, Run_type, report_output_type, password):  
    
    '''
    INPUTS
    Url:            Stanford Law Web Page - Target of scraper                
    Run_type:       Two options, Reset or Start_from_last_lage
    Url:            The web page from which we are scraping data
    add_pages:      Using the 'Start_from_last_page selection, pages_2_add is an additional
                    page to add to the 'Beginning_page' object.  Sometimes the webpage manager
                    choses to insert blank pages into the numerical sequence of pages, which
                    trips up the scraper. 
    report_output   Type of output the user wants to generate.  Used only for the 'Start_from_last_page
                    selection (need to sync up with driver function for gen reports.
    password        email account password (omitt from base script)
    '''
    # Table Object
    table = table
  
    # SCRAPER______________________________________________________________________________________
    
    # RUN-TYPE - RESET
    if Run_type == 'Reset':
        # Reset count values
        Count = 0
        Beginning_page = 100610
        End_page = 107052

        # Clear Database
        print('Clearing data from table {}'.format(table))
        mycursor    = mydb.cursor()
        sql         = "DELETE FROM {} WHERE page_number IS NOT NULL".format(table)     
        # This will not work since we changed the values to varchar()
        mycursor.execute(sql)
        mydb.commit()
        
        # Create Range for Loop
        upper_bound = End_page - Beginning_page
        range_value = range(0, upper_bound)
        
        # Enter For Loop & Scrape All Pages in Range.  
        for x in range_value:
        
            # Increment Count
            Count += 1

            # Progress Recorder - % Total Pages Scraped      
            m0.progress_recorder(Count, upper_bound)

            # Create Beautiful Soup Object per article
            html = urlopen(Url + str(Beginning_page + Count))
            web_page_address = (Url + str(Beginning_page + Count))
            bsObj = BeautifulSoup(html.read(), 'lxml')
            
            # Check to See if Page is Blank
            '''Blank Page:      Don't scrape page and most to next 
               the range of pages from beginning until end.  This creates issues for the scraper.  
               If we hit a blank page, the code will increment the count but skip scraping the page. 
            '''
            Tags = bsObj.find('section', {'id':'company'})
            Defendant = Tags.find('h4').get_text().split(':')[1]
            regex_exp = re.compile(' *[A-Z]+')
            search = re.search(regex_exp, Defendant)

            # If Page Is Not Blank - Scrape
            if bool(search) is True:
                # Load Main Scraper Function
                m4.main_scraper_function(mydb, table, bsObj, web_page_address)
            # Elif Blank - Just increase count & move to the next page
                # do nothing

    

    # RUN-TYPE - START FROM LAST PAGE
    elif Run_type == 'Start_from_last_page':
        # Set Count Objects - Add One Page
        Beginning_page  =           int(m5.get_last_page_scraped(mydb, table))
        End_page        =           Beginning_page + add_pages
        Count           =           0        

        # Status
        print('Scraper starting from count {}'.format(Beginning_page))

        # Create Range for Loop
        upper_bound = End_page - Beginning_page
        range_value = range(0, upper_bound)

        # Enter For Loop & Scrape All Pages in Range.  
        for x in range_value:

            # Count
            Count += 1

            # Progress Recorder - % Total Pages Scraped      
            m0.progress_recorder(Count, upper_bound)

            # Create Beautiful Soup Object per article
            html = urlopen(Url + str(Beginning_page + Count))
            print(Url + str(Beginning_page + Count))
            web_page_address = (Url + str(Beginning_page + Count))
            bsObj = BeautifulSoup(html.read(), 'lxml')

            # Check to See if Page is Blank
            Tags = bsObj.find('section', {'id':'company'})
            Defendant = Tags.find('h4').get_text().split(':')[1]
            regex_exp = re.compile(' *[A-Z]+')
            search = re.search(regex_exp, Defendant)

            # If Page Is Not Blank - Scrape
            if bool(search) is True:
                # Load Main Scraper Function
                m4.main_scraper_function(mydb, table, bsObj, web_page_address)
            # Otherwise, go to next page
            else:
                pass

            
        # Generate Report (Email or Print)-----------------------------------------
        
        # Otherwise print results
        if report_output_type == 'print_results':
            m0.driver_function_post_run_scraper_report(mydb, Beginning_page,
                End_page, 'print_results')

        if report_output_type == 'generate_email':
            # Time Report Generated
            report_gen_time = str(datetime.now())
            
            # Create DataFrame & Write to File
            df_results = m0.driver_function_post_run_scraper_report(mydb, Beginning_page, 
                                                                 End_page, 'dataframe_w_results', target_output_dir, table)
            
	    # Filename + Path for DataFrame as Excel File
            Excel_file = m0.driver_function_post_run_scraper_report(mydb, Beginning_page, 
                                                        End_page, 'dataframe_filename_plus_path', target_output_dir, table)

            # Number Of Companies Added to Table
            num_companies_added = len(df_results['defendant_name'])
            
            # Generate Text File - Body of Emaild
            '''function returns str of filename + path'''
            email_body_filename = m0.driver_function_post_run_scraper_report(mydb, Beginning_page, End_page, 'email_text_body', 
		table = table, target_output_dir = target_output_dir)
            
            # Generate Email
            m0.email_with_attachments(
                    password            = password,   # input for top lvl scraper function 
                    toaddr              = 'chris.cirelli@starrcompanies.com', 
                    subject             = 'Intellisurance Securities Class Action Scraper Update',
                    body                = open(email_body_filename).read(),
                    attachment_filename = Excel_file
                                    )
         

    # Function Returns Nothing
    return None


    # ---------------------------------------------------------------------------------------





# RUN SCRAPER FUNCTION_____________________________________________________________________

'''Run Options:  'Start_from_last_page', 'Reset
   Output Opts:	 'print_results', 'generate_email'	
'''

Scraper_function = SCA_data_scraper(
		   Url, add_pages = 20, table = 'SCA_DATA_2', 
		   Run_type ='Reset', 
                   report_output_type = 'generate_email',
                   password = 'Work4starr')


# Logging
print('\n Generating loggin file')
logging.basicConfig(
        filename = logging_output_dir + 'log.txt', 
        level=logging.DEBUG,
        format='%(asctime)s:%(levelname)s:%(message)s')
print('Log files saved to {}'.format(logging_output_dir))
logging.debug(Scraper_function)



















