import geopandas
import pandas as pd
import branca
import folium
import streamlit as st
from streamlit_folium import st_folium
from folium.plugins import Fullscreen
import matplotlib.pyplot as plt



def get_map(filtered_df, map_type, incude_bp=True):
    base_lon = 20
    base_lat =47.14
    
    if map_type == "regio":
        # group by megye
        regio_money = (
            filtered_df
            .groupby('megval_regio_nev', as_index=False)
            .agg(
                megitelt_tamogatas=('megitelt_tamogatas', 'sum'),
                projektek_szama=('megitelt_tamogatas', 'count')
            )
            .sort_values(by='megitelt_tamogatas', ascending=False)
            )


        # join to regio
        regio_map = pd.merge(regio, regio_money, left_on='regio', right_on='megval_regio_nev', how='left')

        # select columns
        regio_map = regio_map[['geometry', 'regio', 'megitelt_tamogatas',  'projektek_szama']]
        regio_map["megitelt_tamogatas_text"] = regio_map["megitelt_tamogatas"].apply(lambda x: "{:,.0f} Milliárd Ft".format(x / 1000000000))

        try:
            # no regio info for 
            no_info = regio_money[regio_money['megval_regio_nev'] == ' _Nincs megadva régió']

            no_info_text = f'A térképről hiányzik {int(no_info["megitelt_tamogatas"].iloc[0]/1000000000)} Milliárd Ft'
        except:
            no_info_text = None

        if incude_bp==False:
                regio_map.loc[regio_map["regio"] == "Közép-Magyarország", 'megitelt_tamogatas'] = 0


        # Using the RdYlGn colormap from matplotlib
        colormap = branca.colormap.LinearColormap(
            vmin=regio_map["megitelt_tamogatas"].quantile(0.0),
            vmax=regio_map["megitelt_tamogatas"].quantile(1),
            colors=[plt.cm.Reds(i / 255) for i in range(256)],
            caption="Megitélt támogatás régió szinten",
        )

        m = folium.Map(location=[base_lat, base_lon], zoom_start=8)

        popup = folium.GeoJsonPopup(
            fields=["regio", "megitelt_tamogatas_text" ],
            aliases=["Régió", "Megitélt támogatás" ],
            localize=False,
            labels=True,
            style="background-color: yellow;",

        )

        tooltip = folium.GeoJsonTooltip(
            fields=["regio", "megitelt_tamogatas_text" ],
            aliases=["Régió", "Megitélt támogatás" ],
            localize=False,
            sticky=False,
            labels=True,
            style="""
                background-color: #F0EFEF;
                border: 2px solid black;
                border-radius: 3px;
                box-shadow: 3px;
            """,
            max_width=800,
        )
        g = folium.GeoJson(
            regio_map,
            style_function=lambda x: {
                "fillColor": colormap(x["properties"]["megitelt_tamogatas"])
                if x["properties"]["megitelt_tamogatas"] is not None
                else "transparent",
                "color": "black",
                "fillOpacity": 0.4,
            },
            tooltip=tooltip,
            popup=popup,
        ).add_to(m)
        colormap.add_to(m)

        return m, no_info_text
    if map_type == "megye":
        # group by megye
        # group by megye
        megye_money = (
            filtered_df
            .groupby('megval_megye_nev', as_index=False)
            .agg(
                megitelt_tamogatas=('megitelt_tamogatas', 'sum'),
                projektek_szama=('megitelt_tamogatas', 'count')
            )
            .sort_values(by='megitelt_tamogatas', ascending=False)
            )

        # join megye_monex_to megye
        megye_map = pd.merge(megye, megye_money, left_on='megye', right_on='megval_megye_nev', how='left')

        # select columns
        megye_map = megye_map[['geometry', 'megye', 'megitelt_tamogatas',  'projektek_szama']]
        megye_map["megitelt_tamogatas_text"] = megye_map["megitelt_tamogatas"].apply(lambda x: "{:,.0f} Milliárd".format(x / 1000000000))
        
        try:
            no_info = megye_money[megye_money['megval_megye_nev'] == ' _Nincs megadva megye']

            no_info_text = f'A térképről hiányzik {int(no_info["megitelt_tamogatas"].iloc[0]/1000000000)} Milliárd Ft'
        except:
            no_info_text = None

        if incude_bp==False:
            megye_map.loc[megye_map["megye"] == "Budapest", 'megitelt_tamogatas'] = 0


        # Using the RdYlGn colormap from matplotlib
        colormap = branca.colormap.LinearColormap(
            vmin=megye_map["megitelt_tamogatas"].quantile(0.0),
            vmax=megye_map["megitelt_tamogatas"].quantile(1),
            colors=[plt.cm.Reds(i / 255) for i in range(256)],
            caption="Megitélt támogatás megye szinten",
        )

        m = folium.Map(location=[base_lat, base_lon], zoom_start=8)

        popup = folium.GeoJsonPopup(
            fields=["megye", "megitelt_tamogatas_text"],
            aliases=["Megye", "Megitélt támogatás"],
            localize=False,
            labels=True,
            style="background-color: yellow;",

        )

        tooltip = folium.GeoJsonTooltip(
            fields=["megye", "megitelt_tamogatas_text"],
            aliases=["Megye", "Megitélt támogatás"],
            localize=False,
            sticky=False,
            labels=True,
            style="""
                background-color: #F0EFEF;
                border: 2px solid black;
                border-radius: 3px;
                box-shadow: 3px;
            """,
            max_width=600,
        )
        g = folium.GeoJson(
            megye_map,
            style_function=lambda x: {
                "fillColor": colormap(x["properties"]["megitelt_tamogatas"])
                if x["properties"]["megitelt_tamogatas"] is not None
                else "transparent",
                "color": "black",
                "fillOpacity": 0.4,
            },
            tooltip=tooltip,
            popup=popup,
        ).add_to(m)
        colormap.add_to(m)

        return m, no_info_text
    if map_type == "kisterseg":

        # group by kisterseg
        kisterseg_money = (
            filtered_df
            .groupby('kisterseg_nev', as_index=False)
            .agg(
                megitelt_tamogatas=('megitelt_tamogatas', 'sum'),
                projektek_szama=('megitelt_tamogatas', 'count')
            )
            .sort_values(by='megitelt_tamogatas', ascending=False)
            )

        # select kisterseg rows if kisterseg not in kisterseg money
        # nincsen hozzá nyertes projekt
        nincs_adat = kisterseg[~kisterseg['kisterseg'].isin(kisterseg_money['kisterseg_nev'])]

        # nem megjelenitett tartalom a térképen
        nincs_geo = kisterseg_money[~kisterseg_money['kisterseg_nev'].isin(kisterseg['kisterseg'])]


        kisterseg_map = pd.merge(kisterseg, kisterseg_money, left_on='kisterseg', right_on='kisterseg_nev', how='left')

        kisterseg_map = kisterseg_map[['geometry', 'regio', 'megye', 'kisterseg', 'megitelt_tamogatas',  'projektek_szama']]
        kisterseg_map["megitelt_tamogatas_text"] = kisterseg_map["megitelt_tamogatas"].apply(lambda x: "{:,.0f} Millió".format(x / 1000000))

        try:
            no_info_text = f'A térképről hiányzik {int( sum(nincs_geo["megitelt_tamogatas"])/1000000000)} Milliárd Ft'
        except:
            no_info_text = None

        if incude_bp==False:
            kisterseg_map.loc[kisterseg_map["kisterseg"] == "Budapest", 'megitelt_tamogatas'] = 0


        colormap = branca.colormap.LinearColormap(
            vmin=kisterseg_map["megitelt_tamogatas"].quantile(0.0),
            vmax=kisterseg_map["megitelt_tamogatas"].quantile(1),
            colors=[plt.cm.Reds(i / 255) for i in range(256)],
            caption="Megitélt támogatás kistérség szinten",
        )

        m = folium.Map(location=[base_lat, base_lon], zoom_start=8)

        popup = folium.GeoJsonPopup(
            fields=['kisterseg', "megitelt_tamogatas_text",  'megye', 'regio'],
            aliases=['Kistérség', "Megitélt támogatás",  'Megye', 'Régió'],
            localize=False,
            labels=True,
            style="background-color: yellow;",

        )

        tooltip = folium.GeoJsonTooltip(
            fields=["kisterseg", "megitelt_tamogatas_text", 'megye', 'regio'],
            aliases=["Kistérség", "Megitélt támogatás",  'Megye', 'Régió'],
            localize=False,
            sticky=False,
            labels=True,
            style="""
                background-color: #F0EFEF;
                border: 2px solid black;
                border-radius: 3px;
                box-shadow: 3px;
            """,
            max_width=800,
        )
        g = folium.GeoJson(
            kisterseg_map,
            style_function=lambda x: {
                "fillColor": colormap(x["properties"]["megitelt_tamogatas"])
                if x["properties"]["megitelt_tamogatas"] is not None
                else "transparent",
                "color": "black",
                "fillOpacity": 0.4,
            },
            tooltip=tooltip,
            popup=popup,
        ).add_to(m)
        colormap.add_to(m)


        return m, no_info_text

    if map_type == "varos":

        # group by megye
        varos_money = (
            filtered_df
            .groupby('helyseg_nev_join', as_index=False)
            .agg(
                megitelt_tamogatas=('megitelt_tamogatas', 'sum'),
                projektek_szama=('megitelt_tamogatas', 'count')
            )
            .sort_values(by='megitelt_tamogatas', ascending=False)
            )


        # nincsen hozzá nyertes projekt
        nincs_adat = varos[~varos['varos_nev_join'].isin(varos_money['helyseg_nev_join'])]

        # nem megjelenitett tartalom a térképen
        nincs_geo = varos_money[~varos_money['helyseg_nev_join'].isin(varos['varos_nev_join'])]

        # merge
        varos_map = pd.merge(varos, varos_money, left_on='varos_nev_join', right_on='helyseg_nev_join', how='left')

        varos_map = varos_map[['geometry', 'regio', 'megye', 'kisterseg', 'varos', 'megitelt_tamogatas',  'projektek_szama']]
        varos_map["megitelt_tamogatas_text"] = varos_map["megitelt_tamogatas"].apply(lambda x: "{:,.0f} Millió".format(x / 1000000))
        try:
            no_info_text = f'A térképről hiányzik {int( sum(nincs_geo["megitelt_tamogatas"])/1000000000)} Milliárd Ft'
        except:
            no_info_text = None

        if incude_bp==False:
            varos_map.loc[varos_map["varos"] == "Budapest", 'megitelt_tamogatas'] = 0


        colormap = branca.colormap.LinearColormap(
            vmin=varos_map["megitelt_tamogatas"].quantile(0.0),
            vmax=varos_map["megitelt_tamogatas"].quantile(1),
            colors=[plt.cm.Reds(i / 255) for i in range(256)],
            caption="Megitélt támogatás város szinten",
        )

        m = folium.Map(location=[base_lat, base_lon], zoom_start=8)

        popup = folium.GeoJsonPopup(
            fields=["varos", "megitelt_tamogatas_text", 'kisterseg', 'megye', 'regio'],
            aliases=["Város", "Megitélt támogatás", 'Kistérség', 'Megye', 'Régió'],
            localize=False,
            labels=True,
            style="background-color: yellow;",

        )

        tooltip = folium.GeoJsonTooltip(
            fields=["varos", "megitelt_tamogatas_text", 'kisterseg', 'megye', 'regio'],
            aliases=["Város", "Megitélt támogatás", 'Kistérség', 'Megye', 'Régió'],
            localize=False,
            sticky=False,
            labels=True,
            style="""
                background-color: #F0EFEF;
                border: 2px solid black;
                border-radius: 3px;
                box-shadow: 3px;
            """,
            max_width=800,
        )
        g = folium.GeoJson(
            varos_map,
            style_function=lambda x: {
                "fillColor": colormap(x["properties"]["megitelt_tamogatas"])
                if x["properties"]["megitelt_tamogatas"] is not None
                else "transparent",
                "color": "black",
                "fillOpacity": 0.4,
            },
            tooltip=tooltip,
            popup=popup,
        ).add_to(m)
        colormap.add_to(m)


        return m, no_info_text




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



