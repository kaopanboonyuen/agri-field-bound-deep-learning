import streamlit as st
from PIL import Image
import io
import folium
from streamlit_folium import folium_static

st.set_page_config(page_title='Google Satellite Image Cropper', page_icon='🛰️')

def main():
    st.title('Google Satellite Image Cropper')

    default_location = [40.7128, -74.0060]  # Default location: New York City

    # Input for customizing map center
    map_center = st.checkbox("Customize Map Center", False)
    if map_center:
        lat = st.number_input("Latitude", value=default_location[0])
        lon = st.number_input("Longitude", value=default_location[1])
        default_location = [lat, lon]

    zoom_level = st.slider("Zoom level", min_value=1, max_value=18, value=10)

    # Create a Folium map
    m = folium.Map(location=default_location, zoom_start=zoom_level, tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
                   attr='Google Satellite', zoom_control=False)

    # Convert Folium map to HTML
    map_html = m._repr_html_()

    # Display the map using st.write (as Streamlit's pydeck_chart might not display Folium maps directly)
    st.write(map_html, unsafe_allow_html=True)

    # Export Map as Image
    if st.button("Export Map as Image"):
        # Take a screenshot of the map
        img_data = screenshot_to_image(m)

        # Display the image
        st.image(img_data, caption='Google Satellite Image', use_column_width=True)

        # Option to crop the image
        crop = st.checkbox("Crop Image")
        if crop:
            img = Image.open(io.BytesIO(img_data))
            cropped_img = crop_image(img)
            st.image(cropped_img, caption='Cropped Image', use_column_width=True)
            st.markdown(get_image_download_link(cropped_img), unsafe_allow_html=True)

def screenshot_to_image(m):
    map_screenshot = folium.Figure().add_child(m).encode()
    img_data = Image.open(io.BytesIO(map_screenshot))
    img_byte_array = io.BytesIO()
    img_data.save(img_byte_array, format="PNG")
    return img_byte_array.getvalue()

def crop_image(image):
    st.write("Drag the mouse to draw a rectangle for cropping.")
    img = image.copy()
    area = st.image(img, use_column_width=True, clamp=True, channels="RGB", output_format="PNG")
    cropped_area = st.selectable_area("Cropped Area")
    cropped_image = img.crop(cropped_area)
    return cropped_image

def get_image_download_link(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = buffered.getvalue()
    href = f'<a href="data:file/png;base64,{img_str.decode("utf-8")}" download="cropped_image.png">Download Cropped Image</a>'
    return href

if __name__ == '__main__':
    main()