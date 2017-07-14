# Program to convert traffic ticket received by MassDOT
# This program takes each ticket with multiple violations
# and splits it up so each violation is on a separate row
# It also adds additional fields, such as the full name of each department
# and the day of week for each ticket

# import modules
import csv
import time
import datetime
import calendar
import os

# Define initial variables

row_num = 0
previous_rows =0
#infile = "c:/python27/tickets/Tickets2016.csv"
outfile = "c:/python27/tickets/newtix.csv" 
path = "c:/python27/tickets2/"

# Build a list of the text files to process 
ticketfiles = [ i for i in os.listdir(path) if i[-4:] == '.csv']

print ticketfiles


# Ditionary to look up department code
departments = {
'ABI' : 'Abington Police Dept.',
'ACT' : 'Acton Police Dept.',
'ACU' : 'Acushnet Police Dept.',
'ADA' : 'Adams Police Dept.',
'AGA' : 'Agawam Police Dept.',
'ALF' : 'Alford Police Dept.',
'AME' : 'Amesbury Police Dept.',
'AMH' : 'Amherst Police Dept.',
'APD' : 'AMTRAK Police Dept.',
'AND' : 'Andover Police Dept.',
'GAY' : 'Aquinnah Police Dept.',
'ARL' : 'Arlington Police Dept.',
'ASH' : 'Ashburnham Police Dept.',
'ASB' : 'Ashby Police Dept.',
'ASF' : 'Ashfield Police Dept.',
'ASL' : 'Ashland Police Dept.',
'ATH' : 'Athol Police Dept.',
'ATT' : 'Attleboro Police Dept.',
'AUB' : 'Auburn Police Dept',
'AVO' : 'Avon Police Dept.',
'AYE' : 'Ayer Police Dept.',
'BAM' : 'B&M Railroad Police Dept.',
'BAR' : 'Barnstable Police Dept.',
'BAE' : 'Barre Police Dept.',
'BEC' : 'Becket Police Dept.',
'BED' : 'Bedford Police Dept.',
'BEL' : 'Belchertown Police Dept.',
'BEI' : 'Bellingham Police Dept.',
'BEM' : 'Belmont Police Dept.',
'BCP' : 'Bentley University',
'BER' : 'Berkley Police Dept.',
'BEN' : 'Berlin Police Dept.',
'BRN' : 'Bernardston Police Dept.',
'BEV' : 'Beverly Police Dept.',
'BIL' : 'Billerica Police Dept.',
'BLA' : 'Blackstone Police Dept.',
'BLN' : 'Blandford Police Dept.',
'BOL' : 'Bolton Police Dept.',
'BPA' : 'Boston Police Area A',
'BPB' : 'Boston Police Area B',
'BPC' : 'Boston Police Area C',
'BPD' : 'Boston Police Area D',
'BPE' : 'Boston Police Area E',
'BPF' : 'Boston Police Area F',
'BPG' : 'Boston Police Area G',
'BPH' : 'Boston Police Area H',
'BPJ' : 'Boston Police Area J',
'BPK' : 'Boston Police Area K',
'BPL' : 'Boston Police Area L',
'BPX' : 'Boston Police Special OPS',
'BOU' : 'Bourne Police Dept.',
'BOX' : 'Boxborough Police Dept.',
'BOF' : 'Boxford Police Dept.',
'BOY' : 'Boylston Police Dept.',
'BRA' : 'Braintree Police Dept.',
'BRE' : 'Brewster Police Dept.',
'BRI' : 'Bridgewater Police Dept.',
'BSC' : 'Bridgewater State University',
'BRM' : 'Brimfield Police Dept.',
'BRO' : 'Brockton Police Dept.',
'BTT' : 'Brockton Police Truck Team',
'BRF' : 'Brookfield Police Dept.',
'BRL' : 'Brookline Police Dept.',
'BUC' : 'Buckland Police Dept.',
'BCC' : 'Bunker Hill Com College Police',
'BUR' : 'Burlington Police Dept.',
'CAM' : 'Cambridge Police Dept.',
'CAN' : 'Canton Police Dept.',
'CCC' : 'Cape Cod Community College',
'CAP' : 'Capitol Police Dept.',
'CAR' : 'Carlisle Police Dept.',
'CAV' : 'Carver Police Dept.',
'CHA' : 'Charlemont Police Dept.',
'CHO' : 'Charlton Police Dept.',
'CHT' : 'Chatham Police Dept.',
'CHE' : 'Chelmsford Police Dept.',
'CHL' : 'Chelsea Police Dept.',
'CSH' : 'Cheshire Police Dept.',
'CST' : 'Chester Police Dept.',
'CSF' : 'Chesterfield Police Dept.',
'CHI' : 'Chicopee Police Dept.',
'CHM' : 'Chilmark Police Dept.',
'CLA' : 'Clarksburg Police Dept.',
'CLI' : 'Clinton Police Dept.',
'COH' : 'Cohasset Police Dept.',
'COL' : 'Colrain Police Dept.',
'CON' : 'Concord Police Dept.',
'CNW' : 'Conway Police Dept.',
'CPD' : 'CSX Police Dept',
'CUM' : 'Cummington Police Dept.',
'DAL' : 'Dalton Police Dept.',
'DAN' : 'Danvers Police Dept.',
'DAR' : 'Dartmouth Police Dept.',
'DED' : 'Dedham Police Dept.',
'DRF' : 'Deerfield Police Dept.',
'DEN' : 'Dennis Police Dept.',
'BMC' : 'Department Of Mental Health',
'TSH' : 'Department Of Mental Health',
'CMH' : 'Department Of Mental Health',
'ELC' : 'Department Of Mental Health',
'DMH' : 'Dept. Of Mental Health',
'DIG' : 'Dighton Police Dept.',
'DOU' : 'Douglas Police Dept.',
'DOV' : 'Dover Police Dept.',
'DRA' : 'Dracut Police Dept.',
'DUD' : 'Dudley Police Dept.',
'DUN' : 'Dunstable Police Dept.',
'DUX' : 'Duxbury Police Dept.',
'EAS' : 'E. Bridgewater Police Dept.',
'EBF' : 'E. Brookfield Police Dept.',
'EAL' : 'E. Longmeadow Police Dept.',
'EAH' : 'Eastham Police Dept.',
'EAA' : 'Easthampton Police Dept.',
'EAO' : 'Easton Police Dept.',
'EDG' : 'Edgartown Police Dept.',
'EQR' : 'Egremont Police Dept.',
'DLE' : 'Environmental Police',
'ENV' : 'Environmental Police',
'ERV' : 'Erving Police Dept.',
'ESS' : 'Essex Police Dept',
'EVE' : 'Everett Police Dept.',
'FAI' : 'Fairhaven Police Dept.',
'FAL' : 'Fall River Police Dept.',
'FAM' : 'Falmouth Police Dept.',
'FIT' : 'Fitchburg Police Dept.',
'FSC' : 'Fitchburg State University',
'FLO' : 'Florida Police Dept.',
'FOX' : 'Foxborough Police Dept.',
'FRA' : 'Framingham Police Dept.',
'FSU' : 'Framingham State College',
'FRN' : 'Franklin Police Dept.',
'FRE' : 'Freetown Police Dept.',
'GAR' : 'Gardner Police Dept.',
'GEO' : 'Georgetown Police Dept.',
'GIL' : 'Gill Police Dept.',
'GLO' : 'Gloucester Police Dept.',
'GOS' : 'Goshen Police Dept.',
'GSN' : 'Gosnold Police Dept.',
'GRA' : 'Grafton Police Dept.',
'GRN' : 'Granby Police Dept.',
'GRV' : 'Granville Police Dept.',
'GCC' : 'Greenfield Community College',
'GRF' : 'Greenfield Police Dept.',
'GRO' : 'Groton Police Dept.',
'GRL' : 'Groveland Police Dept.',
'GRE' : 'Gt. Barrington Police Dept.',
'HAD' : 'Hadley Police Dept.',
'HAL' : 'Halifax Police Dept.',
'HAM' : 'Hamilton Police Dept.',
'HAP' : 'Hampden Police Dept.',
'HAN' : 'Hancock Police Dept.',
'HAO' : 'Hanover Police Dept.',
'HAS' : 'Hanson Police Dept.',
'HAR' : 'Hardwick Police Dept.',
'HAV' : 'Harvard Police Dept.',
'HUP' : 'Harvard University',
'HAW' : 'Harwich Police Dept.',
'HAT' : 'Hatfield Police Dept.',
'HAE' : 'Haverhill Police Dept.',
'HW L' : 'Hawley Police Dept.',
'HTH' : 'Heath Police Dept.',
'HIN' : 'Hingham Police Dept.',
'HNS' : 'Hinsdale Police Dept.',
'HOL' : 'Holbrook Police Dept.',
'HOD' : 'Holden Police Dept.',
'HOA' : 'Holland Police Dept.',
'HOI' : 'Holliston Police Dept.',
'HCC' : 'Holyoke Community College',
'HOY' : 'Holyoke Police Dept.',
'HOP' : 'Hopedale Police Dept.',
'HOK' : 'Hopkinton Police Dept.',
'HUB' : 'Hubbardston Police Dept.',
'HUD' : 'Hudson Police Dept.',
'HUL' : 'Hull Police Dept.',
'HUN' : 'Huntington Police Dept.',
'IPS' : 'Ipswich Police Dept.',
'KIN' : 'Kingston Police Dept.',
'LAK' : 'Lakeville Police Dept.',
'LAN' : 'Lancaster Police Dept.',
'LNB' : 'Lanesborough Police Dept.',
'LAW' : 'Lawrence Police Dept.',
'LEE' : 'Lee Police Dept.',
'LEI' : 'Leicester Police Dept.',
'LEN' : 'Lenox Police Dept.',
'LEO' : 'Leominster Police Dept.',
'LEV' : 'Leverett Police Dept.',
'LEX' : 'Lexington Police Dept.',
'LEY' : 'Leyden Police Dept.',
'LIN' : 'Lincoln Police Dept.',
'LIT' : 'Littleton Police Dept.',
'LON' : 'Longmeadow Police Dept.',
'LOW' : 'Lowell Police Dept.',
'LUD' : 'Ludlow Police Dept.',
'LUN' : 'Lunenburg Police Dept.',
'LYN' : 'Lynn Police Dept.',
'LYF' : 'Lynnfield Police Dept.',
'MAL' : 'Malden Police Dept.',
'MAN' : 'Manchester Police Dept.',
'MAS' : 'Mansfield Police Dept.',
'MAR' : 'Marblehead Police Dept.',
'MAI' : 'Marion Police Dept.',
'MAB' : 'Marlborough Police Dept.',
'MAH' : 'Marshfield Police Dept.',
'MAP' : 'Mashpee Police Dept.',
'MLA' : 'Mass College of Liberal Arts',
'MMA' : 'Massachusetts Maritime Police',
'MCC' : 'Massasoit Community College',
'MAT' : 'Mattapoisett Police Dept.',
'MAY' : 'Maynard Police Dept.',
'MBT' : 'MBTA Police Dept.',
'MED' : 'Medfield Police Dept.',
'MEF' : 'Medford Police Dept.',
'MEW' : 'Medway Police Dept.',
'MEL' : 'Melrose Police Dept.',
'MEN' : 'Mendon Police Dept.',
'MER' : 'Merrimac Police Dept.',
'MET' : 'Methuen Police Dept.',
'MP7' : 'Metro Police Blue Hills Dist',
'MP3' : 'Metro Police Fells Dist.',
'MP1' : 'Metro Police Headquarters',
'MP4' : 'Metro Police Lower Basin Dist.',
'MPA' : 'Metro Police Marine Dist.',
'MP8' : 'Metro Police Nantasket Dist.',
'MP6' : 'Metro Police Old Colony Dist.',
'MP9' : 'Metro Police Quabbin/W achuset',
'MP2' : 'Metro Police Revere Dist.',
'MP5' : 'Metro Police Upper Basin Dist.',
'MID' : 'Middleborough Police Dept.',
'MDF' : 'Middlefield Police Dept.',
'MDT' : 'Middleton Police Dept.',
'MIF' : 'Milford Police Dept.',
'MIB' : 'Millbury Police Dept.',
'MII' : 'Millis Police Dept.',
'MIL' : 'Millville Police Dept.',
'MIT' : 'Milton Police Dept.',
'MON' : 'Monroe Police Dept.',
'MOS' : 'Monson Police Dept.',
'MOT' : 'Montague Police Dept.',
'MNT' : 'Monterey Police Dept.',
'MTG' : 'Montgomery Police Dept.',
'WCC' : 'Mt Wachusett Community College',
'NOA' : 'N. Attleboro Police Dept.',
'NOE' : 'N. Reading Police Dept.',
'NAH' : 'Nahant Police Dept.',
'NAN' : 'Nantucket Police Dept.',
'NAT' : 'Natick Police Dept.',
'NPS' : 'National Park Service',
'NEE' : 'Needham Police Dept.',
'NAS' : 'New Ashford Police Dept.',
'NEB' : 'New Bedford Police Dept.',
'NBT' : 'New Braintree Police Dept.',
'NMA' : 'New Marlborough Police Dept.',
'NSA' : 'New Salem Police Dept.',
'NEU' : 'Newbury Police Dept.',
'NEY' : 'Newburyport Police Dept.',
'NET' : 'Newton Police Dept.',
'NOR' : 'Norfolk Police Dept.',
'NOT' : 'North Adams Police Dept.',
'NOH' : 'North Andover Police Dept.',
'NBF' : 'North Brookfield Police Dept.',
'NOM' : 'Northampton Police Dept.',
'NOO' : 'Northborough Police Dept.',
'NOI' : 'Northbridge Police Dept.',
'NFD' : 'Northfield Police Dept.',
'NON' : 'Norton Police Dept.',
'NOW' : 'Norwell Police Dept.',
'NOD' : 'Norwood Police Dept.',
'OAB' : 'Oak Bluffs Police Dept.',
'OAK' : 'Oakham Police Dept.',
'ORA' : 'Orange Police Dept.',
'ORL' : 'Orleans Police Dept.',
'OTI' : 'Otis Police Dept.',
'OOS' : 'Out-of-State Police Dept.',
'OXF' : 'Oxford Police Dept.',
'PAL' : 'Palmer Police Dept.',
'PAX' : 'Paxton Police Dept.',
'PEA' : 'Peabody Police Dept.',
'PEL' : 'Pelham Police Dept.',
'PEM' : 'Pembroke Police Dept.',
'PEP' : 'Pepperell Police Dept.',
'PER' : 'Peru Police Dept.',
'PET' : 'Petersham Police Dept.',
'PHI' : 'Phillipston Police Dept.',
'PIT' : 'Pittsfield Police Dept.',
'PLA' : 'Plainfield Police Dept.',
'PLV' : 'Plainville Police Dept.',
'PLY' : 'Plymouth Police Dept.',
'PLM' : 'Plympton Police Dept.',
'PRI' : 'Princeton Police Dept.',
'PAW' : 'Providence And W orcester Pol',
'PRO' : 'Provincetown Police Dept.',
'QUI' : 'Quincy Police Dept.',
'QCC' : 'Quinsigamond Community Colle',
'RAN' : 'Randolph Police Dept.',
'RAY' : 'Raynham Police Dept.',
'REA' : 'Reading Police Dept.',
'RMV' : 'Registry Of Motor Vehicles',
'REH' : 'Rehoboth Police Dept.',
'REV' : 'Revere Police Dept.',
'RIC' : 'Richmond Police Dept.',
'ROC' : 'Rochester Police Dept.',
'ROK' : 'Rockland Police Dept.',
'ROP' : 'Rockport Police Dept.',
'ROW' : 'Rowe Police Dept.',
'ROL' : 'Rowley Police Dept.',
'ROY' : 'Royalston Police Dept.',
'RUS' : 'Russell Police Dept.',
'RUT' : 'Rutland Police Dept.',
'SAL' : 'Salem Police Dept.',
'SSC' : 'Salem State University Police',
'SAI' : 'Salisbury Police Dept.',
'SAN' : 'Sandisfield Police Dept.',
'SAD' : 'Sandwich Police Dept.',
'SAU' : 'Saugus Police Dept.',
'SAV' : 'Savoy Police Dept.',
'SCI' : 'Scituate Police Dept.',
'SEE' : 'Seekonk Police Dept.',
'SHA' : 'Sharon Police Dept.',
'SHE' : 'Sheffield Police Dept.',
'SHL' : 'Shelburne Police Dept.',
'SHR' : 'Sherborn Police Dept.',
'SHI' : 'Shirley Police Dept.',
'SHW' : 'Shrewsbury Police Dept.',
'SHU' : 'Shutesbury Police Dept.',
'SOM' : 'Somerset Police Dept.',
'SPD' : 'Somerville Housing Authority',
'SOE' : 'Somerville Police Dept.',
'SOU' : 'South Hadley Police Dept.',
'SOT' : 'Southampton Police Dept.',
'SOH' : 'Southborough Police Dept.',
'SOB' : 'Southbridge Police Dept.',
'SOW' : 'Southwick Police Dept.',
'SPE' : 'Spencer Police Dept.',
'SCP' : 'Springfield College',
'SPR' : 'Springfield Police Dept.',
'SCT' : 'Springfield Technical Comm Col',
'SF' : 'State Fire Marshals Office',
'SPA' : 'State Police Academy',
'MV2' : 'State Police CDL Section',
'CVE' : 'State Police Comm Vehicle Enf.',
'CTB' : 'State Police Community Action',
'CAT' : 'State Police Community Action',
'MV5' : 'State Police Compliance Unit',
'C9' : 'State Police Devens C-9',
'GH' : 'State Police General HQ',
'SO1' : 'State Police K-9 Section',
'SM' : 'State Police Marine Unit',
'SO' : 'State Police Miscellaneous',
'SO2' : 'State Police Motorcycle Sect.',
'MV3' : 'State Police Salvage',
'MV1' : 'State Police Special Assignmnt',
'TB2' : 'State Police Traffic Bureau',
'TBH' : 'State Police Traffic Bureau',
'TB4' : 'State Police Traffic Bureau',
'TB3' : 'State Police Traffic Bureau',
'TB' : 'State Police Traffic Bureau',
'TB1' : 'State Police Traffic Bureau',
'AH' : 'State Police Troop A HQ',
'A1' : 'State Police Troop A-1',
'A2' : 'State Police Troop A-2',
'A3' : 'State Police Troop A-3',
'A4' : 'State Police Troop A-4',
'A5' : 'State Police Troop A-5',
'A6' : 'State Police Troop A-6',
'A7' : 'State Police Troop A-7',
'A55' : 'State Police Troop A-SE Team',
'BH' : 'State Police Troop B HQ',
'B1' : 'State Police Troop B-1',
'B2' : 'State Police Troop B-2',
'B3' : 'State Police Troop B-3',
'B4' : 'State Police Troop B-4',
'B5' : 'State Police Troop B-5',
'B6' : 'State Police Troop B-6',
'B55' : 'State Police Troop B-SE Team',
'CH' : 'State Police Troop C HQ',
'C1' : 'State Police Troop C-1',
'C2' : 'State Police Troop C-2',
'C3' : 'State Police Troop C-3',
'C4' : 'State Police Troop C-4',
'C5' : 'State Police Troop C-5',
'C6' : 'State Police Troop C-6',
'C7' : 'State Police Troop C-7',
'C8' : 'State Police Troop C-8',
'C55' : 'State Police Troop C-SE Team',
'DH' : 'State Police Troop D HQ',
'D1' : 'State Police Troop D-1',
'D2' : 'State Police Troop D-2',
'D3' : 'State Police Troop D-3',
'D4' : 'State Police Troop D-4',
'D5' : 'State Police Troop D-5',
'D6' : 'State Police Troop D-6',
'D7' : 'State Police Troop D-7',
'D55' : 'State Police Troop D-SE Team',
'EM1' : 'State Police Troop E HQ',
'EH' : 'State Police Troop E HQ',
'E1' : 'State Police Troop E-1',
'E2' : 'State Police Troop E-2',
'E3' : 'State Police Troop E-3',
'E4' : 'State Police Troop E-4',
'E55' : 'State Police Troop E-55 Team',
'ETC' : 'State Police Troop ETC',
'FH' : 'State Police Troop F HQ',
'HH' : 'State Police Troop H HQ',
'H1' : 'State Police Troop H-1',
'H2' : 'State Police Troop H-2',
'H3' : 'State Police Troop H-3',
'H4' : 'State Police Troop H-4',
'H5' : 'State Police Troop H-5',
'H6' : 'State Police Troop H-6',
'H7' : 'State Police Troop H-7',
'H55' : 'State Police Troop H-SE Team',
'I5' : 'State Police Troop I-5',
'I55' : 'State Police Troop I-55 Team',
'I6' : 'State Police Troop I-6',
'I7' : 'State Police Troop I-7',
'I8' : 'State Police Troop I-8',
'IH' : 'State Police Troop IH HQ',
'TU' : 'State Police Tunnels',
'EM4' : 'State Police Tunnels',
'MV4' : 'State Police Vehicle Services',
'STE' : 'Sterling Police Dept.',
'STO' : 'Stockbridge Police Dept.',
'STN' : 'Stoneham Police Dept.',
'STU' : 'Stoughton Police Dept.',
'STW' : 'Stow Police Dept.',
'STR' : 'Sturbridge Police Dept.',
'SUD' : 'Sudbury Police Dept.',
'SUN' : 'Sunderland Police Dept.',
'SUT' : 'Sutton Police Dept.',
'SWA' : 'Swampscott Police Dept.',
'SWN' : 'Swansea Police Dept.',
'TAU' : 'Taunton Police Dept.',
'TDC' : 'Templeton Developmental Cent',
'TEM' : 'Templeton Police Dept.',
'TEW' : 'Tewksbury Police Dept.',
'TIS' : 'Tisbury Police Dept.',
'TOL' : 'Tolland Police Dept.',
'TOP' : 'Topsfield Police Dept.',
'TOW' : 'Townsend Police Dept.',
'TRU' : 'Truro Police Dept.',
'TUF' : 'Tufts University',
'TYN' : 'Tyngsborough Police Dept.',
'TYR' : 'Tyringham Police Dept.',
'UMA' : 'Univ Of Mass Amherst',
'UMB' : 'Univ Of Mass Boston',
'UMD' : 'Univ Of Mass Dartmouth',
'UML' : 'Univ Of Mass Lowell',
'UMW' : 'Univ Of Mass W orcester',
'UPT' : 'Upton Police Dept.',
'UXB' : 'Uxbridge Police Dept.',
'WES' : 'W. Boylston Police Dept.',
'WEG' : 'W. Bridgewater Police Dept.',
'WBR' : 'W. Brookfield Police Dept.',
'WNB' : 'W. Newbury Police Dept.',
'WEP' : 'W. Springfield Police Dept.',
'WSB' : 'W. Stockbridge Police Dept.',
'WTI' : 'W. Tisbury Police Dept.',
'WAK' : 'Wakefield Police Dept.',
'WAL' : 'Wales Police Dept.',
'WAP' : 'Walpole Police Dept.',
'FSS' : 'Walter E. Ferneld State School',
'WAT' : 'Waltham Police Dept.',
'WAR' : 'Ware Police Dept.',
'WAE' : 'Wareham Police Dept.',
'WAN' : 'Warren Police Dept.',
'WRW' : 'Warwick Police Dept.',
'WAS' : 'Washington Police Dept.',
'WAO' : 'Watertown Police Dept',
'WAY' : 'Wayland Police Dept.',
'WEB' : 'Webster Police Dept.',
'WEL' : 'Wellesley Police Dept.',
'WEF' : 'Wellfleet Police Dept.',
'WEN' : 'Wendell Police Dept.',
'WEH' : 'Wenham Police Dept.',
'WSH' : 'Westboro State Hospital',
'WEU' : 'Westborough Police Dept.',
'WNC' : 'Western New England College',
'WED' : 'Westfield Police Dept.',
'WSC' : 'Westfield State University',
'WER' : 'Westford Police Dept.',
'WHT' : 'Westhampton Police Dept.',
'WEM' : 'Westminster Police Dept.',
'WET' : 'Weston Police Dept.',
'WST' : 'Westport Police Dept.',
'WEW' : 'Westwood Police Dept.',
'WEY' : 'Weymouth Police Dept.',
'WHA' : 'Whately Police Dept.',
'WHI' : 'Whitman Police Dept.',
'WIL' : 'Wilbraham Police Dept.',
'WIB' : 'Williamsburg Police Dept.',
'WIA' : 'Williamstown Police Dept.',
'WIM' : 'Wilmington Police Dept.',
'WIN' : 'Winchendon Police Dept.',
'WIC' : 'Winchester Police Dept.',
'WID' : 'Windsor Police Dept.',
'WIT' : 'Winthrop Police Dept.',
'WOB' : 'Woburn Police Dept.',
'WSO' : 'Worcester County Sheriff',
'WOR' : 'Worcester Police Dept.',
'WSU' : 'Worcester State University',
'WOT' : 'Worthington Police Dept.',
'WRE' : 'Wrentham Police Dept.',
'WSS' : 'Wrentham State School',
'YAR' : 'Yarmouth Police Dept.',
'ZZZ' : 'ZZZUnknown Police Dept.',
''    : 'None Listed'}

