
import streamlit as st
import pandas as pd
import plotly.express as px


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

def get_infoplots(df):

    # Assuming df is your DataFrame
    df['tam_dont_datum'] = pd.to_datetime(df['tam_dont_datum'])
    # Extract year and month
    df['year_month'] = df['tam_dont_datum'].dt.to_period('M')
    grouped_df= (
        # df where tamogatas eve nagyobb 2004
        df[df['tam_dont_datum'].dt.year > 2004]         
        .groupby(['year_month', 'fejlesztesi_program_nev'], as_index=False)
        .agg(
            megitelt_tamogatas=('megitelt_tamogatas', 'sum'),
            number_of_projects=('megitelt_tamogatas', 'count')
        )
        .reset_index()
    )
    grouped_df['megitelt_tamogatas'] = grouped_df['megitelt_tamogatas'] / 1000000000

    grouped_df['year_month'] = grouped_df['year_month'].astype(str)

    fig = px.bar(
        grouped_df,
        x='year_month',
        y='megitelt_tamogatas',
        color='fejlesztesi_program_nev',
        title='Megitélt támogatás havonta fejlesztési programonként',
        labels={'year_month': 'Év-hónap', 'megitelt_tamogatas': 'Megitélt támogatás', 'fejlesztesi_program_nev': 'Fejlesztési program'},
        barmode='group'
    )

    fig.update_layout(
        barmode='stack',
        plot_bgcolor='white',
        xaxis_title='Év',
        yaxis_title='Megitélt támogatás összege (Milliárd  Ft)',
        legend_title='Fejlesztési program',
        xaxis=dict(
            tickangle=45
        ),
        height=800
    )

    plot1 = fig
############################################################################xx


    grouped_df= (
        df
        .groupby('fejlesztesi_program_nev', as_index=False)
        .agg(
            megitelt_tamogatas=('megitelt_tamogatas', 'sum'),
            number_of_projects=('megitelt_tamogatas', 'count')
        )    
        .sort_values(by='megitelt_tamogatas', ascending=False)
        .reset_index()
    )
    # show it in millárd
    grouped_df['megitelt_tamogatas'] = grouped_df['megitelt_tamogatas'] / 1000000000

    # Adatok ábrázolása Plotlyval
    fig = px.bar(grouped_df, x='fejlesztesi_program_nev', y='megitelt_tamogatas',
                labels={'fejlesztesi_program_nev': 'Fejlesztesi program nev', 'megitelt_tamogatas': 'Megítélt támogatás (milliárd Ft)'},
                title='Megítélt támogatás (milliárd Ft) fejlesztesi programonként')
    # update the background to white
    fig.update_layout(
        barmode='stack',
        plot_bgcolor='white',
        xaxis_title='Fejlesztési program',
        yaxis_title='Megitélt támogatás (Milliárd  Ft)',
        xaxis=dict(
            tickangle=45
        ),
        height=600
    )

    plot2 = fig
############################################################################xx


    grouped_df= (
        df
        .groupby('megval_regio_nev', as_index=False)
        .agg(
            megitelt_tamogatas=('megitelt_tamogatas', 'sum'),
            number_of_projects=('megitelt_tamogatas', 'count')
        )    
        .sort_values(by='megitelt_tamogatas', ascending=False)
        .reset_index()
    )
    # show it in millárd
    grouped_df['megitelt_tamogatas'] = grouped_df['megitelt_tamogatas'] / 1000000000

    # Adatok ábrázolása Plotlyval
    fig = px.bar(grouped_df, x='megval_regio_nev', y='megitelt_tamogatas',
                labels={'megval_regio_nev': 'Régió', 'megitelt_tamogatas': 'Megítélt támogatás (milliárd Ft)'},
                title='Megítélt támogatás (milliárd Ft) régiónként')
    # update the background to white
    fig.update_layout(
        barmode='stack',
        plot_bgcolor='white',
        xaxis_title='Régió',
        yaxis_title='Megitélt támogatás (Milliárd  Ft)',
        xaxis=dict(
            tickangle=45
        )
    )
    plot3 = fig
############################################################################xx

    grouped_df= (
        df
        .groupby('megval_megye_nev', as_index=False)
        .agg(
            megitelt_tamogatas=('megitelt_tamogatas', 'sum'),
            number_of_projects=('megitelt_tamogatas', 'count')
        )    
        .sort_values(by='megitelt_tamogatas', ascending=False)
        .reset_index()
    )
    # show it in millárd
    grouped_df['megitelt_tamogatas'] = grouped_df['megitelt_tamogatas'] / 1000000000

    # Adatok ábrázolása Plotlyval
    fig = px.bar(grouped_df, x='megval_megye_nev', y='megitelt_tamogatas',
                labels={'megval_megye_nev': 'Megye', 'megitelt_tamogatas': 'Megítélt támogatás (milliárd Ft)'},
                title='Megítélt támogatás (milliárd Ft) megyénként')
    # update the background to white
    fig.update_layout(
        barmode='stack',
        plot_bgcolor='white',
        xaxis_title='Megye',
        yaxis_title='Megitélt támogatás (Milliárd  Ft)',
        xaxis=dict(
            tickangle=45
        )
    )
    plot4 = fig
############################################################################xx

    grouped_df= (
        df
        .groupby('palyazo_neve', as_index=False)
        .agg(
            megitelt_tamogatas=('megitelt_tamogatas', 'sum'),
            number_of_projects=('megitelt_tamogatas', 'count')
        )    
        .sort_values(by='megitelt_tamogatas', ascending=False)
        .head(50)
        .reset_index()
    )
    # show it in millárd
    grouped_df['megitelt_tamogatas'] = grouped_df['megitelt_tamogatas'] / 1000000000

    # Adatok ábrázolása Plotlyval
    fig = px.bar(grouped_df, x='palyazo_neve', y='megitelt_tamogatas',
                labels={'palyazo_neve': 'Pályázó neve', 'megitelt_tamogatas': 'Megítélt támogatás (milliárd Ft)'},
                title='Top 50 legtöbb támogatást elnyerő pályázó ')
    # update the background to white
    fig.update_layout(
        barmode='stack',
        plot_bgcolor='white',
        xaxis_title='Pályázó',
        yaxis_title='Megitélt támogatás (Milliárd  Ft)',
        xaxis=dict(
            tickangle=45
        ),
        height=1000
    )
    plot5 = fig
############################################################################xx

    return plot1, plot2, plot3, plot4, plot5



@st.fragment
def show_basic_info():

    megiteles_eve_plot, fejlesztesi_program_nev_plot, megval_regio_nev_plot, megval_megye_nev_plot, palyazo_neve_plot = get_infoplots(df)

    # Összegző gondolat
    total_projects = df['id_palyazat'].nunique()
    total_funding = df['megitelt_tamogatas'].sum() / 1e9
    st.markdown(f"# Összesen {total_funding:,.2f} milliárd Ft EU-s támogatás érkezett Magyarországra.  {total_projects:,.0f} projekt kapott támogatást.")

    # Plot elrendezés
    with st.container(border=True):
        st.plotly_chart(megiteles_eve_plot)

    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):

            st.plotly_chart(megval_regio_nev_plot)
    with col2:
        with st.container(border=True):
            st.plotly_chart(megval_megye_nev_plot)

    with st.container(border=True):
        st.plotly_chart(fejlesztesi_program_nev_plot)
    with st.container(border=True):
        st.plotly_chart(palyazo_neve_plot)

show_basic_info()