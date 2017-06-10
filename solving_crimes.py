import pandas
import geopandas
from geopandas.tools import sjoin
from shapely.geometry import Point
import pylab as pl

print("hi five!")
import code; code.interact(local=locals())
#-----------------------------
# loading data as dataframes
#-----------------------------
suspects_df 	=	pandas.read_csv('evidence/suspects_footprints.csv',sep=',')

victim_df		=	pandas.read_csv('evidence/victims_footprints.csv',sep=',')


print("data loaded")

#-----------------------------
# having fun with data
#-----------------------------
# columns available on dataset
columns		=	suspects_df.columns
print("dataset columns: ",columns)

# head of dataset
header 		=	suspects_df.head(10)
print("dataset header: ",header)

# dtypes
dtypes 		=	suspects_df.dtypes
print("dataset dtypes: ",dtypes)

#unique elements
print("suspects: ",suspects_df['name'].unique())

#len of dataset
print("len: ",suspects_df.count)

#n rows, n columns
print("len: ",suspects_df.shape)
print("have fun: done!")

#-----------------------------
# loading data as geodataframes
#-----------------------------
crs 				=	{'init': 'epsg:4326'}

#suspects
geometry 			=	[Point(xy) for xy in zip(suspects_df.longitud, suspects_df.latitud)]
suspects_gdf		=	geopandas.GeoDataFrame(suspects_df, crs=crs, geometry=geometry)

#victim
geometry 			=	[Point(xy) for xy in zip(victim_df.longitud, victim_df.latitud)]
victim_gdf			=	geopandas.GeoDataFrame(victim_df, crs=crs, geometry=geometry)

#-----------------------------
# manipulating data
#-----------------------------

#slicing usung conditions
beth 				=	suspects_gdf[suspects_gdf['name']=='Beth']
john 				=	suspects_gdf[suspects_gdf['name']=='John']
jacob 				=	suspects_gdf[suspects_gdf['name']=='Jacob']

lorraine 			= 	victim_gdf[victim_gdf['name']=='Lorraine']
martha 				=	suspects_gdf[(suspects_gdf['name']=='Martha')|(suspects_gdf['name']=='martha')]


#manipulation row values
suspects_gdf['name']=	suspects_gdf['name'].str.title()#st.lower()#str.upper()

martha 				=	suspects_gdf[suspects_gdf['name']=='Martha']

#check
print("suspects: ",suspects_gdf['name'].unique())
#-----------------------------
# visualizing
#-----------------------------

#simple plot
suspects_gdf.plot(marker='*',color='green')
pl.show()

#visualizing using CartoDB
suspects_gdf.to_file('results/suspects_footprints/suspects_footprints.shp')
victim_gdf.to_file('results/victims_footprints/victims_footprints.shp')


#-----------------------------
# spatial JOINS 
#-----------------------------

#load settlements
polygons 			=		geopandas.GeoDataFrame.from_file('settlements/settlements_CDMX.shp')
points_in_polys 	= 		sjoin(suspects_gdf, polygons, how='left')

#new geodataframe inspection
#this gdf is the result of 
#match between polygons and points
#play wit it!
points_in_polys.columns

#reprojecting
other_crs = {'init': 'epsg:3395'}
points_in_polys = points_in_polys.to_crs(other_crs)

#other option
points_in_polys = points_in_polys.to_crs(polygons.crs)

import code; code.interact(local=locals())
