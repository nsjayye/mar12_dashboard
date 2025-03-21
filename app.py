# to import libraries
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
import numpy as np

# first part of the website & setting up the page
st.set_page_config(page_title = "Dashboard", page_icon='📊', layout='centered')
st.title("📊 Welcome to the dashboard 📊")
st.subheader("Select the options below to filter our dataset!")

# to read csv file (our dataset)
ori_data = pd.read_csv('global_biodiversity_dataset.csv')

# convert Date_Time into datetime obj
ori_data['Date_Time'] = pd.to_datetime(ori_data['Date_Time'])
df_data = pd.DataFrame(ori_data)

# to filter out species name and country
names = st.multiselect("Select Species Name", df_data['Species_Name'].unique())
countries = st.multiselect("Select Countries", df_data['Country'].unique())
ecosystem = st.multiselect("Select Ecosystems", df_data['Ecosystem_Type'].unique())

# filter condition check (if multiselect is empty, select all data)
# else, only select the ones they wish to filter
if names == []:
    s_names = df_data['Species_Name'].unique()
else:
    s_names = names 

if countries == []:
    s_countries = df_data['Country'].unique()
else:
    s_countries = countries

if ecosystem == []:
    s_ecosystems = df_data['Ecosystem_Type'].unique()
else:
    s_ecosystems = ecosystem

# to select the appropriate data from the dataset according to selected options
data = ori_data[(ori_data.Species_Name.isin(s_names)) & (ori_data.Country.isin(s_countries)) & (ori_data.Ecosystem_Type.isin(s_ecosystems))]

# to show the different graphs in each tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['Dataset', 'Box Plot', 'Pie Chart 1', 'Pie Chart 2', 'Heat Map', 'Bar Chart'])

# Group by observer type and calculate summary statistics
def graph1():
    st.subheader("Our overall dataset")
    observer_stats = data.groupby("Observer_Type").describe() # lattiude and longtitude are significantly different, which may imply that the locations of data found may be different
    st.dataframe(data)

    st.write("Feel free to sort each columns in any order you'd like! (ascending/descending, etc.)")

def graph2():
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=data, x="Observer_Type", y="Species_Abundance", palette="Set2")
    plt.title("Species Abundance Across Observer Types")
    plt.xticks(rotation=45)
    st.pyplot(plt)

    st.subheader("❔What does this chart mean?")
    st.write("This box plot compares the abundance of species, showing the maximum, minimum and median number of species observed.")
    st.write("In this instance, it shows that there is no significant differences between the different observer types. This implies that there is little to no bias when it comes to preferring a higher or lower abundance of animals to observe for all observer types.")
    

def graph3():
    # types of weather condition and its occurrence, displayed as pie chart
    st.subheader("Pie chart of the weather conditions and its occurrence")
    weathers = {}

    # add weather and count into a dictionary
    for weather, count in data["Weather_Condition"].value_counts().items():
        if weather not in weathers: # check if weather exists in the dictionary first before adding
            weathers[weather] = count

    # convert weather and count into np array
    my_weather = np.array(list(weathers.keys()))
    my_count1 = np.array(list(weathers.values()))

    #create pie chart
    fig1, ax1 = plt.subplots()
    ax1.pie(my_count1, labels=my_weather, autopct='%1.1f%%',colors=sns.color_palette('Set2'))
    ax1.axis('equal')
    st.pyplot(fig1)

    #to show what the pie chart will show
    st.subheader("❔What does this chart mean?")
    st.write("This pie chart shows the proportion of each unique weather found in the (filtered) dataset. This can be used to determine if there is any skewedness when recording the data.")
    st.write("For example, if the data percentage for the 'rainy' weather is significantly higher than the rest, then the dataset may be biased towards recording data when raining.")

