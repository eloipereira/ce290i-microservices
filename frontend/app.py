import os

import matplotlib.pyplot as plt
import requests
import streamlit as st

# Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000/users/")

st.title("User Age Distribution")

# Button to fetch and plot data
if st.button("Get User Ages and Plot Histogram"):
    try:
        # Fetch users from API
        response = requests.get(API_URL)

        if response.status_code == 200:
            users_data = response.json()

            # Extract ages from the response
            ages = [user["age"] for user in users_data.values()]

            if ages:
                st.success(f"Found {len(ages)} users")

                # Create histogram
                fig, ax = plt.subplots()
                ax.hist(ages, bins=10, edgecolor="black")
                ax.set_xlabel("Age")
                ax.set_ylabel("Number of Users")
                ax.set_title("User Age Distribution")

                # Display the plot
                st.pyplot(fig)

                # Show some stats
                st.write("**Statistics:**")
                st.write(f"- Total users: {len(ages)}")
                st.write(f"- Average age: {sum(ages)/len(ages):.1f}")
                st.write(f"- Youngest: {min(ages)}")
                st.write(f"- Oldest: {max(ages)}")
            else:
                st.warning("No users found")
        else:
            st.error(f"API Error: {response.status_code}")

    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to API. Make sure it's running on http://localhost:8000")
    except Exception as e:
        st.error(f"Error: {e}")
