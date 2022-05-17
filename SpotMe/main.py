import functions
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import time

# Page Configurations
st.set_page_config(
    page_title="HCI - Project",
    menu_items={
        'About': '# Welcome to our HCI Project. Developed by team #'
    },
    layout="wide"
)

# Logo Image
with st.container():
    c1, c2, c3 = st.columns([3, 7, 3])

    with c2:
        st.image("media/WM-logo.png")

countries = functions.read_from_file("countries.json")
countries_list = list(countries.keys())

artists = functions.read_from_file("artists.json")
artists_list = list(artists.keys())

# Party Started & Playlist Sidebar
with st.sidebar:
    balloons = st.checkbox("🎉 Get The Party Started! 🎉")
    if balloons:
        st.balloons()
    st.header("🎧 Playlist")

add_selectbox = st.sidebar.selectbox(
    "Select a Genre For Music Playlist",
    ["Electronic", "Pop", "Latin"]
)

# (Electronic-Playlist)
with st.sidebar:
    if add_selectbox == "Electronic":
        col1, col2 = st.columns(2)
        # Populate Columns - Song Name & Art
        with col1:
            st.subheader("Around The World")
            st.caption("- Daft Punk")
            st.caption("Released: April 7th, 1997")
            st.audio("media/m-daftPunk.mp3", format="media/m3", start_time=0)
        # Play Song
        with col2:
            st.image("media/daftPunkWRLD.jpg")
# Stereo Love Column
with st.sidebar:
    if add_selectbox == "Electronic":
        col1, col2 = st.columns(2)
        # Populate Columns - Song Name & Art
        with col1:
            st.subheader("Stereo Love")
            st.caption("- Edward Maya & Vika Jigulina")
            st.caption("Released: September 17th 2009")
            st.audio("media/m-stereoLove.mp3", format="media/m3", start_time=0)
        # Play Song
        with col2:
            st.image("media/stereoLove-IMG.png")
# Ghost N Stuff Column
with st.sidebar:
    if add_selectbox == "Electronic":
        col1, col2 = st.columns(2)
        # Populate Columns - Song Name & Art
        with col1:
            st.subheader("Ghost 'N' Stuff")
            st.caption("- Deadmau5 feat. Rob Swire")
            st.caption("Released: September 27th 2009")
            st.audio("media/m-ghostStuff.mp3", format="media/m3", start_time=0)
        # Play Song
        with col2:
            st.image("media/ghost-IMG.jpeg")

# (Pop-Playlist)
with st.sidebar:
    if add_selectbox == "Pop":
        col1, col2, = st.columns(2)
        with col1:
            st.subheader("Down")
            st.caption("- Jay Sean feat. Lil Wayne")
            st.caption("Released: May 9th, 2009")
            st.audio("media/m-down.mp3", format="media/m3", start_time=0)
            # Play Song
        with col2:
            st.image("media/down-IMG.jpeg")
# Mariah Column
with st.sidebar:
    if add_selectbox == "Pop":
        col1, col2, = st.columns(2)
        with col1:
            st.subheader("We Belong Together")
            st.caption("- Mariah Carey")
            st.caption("Released: March 14th, 2005")
            st.audio("media/m-together.mp3", format="media/m3", start_time=0)
            # Play Song
        with col2:
            st.image("media/together-IMG.png")
# BlackEyedPeas Column
with st.sidebar:
    if add_selectbox == "Pop":
        col1, col2, = st.columns(2)
        with col1:
            st.subheader("Just Can't Get Enough")
            st.caption("- The Black Eyed Peas")
            st.caption("Released: February 18th, 2011")
            st.audio("media/m-enough.mp3", format="media/m3", start_time=0)
            # Play Song
        with col2:
            st.image("media/enough-IMG.png")

# (Latin Playlist)
with st.sidebar:
    if add_selectbox == "Latin":
        col1, col2, = st.columns(2)
        with col1:
            st.subheader("Subete")
            st.caption("- Lary Over & Lirico en la Casa")
            st.caption("Released: September 5th, 2018")
            st.audio("media/m-subete.mp3", format="media/m3", start_time=0)
            # Play Song
        with col2:
            st.image("media/subete-IMG.png")
# Prince Royce Column
with st.sidebar:
    if add_selectbox == "Latin":
        col1, col2, = st.columns(2)
        with col1:
            st.subheader("Stand by Me")
            st.caption("- Prince Royce")
            st.caption("Released: January 19th, 2010")
            st.audio("media/m-stand.mp3", format="media/m3", start_time=0)
            # Play Song
        with col2:
            st.image("media/stand-IMG.png")
