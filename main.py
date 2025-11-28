import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# ----- Streamlit app -----
st.set_page_config(page_title="Plant Care App", layout="wide")
st.title("🌱 Plant Care Prediction")

# Upload photo
uploaded_file = st.file_uploader("Upload a plant photo", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read bytes once
    file_bytes = uploaded_file.read()

    # Display the image
    image = Image.open(BytesIO(file_bytes))
    st.image(image, caption="Uploaded Plant", use_column_width=True)

    with st.spinner("Predicting plant and fetching care card..."):
        try:
            url = "http://127.0.0.1:8000/predict/"
            files = {
                "file": (uploaded_file.name, BytesIO(file_bytes), uploaded_file.type or "image/jpeg")
            }
            response = requests.post(url, files=files, timeout=30)
            if response.status_code != 200:
                st.error(f"API returned {response.status_code}: {response.text}")
                st.stop()

            data = response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Request error: {e}")
            st.stop()
        except Exception as e:
            st.error(f"Error calling API: {e}")
            st.stop()

    # Display prediction
    st.subheader("Prediction Result")
    predicted_plant = data.get("predicted_plant")
    st.markdown(f"**Predicted Plant:** {predicted_plant}")

    # Display whether RAG context was used
    rag_used = data.get("rag_context_available", False)
    st.markdown(f"**Used RAG Context:** {'✅ Yes' if rag_used else '❌ No'}")

    # Display plant care card
    care_card = data.get("plant_care_card", {})
    if care_card:
        st.subheader("🌿 Plant Care Card")
        st.markdown(f"**Common Name:** {care_card.get('common_name')}")
        st.markdown(f"**Latin Name:** {care_card.get('latin_name')}")
        st.markdown(f"**Care Difficulty:** {care_card.get('care_difficulty')}")
        st.markdown(f"**Watering Frequency:** {care_card.get('watering_frequency')}")
        st.markdown(f"**Sunlight:** {care_card.get('sunlight')}")
        st.markdown(f"**Soil Type:** {care_card.get('soil_type')}")
        st.markdown(f"**Fertilizer:** {care_card.get('fertilizer')}")
        st.markdown(f"**Outdoors:** {care_card.get('outdoors')}")
        st.markdown(f"**Notes:** {care_card.get('notes')}")
