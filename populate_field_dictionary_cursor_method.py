# populate existing field(s) in target table from same field in other input table,
#   using common field as key
# *assumes unique id values in key field*


import arcpy as a
from arcpy import env


# access current mxd
a.mapping.MapDocument('CURRENT')   # use if running within ArcMap
mxd = a.mapping.MapDocument('CURRENT')   # use if running within ArcMap


gdb = ""
a.env.workspace = gdb


################################################################################

######  FUNCTION DOESN'T CHANGE  vvvvvvvvvvvvvvvvvv

# DEFINE FUNCTION
def popfields(targettable,targetkey,targetwhere,jointable,joinkey,joinwhere,joinfields,wipe):
				# joinfields should be list of field names like ["name1","name2"] ^

	# assume field(s) to be populated already exist in target table
	
	# wipe existing values in target fields? Y/N?
	if wipe == "Y":
		# wipe target field values in target table
		cursordata = 	targettable
		cursorfields =	[]
		for f in joinfields:
			cursorfields.append(f)  # assume all join fields exist in target table
		whereclause = 	targetwhere
		with a.da.UpdateCursor(cursordata, cursorfields, whereclause) as cursor:
			for row in cursor:
				i = 0
				while i < len(joinfields):
					row[i] = None
					i += 1
				cursor.updateRow(row)
		del cursor

	# build dictionary of values in join fields
	join_dict = {}
	cursordata =	jointable
	cursorfields =	[joinkey]
	for f in joinfields:
		cursorfields.append(f)
	whereclause = 	joinwhere
	with a.da.SearchCursor(cursordata, cursorfields, whereclause) as cursor:
		for row in cursor:
			joinvalues = []
			i = 1
			while i <= len(joinfields):
				joinvalues.append(row[i])
				i +=1
			join_dict[row[0]] = joinvalues
	del cursor

	# cursor to populate join fields in target table from dictionary
	cursordata = 	targettable
	cursorfields =	[targetkey]
	for f in joinfields:
		cursorfields.append(f)  # assume all join fields exist in target table
	whereclause = 	targetwhere
	with a.da.UpdateCursor(cursordata, cursorfields, whereclause) as cursor:
		for row in cursor:
			if row[0] in join_dict:		# account for target records with no match
				i = 1
				while i <= len(joinfields):
					row[i] = join_dict[row[0]][i-1]
					i += 1
				cursor.updateRow(row)
			else:
				pass
	del cursor
	del join_dict

######  FUNCTION DOESN'T CHANGE  ^^^^^^^^^^^^^^^^^^^


# function inputs

targettable =		""  # table file path
targetkey =			""  # key field name
targetwhere	=		""  # where clause - optional - leave as is, or complete

jointable =			""  # table file path
joinkey =			""  # key field name
joinwhere = 		""  # where clause - optional - leave as is, or complete

joinfields = 		[
					"---field1---",
					"---field2---",
					"---field3---",
					]
				
wipe =				""	# populate either "Y" or "N" - 
					# if yes, existing field values will be wiped before populating


# RUN JOIN FIELDS FUNCTION
popfields(targettable,targetkey,targetwhere,jointable,joinkey,joinwhere,joinfields,wipe)