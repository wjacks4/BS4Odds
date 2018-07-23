#---------------------------------------------------------------------------#
#             Web Scraper to pull relevant odds information from            # 
#             Action Network Betting Site using the BeautifulSoup           #
#                           Text Parsing library                            #                      
#---------------------------------------------------------------------------#


#--------------------------IMPORT RELEVANT PACKAGES-------------------------#
import urllib
from urllib.request import urlopen
import bs4
from bs4 import BeautifulSoup
from bs4 import Comment
import pandas as pd
import numpy as np
#import csv
#import json
import MySQLdb
from decimal import Decimal, ROUND_HALF_UP

#--------------------------DEFINE URL TO BE ACCESSED-------------------------#
urltest='https://www.actionnetwork.com/mlb/live-odds'


#--------------------------USE BS4 TO DECIPHER HTML-------------------------#
sauce=urllib.request.urlopen(urltest) 
soup=BeautifulSoup(sauce, 'lxml')


#--------------------------BEGIN PARSING - START BY LOOPING THROUGH ALL 'SCRIPT' TAGS UNTIL THE 'SCRIPT' TAG CONTAINING RELEVANT INFO IS FOUND-------------------------#
scripts=soup.find_all('script')
for script in scripts:
	each=script.text
	#print(each)
	print(" ")
	
	#----------------------------EXTRACT INFO PERTAINING TO THE GAME FIRST----------------------#

	gamesfwd=each.split(',"status":')	
	gameelements=len(gamesfwd)
	if gameelements>1:
		for i in range(0,gameelements):
			#print(i)
			gameschunk=gamesfwd[i]
			gamesdata=gameschunk.split('":{"id":')
			gameid=gamesdata[1]
			#print(gameid)
			
			#----------------------------LOOP THROUGH SCRIPT CONTAINING USEFUL GAME INFO UNTIL LIST ENDS----------------------#
			i=i+1
			try:
				teamschunk=gamesfwd[i]
				#print(teamschunk)
				teamsdata=teamschunk.split('"boxscore":')
				teams=teamsdata[0]
			except IndexError as err:
					print("End of list")
			else:
			
				#----------------------------FIND ACTION NETWORK'S TEAM ID#'s----------------------#
				awayidfwd=teams.split(',"home_team_id":')
				awayidchunk=awayidfwd[0]
				awayiddat=awayidchunk.split('"away_team_id":')
				awayid=awayiddat[1]
			
			
				homeidfwd=teams.split(',"home_team_id":')
				homeidchunk=homeidfwd[1]
				homeiddat=homeidchunk.split(',"winning_team_id"')
				homeid=homeiddat[0]
			
				print(gameid)
				print(awayid)
				print(homeid)
		
				#----------------------------AWAY TEAM INFO (abbreviation, logo in .png format, primary color)----------------------#
				awaysplit='{"id":%s' %(awayid)
				awayfullfwd=teams.split(awaysplit)
				awayfullchunk=awayfullfwd[1]
			
				awayabbrfwd=awayfullchunk.split('"abbr":"')
				awayabbrchunk=awayabbrfwd[1]
				awayabbrdat=awayabbrchunk.split('","logo"')
				awayabbr=awayabbrdat[0]
				print(awayabbr)
			
				awaylogofwd=awayfullchunk.split('"logo":"')
				awaylogochunk=awaylogofwd[1]
				awaylogodat=awaylogochunk.split('","primary_color"')
				awaylogo=awaylogodat[0]
				print(awaylogo)
			
			
				#----------------------------HOME TEAM INFO (abbreviation, logo in .png format, primary color)----------------------#
				homesplit='{"id":%s' %(homeid)
				homefullfwd=teams.split(homesplit)
				homefullchunk=homefullfwd[1]
			
				homeabbrfwd=homefullchunk.split('"abbr":"')
				homeabbrchunk=homeabbrfwd[1]
				homeabbrdat=homeabbrchunk.split('","logo"')
				homeabbr=homeabbrdat[0]
				print(homeabbr)
			
				homelogofwd=homefullchunk.split('"logo":"')
				homelogochunk=homelogofwd[1]
				homelogodat=homelogochunk.split('","primary_color"')
				homelogo=homelogodat[0]
				print(homelogo)
				
			
			#----------------------------USING "i" AS AN INDEX, LOOP THROUGH EACH GAME DEFINED EARLIER AND EXTRACT ODDS INFO----------------------#
			try:
				gamedata=gamesfwd[i]
				oddsfwd=gamedata.split('"odds":')
				oddsfull=oddsfwd[1]
				oddschunk=oddsfull.split(',"players":')
				oddsdata=oddschunk[0]
				#print(oddsdata)
			
			except IndexError as err:
				print("End of list")
			
			else:
				oddslist=oddsdata.split('"game":')	
				oddselements=len(oddslist)
				
				mlawayagg=0
				mlhomeagg=0
				spreadhomeagg=0
				spreadawayagg=0
				lineagg=0
				for book in range(1,oddselements):
					#print(oddslist[book])
					
					booktotal=oddslist[book]
					gameodds=booktotal.split('}')
					odds=gameodds[0]
					#print(odds)
					
					#----------------------------MONEYLINE INFO----------------------#
					mlawayfwd=odds.split('"ml_away":')
					mlawaychunk=mlawayfwd[1]
					mlawaydat=mlawaychunk.split(',', 1)
					mlaway=mlawaydat[0]
					
					mlawaydat=float(mlaway)
					mlawayagg=mlawayagg+mlawaydat
					mlawayavg=(mlawayagg/book)
					
					mlhomefwd=odds.split('"ml_home":')
					mlhomechunk=mlhomefwd[1]
					mlhomedat=mlhomechunk.split(',', 1)
					mlhome=mlhomedat[0]
					
					mlhomedat=float(mlhome)
					mlhomeagg=mlhomeagg+mlhomedat
					mlhomeavg=(mlhomeagg/book)
					
					mlaway=int(round(mlawayavg))
					mlhome=int(round(mlhomeavg))
					#print(mlaway)
					#print(mlhome)
					
					
					mldata=np.array(["Money Line", mlaway, mlhome])
					
					oddstable=(mldata)
					
					#----------------------------SPREAD INFO----------------------#
					spreadawayfwd=odds.split('"spread_away":')
					spreadawaychunk=spreadawayfwd[1]
					spreadawaydat=spreadawaychunk.split(',', 1)
					spreadaway=spreadawaydat[0]
					
					spreadawaydat=float(spreadaway)					
					spreadawayagg=spreadawayagg+spreadawaydat
					spreadawayavg=(spreadawayagg/book)
					
					
					spreadhomefwd=odds.split('"spread_home":')
					spreadhomechunk=spreadhomefwd[1]
					spreadhomedat=spreadhomechunk.split(',', 1)
					spreadhome=spreadhomedat[0]
					
					spreadhomedat=float(spreadhome)
					spreadhomeagg=spreadhomeagg+spreadhomedat
					spreadhomeavg=(spreadhomeagg/book)
					
					spreadaway=spreadawayavg
					spreadhome=spreadhomeavg
					#print(spreadaway)
					#print(spreadhome)
					
					spreaddata=np.array(["Spread", spreadaway, spreadhome])
					
					oddstable=np.append(oddstable, spreaddata)
					
					#----------------------------OVER/UNDER (TOTAL) INFO----------------------#
					linefwd=odds.split('"total":')
					linechunk=linefwd[1]
					linedat=linechunk.split(',', 1)
					line=linedat[0]
					#print(line)
					
					linedat=float(line)					
					lineagg=lineagg+linedat
					lineavg=(lineagg/book)
					
					roundline=int(round(lineavg))
					roundhalf=roundline+.5
					
					halfdif=abs(roundhalf-lineavg)
					rounddif=abs(roundline-lineavg)
					
					if halfdif<rounddif:
						line=roundhalf
					else:
						line=roundline
					
					linetable=np.array(["Line", line, line])
					
					
					#----------------------------NOW COLLECT PUBLIC BETTING TREND INFORMATION----------------------#
					
					#----------------------------OVER/UNDER PUBLIC BETTING INFO----------------------#
					pubunderfwd=odds.split('"total_under_public":')
					pubunderchunk=pubunderfwd[1]
					pubunderdat=pubunderchunk.split(',', 1)
					pubunder=pubunderdat[0]
					#print(pubunder)
					
					puboverfwd=odds.split('"total_over_public":')
					puboverchunk=puboverfwd[1]
					puboverdat=puboverchunk.split(',', 1)
					pubover=puboverdat[0]
					#print(pubover)
					
					if pubunder !='null' and pubover !='null':
						publinetable=np.array(["Public percentage", pubunder, pubover])
						
					#----------------------------MONEYLINE PUBLIC BETTING INFO----------------------#
					awaypublicfwd=odds.split('"ml_away_public":')
					awaypublicchunk=awaypublicfwd[1]
					awaypublicdat=awaypublicchunk.split(',', 1)
					awaypublic=awaypublicdat[0]
					
					
					homepublicfwd=odds.split('"ml_home_public":')
					homepublicchunk=homepublicfwd[1]
					homepublicdat=homepublicchunk.split(',', 1)
					homepublic=homepublicdat[0]

					
					if awaypublic !='null' and homepublic !='null':
						publicmldata=np.array(["Public Money Line Pct.", awaypublic, homepublic])
					
						puboddstable=publicmldata
				
					#----------------------------SPREAD PUBLIC BETTING INFO----------------------#
					pubspreadawayfwd=odds.split('"spread_away_public":')
					pubspreadawaychunk=pubspreadawayfwd[1]
					pubspreadawaydat=pubspreadawaychunk.split(',', 1)
					pubspreadaway=pubspreadawaydat[0]
					
					
					pubspreadhomefwd=odds.split('"spread_home_public":')
					pubspreadhomechunk=pubspreadhomefwd[1]
					pubspreadhomedat=pubspreadhomechunk.split(',', 1)
					pubspreadhome=pubspreadhomedat[0]
					
					#print(pubspreadaway)
					#print(pubspreadhome)
					if pubspreadaway != 'null' and pubspreadhome != 'null':
						publicspreaddata=np.array(["Public Spread Pct", pubspreadaway, pubspreadhome])
						
						puboddstable=np.append(puboddstable, publicspreaddata)
					
						
					
						#oddsdf.to_csv('C:/Users/whjac/Downloads/data science/Betting/odds.csv')
				
				
				#----------------------------DEFINE HOME AND AWAY TEAM VARIABLES----------------------#
				away='%s' %(awayabbr)
				home='%s' %(homeabbr)
				
				
				#----------------------------TRY TO FORMAT EACH GAME'S INFO INTO A PANDAS DATAFRAME----------------------#
				#----------------------------SOME GAMES HAVE BLANK INFO, RETURN ERROR MESSAGE IN THESE CASES----------------------#
				try:
					oddsdf=pd.DataFrame(oddstable.reshape(2,3), columns=["Bet", away, home])
					print(oddsdf)
				
					linedf=pd.DataFrame(linetable.reshape(1,3),columns=["Bet", "Over", "Under"])
					print(linedf)
				
					publinedf=pd.DataFrame(publinetable.reshape(1,3), columns=["Bet", "Over", "Under"])
					print(publinedf)
				
					puboddsdf=pd.DataFrame(puboddstable.reshape(2,3), columns=["Bet", away, home])
					print(puboddsdf)
				
				except ValueError as err:
					missing = "Some odds unavailable for %s @ %s" %(away, home)
					print(missing)
				i=i-1
				
				
				#---------------------------------------------------------------------------#
				#																			#
				#																			#
				#           CONNECT TO AN SQL SERVER (THIS PART IS NOT UPDATED)             #
                #    																		#
				#																			#
				#---------------------------------------------------------------------------#
				
				
				
				
										
				##ESTABLISH CONNECTION TO SERVER W/FOLLOWING CREDENTIALS##
				##SERVER: localhost 
				##USERNAME: root 
				##PASSWORD: root
				##DATABASE: book
										
				connection=MySQLdb.connect('localhost', 'root', 'root', 'book')
				cursor=connection.cursor()
				
				##CREATE STRING 'read' THAT CONTAINS SQL CODE STATEMENT TO SELECT DATA FROM DATABASE 'book'						
				
				read="SELECT * FROM mlb_odds_table WHERE game_id=%s" %(gameid)
				
				##EXECUTE SQL STATEMENT 'read'  AND PRINT OUT RESULTS OF QUERY TO TEST##
				cursor.execute(read)
				data=cursor.fetchall()
				connection.commit()
				print(data)
				
				
				##THIS ALL NEEDS TO BE CHANGED...DOESN'T DO WHAT IT NEEDS TO DO##
				if not data:
					MLBoddstable= "INSERT INTO mlb_odds_table(game_id, home_team, away_team, home_moneyline, away_moneyline, home_spread, away_spread, line) VALUES (%s, '%s','%s',%s,%s,%s,%s,%s);" %(gameid, homeabbr, awayabbr, mlhome, mlaway, spreadhome, spreadaway, line)
					cursor.execute(MLBoddstable)
					connection.commit()
				
				else:
					MLBoddsupdate="UPDATE mlb_odds_table SET home_moneyline=%s, away_moneyline=%s, home_spread=%s, away_spread=%s, line=%s WHERE game_id=%s;" %(mlhome, mlaway, spreadhome, spreadaway, line, gameid)
					cursor.execute(MLBoddsupdate)
					connection.commit()