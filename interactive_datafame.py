import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from st_aggrid import AgGrid,GridOptionsBuilder,GridUpdateMode

import streamlit as st

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

if check_password():
    
    st.title('Retail dataframe')
    st.write('This dataframe contains information about xyz retail business')
    df = pd.read_csv('Retail_Case.csv',sep=',')
    df.drop(['Sl.No','Country'],axis=1,inplace=True)

    authenticator.logout('Logout','sidebar')
    st.sidebar.title(f'Welcome {name}')
    
    column = []
    column = st.sidebar.multiselect('Select required fields',('Order Date','City','Product','Segment','Ship Mode','State','Profit/Loss','Sales'))
    df_temp = pd.DataFrame(df,columns=column)
    if column:
    
        ## AgGrid
        options_builder = GridOptionsBuilder.from_dataframe(df_temp)
        options_builder.configure_selection(selection_mode='multiple',use_checkbox=True)
        grid_options = options_builder.build()

        grid_table = AgGrid(df_temp,height=250,gridOptions=grid_options,update_mode=GridUpdateMode.SELECTION_CHANGED)
        st.write('Selected')
        selected_row = grid_table['selected_rows']
        if selected_row:
            df1 = pd.DataFrame(selected_row,columns=column)
        else:
            df1 = pd.DataFrame(df,columns=column)
            #df1.drop('_selectedRowNodeInfo',axis=1,inplace=True)
        st.dataframe(df1)
    else:

        ## AgGrid
        options_builder1 = GridOptionsBuilder.from_dataframe(df)
        options_builder1.configure_selection(selection_mode='multiple',use_checkbox=True)
        grid_options1 = options_builder1.build()

        grid_table1 = AgGrid(df,height=250,gridOptions=grid_options1,update_mode=GridUpdateMode.SELECTION_CHANGED)
        st.write('Selected')
        selected_row1 = grid_table1['selected_rows']
        if selected_row1:
            df1 = pd.DataFrame(selected_row1)
        else:
            df1 = pd.DataFrame(df)
            #df1.drop(' _selectedRowNodeInfo',axis=1,inplace=True)
        st.dataframe(df1[['City','Order Date','Product','Region','Segment','Ship Mode','State','Profit/Loss','Sales']])

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


