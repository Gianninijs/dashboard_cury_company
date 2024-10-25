

# bibliotecas necessárias
import pandas as pd
import re
import plotly.express as px  # gráficos
import streamlit as st
from datetime import datetime
from PIL import Image
import folium
from streamlit_folium import folium_static 

# import dataset
#df = pd.read_csv( 'dataset/train.csv' )

#colocar um ícone no início da aba
st.set_page_config( page_title='Visão Empresa' , page_icon='📈', layout='wide')
 
def clean_code( df1 ):
    """
    Esta função tem a responsabilidade de limpar o dataframe

    Tipos de limpeza:
    1. Remoção dos dados 'NaN'
    2. Mudança do tipo de coluna de dados
    3. Remoção dos espaços das variáveis texto
    4. Formatação da coluna datas
    5. Limpeza da coluna de tempo ( remoção do texto da variavel numérica )
    Input: Dataframe
    Output: Dataframe
    """
    # removendo o 'NaN '
    linhas = df1['Festival'] != 'NaN '
    df1 = df1.loc[ linhas , : ].copy()
    
    linhas = df1['Delivery_person_Age'] != 'NaN '
    df1 = df1.loc[ linhas , : ].copy()
    
    linhas = df1['Road_traffic_density'] != 'NaN '
    df1 = df1.loc[ linhas , : ].copy()
    
    linhas = df1['City'] != 'NaN '
    df1 = df1.loc[ linhas , : ].copy()
    
    linhas = df1['Delivery_person_Ratings'] != 'NaN '
    df1 = df1.loc[ linhas  , : ].copy()
    
    linhas = df1['multiple_deliveries'] != 'NaN ' 
    df1 = df1.loc[ linhas , : ].copy()
    
    
    # removendo espaços 
    df1.loc[ : , 'ID'] = df1.loc[: , 'ID'].str.strip()
    
    df1.loc[ : , 'Road_traffic_density'] = df1.loc[ : , 'Road_traffic_density'].str.strip()
    
    df1.loc[ : , 'Type_of_order'] = df1.loc[ : , 'Type_of_order'].str.strip()
    
    df1.loc[ : , 'Type_of_vehicle'] = df1.loc[ : , 'Type_of_vehicle'].str.strip()
    
    df1.loc[ : , 'City'] =  df1.loc[ : , 'City'].str.strip()
    
    df1.loc[ : , 'Festival'] = df1.loc[ : , 'Festival'].str.strip()
    
    
    
    # Conversão de texto/categoria/string para números inteiros
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype( int )
    
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype( float )
    
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype( int )
    
    #df1['Time_taken(min)'] = df1['Time_taken(min)'].astype( int )
    
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')
    
    # comando para remover o texto do número //  # Extract the number as a string and convert it to an integer
#    df1 = df1.reset_index ( drop=True )
#    for i in range ( len(df1) ):
#       df1.loc[i , 'Time_taken(min)'] = int(re.findall( #r'\d+' , df1.loc[ i , 'Time_taken(min)'] )[0])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply( lambda x: x.split( '(min) ')[1] )
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype( int )
    
    return df1
# ==========================================               
# Import dataset + cópia para 'df1'
# ==========================================
df = pd.read_csv( 'dataset/train.csv' )
#df1  = df.copy() o 'df1' vem agora após a LIMPEZA

# ==========================================               
# Limpando os Dados
# ==========================================
df1 = clean_code( df )



# ==========================================
#  Funções 
# ==========================================
def order_metric( fig ): 
    cols = ['ID' , 'Order_Date']
    df_aux = df1.loc[: , cols].groupby(       ['Order_Date']).count().reset_index()
    fig=px.bar( df_aux, x='Order_Date' , y='ID')
    
    return fig

def traffic_order_share( df1 ):
     df_aux = ( df1.loc[: , ['ID' , 'Road_traffic_density']]
               .groupby( ['Road_traffic_density'])
               .count()
               .reset_index() )
     df_aux['entregas_perc'] = ( df_aux['ID'] / df_aux['ID'].sum() )     
     fig=px.pie(df_aux, values='entregas_perc' , names='Road_traffic_density' , hole=0.6)  #
               
     return fig

def traffic_order_city( df1 ):
            df_aux = ( df1.loc[: , ['ID' , 'Road_traffic_density' , 'City' ]]
                          .groupby(['City' , 'Road_traffic_density' ])
                          .count()
                          .reset_index() )
                
            df_aux = df_aux.loc[df_aux['City'] != 'NaN', : ]
                            # gráfico
            fig=px.scatter( df_aux, x='City' , y='Road_traffic_density' , size='ID', color='City')
                            
            return fig 

def order_by_week( df1 ):
            df1['week_of_year'] = df1['Order_Date'].dt.strftime( '%U' ) # extrai n0 da semana do ano começando pela segunda e salva na nova coluna
            cols = ['ID' , 'week_of_year']
            df_aux = ( df1.loc[: , cols]
                          .groupby( ['week_of_year'] )
                          .count()
                          .reset_index() )      
            fig=px.line( df_aux, x='week_of_year' , y='ID')
             
            return fig

 # Quantidade de pedidos por semana / Número únicos de entregadores por semana
def order_share_by_week( df1 ):
    df_aux1 = df1.loc[: , ['ID' , 'week_of_year']].groupby( ['week_of_year'] ).count().reset_index()
    df_aux2 = df1.loc[: , ['week_of_year' , 'Delivery_person_ID']].groupby(['week_of_year']).nunique().reset_index()               
    df_aux = pd.merge(df_aux1, df_aux2, how='inner')
    df_aux['order_by_delivery'] = df_aux1['ID'] /  df_aux2['Delivery_person_ID']
                
    fig=px.line(df_aux, x='week_of_year' , y='order_by_delivery')
            
    return fig 

