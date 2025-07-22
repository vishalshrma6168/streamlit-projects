import streamlit as st
from streamlit_drawable_canvas import st_canvas
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image

# Load trained model
model = load_model("digit_model.h5")

st.title("✍️ Handwritten Digit Recognizer")

st.write("Draw a digit (0-9) below. The AI will predict what you wrote.")

# Create drawing canvas
canvas_result = st_canvas(
    fill_color="#000000",
    stroke_width=10,
    stroke_color="#FFFFFF",
    background_color="#000000",
    height=280,
    width=280,
    drawing_mode="freedraw",
    key="canvas"
)

# Process and predict
if st.button("Predict"):
    if canvas_result.image_data is not None:
        img = canvas_result.image_data

        # Convert to grayscale and resize to 28x28
        img = Image.fromarray(np.uint8(img)).convert("L").resize((28, 28))
        img = np.array(img)
        img = img.reshape(1, 28, 28, 1)
        img = img / 255.0

        # Predict
        pred = model.predict(img)
        st.success(f"🧠 I think it's a **{np.argmax(pred)}**!")
