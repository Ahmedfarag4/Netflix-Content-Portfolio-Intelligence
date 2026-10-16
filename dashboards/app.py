from pathlib import Path
import plotly.express as px
import pandas as pd
import streamlit as st

NETFLIX_RED = "#E50914"
NETFLIX_DARK = "#141414"
NETFLIX_GRAY = "#B3B3B3"

st.set_page_config(
    page_title="Netflix Content Portfolio Intelligence",
    page_icon="🎬",
    layout="wide"
)


BASE_DIR = Path(__file__).resolve().parents[1]

CLEAN_DATA_PATH = BASE_DIR / "data" / "processed" / "netflix_cleaned.csv"
GENRES_DATA_PATH = BASE_DIR / "data" / "processed" / "netflix_genres.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(CLEAN_DATA_PATH)
    genres = pd.read_csv(GENRES_DATA_PATH)

    return df, genres


df, genres = load_data()
st.sidebar.header("Filters")

content_type_filter = st.sidebar.multiselect(
    "Content Type",
    options=sorted(df["type"].dropna().unique()),
    default=sorted(df["type"].dropna().unique())
)

country_options = sorted(
    df.loc[
        df["country_clean"] != "Unknown",
        "country_clean"
    ].dropna().unique()
)

country_filter = st.sidebar.multiselect(
    "Country",
    options=country_options,
    default=[]
)

audience_filter = st.sidebar.multiselect(
    "Audience Group",
    options=sorted(df["audience_group"].dropna().unique()),
    default=[]
)

release_year_range = st.sidebar.slider(
    "Release Year",
    min_value=int(df["release_year"].min()),
    max_value=int(df["release_year"].max()),
    value=(
        int(df["release_year"].min()),
        int(df["release_year"].max())
    )
)

filtered_df = df[
    df["type"].isin(content_type_filter)
].copy()

if country_filter:
    filtered_df = filtered_df[
        filtered_df["country_clean"].isin(country_filter)
    ]

if audience_filter:
    filtered_df = filtered_df[
        filtered_df["audience_group"].isin(audience_filter)
    ]

filtered_df = filtered_df[
    filtered_df["release_year"].between(
        release_year_range[0],
        release_year_range[1]
    )
]

st.sidebar.caption(
    f"Showing {len(filtered_df):,} of {len(df):,} titles"
)
if filtered_df.empty:
    st.warning(
        "No titles match the selected filters. "
        "Please adjust your filter selections."
    )
    st.stop()

st.markdown(
    """
    <h1 style="margin-bottom:0;">
        Netflix Content Portfolio Intelligence
    </h1>
    <p style="font-size:18px; color:#666; margin-top:6px;">
        Interactive analysis of content strategy, market distribution,
        audience segments, genres, and historical trends.
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <hr style="margin-top:10px; margin-bottom:20px;">
    """,
    unsafe_allow_html=True
)
with st.expander("Data Scope & Methodology"):
    st.markdown(
        f"""
        - **Dataset size:** {len(df):,} cleaned titles
        - **Release years:** {int(df["release_year"].min())}–{int(df["release_year"].max())}
        - **Netflix addition period:** {int(df["year_added"].min())}–{int(df["year_added"].max())}
        - **Data quality:** Business duplicates were removed and semantic missing values were handled during preprocessing.
        - **Important:** This is a historical Netflix catalog dataset and should not be interpreted as the current Netflix catalog.
        - **Audience groups:** Analytical segments derived from content ratings for this project, not official Netflix audience categories.
        """
    )

total_titles = len(filtered_df)
total_movies = (filtered_df["type"] == "Movie").sum()
total_tv_shows = (filtered_df["type"] == "TV Show").sum()

total_countries = (
    filtered_df.loc[
        filtered_df["country_clean"] != "Unknown",
        "country_clean"
    ]
    .nunique()
)

filtered_show_ids = set(filtered_df["show_id"])

