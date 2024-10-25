# bibliotecas necessárias
import pandas as pd #pandas vai ajudar a importar o dado com apelido pd

#import plotly.graph_objects as go 
# from haversine import haversine
import re
import numpy as np
import plotly.express as px  # gráficos
import streamlit as st
from datetime import datetime
from PIL import Image
import folium
from streamlit_folium import folium_static 
from haversine import haversine
import plotly.graph_objects as go

#colocar um ícone no início da aba
st.set_page_config( page_title='Visão Restaurantes' , page_icon='🍽️', layout='wide' )
 
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


def avg_std_city_traffic ( df1 ):
            # selecionar as colunas
            cols = ['City' , 'Road_traffic_density' , 'Time_taken(min)']
            
            # agrupar por cidade e densidade , tirar a média e desvio usando o 'agg'
            df_aux = df1.loc[ : , cols].groupby(['City' , 'Road_traffic_density']).agg({'Time_taken(min)': ['mean' , 'std']})
            
            # dar um nome melhor para as novas colunas
            df_aux.columns = ['avg_time' , 'std_time']
            
            # show
            df_aux = df_aux.reset_index()
            
            fig = px.sunburst( df_aux, path=['City' , 'Road_traffic_density'], values='avg_time',
                                             color='std_time', color_continuous_scale='RdBu',
                                            color_continuous_midpoint=np.average(df_aux['std_time']))
            
            return fig

def dist_avg_rest_entrega( df1 ):
            df1['distance(km)'] = ( df1.loc[ : , ['Restaurant_latitude' , 'Restaurant_longitude' , 'Delivery_location_latitude' , 'Delivery_location_longitude']]
                                        .apply( lambda x: haversine(  (x['Restaurant_latitude'] , x['Restaurant_longitude']) ,
                                                                      (x['Delivery_location_latitude'] , x['Delivery_location_longitude'])), axis=1) )
            df_aux = df1['distance(km)'].mean()
                
            avg_distance = round( df_aux, 2 )
            
            return ( avg_distance )

# ==========================================               
# Import dataset + cópia para 'df1'
# ==========================================
df = pd.read_csv( 'dataset/train.csv' )
 

# ==========================================               
# Limpando os Dados
# ==========================================
df1 = clean_code( df )
 
def distancia_avg_rest( df1 ):
             # código com gráfico ( é um pouco diferente do código acima )
            cols = ['Delivery_location_latitude' , 'Delivery_location_longitude' , 'Restaurant_longitude', 'Restaurant_latitude' ]
            df1['distance'] = df1.loc[: , cols].apply( lambda x:
                                                          haversine( (x['Restaurant_latitude'] , x['Restaurant_longitude']),
                                                                  ( x['Delivery_location_latitude'] , x['Delivery_location_longitude'])) , axis=1) 
            avg_distance = df1.loc[: , ['City' , 'distance']].groupby(['City']).mean().reset_index()
                
                # gráfico
                # pull is given as a fraction of the pie radius 
            fig = go.Figure ( data=[ go.Pie( labels=avg_distance['City'], values=avg_distance['distance'], pull=[0, 0, 0.05] )])
    
            return fig



def avg_std_time_graph_city( df1 ):
        st.markdown('##### Distribuição Tempo por Cidade')
        
        cols = ['City' , 'Time_taken(min)']
        df_aux = df1.loc[: , cols].groupby( ['City'] ).agg( {'Time_taken(min)' : ['mean' , 'std']} )
            
        df_aux.columns = ['avg_time' , 'std_time']
            
        df_aux = df_aux.reset_index()
            
        fig=go.Figure()
        fig.add_trace( go.Bar( name='Control',
                                  x=df_aux['City'],
                                   y=df_aux['avg_time'],
                                   error_y=dict (type='data' , array=df_aux['std_time']) ) )
        fig.update_layout(barmode='group')
                    
        return fig

 
def avg_std_city_order_type( df1 ):
            st.markdown( '##### O Tempo Médio e o Desvio Padrão de Entrega por Cidade e Tipo de Pedido' )
            cols = ['City' , 'Time_taken(min)', 'Type_of_order']
    
            df_aux = df1.loc[ : , cols].groupby( ['City' , 'Type_of_order'] ).agg({ 'Time_taken(min)' : ['mean' , 'std'] })
             
            df_aux.columns = ['avg_time' , 'std_time']
            
            df_aux.reset_index()
    
            st.dataframe( df_aux )
    
            return df_aux

