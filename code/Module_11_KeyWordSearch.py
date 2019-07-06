

sql_query_1kw = '''

        SELECT  filling_date, 
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
        WHERE case_summary LIKE "%{}%"
	'''.format(keyword_1)

sql_query_2kw = '''
	
        SELECT  filling_date, 
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
	WHERE case_summary LIKE "%{}%"
	OR case_summary LIKE "%{}%"
	'''.format(keyword_1, keyword_2)


sql_query_3kw= '''

        SELECT  filling_date, 
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
	WHERE case_summary LIKE "%{}%"
	OR case_summary LIKE "%{}%"
	OR case_summary LIKE "%{}%"
	'''.format(keyword_1, keyword_2, keyword_3)
	


