BostonNeighborhoods = ['WEST ROXBURY', 'ROSLINDALE', 'JAMAICA PLAIN', 'EAST BOSTON', 'DORCHESTER', 'CHARLESTOWN/BOS', 'BRIGHTON', 'SOUTH BOSTON', 'HYDE PARK', 'ROXBURY/BOSTON']

ticket_list  = {}

 
# Count the number of violations on the ticket. SHould be between 1 and 4.
def violation_count(row):
  if row[25].strip() != '':
      violations = 4
  elif row[21].strip() != "":
      violations = 3
  elif row[17].strip() != "":
      violations = 2
  else:
      violations = 1
  #print row
  if row[0] == "":
  	  violations =0
  else:
  	 #ticket_list[row[0]] = violations
  	 pass
  return violations

#checks to see whether there were additional violations recorded on previous tickets with the same citation number.
#Each ticket can only fit four violations, so police sometimes have to issue multiple tickets to cover all the violations.
def check_previous_tickets(ticket,violations):
	if ticket in ticket_list:
		old_violations = ticket_list.pop(ticket)
		ticket_list[ticket] = violations + old_violations
	else: 
	    ticket_list[ticket] = violations
	    old_violations = 0
	#print ticket
	#print old_violations
	#time.sleep(.5)
	return old_violations