# Bacilos Column
with st.sidebar:
    if add_selectbox == "Latin":
        col1, col2, = st.columns(2)
        with col1:
            st.subheader("Mi Primer Millon")
            st.caption("- Bacilos")
            st.caption("Released: February 2nd, 2003")
            st.audio("media/m-millon.mp3", format="media/m3", start_time=0)
            # Play Song
        with col2:
            st.image("media/millon-IMG.png")


# Music Charts Header
with st.container():

    st.header("🔥 Music Charts 🔥")
    st.caption("Provides international music charts that get regularly updated.")
    country_chart_selected = st.selectbox("Select a country to view charts...", options=countries_list)
    chart_type_selected = st.selectbox("Select the chart type...", options=["Top", "Hot", "MxMweekly", "MxMweekly_new"])

    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption("Top 10 track list for country selected.")
        charts_bttn = st.button("Load Chart")
    with col2:
        st.caption("Get top 10 Artists")
        artist_bttn = st.button("Track Artists")
    with col3:
        st.caption("Get top 10 lyrics")
        lyrics_bttn = st.button("Track Lyrics")

    if charts_bttn:
        load_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.02)
            load_bar.progress(percent_complete + 1)
            if percent_complete == 99:
                st.success("Successfully Loaded Charts. 💯")

                if country_chart_selected and chart_type_selected:
                    top_tracks = functions.request_top_tracks(countries[country_chart_selected], chart_type_selected)
                    chartlist_names = [['Track Name', 'Artist']]  # Chart Made HERE
                    chartCount = 1

                    for i in top_tracks["message"]["body"]["track_list"]:
                        chartline = []  # Stores data for chart rows
                        chartline.append(i["track"]["track_name"])
                        chartline.append(i["track"]["artist_name"])
                        chartlist_names.append(chartline)

                    chartCount += 1
                    st.header(chart_type_selected + ' Chart  📈')  # Header for chart
                    interChart = pd.DataFrame(chartlist_names,
                                          columns=['Track Name', 'Artist'])  # Create Dataframe for chart
                    st.dataframe(interChart)  # Display Chart

    if artist_bttn:
        load_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.02)
            load_bar.progress(percent_complete + 1)
            if percent_complete == 99:
                st.success("Successfully Loaded Artists. 🎤")

                if country_chart_selected and chart_type_selected:
                    index = 1
                    top_artists = functions.request_top_artists(countries[country_chart_selected])
                    st.header("🌍 Top 10 Artists Around The World ")

                    for i in top_artists["message"]["body"]["artist_list"]:
                        st.write(str(index), ")", i["artist"]["artist_name"])
                        index += 1

    if lyrics_bttn:
        load_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.02)
            load_bar.progress(percent_complete + 1)
            if percent_complete == 99:
                st.success("Lyric Links Available. 🎶")

                if country_chart_selected and chart_type_selected:
                    top_tracks = functions.request_top_tracks(countries[country_chart_selected], chart_type_selected)
                    chartlist_lyrics = [['Track Name', 'Artist', 'Lyrics']]  # Get Lyrics HERE
                    numCount = 1

                    for i in top_tracks["message"]["body"]["track_list"]:
                        track_name = i["track"]["track_name"]
                        track_artist = i["track"]["artist_name"]
                        track_lyrics = "[Lyrics]({})".format(i["track"]["track_share_url"])

                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(str(numCount), ")", track_name, "by ", track_artist)
                        with col2:
                            st.write(track_lyrics)

                        numCount += 1