@st.cache_data(ttl=3600*24)
def read_geojsons():
    regio = geopandas.read_file("map_data/regio.geojson")
    megye = geopandas.read_file("map_data/megye.geojson")
    kisterseg = geopandas.read_file("map_data/kisterseg.geojson")
    varos = geopandas.read_file("map_data/varos.geojson")
    return regio, megye, kisterseg, varos
regio, megye, kisterseg, varos = read_geojsons()



# top 200 winners by megitelt tamogatas first grup by
# top_200_winners = df.groupby('palyazo_neve', as_index=False).agg(megitelt_tamogatas=('megitelt_tamogatas', 'sum')).sort_values(by='megitelt_tamogatas', ascending=False).head(200)['palyazo_neve'].tolist()



@st.fragment
def show_map():
    
    col1, col2, col3, col4 = st.columns([1.4, 1, 1, 1])
    # filter at col1
    with col1:
        
        # check box for filter 
        
        with st.container(border=True):
            # create filter for fejlesztesi program neve, forrás, nyerter top 200, megitelt év
            st.markdown("## Szűrés")
            
            filter_for_fejlesztesi_program_neve = st.checkbox("Filter fejlesztesi program neve")
            
            if filter_for_fejlesztesi_program_neve:
                # filter by fejlesztesi program neve
                fejlesztesi_program_neve = st.multiselect(
                    "Válassz fejlesztési programot:",
                    list(df['fejlesztesi_program_nev'].unique()),
                    default=None,
                )
            filter_for_forras = st.checkbox("Filter forrás")
            if filter_for_forras:        
                # filter by forras
                forras = st.multiselect(
                    "Válassz forrást:",
                    list(df['forras'].unique()),
                    default=None,
                )
            filter_for_megitelt_ev = st.checkbox("Filter megitéslés éve")
            # numeric slider from 2004 to 2025
            
            
            if filter_for_megitelt_ev:
                # filter by megitelt év
                megitelt_ev_slider = st.slider("Válassz megitelt évet:", 2004, 2025, (2004, 2025))
                megitelt_ev = list(range(megitelt_ev_slider[0], megitelt_ev_slider[1]+1))

            
    
    with col2:
        
        with st.container(border=True):
            st.markdown("## Térkép típus")
            # selector for map type
            map_type = st.selectbox(
                "# Válassz térképtípust:",
                ["Régió", "Megye", "Kistérség", "Város"],
            )
        
    # dictory for map type
    map_dict = {
        "Megye": "megye",
        "Régió": "regio",
        "Kistérség": "kisterseg",
        "Város": "varos",
    }
    
    with col3:
        with st.container(border=True):
            st.markdown("## Budapest")

            # radio button for including budapest
            include_budapest = st.radio(
                "Budapest megjelenítése?",
                ["Igen", "Nem"],
                index=1,
            )
            
    with col4:
        with st.container(border=True):
            # refresh button
            refresh_button = st.button("Mehet!")
  
    if refresh_button:
        with st.spinner("Térkép frissítése..."):
            # filtere df
            filtered_df_map = df.copy()
            if filter_for_fejlesztesi_program_neve:
                if fejlesztesi_program_neve:
                    filtered_df_map = filtered_df_map.loc[filtered_df_map['fejlesztesi_program_nev'].isin(fejlesztesi_program_neve)]
            if filter_for_forras:
                if forras:
                    filtered_df_map = filtered_df_map.loc[filtered_df_map['forras'].isin(forras)]
            if filter_for_megitelt_ev:
                if megitelt_ev:
                    filtered_df_map = filtered_df_map.loc[filtered_df_map['megitelt_tamogatas_eve'].isin(megitelt_ev)]
            
            filtered_df_map.reset_index(drop=True, inplace=True)
                    
            
            try:
                m, no_data_info = get_map(filtered_df_map, map_type=map_dict[map_type], incude_bp= True if include_budapest=="Igen" else False)
                Fullscreen(position="topleft").add_to(m)
                if no_data_info:
                    st.markdown(f"### {no_data_info}")
                st_folium(m, height=900,width=1800, returned_objects=[])
            except Exception as e:
                st.markdown(f"### Hiba történt a térkép generálása közben, probáld újra! {e}")


show_map()
