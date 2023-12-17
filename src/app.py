import streamlit as st
import folium
from PIL import Image
import io

def main():
    st.title('Google Satellite Image Cropper')

    # Create a map centered around a specific location
    default_location = [40.7128, -74.0060]  # Example: New York City
    map_center = st.checkbox("Customize Map Center", False)
    if map_center:
        lat = st.number_input("Latitude", value=default_location[0])
        lon = st.number_input("Longitude", value=default_location[1])
        default_location = [lat, lon]

    zoom_level = st.slider("Zoom level", min_value=1, max_value=18, value=10)

    m = folium.Map(location=default_location, zoom_start=zoom_level, tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
                   attr='Google Satellite', zoom_control=False)

    folium_static(m)

    # Export Map as Image
    if st.button("Export Map as Image"):
        # Take a screenshot of the map
        map_screenshot = folium.Map(location=default_location, zoom_start=zoom_level, tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
                                    attr='Google Satellite', zoom_control=False).get_root().render()
        img_data = screenshot_to_image(map_screenshot)

        # Display the image
        st.image(img_data, caption='Google Satellite Image', use_column_width=True)

        # Option to crop the image
        crop = st.checkbox("Crop Image")
        if crop:
            img = Image.open(io.BytesIO(img_data))
            cropped_img = crop_image(img)
            st.image(cropped_img, caption='Cropped Image', use_column_width=True)
            st.markdown(get_image_download_link(cropped_img), unsafe_allow_html=True)

def screenshot_to_image(screenshot):
    image = Image.open(io.BytesIO(screenshot.encode()))
    img_byte_array = io.BytesIO()
    image.save(img_byte_array, format='PNG')
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
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/png;base64,{img_str}" download="cropped_image.png">Download Cropped Image</a>'
    return href

if __name__ == '__main__':
    main()
