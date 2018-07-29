import csv
from difflib import get_close_matches

positions = []

with open('PlayerPositions.csv') as csvfile:
     PlayerPositions = csv.reader(csvfile, delimiter=',')
     for row in PlayerPositions:
         positions.append(row)

#print positions["Cristiano Ronaldo"]

matchData = {}

with open('SPIs.csv') as csvfile:
     SPI = csv.reader(csvfile, delimiter=',')
     for row in SPI:
         mkey = row[3]+"#"+row[4]
         matchData[mkey] = row

#print matchData["Burnley#Everton"]
events = []

with open('final_events.tsv') as csvfile:
     eventss = csv.reader(csvfile, delimiter='\t')
     for row in eventss:
        row[0] =row[0].split(",")[0:3]
        events.append(row)   
        #print row

def TS(time,hplrs,aplrs):
    ho = 0
    hd = 0
    ao = 0
    ad = 0
    for a in hplrs[0]:            
        ho += a[0] * ((time-a[1])*-4/9 + 100)/100
    for a in hplrs[1]:            
        hd += a[0] * ((time-a[1])*-4/9 + 100)/100
    for a in aplrs[0]:            
        ao += a[0] * ((time-a[1])*-4/9 + 100)/100
    for a in aplrs[1]:            
        ad += a[0] * ((time-a[1])*-4/9 + 100)/100
    #h = inh * ((time-pupdate)*-4/9 + 100)/100
    #hSPI = r[0] * ((time)*-4/9 + 100)/100 - r[3] * ((time)*-4/9 + 100)/100
    #aSPI = r[2] * ((time)*-4/9 + 100)/100 - r[1] * ((time)*-4/9 + 100)/100
    return(ho,hd,ao,ad)

def searchPlayer(club,name):
    poss = []
    poss2 = []
    #print name, club
    for player in positions:
        if player[3] == club:
            poss.append(player[1])
            poss2.append(player)
           
    #print poss2

    #print name
    ze_name = get_close_matches(name,poss,len(poss), 0)
    #print ze_name
    for i in poss2:
        #print ze_name[0], i[1]
        if ze_name[0] == i[1]:
            posi = i[4]
            break
    #print posi
    posi = posi.replace(" ", "")
    if posi in ["SW","RWB","RB","RCB","CB","LCB","LB","LWB"]:
        return ('d')
    elif posi == 'gk':
        return ('g')
    elif posi in ['RF','CF','LF','RS','ST','LS']:
        return ('f')
    else:
        return ('m')