def country_maps( df1 ): # a própria função faz o mapa
        cols= ['City' , 'Road_traffic_density' , 'Delivery_location_longitude', 'Delivery_location_latitude']
        df_aux = ( df1.loc[: , cols ]
                      .groupby( ['City' , 'Road_traffic_density'])
                      .median()
                      .reset_index() )  
        map = folium.Map() 
        for index, location_info in df_aux.iterrows(  ):
            folium.Marker( [location_info['Delivery_location_latitude'],
                            location_info['Delivery_location_longitude']],                  
                            popup=location_info[['City','Road_traffic_density']]).add_to( map )
            #preciso usar o FOLUIM_STATIC importar aqui e instalar no terminal pip install streamlit-foluim
        folium_static( map, width=1024, height=600 ) # CUIDADO, se esse folium estiver identado no for, vai aparecer 4 gráficos
    
# return None --> não precisa de retorno aqui




    


# ----------------------------Início da Estrutura Lógica do Código----------------------------





# ==========================================
# SideBar no Streamlit 
# ==========================================

st.header( 'Marketplace - Visão Empresa' ) 

# imagem 
#image_path =r'C:\Users\giann\Documents\repos\Analista de Dados\Comunidade DS AD\ftc_programacao_python\delivery_01.png'
image = Image.open( 'delivery_01.png' )
st.sidebar.image( image, width=220 )

# título da sidebar
st.sidebar.markdown( '# Cury Company' )
st.sidebar.markdown( '## Fastest Delivery in Town!' ) 

# linha que separa o sidebar 
st.sidebar.markdown( """---""" ) 

st.sidebar.markdown( '## Selecione uma data limite' )
date_slider = st.sidebar.slider(
    'Ajuste o intervalo',
    value=datetime( 2022, 4, 13),
    min_value=datetime( 2022, 2, 11),
    max_value=datetime( 2022, 4, 13),
    format='DD-MM-YYYY'
) 
# exibir o valor / vou deixar comentado, e usar onde quiser depois
#st.header( date_slider )  

# linha que separa o sidebar 
st.sidebar.markdown( """---""" ) 

# segundo filtro 
traffic_options = st.sidebar.multiselect( 
    'Quais as condições de trânsito?',
    ['Low', 'Medium' , 'High', 'Jam'],
    default=['Low', 'Medium' , 'High', 'Jam']
)
st.sidebar.markdown( """---""" ) 
weather_conditions = st.sidebar.multiselect(
    'Quais as condições de clima?',
    ['conditions Cloudy', 'conditions Fog', 'conditions Sandstorms', 'conditions Stormy' , 'conditions Sunny', 'conditions Windy'],
    default=['conditions Cloudy', 'conditions Fog', 'conditions Sandstorms', 'conditions Stormy' , 'conditions Sunny', 'conditions Windy']
)

st.sidebar.markdown( """---""" )
st.sidebar.markdown( '### Powered by Giannini J. Silva' ) 

# ==========================================
#Conectar gráficos ao Filtro  
# ==========================================

# Filtro de Data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]
# coloco esse código abaixo para ver se as coisas estão funcionando, e coloco o slide na última data, precisa mostrar todos os dados no dataframe
#st.dataframe( df1 ) 

# Filtro de Tipo de Trânsito
linhas_selecionadas = df1['Road_traffic_density'].isin( traffic_options )
df1 = df1.loc[linhas_selecionadas, : ]
 
# Filtro de Tipo de Condições Climáticas
linhas_selecionadas = df1['Weatherconditions'].isin( weather_conditions )
df1 = df1.loc[linhas_selecionadas , :]

# ==========================================
# Layout no Streamlit  - Abas 
# ==========================================

# Criação das Tabs
tab1, tab2, tab3 = st.tabs( ['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'] )

with tab1: # ABA 'Visão Gerencial
     
    with st.container():
         fig=order_metric( df1 )
         st.markdown( '# Quantidade de pedidos por dia' ) 
         st.plotly_chart( fig, use_container_width=True ) 
       
   

# Criar as DUAS COLUNAS para colocar os dois próximos gráficos segundo o layout  
    with st.container():
        col1, col2 = st.columns( 2 ) # Colunas dentro do Container acima
        with col1:  
            fig=traffic_order_share( df1 )
            # gráfico de pizza
            st.markdown( '# Traffic Order Share' ) 
            st.plotly_chart( fig, use_container_width=True )
            
            
    
# gráfico 3 na segunda coluna
        with col2:
            # gráfico de bolha
            st.markdown( '# Traffic Order City' ) # mostro o título 
            fig=traffic_order_city( df1 ) # criar a figura  
            st.plotly_chart( fig, use_container_width=True ) # plotar a fig 
            


with tab2:
    with st.container():
        st.markdown( '# Order by Week' ) # mostrar o título 
        fig=order_by_week( df1 ) # criar a figura
        st.plotly_chart( fig, use_container_width=True ) # ploitar a figura
        
        
        
    
    with st.container():
        st.markdown( '# Order Share by Week' ) # mostrar o título 
        fig=order_share_by_week( df1 ) # criar figura
        st.plotly_chart( fig, use_container_width=True )   # plotar figura       
        
        
    
with tab3:
    st.markdown( '# Country Maps' ) # mostrar título
    country_maps( df1 ) # criar e mostrar ( nesse caso )
