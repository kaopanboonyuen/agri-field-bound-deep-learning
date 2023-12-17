import streamlit as st
from PIL import Image as PILImage
import numpy as np
import cv2
import geopandas as gpd
import tempfile
import zipfile
import os

st.set_page_config(page_title='TH: Google Satellite Image Boundary Detection', page_icon=":rocket:")
st.title('TH: Google Satellite Image Boundary Detection')

uploaded_file = st.file_uploader("Choose a satellite image (JPG, JPEG, PNG, TIFF)", type=["jpg", "jpeg", "png", "tiff"])

if uploaded_file is not None:
    file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type}
    st.write(file_details)

    # Load the uploaded image
    image = PILImage.open(uploaded_file)

    # Display the original uploaded image
    st.subheader("Original Image:")
    st.image(image, caption='Uploaded Image', use_column_width=True)

    if st.button('Detect Edges'):
        # Convert the image to a NumPy array for processing
        img_array = np.array(image)

        # Perform edge detection (example using Canny edge detection)
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 100, 200)

        # Expand thinner edges by applying dilation
        kernel = np.ones((3, 3), np.uint8)
        dilated_edges = cv2.dilate(edges, kernel, iterations=1)

        # Display the edge-detected image
        st.subheader("Edge Detected Image:")
        st.image(dilated_edges, caption='Edge Detected Image', use_column_width=True)

        if st.button('Save as .shape file'):
            # Allow user to input latitude and longitude
            lat = st.number_input("Latitude:")
            lon = st.number_input("Longitude:")

            # Convert lat/lon coordinates to a GeoDataFrame and save as .shape file
            boundary_points = [(lon, lat)]  # Example boundary points, add more points from contours if needed
            gdf = gpd.GeoDataFrame(geometry=gpd.points_from_xy([point[0] for point in boundary_points],
                                                               [point[1] for point in boundary_points]))

            # Create a temporary directory to store the shapefile
            temp_dir = tempfile.mkdtemp()

            # Save GeoDataFrame as a shapefile in the temporary directory
            shapefile_path = os.path.join(temp_dir, "boundary.shp")
            gdf.to_file(shapefile_path)

            # Zip the shapefile
            with zipfile.ZipFile('boundary_shapefile.zip', 'w') as zipf:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        zipf.write(os.path.join(root, file), file)

            # Provide the download link for the shapefile
            st.success('Shapefile Saved Successfully!')
            with open('boundary_shapefile.zip', 'rb') as f:
                st.download_button('Download Shapefile', f)