def putMatchinTable(parts,matchCode):
    x = 0
    matchEvents = []
    
    for i in events:
        #print i[0][0]
        if i[0][0] == matchCode:
            #print "WOOOOOHOOOOOO"
            matchEvents.append(i)
            
        if(len(matchEvents) > 0)and(i[0][0] != matchCode):
            break
    #print matchEvents
    
    data = matchData[matchEvents[0][0][1]+"#"+matchEvents[0][0][2]]
    #5,6
    h = (float(data[5]))
    #hdSPI = hoSPI
    a = (float(data[6]))
    #adSPI = aoSPI
    '''inh = h
    ina = a
    t_r = [h/2,h/2,a/2,a/2] #[HOME_OFFENSIVE,HOME_DEFENSIVE,AWAY_OFFENSIVE,AWAY_DEFENSIVE]
    hSPI = t_r[0]-t_r[3]
    aSPI = t_r[2] - t_r[1]'''

    hplrs = [[[h/10,0],[h/10,0],[h/10,0],[h/20,0],[h/20,0],[h/20,0],[h/20,0],[0,0],[0,0],[0,0]],[[0,0],[0,0],[0,0],[h/20,0],[h/20,0],[h/20,0],[h/20,0],[h/10,0],[h/10,0],[h/10,0]]]
    aplrs = [[[a/10,0],[a/10,0],[a/10,0],[a/20,0],[a/20,0],[a/20,0],[a/20,0],[0,0],[0,0],[0,0]],[[0,0],[0,0],[0,0],[a/20,0],[a/20,0],[a/20,0],[a/20,0],[a/10,0],[a/10,0],[a/10,0]]]

    table = []
    
    minTBC = 90/parts
    part = 0
    gd = 0
    pupdate = 0
    #hSPI,aSPI,h,a = 0,0,0,0
    print len(matchEvents)

    while part!= parts:
        
        for event in matchEvents:
            event[2]=int(event[2])
            '''print event[2],(0+part*minTBC),(part*minTBC+minTBC)
            if event[2]>(0+part*minTBC):
                print "yeahhhh"
            if (int(event[2]) <= (part*minTBC+minTBC)):
                print "yeahhhh"'''
            if (event[2] > (0+part*minTBC)) and (event[2] <= (part*minTBC+minTBC)):
                #print "HIII"
                if event[4] == 'goal':
                    if event[1] == 'away':
                        gd -= 1
                    else:
                        gd += 1
                elif event[4] == 'sub':
                    #hSPI,aSPI,h,a = TS(event[2],pupdate,hSPI,aSPI,h,a,inh,ina)
                    pupdate = event[2]
                    if event[1] == 'away':
                        club = event[0][2]
                        p1 = searchPlayer(club,event[5])
                        p2 = searchPlayer(club,event[6])
                        tbr = 0
                        if p1 == 'd':
                            for i in range(7,10):
                                if aplrs[1][i][1]==0:
                                    aplrs[1][i][0] = 0
                                    tbr = i
                        elif p1 == 'f':
                            for i in range(0,3):
                                if aplrs[0][i][1]==0:
                                    aplrs[0][i][0] = 0
                                    tbr = i
                        elif p1 == 'm':
                            for i in range(3,7):
                                if aplrs[1][i][1]==0:
                                    aplrs[1][i][0] = 0
                                    aplrs[0][i][0] = 0
                                    tbr = i
                        if p2 == 'd':
                            aplrs[1][tbr][0] = a/10
                            aplrs[1][tbr][1] = event[2]
                        elif p2 == 'm':
                            aplrs[1][tbr][0] = a/20
                            aplrs[0][tbr][0] = a/20
                            aplrs[0][tbr][1] = event[2]
                            aplrs[1][tbr][1] = event[2]
                        elif p2 == 'f':
                            aplrs[0][tbr][0] = a/10
                            aplrs[0][tbr][1] = event[2]
                                                        
                    else:
                        club = event[0][1]
                        p1 = searchPlayer(club,event[5])
                        p2 = searchPlayer(club,event[6])
                        tbr = 0
                        if p1 == 'd':
                            for i in range(7,10):
                                if hplrs[1][i][1]==0:
                                    hplrs[1][i][0] = 0
                                    tbr = i
                        elif p1 == 'f':
                            for i in range(0,3):
                                if hplrs[0][i][1]==0:
                                    hplrs[0][i][0] = 0
                                    tbr = i
                        elif p1 == 'm':
                            for i in range(3,7):
                                if hplrs[1][i][1]==0:
                                    hplrs[1][i][0] = 0
                                    hplrs[0][i][0] = 0
                                    tbr = i
                        if p2 == 'd':
                            hplrs[1][tbr][0] = h/10
                            hplrs[1][tbr][1] = event[2]
                        elif p2 == 'm':
                            hplrs[1][tbr][0] = h/20
                            hplrs[0][tbr][0] = h/20
                            hplrs[0][tbr][1] = event[2]
                            hplrs[1][tbr][1] = event[2]
                        elif p2 == 'f':
                            hplrs[0][tbr][0] = h/10
                            hplrs[0][tbr][1] = event[2]
                    
        ho,hd,ao,ad = TS(event[2],hplrs,aplrs)
        #print h,a
        pupdate = minTBC+minTBC*part
        table.append([minTBC+minTBC*part,ho,hd,ao,ad,gd])
        #print pupdate
        part += 1
    return (table)                
    
    

print putMatchinTable(3,"hCrslmeI")
'''for i in range(1,3):
    print i'''
#print searchPlayer('Swansea', 'Bony W.')                
                    


         
