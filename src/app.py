import streamlit as st
import numpy as np
import io
import cv2
import matplotlib.pyplot as plt
import base64
import folium
from streamlit_folium import folium_static
from PIL import Image as PILImage

st.set_page_config(page_title='TH: Google Satellite Image Cropper', page_icon='🛰️')

def main():
    st.title('TH: Google Satellite Image Cropper')

    default_location = [14.5379, 99.9912]  # Default location: Suphan Buri

    # Create a map centered around a specific location
    map_center = st.checkbox("Customize Map Center", False)
    if map_center:
        lat = st.number_input("Latitude", value=default_location[0])
        lon = st.number_input("Longitude", value=default_location[1])
        default_location = [lat, lon]

    zoom_level = st.slider("Zoom level", min_value=1, max_value=18, value=10)

    # Displaying the map using Folium (streamlit_folium)
    m = folium.Map(location=default_location, zoom_start=zoom_level, tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
                   attr='Google Satellite', zoom_control=False)

    folium_static(m)

    # Option to select boundary and detect edges using a button
    select_boundary = st.button("Select Boundary and Detect Edges")
    if select_boundary:
        st.write("Please draw a rectangle around the desired area to detect edges.")

        # Take a screenshot of the map using Selenium
        img_data = capture_map_screenshot(default_location, zoom_level)

        # Display the image
        if img_data:
            st.image(img_data, caption='Google Satellite Image', use_column_width=True)
            # Additional processing or edge detection can be added here if needed
        else:
            st.write("Failed to load the image.")

def capture_map_screenshot(location, zoom):
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        
        # Construct the URL for the map screenshot
        url = f'https://www.google.com/maps/@{location[0]},{location[1]},{zoom}z'

        # Open the map in Chrome browser
        driver.get(url)

        # Capture the screenshot
        screenshot = driver.get_screenshot_as_png()
        driver.quit()

        img = PILImage.open(io.BytesIO(screenshot))
        img_byte_array = io.BytesIO()
        img.save(img_byte_array, format='PNG')
        return img_byte_array.getvalue()
    except Exception as e:
        print("Error:", e)
        return None

def crop_image(image):
    # Convert to RGB (OpenCV uses BGR by default)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    x, y, w, h = cv2.selectROI("Select Boundary", image_rgb, fromCenter=False, showCrosshair=False)
    cropped_image = image[y:y + h, x:x + w]
    return cropped_image

def detect_edges(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply Canny edge detection
    edges = cv2.Canny(gray, 100, 200)
    # Convert edges to RGB for displaying with Streamlit
    edges_rgb = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
    return edges_rgb

if __name__ == '__main__':
    main()