#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 13:55:23 2023

@author: ewansaw
"""
#!pip install --upgrade scipy
#!pip install statsmodels
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import os
from mpl_toolkits import mplot3d
    
#define current working directory
cwd = os.getcwd()

#import file and define the dataframe
path = os.path.join(cwd, "Kay_ST15_material_properties_Kopperdahl_linear_2002.csv")
df = pd.read_csv(path)

df = df.sort_values(['Z', 'Y', 'X'], ascending=[True, True, True])

#find smallest positive value for density in data
pos_min = df[df['DENS']>0]['DENS'].min()

#change negative values of density in data into smallest positive value for density
df['DENS'] = df['DENS'].apply(lambda x: pos_min if x < 0 else x)

'''
#create grid 
#want rougly 300 points in z direction
#use grid points to save values within their cube (+1 in each dimension )
may need to change this in future to make step size in z dimension different!! 
'''
#stepsize, h (i.e. spacing between grid points) 
h = 5

# create dictionary of all grid coordinates
dims = {'X', 'Y', 'Z'}
coords = {}

for dim in dims:
    coords[dim] = np.arange(min(df[f'{dim}']), max(df[f'{dim}']), h)
    
#create 3d grid where xx, yy, zz represent the coordinates of the points for each respective dimension
xx, yy, zz = np.meshgrid(coords['X'], coords['Y'], coords['Z'], indexing='ij')  

#create array to save density data
vals = np.zeros(xx.shape)
stds = np.zeros(xx.shape)

#loop through the coordinates in each dimension
for i in range(len(vals)): #X
    for j in range(len(vals[0])): #Y
        for k in range(len(vals[0][0])): #Z
            print('x =', xx[i][j][k])
            print('y =', yy[i][j][k])
            print('z =', zz[i][j][k])
            print('=========')
            
            #find the rows of data within our dataframe which fall within to the desired 3D volume
            #i.e. current coord within loop + one step size in each dimension            
            mask = df[df['X'].between(xx[i][j][k], xx[i][j][k] + h, 'left')]
            mask = mask[mask['Y'].between(yy[i][j][k], yy[i][j][k] + h, 'left')]
            mask = mask[mask['Z'].between(zz[i][j][k], zz[i][j][k] + h, 'left')]
            print(mask)
            print('=========')
            
            #now want average values of density and young's modulus from these rows
            dens = mask.loc[:, 'DENS'].mean()
            std = mask.loc[:, 'DENS'].std()
            print(dens)
            
            stds[i][j][k] = std
            
            #update vals array for average density values
            if np.isnan(dens) == True:
                vals[i][j][k] = np.nan #arbitrary choice just to make the plotting look nicer, change in future
            else:
                vals[i][j][k] = dens

#%%
fig = plt.figure()
ax = plt.axes(projection='3d')

# Data for three-dimensional scattered points
zdata = zz
xdata = np.sin(zdata) + 0.1 * np.random.randn(100)
ydata = np.cos(zdata) + 0.1 * np.random.randn(100)
ax.scatter3D(coords['X'], coords['Y'], coords['Z'], c=vals, cmap='Greens');
        
        
#%% notes
'''
collect means and ALSO variances of each grid point ??
 but this is also subject to the amount of data you have available within each volume, which can be 
 arbitrary, depending on the mesh
'''     
 
        
        
        
        
        
        
        