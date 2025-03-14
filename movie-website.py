import streamlit as st
import os
import random
from pathlib import Path

def get_random_color():
    """Generate a random HEX color."""
    return f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"

# Set page configuration
st.set_page_config(page_title="Movie Streaming Website", layout="wide")

# Apply colorful styling
st.markdown(
    f"""
    <style>
        .stApp {{
            background-color: {get_random_color()};
        }}
        .stVideo {{
            border-radius: 15px;
            box-shadow: 5px 5px 15px rgba(0,0,0,0.3);
        }}
        .movie-card {{
            padding: 10px;
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
            text-align: center;
            margin-bottom: 20px;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🍿 Movie Streaming Website")
st.markdown("Upload and watch your favorite movies!")

# Founder Credit
st.sidebar.markdown("### 👨‍💻 Created by Kaustav Roy Chowdhury")

# Sidebar for movie selection
st.sidebar.header("Movie Library")

# Video and Image upload section
uploaded_video = st.file_uploader("Upload a movie", type=["mp4", "mov", "avi", "mkv"])
uploaded_image = st.file_uploader("Upload a movie poster", type=["jpg", "jpeg", "png"])

if uploaded_video is not None:
    # Save the uploaded file to a temporary directory
    save_path = Path("movies")
    save_path.mkdir(exist_ok=True)
    movie_path = save_path / uploaded_video.name
    
    with open(movie_path, "wb") as f:
        f.write(uploaded_video.getbuffer())
    
    st.success(f"Movie saved: {uploaded_video.name}")
    
    # Display movie
    st.video(str(movie_path))

if uploaded_image is not None:
    # Save the uploaded image
    image_path = Path("posters")
    image_path.mkdir(exist_ok=True)
    poster_path = image_path / uploaded_image.name
    
    with open(poster_path, "wb") as f:
        f.write(uploaded_image.getbuffer())
    
    st.success(f"Poster saved: {uploaded_image.name}")
    
    # Display movie poster
    st.image(str(poster_path), caption="Movie Poster", use_column_width=True)

# List available movies
movies = list(Path("movies").glob("*.mp4"))
if movies:
    st.sidebar.subheader("Available Movies")
    movie_data = []
    for movie in movies:
        poster_file = Path("posters") / (movie.stem + ".jpg")
        poster_exists = poster_file.exists()
        
        movie_data.append({
            "Title": movie.stem.replace("_", " "),
            "File Name": movie.name,
            "Size (MB)": round(movie.stat().st_size / (1024 * 1024), 2),
            "Duration": "Unknown",  # You can enhance this by extracting metadata
            "Poster Available": "✅" if poster_exists else "❌"
        })
    
    import pandas as pd
    df = pd.DataFrame(movie_data)
    st.sidebar.dataframe(df)
    
    selected_movie = st.sidebar.selectbox("Choose a movie", df["File Name"].tolist())
    if selected_movie:
        movie_path = Path("movies") / selected_movie
        st.video(str(movie_path))
        
        # Display associated poster if available
        selected_poster = Path("posters") / (Path(selected_movie).stem + ".jpg")
        if selected_poster.exists():
            st.image(str(selected_poster), caption="Movie Poster", use_column_width=True)
