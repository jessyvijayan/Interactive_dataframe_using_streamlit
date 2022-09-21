import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from st_aggrid import AgGrid,GridOptionsBuilder,GridUpdateMode

st.title('Retail dataframe')
st.write('This dataframe contains information about xyz retail business')
df = pd.read_csv('Retail_Case.csv',sep=',')
df.drop(['Sl.No','Country'],axis=1,inplace=True)


columns = []
columns = st.sidebar.multiselect('Select required fields',('Order Date','City','Product','Segment','Ship Mode','State','Profit/Loss','Sales'))


## AgGrid
options_builder = GridOptionsBuilder.from_dataframe(df)
options_builder.configure_selection(selection_mode='multiple',use_checkbox=True)
grid_options = options_builder.build()

grid_table = AgGrid(df,height=250,gridOptions=grid_options,update_mode=GridUpdateMode.SELECTION_CHANGED)
st.write('Selected')
selected_row = grid_table['selected_rows']
if selected_row:
    df1 = pd.DataFrame(selected_row,columns=columns)
else:
    df1 = pd.DataFrame(df,columns=columns)
    #df1.drop('_selectedRowNodeInfo',axis=1,inplace=True)
st.dataframe(df1)

## sidebar
st.sidebar.write('Select from the below options for chart')
chart = st.sidebar.selectbox('Select the type of chart',('-','Line chart','Area chart','Scatterplot','Bar chart'))

if chart == 'Line chart':
    x_axis = st.sidebar.selectbox('Select required x-axis',('Order Date','Profit/Loss','Sales'),key=1)
    y_axis = st.sidebar.selectbox('Select required y-axis',('Order Date','Profit/Loss','Sales'),key=2)
    df2 = df1.groupby('Order Date')[['Order Date','Profit/Loss','Sales']].sum()
    df2 = df2.reset_index()
    st.line_chart(data=df2,x=x_axis,y=y_axis)
elif chart == 'Area chart':
    x_axis1 = st.sidebar.selectbox('Select required x-axis',('Order Date','Profit/Loss','Sales'),key=3)
    y_axis1 = st.sidebar.selectbox('Select required y-axis',('Order Date','Profit/Loss','Sales'),key=4)
    df2 = df1.groupby('Order Date')[['Order Date','Profit/Loss','Sales']].sum()
    df2 = df2.reset_index()
    st.area_chart(data=df2,x=x_axis1,y=y_axis1)
elif chart == 'Scatterplot':
    x_axis2 = st.sidebar.selectbox('Select required x-axis',('Profit/Loss','Sales'),key=5)
    y_axis2 = st.sidebar.selectbox('Select required y-axis',('Profit/Loss','Sales'),key=6)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(data=df1,x=x_axis2,y=y_axis2)
    st.pyplot(fig)
elif chart == 'Bar chart':
    x_axis1 = st.sidebar.selectbox('Select required x-axis',('Order Date','Profit/Loss','Sales'),key=3)
    y_axis1 = st.sidebar.selectbox('Select required y-axis',('Order Date','Profit/Loss','Sales'),key=4)
    df2 = df1.groupby('Order Date')[['Order Date','Profit/Loss','Sales']].sum()
    df2 = df2.reset_index()
    st.bar_chart(data=df2,x=x_axis1,y=y_axis1)
else:
    st.sidebar.error('Select chart!!')


