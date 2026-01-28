import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
from collections import Counter

# Page config
st.set_page_config(page_title="Chat History Analyzer", layout="centered")

st.title("💬 Chat History Analyzer")
st.write("Upload a chat file to analyze messages, users, and word usage.")

# File upload
uploaded_file = st.file_uploader("Upload chat file (.txt)", type="txt")

if uploaded_file:
    data = uploaded_file.read().decode("utf-8")

    messages = []
    users = []

    lines = data.split("\n")

    for line in lines:
        match = re.match(r"(.*?)-(.*?):(.*)", line)
        if match:
            users.append(match.group(2).strip())
            messages.append(match.group(3).strip())

    # Create DataFrame
    df = pd.DataFrame({
        "User": users,
        "Message": messages
    })

    st.subheader("📊 Basic Statistics")
    st.write(f"**Total Messages:** {len(df)}")
    st.write(f"**Total Users:** {df['User'].nunique()}")

    # Messages per user
    user_counts = df["User"].value_counts()

    st.subheader("👤 Messages per User")
    st.dataframe(user_counts)

    # Most active user
    st.success(f"🏆 Most Active User: {user_counts.idxmax()}")

    # Bar Chart
    st.subheader("📈 User Activity Chart")
    fig, ax = plt.subplots()
    user_counts.plot(kind='bar', ax=ax)
    ax.set_xlabel("User")
    ax.set_ylabel("Messages")
    st.pyplot(fig)

    # Word Analysis
    st.subheader("📝 Most Common Words")

    words = []
    for msg in df["Message"]:
        clean_words = re.findall(r"\b\w+\b", msg.lower())
        words.extend(clean_words)

    common_words = Counter(words).most_common(10)
    word_df = pd.DataFrame(common_words, columns=["Word", "Frequency"])

    st.table(word_df)

else:
    st.info("👆 Please upload a chat file to begin analysis.")
