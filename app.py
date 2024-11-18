""" main app """

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from wordcloud import WordCloud

from gitdashboard_app.utils import fetch_data, find_most_common_word


@st.cache_data
def get_data(url):
    """("call the function fetch_data from gitdashboard_app.utils "
    "with the url of the endpoint as param)"""
    return fetch_data(url)


URL = "https://api.github.com/users/torvalds/repos"

data = get_data(URL).json()
df = pd.DataFrame(data)

owners = pd.json_normalize(df["owner"])

with st.sidebar:
    selected_owner = st.selectbox(
        "Select the git user you would like to see ",
        owners["login"].unique(),
        index=None,
        placeholder="Select a git user...",
    )
    df_owner_filtered = df[
        df["owner"].apply(lambda x: x.get("login") == selected_owner)
    ]

st.title("Git user dashsboard")

tab1, tab2, tab3 = st.tabs(["global_overview", "project_overview", "owner_overview"])
with tab1:
    if not df_owner_filtered.empty:

        most_popular_project = df_owner_filtered.loc[
            df_owner_filtered["watchers_count"].idxmax()
        ]
        most_recent_update = df_owner_filtered.loc[
            df_owner_filtered["updated_at"].idxmax()
        ]
        ALL_DESCRIPTIONS = " ".join(df_owner_filtered["description"])
        count_project_with_description = df_owner_filtered["description"].count()
        mostCommonWordDescription = find_most_common_word(ALL_DESCRIPTIONS)

        st.title(f"Overview of projects from {selected_owner}")
        st.write("Number of opened issues per project")
        st.bar_chart(
            data=df_owner_filtered,
            x="name",
            y="open_issues",
            x_label="Git project name",
            y_label="number of opened issues",
            use_container_width=True,
        )

        st.write("Number of forks per project")
        st.bar_chart(
            data=df_owner_filtered,
            x="name",
            y="forks",
            x_label="Git project name",
            y_label="number of forks",
            use_container_width=True,
        )

        st.write(
            f"The most popular project is {most_popular_project['name']} "
            f"with {most_popular_project['watchers_count']} watchers."
        )
        st.write(
            f"The latest update was made at  {most_recent_update['updated_at']}. "
            f"It was an update on the "
            f"project {most_recent_update['name']}."
        )
        st.write(
            f"{count_project_with_description} projects have a "
            f"description, here is a wordcloud of the more frequent "
            f"words in the descriptions."
        )

        wordcloud = WordCloud().generate(ALL_DESCRIPTIONS)
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        st.pyplot(plt)
        st.write(
            f"The most common words across all the projects description is "
            f"'{mostCommonWordDescription[0]}', it appears {mostCommonWordDescription[1]} times"
        )
    else:
        st.write("no user selected")

with tab2:
    st.title("Project details")
    st.write("Please select a project")
    selected_project = st.selectbox(
        "Select the project you would like to see ",
        df_owner_filtered["name"].unique(),
        index=None,
        placeholder="Select a project...",
    )
    if selected_project:
        df_specific_project = df_owner_filtered[
            df_owner_filtered["name"] == selected_project
        ]
        st.write(f"Main KPI for the project {selected_project}")
        col1, col2, col3 = st.columns(3)
        col1.metric("forks", df_specific_project["forks_count"])
        col2.metric("open_issues", df_specific_project["open_issues"])
        col3.metric("watchers", df_specific_project["watchers"])

with tab3:
    st.title("Information about the git account")
    # st.write(f"Username {owners['login'][0]}")
    if not df_owner_filtered.empty:
        st.write(f"git project url {owners['html_url'][0]}")
        st.write(f"the user has a {owners['user_view_type'][0]} profile")
        st.write(f"Number of projects: {len(df)}")
        st.write("Avatar :")
        st.markdown(f"![Avatar]({owners['avatar_url'][0]})")

    else:
        st.write("no user selected")
