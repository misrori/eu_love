import streamlit as st
import pandas as pd
import plotly.express as px

if 'grouped_df' not in st.session_state:
    st.session_state.grouped_df = None    

@st.cache_data(ttl=3600*24)
def read_data():
    df = pd.read_parquet('all_eu_money.parquet')
    df = df.loc[df['megitelt_tamogatas'].notna()]
    df['megitelt_tamogatas'] = df['megitelt_tamogatas'].astype(int)
    df = df.sort_values(by='megitelt_tamogatas', ascending=False)
    df['tam_dont_datum'] = pd.to_datetime(df['tam_dont_datum'], format='%Y.%m.%d').dt.date
    df['megitelt_tamogatas_eve'] = pd.to_datetime(df['tam_dont_datum'], format='%Y.%m.%d').dt.year
    df.reset_index(drop=True, inplace=True)
    return df
df = read_data()



@st.fragment
def show_grouped_data():
    st.markdown("#### Ebben a részben csoportosíthatod az adatokat, és megtekintheted az eredményeket.")
    
    column_descriptions = {
        'palyazo_neve': 'Pályázó neve',
        'fejlesztesi_program_nev': 'Fejlesztési program neve',
        'forras': 'Forrás',
        'op_kod': 'Operatív program kódja',
        'konstrukcio_nev': 'Konstrukció neve',
        'konstrukcio_kod': 'Konstrukció kódja',
        'megval_regio_nev': 'Megvalósítási régió neve',
        'megval_megye_nev': 'Megvalósítási megye neve',
        'kisterseg_nev': 'Kistérség neve',
        'helyseg_nev': 'Helység neve',
        'jaras_nev': 'Járás neve',
        'megitelt_tamogatas_eve': 'Megítélt támogatás éve'
    }

    reverse_mapping = {v: k for k, v in column_descriptions.items()}
    selected_descriptions = st.multiselect("Válassz oszlopokat:", list(column_descriptions.values()))
    selected_columns = [reverse_mapping[desc] for desc in selected_descriptions]

    if st.button("Csoportosítás"):
        if selected_columns:
            grouped_df = (df
                          .groupby(selected_columns, as_index=False)
                          .agg(
                              megitelt_tamogatas=('megitelt_tamogatas', 'sum'),
                              number_of_projects=('megitelt_tamogatas', 'count')
                          )
                          .sort_values(by='megitelt_tamogatas', ascending=False)
                          )
            grouped_df = grouped_df.rename(columns=column_descriptions)
            grouped_df = grouped_df.rename(columns={'megitelt_tamogatas': 'Megítélt támogatás', 'number_of_projects': 'Projektek száma'})
            grouped_df.reset_index(drop=True, inplace=True)
            st.dataframe(grouped_df)
            st.session_state.grouped_df = grouped_df
    else:
        st.write("Válassz legalább egy oszlopot a csoportosításhoz.")
    
    # display grouped data
    if st.session_state.grouped_df is not None:
        grouped_df = st.session_state.grouped_df
        
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            x_axis = st.selectbox("X tengely:", grouped_df.columns, index=0)
        with col2:
            y_axis = st.selectbox("Y tengely:", grouped_df.columns, index=2)
        # if data has at least 5 columns, display color selector
        if grouped_df.shape[1] > 3:
            with col3:
                color = st.selectbox("Szín:", grouped_df.columns, index=None)
        else:
            color = None
        with col4:
            top_n = st.number_input("Megjelenítendő sorok száma:", min_value=1, max_value=len(grouped_df), value=100 if len(grouped_df) > 100 else len(grouped_df))
        
        if color:
            fig = px.bar(grouped_df.head(top_n), x=x_axis, y=y_axis, color=color,
                        title=f'Megítélt támogatások csoportosítása {x_axis} szerint' )
            fig.update_layout( xaxis_title=x_axis, yaxis_title=y_axis, height=900, legend_title=color)  

        else: 
            fig = px.bar(grouped_df.head(top_n), x=x_axis, y=y_axis,
                            title=f'Megítélt támogatások csoportosítása {x_axis} szerint' )
            fig.update_layout( xaxis_title=x_axis, yaxis_title=y_axis, height=900)  
        st.plotly_chart(fig)


show_grouped_data()