total_genres = (
    genres[
        genres["show_id"].isin(filtered_show_ids)
    ]["genre"]
    .nunique()
)

total_countries = (
    df.loc[
        df["country_clean"] != "Unknown",
        "country_clean"
    ]
    .nunique()
)

total_genres = genres["genre"].nunique()


col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Titles", f"{total_titles:,}")
col2.metric("Movies", f"{total_movies:,}")
col3.metric("TV Shows", f"{total_tv_shows:,}")
col4.metric("Countries", f"{total_countries:,}")
col5.metric("Genres", f"{total_genres:,}")
avg_movie_duration = filtered_df.loc[
    filtered_df["type"] == "Movie",
    "duration_value"
].mean()

avg_tv_seasons = filtered_df.loc[
    filtered_df["type"] == "TV Show",
    "duration_value"
].mean()

metric_col1, metric_col2 = st.columns(2)

metric_col1.metric(
    "Avg. Movie Duration",
    f"{avg_movie_duration:.1f} min"
    if pd.notna(avg_movie_duration)
    else "N/A"
)

metric_col2.metric(
    "Avg. TV Show Length",
    f"{avg_tv_seasons:.2f} seasons"
    if pd.notna(avg_tv_seasons)
    else "N/A"
)

st.info(
    f"""
    **Portfolio Snapshot:**  
    Movies represent {total_movies / total_titles * 100:.1f}% of the current filtered catalog,
    while TV Shows represent {total_tv_shows / total_titles * 100:.1f}%.
    """
)

st.divider()

st.subheader("Content Overview")

content_type_counts = (
    filtered_df["type"]
    .value_counts()
    .reset_index()
)

content_type_counts.columns = [
    "Content Type",
    "Number of Titles"
]

fig_content_type = px.bar(
    content_type_counts,
    x="Content Type",
    y="Number of Titles",
    text="Number of Titles",
    title="Movies vs TV Shows",
    color_discrete_sequence=[NETFLIX_RED]
)

fig_content_type.update_traces(
    texttemplate="%{text:,}",
    textposition="outside"
)

fig_content_type.update_layout(
    xaxis_title="",
    yaxis_title="Number of Titles"
)

st.plotly_chart(
    fig_content_type,
    use_container_width=True
)
st.divider()

st.subheader("Market Distribution")

top_countries = (
    filtered_df[
        filtered_df["country_clean"] != "Unknown"
    ]["country_clean"]
    .value_counts()
    .head(10)
    .reset_index()
)

top_countries.columns = [
    "Country",
    "Number of Titles"
]

fig_countries = px.bar(
    top_countries,
    x="Number of Titles",
    y="Country",
    orientation="h",
    text="Number of Titles",
    title="Top 10 Countries by Number of Titles",
    color_discrete_sequence=[NETFLIX_RED]
)

fig_countries.update_traces(
    texttemplate="%{text:,}",
    textposition="outside"
)

fig_countries.update_layout(
    xaxis_title="Number of Titles",
    yaxis_title="",
    yaxis=dict(autorange="reversed")
)

st.plotly_chart(
    fig_countries,
    use_container_width=True
)
if not top_countries.empty:
    top_market = top_countries.iloc[0]

    top_market_share = (
        top_market["Number of Titles"]
        / total_titles
        * 100
    )

    st.info(
        f"""
        **Market Insight:**  
        {top_market["Country"]} is the largest market in the current selection,
        with {top_market["Number of Titles"]:,} titles,
        representing {top_market_share:.1f}% of the filtered catalog.
        """
    )

top_country_names = top_countries["Country"].tolist()

country_type = (
    filtered_df[
        filtered_df["country_clean"].isin(top_country_names)
    ]
    .groupby(["country_clean", "type"])
    .size()
    .reset_index(name="Number of Titles")
)

fig_country_type = px.bar(
    country_type,
    x="Number of Titles",
    y="country_clean",
    color="type",
    orientation="h",
    barmode="group",
    title="Movies vs TV Shows Across Top 10 Countries",
    
)

