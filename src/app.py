import streamlit as st
from PIL import Image
import io
import cv2
from PIL import Image as PILImage
import base64
import folium
from streamlit_folium import folium_static
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

st.set_page_config(page_title='Google Satellite Image Cropper', page_icon='🛰️')

def main():
    st.title('Google Satellite Image Cropper')

    default_location = [40.7128, -74.0060]  # Default location: New York City

    # Create a map centered around a specific location
    map_center = st.checkbox("Customize Map Center", False)
    if map_center:
        lat = st.number_input("Latitude", value=default_location[0])
        lon = st.number_input("Longitude", value=default_location[1])
        default_location = [lat, lon]

    zoom_level = st.slider("Zoom level", min_value=1, max_value=18, value=10)

    m = folium.Map(location=default_location, zoom_start=zoom_level, tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
                   attr='Google Satellite', zoom_control=False)

    folium_static(m)

    # Option to select boundary and detect edges
    select_boundary = st.checkbox("Select Boundary and Detect Edges")
    if select_boundary:
        st.write("Please draw a rectangle around the desired area to detect edges.")

        # Take a screenshot of the map
        map_screenshot = folium.Map(location=default_location, zoom_start=zoom_level, tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
                                    attr='Google Satellite', zoom_control=False).get_root().render()
        
        img_data = screenshot_to_image(map_screenshot)

        # Display the image
        if img_data:
            st.image(img_data, caption='Google Satellite Image', use_column_width=True)
            # Convert to OpenCV format
            cv_image = np.array(img_data)
            
            cropped_image = crop_image(cv_image)
            edge_detected_image = detect_edges(cropped_image)
            st.image(edge_detected_image, caption='Edge Detected Image', use_column_width=True)
        else:
            st.write("Failed to load the image.")

def screenshot_to_image(screenshot):
    try:
        plt.figure(figsize=(8, 6))
        plt.imshow(screenshot)
        plt.axis('off')
        img_byte_array = io.BytesIO()
        plt.savefig(img_byte_array, format='png')
        plt.close()
        return img_byte_array.getvalue()
    except Exception as e:
        print("Error:", e)
        return None

# Remaining functions (crop_image, detect_edges) remain unchanged...

if __name__ == '__main__':
    main()