import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
#from babel.numbers import format_currency
sns.set(style='dark')

# Menyiapkan DataFrame
def ts_sewa(df):
    ts_sewa = df.groupby(['mnth','yr'])[['dteday','casual', 'registered', 'cnt']].mean().sort_values(by='dteday').reset_index()
    return ts_sewa

def share_report(df):
    share_report = df.groupby('yr_conv')[['casual', 'registered', 'cnt']].sum().reset_index()
    share_report_melted = pd.melt(
    share_report,
    id_vars=['yr_conv'],
    value_vars=['casual', 'registered', 'cnt'],
    var_name='Jenis Penyewaan',
    value_name='Jumlah Penyewaan')
    return share_report_melted

def weathersit_count(df):
    weathersit_count = df.groupby('yr_conv')['weathersit'].value_counts().reset_index()
    return weathersit_count

def create_cluster(df):
    cluster_summary = df.groupby('category', observed=False).agg(
    jumlah_hari = ('cnt','count'),
    rata_cnt = ('cnt','mean'),
    rata_temp = ('temp_conv','mean'),
    rata_hum = ('hum_conv','mean'),
    mode_musim = ('season_conv', lambda x: x.mode().iloc[0]),
    mode_weather = ('weathersit', lambda x: x.mode().iloc[0])).reset_index()
    cluster_summary.columns = ['Cluster', 'Jumlah Hari', 'Rata-Rata Jumlah Penyewaan', 'Rata-Rata Temperatur', 'Rata-Rata Humidity', 'Mode Musim', 'Mode Cuaca']
    cluster_summary = cluster_summary.sort_values(by='Rata-Rata Jumlah Penyewaan', ascending=False).reset_index(drop=True)
    return cluster_summary

def sshare_byweathersit(df):
    share_byweathersit = df.groupby('weathersit')['cnt'].mean().reset_index()
    return share_byweathersit

def total_reg_perhour(df):
    total_reg_perhour = df[(df['workingday']==1)].groupby('hr')['registered'].sum().sort_values(ascending=False).reset_index(name='total_registered')
    return total_reg_perhour

# Menyiapkan DataFrame
all_df = pd.read_csv("day_df.csv")
hour = pd.read_csv("hour_df.csv")

datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)
hour.sort_values(by="dteday", inplace=True) 
hour.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])
    hour[column] = pd.to_datetime(hour[column])

# Membuat Komponen Filter
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTG8cu0RH3RnDMLUFhsFcUy5OK0-qMC3z2ItPdEUe8aXY7cxqb2seJc5Xed&s=10")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]
hour_df = hour[(hour["dteday"] >= str(start_date)) & 
                (hour["dteday"] <= str(end_date))]

ts_sewa = ts_sewa(main_df)
share_report = share_report(main_df)
weathersit_count = weathersit_count(main_df)
cluster_summary = create_cluster(main_df)
share_byweathersit = sshare_byweathersit(main_df)
total_reg_perhour = total_reg_perhour(hour_df)  

# Melengkapi Dashboard dengan Berbagai Visualisasi Data
st.header('Bike Sharing Dashboard :bike:')

# Total Penyewaan Sepeda
st.subheader('Total Penyewaan Sepeda')
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label='Total Penyewaan Sepeda', value=f"{main_df['cnt'].sum():,}")

with col2:
    st.metric(label='Total Penyewaan Sepeda Casual', value=f"{main_df['casual'].sum():,}")

with col3:
    st.metric(label='Total Penyewaan Sepeda Registered', value=f"{main_df['registered'].sum():,}")

fig, ax = plt.subplots(figsize=(16,8))
ax.plot(ts_sewa['dteday'], ts_sewa['casual'], 'o-', label='Penyewaan Tak Terdaftar')
ax.plot(ts_sewa['dteday'], ts_sewa['registered'], 'o-', label='Penyewaan Terdaftar')
ax.plot(ts_sewa['dteday'], ts_sewa['cnt'], 'o-', label='Total Penyewaan')

ax.set_title('Pertumbuhan Penyewaan Sepeda per Kategori')
ax.set_xlabel('Tanggal')
ax.set_ylabel('Jumlah Penyewaan')
ax.set_xticks(ts_sewa['dteday'])
ax.tick_params(axis='x', rotation=45)
ax.grid(True)
ax.legend()
st.pyplot(fig)

    # Perbandingan Jumlah Penyewaan per Jenis Penyewaan (2011-2012)
st.subheader('Perbandingan Jumlah Penyewaan per Jenis Penyewaan')
fig, ax = plt.subplots(figsize=(10, 6))
ax = sns.barplot(data=share_report, x='Jenis Penyewaan', y='Jumlah Penyewaan', hue='yr_conv')

for container in ax.containers:
    ax.bar_label(container, fmt='%d', padding=3)

ax.set_title('Perbandingan Jumlah Penyewaan per Jenis Penyewaan')
ax.set_xlabel('Jenis Penyewaan')
ax.set_ylabel('Jumlah Penyewaan')
ax.legend(title='Tahun')
st.pyplot(fig)

# Perbandingan Jumlah Penyewaan per Jenis Penyewaan (2011-2012)
st.subheader('Jumlah Hari per Index Cuaca')
fig, ax = plt.subplots(figsize=(10, 6))
ax = sns.barplot(data=weathersit_count, x='weathersit', y='count', hue='yr_conv')

for container in ax.containers:
    ax.bar_label(container, padding=3)

ax.set_title('Jumlah Hari per Index Cuaca)')
ax.set_xlabel('Index Cuaca')
ax.set_ylabel('Jumlah Hari')
ax.legend(title='Tahun')
st.pyplot(fig)

# Menampilkan Rata-Rata Jumlah Penyewaan Sepeda per Index Cuaca
st.subheader('Rata-Rata Penyewaan Berdasarkan Index Cuaca')
fig, ax = plt.subplots(figsize=(10, 6))
ax = sns.barplot(data=share_byweathersit, x='weathersit', y='cnt')

for container in ax.containers:
    ax.bar_label(container, padding=3)

ax.set_title('Rata-rata Penyewaan Berdasarkan Index Cuaca)')
ax.set_xlabel('Index Cuaca')
ax.set_ylabel('Rata-rata Penyewaan')
ax.legend(title='Tahun')
st.pyplot(fig)

# Total tenyewaan terdaftar per jam pada hari kerja tahun 2012
st.subheader('Total Penyewaan Terdaftar per Jam pada Hari Kerja')
fig, ax = plt.subplots(figsize=(10, 7))

total_reg_sorted = total_reg_perhour.sort_values(by='total_registered', ascending=False)
y_labels = total_reg_sorted['hr'].astype(str)

bars = ax.barh(y_labels, total_reg_sorted['total_registered'], color='blue')
ax.bar_label(bars, padding=3, rotation=0, fontsize=8)

ax.invert_yaxis()

ax.set_ylabel('Jam (hr)')
ax.set_xlabel('Total peminjaman terdaftar (registered)')
ax.set_title('Total Penyewaan Terdaftar per Jam pada Hari Kerja')
st.pyplot(fig)

# Menampilkan Tabel Cluster Summary
st.subheader('Profil Data Berdasarakan Tingkat Peminjaman')
st.dataframe(cluster_summary)