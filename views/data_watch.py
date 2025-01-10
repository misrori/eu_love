import streamlit as st
import pandas as pd

@st.cache_data()
def read_data():
    df = pd.read_parquet('eu_money/all_eu_money.parquet')
    df = df.loc[df['megitelt_tamogatas'].notna()]
    df = df.sort_values(by='megitelt_tamogatas', ascending=False)
    return df
df = read_data()



@st.fragment
def show_stock_filter():

    # Oszlop leírások
    column_descriptions = {
        'fejlesztesi_program_nev': 'Fejlesztési program neve',
        'forras': 'Forrás',
        'kiiras_eve': 'Kiírás éve',
        'op_kod': 'Operatív program kódja',
        'konstrukcio_nev': 'Konstrukció neve',
        'konstrukcio_kod': 'Konstrukció kódja',
        'palyazo_neve': 'Pályázó neve',
        'projekt_cime': 'Projekt címe',
        'megval_regio_nev': 'Megvalósítási régió neve',
        'megval_megye_nev': 'Megvalósítási megye neve',
        'kisterseg_nev': 'Kistérség neve',
        'helyseg_nev': 'Helység neve',
        'tam_dont_datum': 'Támogatási döntés dátuma',
        'megitelt_tamogatas': 'Megítélt támogatás',
        'id_palyazat': 'Pályázat azonosítója',
        'load_date': 'Betöltési dátum',
        'jaras_nev': 'Járás neve'
    }

    # Oszlopok sorrendje
    filter_column_order = list(column_descriptions.keys())

    # Visszafelé leképezés a leírásokhoz
    reverse_mapping = {v: k for k, v in column_descriptions.items()}

    # Multi-select widget a szűrni kívánt oszlopok kiválasztásához
    selected_descriptions = st.multiselect("Válassz oszlopokat:", list(column_descriptions.values()))

    # Kiválasztott leírások leképezése az eredeti oszlopnevekre
    selected_columns = [reverse_mapping[desc] for desc in selected_descriptions]

    # Dinamikus szűrők megjelenítése a kiválasztott oszlopok alapján
    filters = {}
    for col in selected_columns:
        if df[col].dtype in ['float64', 'int64']:
            min_value, max_value = float(df[col].min()), float(df[col].max())
            value_range = st.slider(
                f"Válassz értéktartományt - {column_descriptions[col]}",
                min_value=min_value,
                max_value=max_value,
                value=(min_value, max_value)
            )
            filters[col] = value_range
        else:
            unique_values = df[col].unique().tolist()
            selected_values = st.multiselect(f"Válassz értékeket - {column_descriptions[col]}", unique_values)
            filters[col] = selected_values

    # Szűrők alkalmazása a DataFrame-re
    filtered_df = df.copy()
    for col, condition in filters.items():
        if df[col].dtype in ['float64', 'int64']:
            filtered_df = filtered_df[(filtered_df[col] >= condition[0]) & (filtered_df[col] <= condition[1])]
        elif condition:
            filtered_df = filtered_df[filtered_df[col].isin(condition)]


    # Szűrt DataFrame megjelenítése
    if len(filtered_df) > 0:
        st.dataframe(filtered_df)
    else:
        st.write("Nincsenek megfelelő adatok a megadott szűrők alapján.")
        
      # Csoportosításhoz oszlopok kiválasztása
    selected_group_descriptions = st.multiselect(
        "Válassz oszlopokat csoportosításhoz:",
        list(column_descriptions.values())
    )
    selected_group_columns = [reverse_mapping[desc] for desc in selected_group_descriptions]

    
    
    # Csoportosítás és összegzés végrehajtása
    if st.button("Csoportosítás"):
        if selected_group_columns:
            grouped_df = (filtered_df
            .groupby(selected_group_columns, as_index=False)
            .agg(megitelt_tamogatas = ('megitelt_tamogatas', 'sum'))
            .sort_values(by='megitelt_tamogatas', ascending=False)
            .reset_index()
            )
            st.dataframe(grouped_df, hide_index=True)
    else:
        st.write("Válassz legalább egy oszlopot a csoportosításhoz.")

show_stock_filter()