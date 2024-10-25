# Visão Entreadores

# bibliotecas necessárias
import pandas as pd #pandas vai ajudar a importar o dado com apelido pd

#import plotly.graph_objects as go 
# from haversine import haversine
import re
import plotly.express as px  # gráficos
import streamlit as st
from datetime import datetime
from PIL import Image
import folium
from streamlit_folium import folium_static 

#colocar um ícone no início da aba
st.set_page_config( page_title='Visão Entregadores', page_icon='🚚', layout='wide' )

# ==========================================
#  Funções 
# ==========================================
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

def entregadores_mais_lentos( df1 ):
    df_aux = (df1.loc[: , ['Delivery_person_ID' , 'City' , 'Time_taken(min)']]
                 .groupby( ['City' , 'Delivery_person_ID']).max()
                 .sort_values( ['City' , 'Time_taken(min)'], ascending=False ).reset_index())
                 
    df_aux1 = df_aux.loc[df_aux['City'] == 'Metropolitian' , : ].head(10)
    df_aux2 = df_aux.loc[df_aux['City'] == 'Urban' , : ].head(10)
    df_aux3 = df_aux.loc[df_aux['City'] == 'Semi-Urban' , : ].head(10)
                    
                    # unir as 3 colunas em uma só
    df_concat = pd.concat([ df_aux1 , df_aux2 , df_aux3] ).reset_index( drop=True )
                 
    return df_concat 

def entregadores_mais_rapidos( df1 ):  
    df_aux = (df1.loc[: , ['Delivery_person_ID' , 'City', 'Time_taken(min)']]
                 .groupby(['City' , 'Delivery_person_ID' ]).min()
                 .sort_values( ['City','Time_taken(min)'], ascending=True ).reset_index())
                
    df_aux1 = df_aux.loc[df_aux['City'] == 'Metropolitian', :].head(10)
    df_aux2 = df_aux.loc[df_aux['City'] == 'Urban' , :].head(10)
    df_aux3 = df_aux.loc[df_aux['City'] == 'Semi-Urban'].head(10)
                
                # agora concatenar os 3 resultado // # o index ficou bagunçado preciso resetar, e 'drop=True' para apagar um index velho
    df_concat = pd.concat( [df_aux1 , df_aux2 , df_aux3] ).reset_index( drop=True )
                 
    return df_concat


# import dataset
df = pd.read_csv( 'dataset/train.csv' )
#df1  = df.copy() não preciso mais, faço a cópia na limpeza
# ==========================================               
# Limpando os Dados
# ==========================================
df1 = clean_code ( df )

# ==========================================
            # SideBar no Streamlit 
# ==========================================

st.header( 'Marketplace - Visão Entregadores' ) 

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
# Final Filtros
# ==========================================
# ==========================================
# Layout no Streamlit  - Abas ( tabs ) 
# ==========================================

# Criação das Tabs
tab1, tab2, tab3 = st.tabs( ['Visão Gerencial', '__', '__'] )

with tab1: # criar aba
    with st.container(): # criar um container com 4 colunas ( caixinhas ) 
        st.title('Métricas Gerais dos Entregadores') # 'gap='large'' é espaço entre as colunas ( caixinhas ) 
        col1, col2, col3, col4 = st.columns ( 4, gap='large' )
        
        with col1:
           # st.subheader( 'Maior de Idade' ) 
             # maior idade dos entregadores
            maior_idade = df1.loc[: , 'Delivery_person_Age'].max()
            col1.metric( 'Maior de Idade', maior_idade )
            
        with col2:
            #st.subheader( 'Menor de Idade' )
              # menor idade dos entregadores
            menor_idade =  df1.loc[: , 'Delivery_person_Age'].min()  
            col2.metric( 'Menor de Idade', menor_idade )
       
        with col3:
           # st.subheader( 'Pior Condição de Veículo' )
            # pior condição de carro
            pior_cond = df1.loc[: , 'Vehicle_condition'].min() 
            col3.metric( 'A Pior Condição de Veículo' , pior_cond)

        with col4:
            #st.subheader( 'Melhor Condição de Veículo') 
            # melhor condição de carro
            melhor_cond = df1.loc[ : , 'Vehicle_condition'].max() 
            col4.metric( 'A Melhor Condição', melhor_cond)
             
    with st.container():
         st.markdown( """___""" )
         st.title( 'Avaliações dos Entregadores' )

         col1, col2 = st.columns( 2 )
         with col1:
            st.markdown( '##### Avaliações Média por Entregador' )
            df_avg_ratings_per_delivery = ( df1.loc[: , ['Delivery_person_Ratings' , 'Delivery_person_ID']]
                                           .groupby( ['Delivery_person_ID'] )
                                           .mean().reset_index() )
            st.dataframe( df_avg_ratings_per_delivery )            
         with col2:
            st.markdown( '##### Avaliação Média por Tipo de Trânsito' ) 
            # Resposta do Meigarom usando a função 'agg' // Método agg vídeo 6 Teo Calvo Desbravando Pandas
            df_aux = ( df1.loc[: , ['Delivery_person_Ratings' , 'Road_traffic_density']]
                          .groupby(['Road_traffic_density'])
                          .agg({'Delivery_person_Ratings' : ['mean' , 'std']}) )
            # mas deixando do jeito acima fica confuso a organização, então preciso renomear as colunas
            
            # esse comando vai mostrar que tem multiindex e isso deixa ruim/feio a estrutura quando faço a visualização
            #df_aux.columns
            
            # modificando os nomes das colunas
            df_aux.columns = ['Delivery_mean' , 'Delivery_std']
            # exibir o resultado e resetar o índex
            df_aux.reset_index()
            st.dataframe( df_aux ) 
             
            st.markdown( '##### Avaliação AVG & STD por tipo de Clima' ) 
            # agg( {coluna que recebe a operação : [lista das operações que quero fazer] } )
            df_aux = ( df1.loc[: , ['Delivery_person_Ratings' , 'Weatherconditions']]
                          .groupby(['Weatherconditions'])
                          .agg({'Delivery_person_Ratings': ['mean' , 'std']}) )
            
            #modificar os nomes das colunas
            df_aux.columns = ['Delivery_person_Ratings_mean' , 'Delivery_person_Ratings_std']
            
            # exibir e resetar o index
            df_aux.sort_values('Delivery_person_Ratings_mean' , ascending=False).reset_index()
            st.dataframe( df_aux ) 
        
    with st.container():
       
         st.markdown( """___""" )
         st.title( 'Velocidade de Entrega' ) 

         col1, col2 = st.columns( 2 ) 
         with col1:
             
              st.subheader( 'Entregadores Mais Rápidos' ) 
              df_concat=entregadores_mais_rapidos( df1 )
              st.dataframe( df_concat )


         with col2:                       
             
             st.subheader( 'Entregadores Mais Lentos' ) 
             df_concat=entregadores_mais_lentos( df1 )
             st.dataframe( df_concat )             