def graph4():
    # find proportion of observer_type and display as pie chart
    st.subheader("Pie chart of the proportion of observer types")
    observers = {}

    # add observer and count into a dictionary
    for observer, count in data["Observer_Type"].value_counts().items():
        if observer not in observers: # check if observer exists in the dictionary first before adding
            observers[observer] = count

    # convert observer and count into np array
    my_label = np.array(list(observers.keys()))
    my_count2 = np.array(list(observers.values()))

    #create pie chart
    fig1, ax1 = plt.subplots()
    ax1.pie(my_count2, labels=my_label, autopct='%1.1f%%',colors=sns.color_palette('Set2'))
    ax1.axis('equal')
    st.pyplot(fig1)

    #to show what the pie chart will show
    st.subheader("❔What does this chart mean?")
    st.write("This pie chart shows the proportion of each unique observer type found in the (filtered) dataset. This can be used to determine if there is any skewedness when recording the data.")
    st.write("For example, if the data percentage collected by 'researcher' is significantly higher than the rest, then the dataset may be biased towards having researchers to record the data.")

def graph5():
    species_observer_counts = data.groupby(['Species_Name', 'Observer_Type']).size().reset_index(name='Counts')
    # Create pivot table
    heatmap_data = species_observer_counts.pivot(index='Species_Name', columns='Observer_Type', values='Counts').fillna(0)

    # Create visualization
    plt.figure(figsize=(14, 12))  # Large figure for better readability

    ax = sns.heatmap(
        heatmap_data,
        cmap='YlGnBu',
        linewidths=0.5,
        linecolor='lightgray',
        annot=True,               # Show numbers in cells
        fmt='d',
        annot_kws={'size': 10},
        cbar_kws={'label': 'Number of Observations'}  # Colorbar label
    )

    # Customize title
    plt.title("How Different Observer Types Track Species\n")


    plt.xticks(rotation=45)
    plt.yticks()


    plt.tight_layout()
    plt.savefig('species_observations_heatmap.png')
    st.pyplot(plt)

    st.subheader("❔What does this chart mean?")
    st.write("The heatmap shows how different observer types contribute to species tracking in unique ways. "
    "Automated sensors outstanding at capturing species that are either very active or difficult for humans to observe, "
    "such as Honeybees and Snowy Owls.  Their consistent and automated monitoring makes it easier to detect these species."
    "Citizen Scientists often focus on species that are visually interesting and attract their attention, such as Coral Reef "
    "Fish, Blue jays, and Green Frogs.")
    st.write("Their observations often reflect a bias towards colourful species. Lastly, Researchers "
    "specialise in targeted studies. They focus on specials that require scientific precision, such as the Great White Shark, "
    "and use specialised tools (e.g. microscopes) to detect species that casual observers unable to detect.It's a bit like a "
    "treasure hunt. Citizen Scientists explore broadly and gather lots of common finds, while Researchers dig deep in one spot"
    " and uncover the rare gems.")
    st.write("Both approaches give us a fuller picture of biodiversity, and this heatmap helps show the strengths "
    "and biases of each observer type.")

def graph6():
    observer_country_counts = data.groupby(["Observer_Type", "Country"]).size().unstack(fill_value=0).stack().reset_index(name="Count")

    #bar plot
    plt.figure(figsize=(14, 10))
    sns.barplot(x="Country", y="Count", hue="Observer_Type", data=observer_country_counts)

    # labels and title
    plt.xlabel("Country", fontsize=15)
    plt.ylabel("Number of Reports", fontsize=15)
    plt.title("Observer Type Reports for All Countries", fontsize=14)
    plt.xticks(rotation=45)

    # move legend outside the graph
    plt.legend(title="Observer Type", bbox_to_anchor=(1.05, 1), loc="upper left")
    st.pyplot(plt)

    st.subheader("❔What does this chart mean?")
    st.write("This bar chart displays the number of reports recorded for each country, categorized by obeserver type. It helps identify patterns in how different observer types contribute to data collection across various countries.")
    st.write("For example, if one observer type has significantly higher number of reports in a specific country, it may indicate that certain observer groups are more active or that the data collection process favors specific observers.")


# st.pyplot()
with tab1:
    graph1()
with tab2:
    graph2()
with tab3:
    graph3()
with tab4:
    graph4()
with tab5:
    graph5()
with tab6:
    graph6()