fig_country_type.update_layout(
    xaxis_title="Number of Titles",
    yaxis_title="",
    legend_title="Content Type",
    yaxis=dict(
        categoryorder="array",
        categoryarray=top_country_names[::-1]
    )
)

st.plotly_chart(
    fig_country_type,
    use_container_width=True
)
st.divider()

st.subheader("Historical Trends")

release_type_trend = (
    filtered_df
    .groupby(["release_year", "type"])
    .size()
    .reset_index(name="Number of Titles")
)

fig_release_trend = px.line(
    release_type_trend,
    x="release_year",
    y="Number of Titles",
    color="type",
    markers=True,
    title="Movies vs TV Shows by Release Year"
)

fig_release_trend.update_layout(
    xaxis_title="Release Year",
    yaxis_title="Number of Titles",
    legend_title="Content Type"
)

st.plotly_chart(
    fig_release_trend,
    use_container_width=True
)
added_type_trend = (
    filtered_df
    .groupby(["year_added", "type"])
    .size()
    .reset_index(name="Number of Titles")
)

fig_added_trend = px.line(
    added_type_trend,
    x="year_added",
    y="Number of Titles",
    color="type",
    markers=True,
    title="Movies vs TV Shows Added to Netflix by Year"
)

fig_added_trend.update_layout(
    xaxis_title="Year Added",
    yaxis_title="Number of Titles",
    legend_title="Content Type"
)

st.plotly_chart(
    fig_added_trend,
    use_container_width=True
)
st.divider()

st.subheader("Audience Analysis")

audience_counts = (
    filtered_df["audience_group"]
    .value_counts()
    .reset_index()
)

audience_counts.columns = [
    "Audience Group",
    "Number of Titles"
]

fig_audience = px.bar(
    audience_counts,
    x="Number of Titles",
    y="Audience Group",
    color_discrete_sequence=[NETFLIX_RED],
    orientation="h",
    text="Number of Titles",
    title="Netflix Content by Audience Group"
)

fig_audience.update_traces(
    texttemplate="%{text:,}",
    textposition="outside"
)

fig_audience.update_layout(
    xaxis_title="Number of Titles",
    yaxis_title="",
    yaxis=dict(autorange="reversed")
)

st.plotly_chart(
    fig_audience,
    use_container_width=True
)
if not audience_counts.empty:
    top_audience = audience_counts.iloc[0]

    top_audience_share = (
        top_audience["Number of Titles"]
        / total_titles
        * 100
    )

    st.info(
        f"""
        **Audience Insight:**  
        {top_audience["Audience Group"]} is the dominant audience segment
        in the current selection, with {top_audience["Number of Titles"]:,} titles,
        representing {top_audience_share:.1f}% of the filtered catalog.
        """
    )

audience_type = (
    filtered_df
    .groupby(["audience_group", "type"])
    .size()
    .reset_index(name="Number of Titles")
)

fig_audience_type = px.bar(
    audience_type,
    x="Number of Titles",
    y="audience_group",
    color="type",
    orientation="h",
    barmode="group",
    title="Audience Groups by Content Type"
)

fig_audience_type.update_layout(
    xaxis_title="Number of Titles",
    yaxis_title="",
    legend_title="Content Type"
)

st.plotly_chart(
    fig_audience_type,
    use_container_width=True
)
st.divider()

st.subheader("Genre Analysis")

filtered_show_ids = set(filtered_df["show_id"])

filtered_genres = genres[
    genres["show_id"].isin(filtered_show_ids)
].copy()

top_genres = (
    filtered_genres["genre"]
    .value_counts()
    .head(15)
    .reset_index()
)

top_genres.columns = [
    "Genre",
    "Number of Titles"
]

fig_genres = px.bar(
    top_genres,
    x="Number of Titles",
    color_discrete_sequence=[NETFLIX_RED],
    y="Genre",
    orientation="h",
    text="Number of Titles",
    title="Top 15 Genres"
)

