import streamlit as st
from PIL import Image 

# diz para o streamlit buscar um arquivo dentro da pasta pages

st.set_page_config( 
    page_title='Home',
    page_icon='📊'
)


#image_path='C:\\Users\\giann\Documents\\repos\\Analista de Dados\\Comunidade DS AD\\ftc_programacao_python\\'
image = Image.open('delivery_01.png' )
st.sidebar.image( image, width=120 )

# imagem 
#image_path =r'C:\Users\giann\Documents\repos\Analista de Dados\Comunidade DS AD\ftc_programacao_python\delivery.jpg'
#image = Image.open( image_path )
#st.sidebar.image( image, width=220 )

# título da sidebar
st.sidebar.markdown( '# Cury Company' )
st.sidebar.markdown( '## Fastest Delivery in Town!' ) 
# linha que separa o sidebar 
st.sidebar.markdown( """---""" ) 

st.write( '# Curry Company Growth Dashboard' )

st.markdown( 
    """
    Growth Dashboard foi construído para acompanhar as métricas de crescimento dos Entregadores e Restaurantes.
    ### Como utilizar esse Growth Dashboard?
    - Visão Empresa:
        - Visão Gerencial: Métricas Gerais de Comportamento
        - Visão Tática: Indicadores Semanais de Crescimento
        - Visão Geográfica: Insights de Geolocalização
    - Visão Entregador:
        - Acompanhamento dos Indicadores Semanais de Crescimento
    - Visão Restaurante:
        - Indicadores Semanais de Crescimento dos Restaurantes
    ### Ask for help 
    - Email time de Data Science  
        - Email:    giannini_js@hotmail.com
        - LinkedIn: Giannini Jefferson da Silva
         
        
    """ )









