import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from instagrapi import Client
import json

# Read the credentials from the JSON file
with open('credentials.json') as file:
    credentials = json.load(file)

# Access the individual credentials
username = credentials['username']
password = credentials['password']

cl = Client()
cl.login(username, password, verification_code="<2FA CODE HERE>")

# Function to retrieve hashtag data
def retrieve_hashtag_data(hashtag, amount=50):
    medias = cl.hashtag_medias_top(hashtag, amount=amount)
    data = []
    for media in medias:
        media_data = {
            'Hashtag': hashtag,
            'Username': media.user.username,
            'Likes': media.like_count,
            'Comments': media.comment_count,
            'Location': media.location,
            'Caption': media.caption_text
        }
        data.append(media_data)
    return pd.DataFrame(data)

# Streamlit app
st.title('Hashtag Analysis')

# User input for first hashtag
hashtag1 = st.text_input('Enter the first hashtag')

# User input for second hashtag
hashtag2 = st.text_input('Enter the second hashtag')

# User input for third hashtag
hashtag3 = st.text_input('Enter the third hashtag')

if hashtag1 and hashtag2 and hashtag3:
    # Retrieve data for the first hashtag
    df1 = retrieve_hashtag_data(hashtag1)

    # Retrieve data for the second hashtag
    df2 = retrieve_hashtag_data(hashtag2)

    # Retrieve data for the third hashtag
    df3 = retrieve_hashtag_data(hashtag3)

    # Combine the dataframes
    df = pd.concat([df1, df2, df3])

    # Plotting the analysis diagram
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    # Bar plot for Likes
    axs[0].bar(df['Hashtag'], df['Likes'], alpha=0.7, label='Likes')
    axs[0].set_ylabel('Total Likes')
    axs[0].set_title(f'Comparison of Total Likes for Hashtags')

    # Bar plot for Comments
    axs[1].bar(df['Hashtag'], df['Comments'], alpha=0.7, label='Comments')
    axs[1].set_ylabel('Total Comments')
    axs[1].set_title(f'Comparison of Total Comments for Hashtags')

    axs[0].legend()
    axs[1].legend()
    plt.tight_layout()

    # Display the plot on Streamlit
    st.pyplot(fig)

    # Pie chart for overall engagement
    fig, ax = plt.subplots(figsize=(6, 6))
    engagement = df.groupby('Hashtag')['Likes', 'Comments'].sum()
    ax.pie(engagement.sum(), labels=engagement.index, autopct='%1.1f%%', startangle=90)
    ax.set_title('Overall Engagement Distribution')

    # Display the pie chart on Streamlit
    st.pyplot(fig)
    
    # Find the most used hashtag
    most_used_hashtag = df['Hashtag'].value_counts().idxmax()

    # Filter the DataFrame for the most used hashtag
    most_used_hashtag_df = df[df['Hashtag'] == most_used_hashtag]

    # Find the user with the most followers among the most used hashtag
    most_followers_user = most_used_hashtag_df[most_used_hashtag_df['Followers'] == most_used_hashtag_df['Followers'].max()]['Username'].iloc[0]
    most_followers_count = most_used_hashtag_df['Followers'].max()

    # Display the user with the most followers among the most used hashtag
    st.write("User with the most followers among the most used hashtag:")
    st.write("Hashtag:", most_used_hashtag)
    st.write("Username:", most_followers_user)
    st.write("Followers:", most_followers_count)

else:
    st.write('Enter all three hashtags to see the analysis.')