fig_genres.update_traces(
    texttemplate="%{text:,}",
    textposition="outside"
)

fig_genres.update_layout(
    xaxis_title="Number of Titles",
    yaxis_title="",
    yaxis=dict(autorange="reversed")
)

st.plotly_chart(
    fig_genres,
    use_container_width=True
)
if not top_genres.empty:
    top_genre = top_genres.iloc[0]

    top_genre_share = (
        top_genre["Number of Titles"]
        / total_titles
        * 100
    )

    st.info(
        f"""
        **Genre Insight:**  
        {top_genre["Genre"]} is the most represented genre
        in the current selection, appearing in {top_genre["Number of Titles"]:,} titles.

        This equals approximately {top_genre_share:.1f}% of the filtered catalog.
        """
    )

movie_genres = (
    filtered_genres[
        filtered_genres["type"] == "Movie"
    ]["genre"]
    .value_counts()
    .head(10)
    .reset_index()
)


movie_genres.columns = [
    "Genre",
    "Number of Titles"
]


tv_genres = (
    filtered_genres[
        filtered_genres["type"] == "TV Show"
    ]["genre"]
    .value_counts()
    .head(10)
    .reset_index()
)

tv_genres.columns = [
    "Genre",
    "Number of Titles"
]


col1, col2 = st.columns(2)


with col1:
    fig_movie_genres = px.bar(
        movie_genres,
        x="Number of Titles",
        y="Genre",
        orientation="h",
        title="Top 10 Movie Genres"
    )

    fig_movie_genres.update_layout(
        xaxis_title="Number of Titles",
        yaxis_title="",
        yaxis=dict(autorange="reversed")
    )

    st.plotly_chart(
        fig_movie_genres,
        use_container_width=True
    )


with col2:
    fig_tv_genres = px.bar(
        tv_genres,
        x="Number of Titles",
        y="Genre",
        orientation="h",
        title="Top 10 TV Show Genres"
    )

    fig_tv_genres.update_layout(
        xaxis_title="Number of Titles",
        yaxis_title="",
        yaxis=dict(autorange="reversed")
    )

    st.plotly_chart(
        fig_tv_genres,
        use_container_width=True
    )
    st.divider()

st.subheader("Duration Analysis")

movie_duration = filtered_df.loc[
    filtered_df["type"] == "Movie",
    "duration_value"
]

tv_seasons = filtered_df.loc[
    filtered_df["type"] == "TV Show",
    "duration_value"
]

col1, col2 = st.columns(2)

with col1:
    fig_movie_duration = px.histogram(
        movie_duration,
        nbins=30,
        color_discrete_sequence=[NETFLIX_RED],
        title="Movie Duration Distribution",
        labels={"value": "Duration (Minutes)"}
    )

    fig_movie_duration.update_layout(
        xaxis_title="Duration (Minutes)",
        yaxis_title="Number of Movies",
        showlegend=False
    )

    st.plotly_chart(
        fig_movie_duration,
        use_container_width=True
    )

with col2:
    season_counts = (
        tv_seasons
        .value_counts()
        .sort_index()
        .reset_index()
    )

    season_counts.columns = [
        "Number of Seasons",
        "Number of TV Shows"
    ]

    fig_tv_seasons = px.bar(
        season_counts,
        x="Number of Seasons",
        color_discrete_sequence=[NETFLIX_RED],
        y="Number of TV Shows",
        title="TV Shows by Number of Seasons"
    )

    fig_tv_seasons.update_layout(
        xaxis_title="Number of Seasons",
        yaxis_title="Number of TV Shows"
    )

    st.plotly_chart(
        fig_tv_seasons,
        use_container_width=True
    )
    st.divider()

st.subheader("Content Age Analysis")

content_age_data = (
    filtered_df["content_age_group"]
    .value_counts()
    .reindex([
        "Same Year",
        "1-2 Years",
        "3-5 Years",
        "6-10 Years",
        "10+ Years"
    ])
    .reset_index()
)

