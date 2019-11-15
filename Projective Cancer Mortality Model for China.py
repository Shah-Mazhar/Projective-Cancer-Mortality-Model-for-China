## Getting  Libraries and Functions
# install the pint function which works with units in python
pip install pint 
# Configure Jupyter so figures appear in the notebook
%matplotlib inline
# Configure Jupyter to display the assigned value after an assignment
%config InteractiveShell.ast_node_interactivity='last_expr_or_assign'
# import functions from the modsim.py module
from modsim import *
# Import functions from pandas.py module and read it as pd
import pandas as pd

## Data Collection
"""We collected two sets of data. One is for the deaths for cancer
and another is the life expectancy. We got our datas from two website
which is an html format, we turned it into a csv files to have accurate computation.
We got our 'deaths by cancer' dataset from "https://ourworldindata.org/cancer" and the
'life expectancy' dataset from "https://en.wikipedia.org/wiki/Demographics_of_China".""" 
#reading the csv file 'Deaths by Cancer'
data_cancer = pd.read_csv('cancerdeathrates.csv')
#giving the columns name for data_cancer to easy to work with
data_cancer.columns=['entity', 'code','year','death_age','death_all_age', 'total_death']
#choosing the 'death_age' column as the deaths_cancer 
deaths_cancer = data_cancer.death_age
#reading the csv file 'Life Expectancy'
data_life_expectancy = pd.read_csv('Life Expectancy of China.csv')
#giving the clolumns name for data_life_expectancy to easy to work with
data_life_expectancy.columns = ['years', 'life_exp']
#choosing 'life_exp' column as the life_expectancy
life_expectancy = data_life_expectancy.life_exp

## Defining Functions
def cancer_run_simulation(system):
    """Runs the constant growth model
    
    system: System Object
    
    returns: TimeSeries
    """
 
    cancer_results = TimeSeries()
    cancer_results[cancer_system.cancer_t_0] = cancer_system.cancer_p_0
    
    for t in linrange(cancer_system.cancer_t_0, cancer_system.cancer_t_end):
        cancer_results [t+1] = cancer_results[t] + cancer_system.cancer_annual_growth
        
    return cancer_results
def cancer_plot_results(deaths_all, timeseries, title):
    """Plot the estimates and the model.
    
    death_cancer: Datasets for Deaths by Cancer
    life_expectancy: Datasets for life expectancy
    timeseries: TimeSeries of simulation results
    title: string
    """
    plot(deaths_cancer, ':', label='Deaths by Cancer')
    plot(life_expectancy, ':', label='Life Expectancy')
    plot(timeseries, color='gray', label='Projection Model')
    
    decorate(xlabel='Year (0=1990, 60=2050)', 
             ylabel='Number of people (in Hundreads)/Age(1-100)',
             title=title)
def plot_sweep_parameters(life_expectancy,deaths_cancer):
    """Plot the sweep parameters which are life_expectancy and deaths_cancer
     
    X-axis: Life Expectancy by Age
    Y-axis: Deaths by Cancer in hundreds
    title: string
    """
    decorate(xlabel = 'Life Expectancy (Age)',
             ylabel = 'Deaths by Cancer(in Hundereds)',
             title = 'Life Expectancy vs Death by Cancer')
    plot(life_expectancy, deaths_cancer)
    
## Building Projection Model
"""We are trying to make a projection for our deaths_cancer datasets.
In our datasets, we have the data from year 1990-2014.
We are going to create TimeSeries model that will predict the deaths by cancer from 1990-2050.
Based on our data, we assumed it is a constant growth. So, we are using the constant growth model to build our projection."""
#extracting data  from a certan cell of the csv file and putting it for a variable, in this case the time 
cancer_t_0 = get_first_label(deaths_cancer)
cancer_t_end = get_last_label(deaths_cancer)
cancer_elapsed_time = cancer_t_end - cancer_t_0
#extracting data  from a certan cell of the csv file and putting it for a variable, in this case the deaths by cancer
cancer_p_0 = get_first_value(deaths_cancer)
cancer_p_end = get_last_value(deaths_cancer)
cancer_total_growth = cancer_p_end - cancer_p_0
#a formula that is needed for constant growth model
cancer_annual_growth = cancer_total_growth / cancer_elapsed_time
#creating a system for constant growth model
cancer_system = System(cancer_t_0 = cancer_t_0,
                cancer_t_end = cancer_t_end,
                cancer_p_0 = cancer_p_0,
                cancer_annual_growth = cancer_annual_growth)

## Results
#giving the end time for the projection constant model
cancer_system.cancer_t_end = 60
#running the simulation with cancer_system for cancer_results
cancer_results = cancer_run_simulation(cancer_system)
#Plotting the 'Projection of Deaths by Cancer in China' graph with deaths_cancer and cancer_results
cancer_plot_results(deaths_cancer, cancer_results, 'Projective Cancer Mortality Model for China')
#plotting the sweep parameters that answer the relationship between life expectancy vs deaths by cancer
plot_sweep_parameters(life_expectancy, deaths_cancer)