# Artist Top Albums Header
st.write("")
with st.container():

    st.header("🌍 Artists Top Albums 🌍")
    top_singers = []
    top_artists = functions.request_top_artists(0)
    maps = {}

    for i in top_artists["message"]["body"]["artist_list"]:
        top_singers.append(i["artist"]["artist_name"])
        maps[i["artist"]["artist_name"]] = i["artist"]['artist_id']
    artist_selected = st.selectbox("Select an Artist", options=top_singers)
    # Returns Top Artists
    if artist_selected:
        all_albums = []
        album_maps = {}
        albums = functions.request_artist_albums(maps[artist_selected])
        for i in albums["message"]["body"]["album_list"]:

            all_albums.append(i["album"]["album_name"])
            album_maps[i["album"]["album_name"]] = i["album"]["album_id"]
        album_selected = st.selectbox("Select an Album", options=all_albums)
        if album_selected:
            info = functions.trackHelper(album_maps[album_selected])
            all_lyrics = info[0][0]
            track_names = info[1]
            track_ratings = info[2]

            words = st.checkbox("View Most Used Words per Album")
            if words:
                st.subheader("🎙 Most Used Words on Album ")
                all_lyrics_freq_dist = functions.generate_frequency_distribution(all_lyrics)
                max_len = max([len(x[0]) for x in all_lyrics_freq_dist])
                word_length = st.slider("Select a minimum word length", 1, max_len, 2)

                filtered_lyrics_by_length = functions.filter_by_length(all_lyrics_freq_dist, word_length)

                functions.generate_plot(filtered_lyrics_by_length)

                chart_data = pd.DataFrame({
                    'Tracks': track_names,
                    'Ratings': track_ratings,
                })
                chart_data = chart_data.sort_values(by=['Ratings'], ascending=False)

            ratings = st.checkbox("View Album Ratings")
            if ratings:
                st.subheader("🏆 Song Ratings by Album")

                st.altair_chart(alt.Chart(chart_data).mark_bar().encode(
                    x=alt.X('Tracks', sort=None),
                    y='Ratings',
                ), True)

# Artist Details Header
st.write("")
with st.container():

    st.header("🧭 Artist Details 🧭")
    st.caption("Provides insight on the current top 3 trending artist's in the U.S.")

    with st.expander("View Details"):
        artists_selected = st.selectbox("Select Artists", options=artists_list)
        # Return Artists Country
        if artists_selected:
            artist_country = functions.request_artist_country(artists[artists_selected])
            st.write(artists_selected, "- Trending Artist in the ", artist_country["message"]["body"]["artist"]["artist_country"])

            if artists_selected == "Walker Hayes":
                col1, col2 = st.columns(2)
                with col1:
                    st.image("media/walker-IMG.png")
                    st.subheader("Background")
                    st.markdown("**_Born:_** December 27th 1979")
                    st.markdown("**_From:_** Mobile, Alabama, U.S")
                    st.markdown("**_Genres:_** Pop Country")
                with col2:
                    walker_map = pd.DataFrame(
                        np.array([[30.6954, -88.0399]]), columns=['lat', 'lon'])
                    st.map(walker_map)
                    st.caption("Mobile is a port city on Alabama’s Gulf Coast.")

            if artists_selected == "Code Swindell":
                col1, col2 = st.columns(2)
                with col1:
                    st.image("media/cole-IMG.png")
                    st.subheader("Background")
                    st.markdown("**_Born:_** June 30th, 1983")
                    st.markdown("**_From:_** Bronwood, Georgia, U.S")
                    st.markdown("**_Genres:_** Country Pop")
                with col2:
                    code_map = pd.DataFrame(
                        np.array([[31.8310, -84.364332]]), columns=['lat', 'lon'])
                    st.map(code_map)
                    st.caption("Bronwood is a town in Terrell County, Georgia, U.S.")

            if artists_selected == "Lauren Spencer-Smith":
                col1, col2 = st.columns(2)
                with col1:
                    st.image("media/lauren-IMG.png")
                    st.subheader("Background")
                    st.markdown("**_Born:_** September 28th, 2003")
                    st.markdown("**_From:_** Portsmouth, England, U.K")
                    st.markdown("**_Genres:_** Pop")
                with col2:
                    code_map = pd.DataFrame(
                        np.array([[50.8198, -1.0880]]), columns=['lat', 'lon'])
                    st.map(code_map)
                    st.caption("Portsmouth is a port city and naval base on England’s south coast, "
                           "mostly spread across Portsea Island.")


# Sign Up Header
st.write("")
with st.container():

    st.header("📲 Sign up")
    st.caption("Sign up for email and text message notifications for chart updates.")
    col1, col2, col3 = st.columns(3)
    with col1:
        name = st.text_input('Enter Name', ' ')

    with col2:
        email = st.text_input('Enter Email', ' ')

    with col3:
        st.caption("Stay Updated!")
        submit = st.button("Submit")
        if submit:
            if name == ' ':
                st.error("Missing Name")
            if email == ' ':
                st.error("Missing Email")
            else:
                submit: \
                    st.text_area("Successfully Signed Up For Email Listing!", ""
                                    "Thank you for choosing World's Music!"
                                    " A verification email has been sent.")