# Help cleanup the initial data
def cleanup_row(row):
  for column in range(len(row)):
    if isinstance(row[column], str):
      row[column]=row[column].encode('utf-8')
      row[column]=row[column].strip()
      row[column]=row[column].replace(",",";")
      row[column]=row[column].replace("/r/n","")
      row[column]=row[column].replace("/n","")
      row[column]=row[column].replace("\\","")
      row[column]=row[column].replace("  "," ")
      row[column]=row[column].upper()
  #print row
  return row

# Calculate the speed someone is going over the limit
def calc_speed_dif(speed_observed,speed_posted):
  try:
    if 4<int(speed_posted)<100 and 5<int(speed_observed)<270:
      speed_dif = int(speed_observed) - int(speed_posted)
      if speed_dif<1:
        speed_dif = ""
    else:
      speed_dif = ""
  except ValueError:
    speed_dif =""
  return speed_dif

#Function to get new date info
def convert_date(old_date):
  new_date = old_date.split("/")
  if len(new_date)==3:
    try:
      year=int(new_date[2])
      day=int(new_date[1])
      month=int(new_date[0])
      date_object = datetime.date(year,month,day)
      dayofweek = calendar.day_name[date_object.weekday()]
      date_mysql = str(date_object)
    except TypeError:
      dayofweek = ""
      year=""
      day=""
      month = ""
      date_mysql = ""
  else:
      dayofweek = ""
      year=""
      day=""
      month = ""
      date_mysql = ""
  return [year,day,month,dayofweek,date_mysql]



