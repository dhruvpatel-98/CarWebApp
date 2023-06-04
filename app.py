import pandas as pd
import streamlit as st
import plotly_express as px

df = pd.read_csv('vehicles_us.csv')
#read the data
df['manufacturer'] = df['model'].apply(lambda x: x.split()[0])
df['is_4wd'] = df['is_4wd'].where(df['is_4wd'] != 1.0 , 'yes')
df['is_4wd'] = df['is_4wd'].fillna('no')
df['model_year'] = df['model_year'].fillna(df.groupby('model')
['model_year'].transform('median'))
df['cylinders'] = df['cylinders'].fillna(df.groupby('model')
['cylinders'].transform('median'))
df['odometer'] = df['odometer'].fillna(df.groupby('model_year')
['odometer'].transform('median'))
df['paint_color'] = df['paint_color'].fillna('No info')
#replace four wheel drive values with yes and no
st.title('Figures on car sales')

st.header('Data viewer')
st.dataframe(df)
#There will be two plots
#A scatterplot should be able to show a strong or week correlation between two variables
#The two variables ill select is price and odometer
#I was able to observe that odometer contains some missing information so i will remove the cars with missing values
#I will be able to observe the strength of the correlation between these variables
#i will now create a data set with all missing values in the odometer collumn removed

df_model_year = df.dropna(subset = ['odometer'])
st.header('Scatter Plot: Price VS Odometer (make a selection to see cars by condition)')
cond_list = sorted(df['condition'].unique())
condition = st.selectbox(
    label= 'select condition',
    options= cond_list,
    index= cond_list.index('new')
)
df_conditon = df[df['condition'] == condition]

fig = px.scatter(df_conditon , 
                 x = 'odometer', 
                 y = 'price', 
                 color = 'condition',
                 title = 'Odometer vs Price (Make selection to see different car condition selections)',
                 hover_name = 'model'
                 )
#also contains name of car
st.write(fig)

st.header('Histogram: Manfacturer and odometer readings')

manufac_list = sorted(df['manufacturer'].unique())
manufacturer_1 = st.selectbox('Select manufacturer 1',
                              manufac_list, index=manufac_list.index('chevrolet'))

manufacturer_2 = st.selectbox('Select manufacturer 2',
                              manufac_list, index=manufac_list.index('hyundai'))
mask_filter = (df['manufacturer'] == manufacturer_1) | (df['manufacturer'] == manufacturer_2)
df_filtered = df[mask_filter]
normalize = st.checkbox('Normalize histogram', value=True)
if normalize:
    histnorm = 'percent'
else:
    histnorm = None
st.write(px.histogram(df_filtered,
                      x='odometer',
                      nbins=40,
                      color='manufacturer',
                      histnorm=histnorm,
                      barmode='overlay'))

