import streamlit as st
import pandas as pd
import altair as alt

# Load data
gp = pd.read_excel('gp_visualized.xlsx')

# Add unique label for each person
gp['Label'] = gp['First Name'] + ' ' + gp['Last Name']

# ========== TITLE ==========
st.title("Gameplay Engineers Diversity Talent Mapping & Competitor Analysis")
st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)

# ========== PLOT 1: SCATTER PLOTS (She/Her & He/Him) ==========
filtered_df_she = gp[gp['Tags'] == 'She/Her']
filtered_df_he = gp[gp['Tags'] == 'He/Him']

select_level = alt.selection_point(fields=['Level'], bind='legend')
countries_sorted = sorted(gp['Country'].dropna().unique())
dropdown_country = alt.binding_select(name='Country: ', options=countries_sorted)
selection_country = alt.selection_point(fields=['Country'], bind=dropdown_country)

# Scatter plot for She/Her
scatter_chart_she = alt.Chart(filtered_df_she).mark_circle(size=60).encode(
    x='AAA Experience:Q',
    y='Total Experience:Q',
    color='Level:N',
    opacity=alt.condition(select_level, alt.value(0.8), alt.value(0.1)),
    tooltip=[
        'First Name', 'Last Name', 'AAA Experience', 'Total Experience',
        'Current Position', 'Current Studio'
    ]
).transform_filter(
    selection_country
).properties(
    title=alt.TitleParams('Gameplay Engineer Diverse Talent (She/Her) Experience Level', anchor='middle'),
    width=400
).add_params(
    selection_country, select_level
).interactive()

# Scatter plot for He/Him
scatter_chart_he = alt.Chart(filtered_df_he).mark_circle(size=60).encode(
    x='AAA Experience:Q',
    y='Total Experience:Q',
    color='Level:N',
    opacity=alt.condition(select_level, alt.value(0.8), alt.value(0.1)),
    tooltip=[
        'First Name', 'Last Name', 'AAA Experience', 'Total Experience',
        'Current Position', 'Current Studio'
    ]
).transform_filter(
    selection_country
).properties(
    title=alt.TitleParams('Gameplay Engineer (He/Him) Experience Level', anchor='middle'),
    width=400
).add_params(
    selection_country, select_level
).interactive()

# Combine scatter plots
scatter_plots = (scatter_chart_she | scatter_chart_he).configure_view(stroke=None)
st.altair_chart(scatter_plots, use_container_width=True)

# ========== SELECT AND SHOW LINKEDIN URL ==========
st.markdown("### 🔎 Select a talent to view their LinkedIn Profile")

selected_label = st.selectbox("Choose a person from the plots above:", gp['Label'].unique())

# Show LinkedIn URL
person = gp[gp['Label'] == selected_label]
if not person.empty:
    linkedin_url = person['LinkedIn Url'].values[0]
    st.markdown(f"🔗 [View {selected_label}'s LinkedIn Profile]({linkedin_url})", unsafe_allow_html=True)

# ========== SPACING ==========
st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)

# ========== PLOT 2: TALENT SOURCING SCATTER ==========
st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

# Prepare filter inputs
sorted_tags = sorted(gp['Tags'].dropna().unique())
studio_sorted = sorted(gp['Current Studio'].dropna().unique())

# Altair bindings
radiobuttons_tags = alt.binding_radio(name='Pronoun: ', options=sorted_tags)
slider_AAA = alt.binding_range(name='AAA Experience', min=0, max=50, step=1)
dropdown_studio = alt.binding_select(name='Studio Name: ', options=studio_sorted)
dropdown_country_2 = alt.binding_select(name='Country: ', options=countries_sorted)

# Selections
selection_tags = alt.selection_point(fields=['Tags'], bind=radiobuttons_tags)
selection_AAA = alt.selection_point(fields=['AAA Experience'], bind=slider_AAA)
selection_studio = alt.selection_point(fields=['Current Studio'], bind=dropdown_studio)
selection_country2 = alt.selection_point(fields=['Country'], bind=dropdown_country_2)

# Final scatter plot
final_plot = alt.Chart(gp).mark_circle(size=60).encode(
    x='AAA Experience:Q',
    y='Total Experience:Q',
    color='Level:N',
    tooltip=[
        'First Name', 'Last Name', 'AAA Experience', 'Total Experience',
        'Current Position', 'Current Studio', 'Country', 'Tags'
    ],
    opacity=alt.condition(selection_tags, alt.value(1), alt.value(0.1))
).transform_filter(
    selection_AAA & selection_studio & selection_country2
).properties(
    title=alt.TitleParams("Talent Sourcing & Competitior analysis for Gameplay Engineer", anchor='middle'),
    width=700,
    height=450
).add_params(
    selection_tags,
    selection_AAA,
    selection_studio,
    selection_country2
).interactive().configure_view(stroke=None)

st.altair_chart(final_plot, use_container_width=True)

# ========== SELECT FROM FINAL PLOT ==========
st.markdown("### 🔎 Select a talent to view their LinkedIn Profile")

selected_label_2 = st.selectbox("Choose a talent from plot above:", gp['Label'].unique())

person2 = gp[gp['Label'] == selected_label_2]
if not person2.empty:
    linkedin_url2 = person2['LinkedIn Url'].values[0]
    st.markdown(f"🔗 [View {selected_label_2}'s LinkedIn Profile]({linkedin_url2})", unsafe_allow_html=True)
