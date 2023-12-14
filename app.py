from pathlib import Path
import PIL
from collections import Counter

# External packages
import streamlit as st

import settings
import helper
from recognition_records import display_recognition_records , save

st.set_page_config(
    page_title="test",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.write("""
<style>
h1 {
    background-color: rgb(94, 89, 84); 
    padding: 20px;
    border-radius: 10px;
    color: #fff;
    font-size: 30px;
    font-weight: bold;
    width: 100%; 
    height: 80px; 
    font-family : Courier, monospace;
}
h3 {
    text-align: center;
    color: #dee;
    font-size: 30px;
    font-weight: 3px;
}
p {
    font-family : Courier, monospace;
    text-align:center;
    color : #fff;
    font-size : 22px;
    font-weight:3px;
}
img {
    border-radius: 1.5em;
    padding-top:10px;
}
.stButton > button:first-child { 
    background-color: #666; 
    color: #fff;
    border: 5px gainsboro;
    border-radius: 20px;
    padding: 10px 20px;
    margin-bottom: 10px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    width: 200px;
    text-decoration: none; 
    text-align: center; 
    white-space: normal; 
}
.stButton > button:hover { 
    background-color: #444; 
}
.stButton > button:active{
    background-color: #111; 
}
.stDataFrame{
    border-radius : 30px;
    padding-top:20px;
    color:white; 
    text-align:left !important;
}        
[data-testid=stSidebar] {
    background-color: #555;
    font-size:15px;
}
[data-testid=stRadio] {
    padding-right: 10px;
    padding-left: 4px;
    padding-bottom: 3px;
    margin: 4px;
}
[data-testid=stAppViewContainer] {
    background-color: #777;
}
[data-testid=stHeader] {
    background-color: #777;
}
video{
    border-radius:30px;
    padding : 20px;
}
</style>
""", unsafe_allow_html=True)

st.title("Greenhouse Plants Detection")

model_type = 'Detection'

if model_type == 'Detection':
    model_path = Path(settings.DETECTION_MODEL)

try:
    model = helper.load_model(model_path)
except Exception as ex:
    st.error(f"Unable to load model. Check the specified path: {model_path}")
    st.error(ex)

if 'selected_button' not in st.session_state:
    st.session_state.selected_button = None

image_bt = st.sidebar.button('Select Image')
if image_bt:
    st.session_state.selected_button = "image_bt"
video_bt = st.sidebar.button('Select video')
if video_bt:
    st.session_state.selected_button = "video_bt"
rtmp_bt = st.sidebar.button('Input RTMP')
if rtmp_bt:
    st.session_state.selected_button = "rtmp_bt"
view_bt = st.sidebar.button('View Categories')
if view_bt:
    st.session_state.selected_button = "view_bt"
his_bt = st.sidebar.button('View History')
if his_bt:
    st.session_state.selected_button = "his_bt"

source_img = None
if st.session_state.selected_button == "image_bt":
    source_img = st.sidebar.file_uploader(
        "Choose image...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))

    col1, col2 = st.columns(2)

    with col1:
        try:
            if source_img is None:
                default_image_path = str(settings.DEFAULT_IMAGE)
                default_image = PIL.Image.open(default_image_path)
                st.image(default_image_path,use_column_width=True)
            else:
                uploaded_image = PIL.Image.open(source_img)
                st.image(source_img, caption="Uploaded Image",use_column_width=True)
                
        except Exception as ex:
            st.error("Error occurred while opening the image.")
            st.error(ex)

    with col2:
        if st.sidebar.button('Start Detect',key='detect'):
            res = model.predict(uploaded_image,device=0,retina_masks=True)
            boxes = res[0].boxes
            res_plotted = res[0].plot(conf=False)[:, :, ::-1]
            st.image(res_plotted, caption='Detected Image',
                    use_column_width=True)
            tensor_data = boxes.cls
            tensor_data_cpu = tensor_data.cpu()
            numpy_array = tensor_data_cpu.numpy().astype(int)
            counter = Counter(numpy_array)
            names = ['火焰萵苣[還不可收成]', '火焰萵苣[可收成]', '奶油萵苣[還不可收成]', '奶油萵苣[可收成]', '翠綠橡木萵苣[還不可收成]', '翠綠橡木萵苣[可收成]', '綠捲萵苣[還不可收成]', '綠橡木萵苣[還不可收成]',  '綠橡木萵苣[可收成]',  '紫橡木萵苣[還不可收成]',  '紫橡木萵苣[可收成]',  '紅捲萵苣[還不可收成]', '紅捲萵苣[可收成]',  '羅曼萵苣[還不可收成]',  '羅曼萵苣[可收成]']
            result_string = "; ".join([f"{names[num - 1]}: {count}" for num, count in counter.items() if num > 0 and count >= 1])
            save(result_string)
            try:
                with st.expander("Detection Results"):
                    for box in boxes:
                        st.write(box.data)
            except Exception as ex:
                st.write("No image is uploaded yet!")
    pass
    

elif st.session_state.selected_button == "video_bt":
    helper.play_stored_video(model)
    pass

elif st.session_state.selected_button == "rtmp_bt":
    helper.play_rtsp_stream(model)
    pass

elif st.session_state.selected_button == "view_bt":
    plants = [
        {
            'name': 'Batavia Lettuce','cname':'綠火焰萵苣',
            'details': '播種到採收的時間約為45~50天',
            'details2': '生長週期為50~70天',
            'image': 'images/Batavia.png',
        },
        {
            'name': 'Butterhead Lettuce','cname':'波士頓奶油萵苣',
            'details': '生長週期為45~60天',
            'details2': '',
            'image': 'images/Butterhead.png',
        },
        {
            'name': 'Light Green Oakleaf','cname':'綠橡木葉萵苣',
            'details': '大約30天可進行採收',
            'details2': '生長週期為45~60天',
            'image': 'images/green_oak.png',
        },
        {
            'name': 'Dark Green Oakleaf','cname':'翠綠橡木葉萵苣',
            'details': '大約30天可進行採收',
            'details2': '生長週期為45~60天',
            'image': 'images/dark_oak.png',
        },
        {
            'name': 'Red Carol Lettuce','cname':'紅卷萵苣',
            'details': '生長週期為55~65天',
            'details2': '',
            'image': 'images/lollo.png',
        },
        {
            'name': 'Romaine Lettuce','cname':'蘿蔓萵苣',
            'details': '生長週期為60~80天',
            'details2': '',
            'image': 'images/romaine.png',
        }
    ]

    col1, col2,col3,col4 = st.columns(4)

    with col1:
        for plant in plants[:2]:
            st.image(plant['image'], use_column_width=True)
            st.subheader(plant['cname'])
            st.subheader(plant['name'])
            st.write(plant['details'])
            st.write(plant['details2'])

    with col2:
        for plant in plants[2:4]:
            st.image(plant['image'], use_column_width=True)
            st.subheader(plant['cname'])
            st.subheader(plant['name'])
            st.write(plant['details'])
            st.write(plant['details2'])


    with col3:
        for plant in plants[4:5]:
            st.image(plant['image'], use_column_width=True)
            st.subheader(plant['cname'])
            st.subheader(plant['name'])
            st.write(plant['details'])
            st.write(plant['details2'])
    with col4:
        for plant in plants[5:]:
            st.image(plant['image'], use_column_width=True)
            st.subheader(plant['cname'])
            st.subheader(plant['name'])
            st.write(plant['details'])
            st.write(plant['details2'])
    pass

elif st.session_state.selected_button == "his_bt":
    display_recognition_records()
    pass