def process_file(infile,file_year):
  print file_year
  global previous_rows
  row_num = 0
  with open(infile, 'rb') as csvfile:
    current_file = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in current_file:   
      if row_num>0:
        new_row = cleanup_row(row)
        violation_number = violation_count(row)
        if new_row[4].strip() in BostonNeighborhoods: new_row[4] = "BOSTON"
        if new_row[11].strip() in BostonNeighborhoods: new_row[11] = "BOSTON"
        if violation_number>0:   #and new_row[0] != "MISSING"
        	ticket_number = new_row[0] + new_row[2] + new_row[4] + new_row[10] + new_row[11]
        	old_violations = check_previous_tickets(ticket_number,violation_number)
        else:
        	old_violations = 0
        for violation in range(violation_number):
          new_row = row[:13]
          new_row.append(row[13+(4*violation)])
          new_row.append(row[14+(4*violation)])
          new_row.append(row[15+(4*violation)])
          new_row.append(row[16+(4*violation)])
          new_row.append(calc_speed_dif(row[15+(4*violation)],row[16+(4*violation)]))
          new_row.extend(convert_date(new_row[2]))
          new_row.append(file_year)
          new_row.append(departments.get(new_row[6]))
          new_row.append(row[6]+row[7])    
          new_row.append(violation+1+old_violations)
          if (violation_number + old_violations) == 1:
            new_row.append("SINGLE")
          else:
            new_row.append("MULTIPLE")
          new_row.insert(0,(row_num+previous_rows))
          row_num += 1
          #if new_row[1] == "MISSING": 
          #	 print new_row
          with open(outfile,'ab') as csvfile:
          	rowwriter = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
          	rowwriter.writerow(new_row)    
          #print new_row
          #time.sleep(1.5)
      else:
        row_num +=1
    print " I just processed " + str(row_num -1) + "  more rows."
    previous_rows += row_num - 1   
    #print ticket_list

header_row =['Row', 'Citation','Type','Date','Hour','Location','Search','DeptCode','Badge','Race','Sex','Age','ViolatorTown','State','Violation','Description','SpeedObserved','SpeedPosted','SpeedOver','Year','Month','Day','WeekDay','DateSQL','YearFile','DeptName','OfficerID','ViolationNumber','ViolationsOnTicket']

#print "here is the header row"
#open(outfile, "wb")
print "test"
with open(outfile,'wb') as csvfile:
  rowwriter = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
  rowwriter.writerow(header_row)
        

print "starting...."
for file in ticketfiles:
  file_year = file[7:11]
  print file_year
  process_file(path+file,file_year)
  print "I processed " + str(previous_rows) + " rows of data - not counting the header for " + str(file_year) + "."
print "the end"

