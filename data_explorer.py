import streamlit as st
import pandas as pd
import requests

st.set_page_config(
    page_title="User Data Explorer",
    page_icon="📊",
    layout="wide"
)

@st.cache_data
def fetch_users():
    response = requests.get(
        "https://jsonplaceholder.typicode.com/users"
    )

    if not response.ok:
        raise Exception(
            f"HTTP {response.status_code}"
        )

    return response.json()


users = fetch_users()

rows = []

for user in users:
    rows.append({
        "Name": user["name"],
        "Email": user["email"],
        "City": user["address"]["city"],
        "Company": user["company"]["name"]
    })

df = pd.DataFrame(rows)


st.title("📊 User Data Explorer")


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Users",
        len(df)
    )

with col2:
    st.metric(
        "Unique Cities",
        df["City"].nunique()
    )

with col3:
    st.metric(
        "Unique Companies",
        df["Company"].nunique()
    )


st.divider()


with st.sidebar:
    st.title("🔍 Filters")

    name_filter = st.text_input(
        "Search by name"
    )


if name_filter:
    filtered_df = df[
        df["Name"].str.contains(
            name_filter,
            case=False,
            na=False
        )
    ]
else:
    filtered_df = df


st.subheader("Users")

st.dataframe(
    filtered_df,
    use_container_width=True
)


st.subheader("Users per City")

city_counts = (
    filtered_df["City"]
    .value_counts()
    .reset_index()
)

city_counts.columns = ["City", "Users"]

st.bar_chart(
    city_counts,
    x="City",
    y="Users"
)