def avg_std_delivery_com_festival( df1 , Festival,  op ):
                   
   # cols = ['Time_taken(min)' , 'Festival']
            df_aux =  df1.loc[ : , ['Time_taken(min)','Festival']].groupby(['Festival']).agg({'Time_taken(min)': ['mean' , 'std']}) 
                                
            df_aux.columns = ['avg_time' , 'std_time']
            df_aux = df_aux.reset_index() 
                            
                             #filtrar apenas dias de Festival
            df_aux = np.round( df_aux.loc[ df_aux['Festival'] == Festival , op ] , 2 )
                                       
                    
            return df_aux

def avg_std_delivery_sem_festival( df1 , Festival,  op ):
            """
            Esta função calcula o tempo médio e o desvio padrão do tempo de entrega em datas SEM o Festival.
            Parâmetros:
                Input:
                    -df: Dataframe com os dados necessários para o cálculo 
                    -op: Tipo de operação que precisa ser calculado
                    'avg_time': calcula o tempo médio
                    'std_time': calcula o desvio padrão
                Output:
                    -df: Dataframe com duas colunas e uma linha.
            """ 
            df_aux = df1.loc[ : , ['Time_taken(min)','Festival']].groupby(['Festival']).agg({'Time_taken(min)': ['mean' , 'std']})
                
            df_aux.columns = ['avg_time' , 'std_time']
            df_aux = df_aux.reset_index() 
            
             #filtrar apenas dias de Festival
            df_aux = np.round( df_aux.loc[ df_aux['Festival'] == Festival , op ] , 2 ) 
            #col4.metric( 'STD c/ Festival' , df_aux )
              
            return df_aux 
# ==========================================
# SideBar no Streamlit 
# ==========================================

st.header( 'Marketplace - Visão Restaurantes' ) 

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
# Final Filtros
# ==========================================
# ==========================================
# Layout no Streamlit  - Abas ( tabs ) 
# ==========================================

tab1, tab2, tab3 = st.tabs( ['Visão Geral' , '__' , '__' ] )

with tab1:
    with st.container():
         st.title( 'Métricas Gerias sobre tempo de Entrega e Entregadores ')
         col1, col2, col3, col4, col5, col6 = st.columns ( 6 )
    with col1:
    
         #st.title('OverAll')
        #st.markdown( '##### Quantidade de Entregadores' )
         qtd = df1.loc[: , 'Delivery_person_ID'].nunique()
         col1.metric( 'Qdt Entregadores Únicos' , qtd)
        
    with col2:
        
        avg_distance=dist_avg_rest_entrega( df1 )
        col2.metric( 'Distância AVG Resturantes vs Locais de Entrega.' , avg_distance )
        
        
        
    with col3:
        
        df_aux=avg_std_delivery_com_festival ( df1, 'Yes', 'avg_time' ) 
        col3.metric( 'AVG Tempo Entrega c/ Festival' , df_aux )
         
            
     
    with col4:
        
         df_aux=avg_std_delivery_com_festival ( df1, 'Yes', 'std_time' ) 
         col4.metric( 'STD Tempo Entrega c/ Festival' , df_aux )

          
        
    with col5:
        
         df_aux=avg_std_delivery_sem_festival( df1, 'No', 'avg_time' )
         col5.metric( 'AVG Tempo Entrega s/ Festival' , df_aux )

         
        
    with col6:

         df_aux=avg_std_delivery_sem_festival( df1, 'No', 'std_time' )
         col6.metric( 'STD Tempo Entrega s/ Festival' , df_aux )
         

          
         
        

with st.container():
    
    st.markdown("""___""")
    st.title( 'Tempo Médio de Entrega por Cidade' )
    col1, col2 = st.columns( 2 )
     
    with col1:
          
        st.markdown( '##### A Distância Média dos Resturantes e dos Locais de Entrega' )
        fig=distancia_avg_rest( df1 )
        st.plotly_chart( fig , use_container_width=True )

                 
    with col2:
        
        st.markdown('##### AVG e STD Entrega por Cidade e Tráfego')
        fig=avg_std_city_traffic( df1 )
        st.plotly_chart( fig ) 


with st.container():
    
    st.markdown("""___""")
    
    st.title( 'Distribuição do Tempo' ) 
    fig=avg_std_time_graph_city( df1 )
    st.plotly_chart( fig, use_container_width=True )
 
          

with st.container():
    
    st.markdown("""___""")

    st.title( ' Distribuição da Distância' )
    df_aux=avg_std_city_order_type( df1 )
    
        
        
    
 