content_age_data.columns = [
    "Content Age Group",
    "Number of Titles"
]

content_age_data["Percentage"] = (
    content_age_data["Number of Titles"]
    / content_age_data["Number of Titles"].sum()
    * 100
).round(2)

fig_content_age = px.bar(
    content_age_data,
    x="Content Age Group",
    color_discrete_sequence=[NETFLIX_RED],
    y="Number of Titles",
    text="Percentage",
    title="How Quickly Content Was Added to Netflix"
)

fig_content_age.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_content_age.update_layout(
    xaxis_title="Years Between Release and Netflix Addition",
    yaxis_title="Number of Titles"
)

st.plotly_chart(
    fig_content_age,
    use_container_width=True
)
same_year_count = content_age_data.loc[
    content_age_data["Content Age Group"] == "Same Year",
    "Number of Titles"
].sum()

one_two_years_count = content_age_data.loc[
    content_age_data["Content Age Group"] == "1-2 Years",
    "Number of Titles"
].sum()

recent_additions = same_year_count + one_two_years_count

valid_age_total = content_age_data["Number of Titles"].sum()

recent_share = (
    recent_additions / valid_age_total * 100
    if valid_age_total > 0
    else 0
)

st.info(
    f"""
    **Content Age Insight:**  
    {recent_share:.1f}% of titles in the current selection were added to Netflix
    within two years of their release.
    """
)
age_type = (
    filtered_df
    .dropna(subset=["content_age_group"])
    .groupby(
        ["content_age_group", "type"],
        observed=False
    )
    .size()
    .reset_index(name="Number of Titles")
)

age_type = age_type.rename(
    columns={
        "content_age_group": "Content Age Group",
        "type": "Content Type"
    }
)

fig_age_type = px.bar(
    age_type,
    x="Content Age Group",
    y="Number of Titles",
    color="Content Type",
    barmode="group",
    title="Content Age by Content Type",
    category_orders={
        "Content Age Group": [
            "Same Year",
            "1-2 Years",
            "3-5 Years",
            "6-10 Years",
            "10+ Years"
        ]
    }
)

fig_age_type.update_layout(
    xaxis_title="Years Between Release and Netflix Addition",
    yaxis_title="Number of Titles",
    legend_title="Content Type"
)

st.plotly_chart(
    fig_age_type,
    use_container_width=True
)
st.divider()

st.subheader("Market Audience Mix")

top_country_names = top_countries["Country"].tolist()

filtered_top_countries = (
    filtered_df[
        filtered_df["country_clean"] != "Unknown"
    ]["country_clean"]
    .value_counts()
    .head(10)
    .index
    .tolist()
)

country_audience = (
    filtered_df[
        filtered_df["country_clean"].isin(filtered_top_countries)
    ]
    .groupby(["country_clean", "audience_group"])
    .size()
    .unstack(fill_value=0)
)

country_audience_pct = (
    country_audience
    .div(country_audience.sum(axis=1), axis=0)
    .mul(100)
    .round(1)
)

fig_market_audience = px.imshow(
    country_audience_pct,
    text_auto=".1f",
    aspect="auto",
    title="Audience Mix Across Top Netflix Markets",
    labels={
        "x": "Audience Group",
        "y": "Country",
        "color": "Percentage"
    }
)

fig_market_audience.update_layout(
    xaxis_title="Audience Group",
    yaxis_title="Country"
)

st.plotly_chart(
    fig_market_audience,
    use_container_width=True
)
st.divider()

st.subheader("Explore Filtered Data")

with st.expander("View filtered records"):
    st.dataframe(
        filtered_df[
            [
                "title",
                "type",
                "country_clean",
                "release_year",
                "rating",
                "audience_group",
                "duration"
            ]
        ],
        use_container_width=True
    )

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name="netflix_filtered_data.csv",
    mime="text/csv"
)