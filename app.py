import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly
import palmerpenguins  # This package provides the Palmer Penguins dataset
import pandas as pd
import seaborn as sns
from shiny import reactive, render, req

# Loading Palmer Penguins dataset
penguins= palmerpenguins.load_penguins()

# Naming page
ui.page_opts(title="K.Young Penguin Visualization", fillable=True)

# Add a Shiny UI sidebar
with ui.sidebar(open="open"):
    ui.h2("Sidebar")

# Create a dropdown input to choose a column with ui.input_selectize()
    ui.input_selectize("selected_attribute","Select Attribute",["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"])

# Add numeric input for the number of Plotly histogram bins
    ui.input_numeric("plotly_bin_count", "Number of Plotly Histogram Bins", value=20)

# Add slider input for the number of Seaborn bin
    ui.input_slider("seaborn_bin_count", "Number of Seaborn Bins", 1, 20, 5)

# Add checkbox group input to filter the species
    ui.input_checkbox_group(
    "selected_species_list",
    "Select Species",
    ["Adelie", "Gentoo", "Chinstrap"],
    selected=["Adelie"],
    inline=True)

# Adding a horizontal rule to the sidebar
    ui.hr()

# Using ui.a() to add a hyperlink to the sidebar
    ui.a("K.Young GitHub", href="https://github.com/Keyoungg2/cintel-02-data/tree/main", target="_blank")

# Plot Charts for pegiuns data for body mass by island 
with ui.layout_columns():

    @render_plotly
    def plot_plt():
        return px.histogram(
            filtered_data(),
            x="body_mass_g",
            title="Penguin Mass Plotly    vs  Seaborn Species Count",
            labels={"body_mass_g": "Body Mass (g)", "count": "Count"})

#Plot Charts for pegiuns data for body mass by species  
    @render.plot
    def plot_sns():
            return sns.histplot(filtered_data(), x="species", kde=False)

#Creating ui navigation panel of  plots to difference in plotly vs Seaborn 
with ui.navset_card_tab(id="tab"):
    with ui.nav_panel("Seaborn Histogram"):

        @render.plot
        def seaborn_histogram():
            seaborn_hist = sns.histplot(filtered_data(),x=input.selected_attribute(),bins=input.seaborn_bin_count(),)
            seaborn_hist.set_title("Seaborn Penguin Data")
            seaborn_hist.set_xlabel("Selected Attribute")
            seaborn_hist.set_ylabel("Count")

    # Creating Scatter plot
    with ui.nav_panel("Plotly scatterplot"):
        ui.card_header("Species Scatterplot")

        @render_plotly
        def plotly_scatterplot():
        # Scatterplot for flipper and bill lengeth correlation 
            return px.scatter(
                filtered_data(),
                x="flipper_length_mm",
                y="bill_length_mm",
                color="species",
                facet_col="sex",
                title="Flipper and Bill Lengeth Correlation Scatterplot",
                labels={
                "flipper_length_mm": "Flipper Length (mm)",
                "bill_length_mm": "Bill Length (mm)",})


    # Creating Plotly Pie Chart plot
    with ui.nav_panel("Plotly Pie Chart"):
        ui.card_header("Body Mass Pie Chart")
    
        @render_plotly
        def plotly_pie():
            pie_chart = px.pie(
                filtered_data(),
                values="body_mass_g",
                names="island",
                title="Body mass on Islands",
            )
            return pie_chart
# Show Data
with ui.layout_columns():
    with ui.accordion(id="acc", open="closed"):
        with ui.accordion_panel("Data Table"):
            @render.data_frame
            def penguins_datatable():
                return render.DataTable(penguins)
         
        with ui.accordion_panel("Data Grid"):
            @render.data_frame
            def penguins_grid():
                return render.DataGrid(penguins)

# --------------------------------------------------------
# Reactive calculations and effects
# --------------------------------------------------------

# Add a reactive calculation to filter the data
# By decorating the function with @reactive, we can use the function to filter the data
# The function will be called whenever an input functions used to generate that output changes.
# Any output that depends on the reactive function (e.g., filtered_data()) will be updated when the data changes.
    @reactive.calc
    def filtered_data():
        return penguins[penguins["species"].isin(input.selected_species_list())]
