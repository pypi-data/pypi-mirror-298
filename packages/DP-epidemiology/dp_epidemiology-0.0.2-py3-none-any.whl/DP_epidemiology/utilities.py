import pandas as pd
import numpy as np
from datetime import datetime
import opendp.prelude as dp

dp.enable_features("contrib", "floating-point", "honest-but-curious")



def dataframe_domain(public_key_sets=None):
    """Creates a domain representing the set of all data frames.
    
    Assumes column names and types are public information.
    Key sets optionally named for columns in `public_key_sets` are considered public information.

    Two data frames differing in their public information 
    are considered to have a data set distance of infinity.
    """
    return dp.user_domain(
        "DataFrameDomain", lambda x: isinstance(x, pd.DataFrame), public_key_sets
    )


def series_domain():
    """Creates a domain representing the set of all series.

    Assumes series name and type are public information.

    Two series differing in their public information 
    are considered to have a data set distance of infinity.
    """
    return dp.user_domain("SeriesDomain", lambda x: isinstance(x, pd.Series))

def identifier_distance():
    """Symmetric distance between the id sets."""
    return dp.user_distance("IdentifierDistance")


def approx_concentrated_divergence():
    """symmetric distance between the id sets"""
    return dp.user_distance("ApproxConcentratedDivergence()")

def make_preprocess_location():
    """Create a 1-stable transformation to bin `merch_postal_code` by city"""

    def categorize_city(code):
        if code.startswith("5"):
            return "Medellin"
        elif code.startswith("11"):
            return "Bogota"
        elif code.startswith("70"):
            return "Brasilia"
        else:
            return "Santiago"

    def location_preprocess(df):
        loc_df = df.copy()
        # Convert merchant_postal_code into str type
        loc_df["merch_postal_code"] = loc_df["merch_postal_code"].astype(str)
        # Apply the function to create a new column
        loc_df["city"] = loc_df["merch_postal_code"].apply(
            categorize_city
        )
        return loc_df

    return dp.t.make_user_transformation(
        input_domain=dataframe_domain(),
        input_metric=identifier_distance(),
        output_domain=dataframe_domain(),
        output_metric=identifier_distance(),
        function=location_preprocess,
        stability_map=lambda d_in: d_in,
    )

def make_truncate_time(start_date, end_date, time_col):
    """Create a transformation that filters the data to a given time frame.
    
    WARNING: Assumes that the data has at most one contribution per individual per week.
    """
    number_of_timesteps = (end_date - start_date).days // 7

    def time_preprocess(df):
        df = df.copy()

        # Convert time_col into datetime type
        df[time_col] = pd.to_datetime(df[time_col])

        # Filter the DataFrame based on the specified dates
        return df[(df[time_col] >= start_date) & (df[time_col] <= end_date)]

    return dp.t.make_user_transformation(
        input_domain=dataframe_domain(),
        input_metric=identifier_distance(),
        output_domain=dataframe_domain(),
        output_metric=dp.symmetric_distance(),
        function=time_preprocess,
        stability_map=lambda d_in: d_in * number_of_timesteps,
    )

def make_sum_by(column, by, bounds):
    """Create a transformation that computes the grouped bounded sum of `column`"""
    L, U = bounds
    def function(df):
        df = df.copy()
        df[column] = df[column].clip(*bounds)
        return df.groupby(by)[column].sum()

    return dp.t.make_user_transformation(
        input_domain=dataframe_domain(),
        input_metric=dp.symmetric_distance(),
        output_domain=series_domain(),
        output_metric=dp.l2_distance(T=float),
        function=function,
        stability_map=lambda d_in: np.sqrt(d_in) * max(abs(L), U),
    )


def make_private_sum_by(column, by, bounds, scale):
    """Create a measurement that computes the grouped bounded sum of `column`"""
    space = dp.vector_domain(dp.atom_domain(T=int)), dp.l2_distance(T=float)
    m_gauss = space >> dp.m.then_gaussian(scale)
    t_sum = make_sum_by(column, by, bounds)

    def function(df):
        exact = t_sum(df)
        # print(exact)
        noisy_sum = pd.Series(
            np.maximum(m_gauss(exact.to_numpy().flatten()), 0), 
        )
        # print(noisy_sum)
        noisy_sum=noisy_sum.to_frame(name="df_nb_transactions")
        noisy_sum["postal_code"] = exact.index
        return noisy_sum

    return dp.m.make_user_measurement(
        input_domain=dataframe_domain(public_key_sets=[by]),
        input_metric=dp.symmetric_distance(),
        output_measure=dp.zero_concentrated_divergence(T=float),
        function=function,
        privacy_map=lambda d_in: m_gauss.map(t_sum.map(d_in)),
    )

def make_filter(column,entry, sensetivity:int= 1):
        """filters offline entries"""
        
        def function(df):
            df = df.copy()
            return df[(df[column] == entry)]


        return dp.t.make_user_transformation(
        input_domain=dataframe_domain(),
        input_metric=identifier_distance(),
        output_domain=dataframe_domain(),
        output_metric=identifier_distance(),
        function=function,
        stability_map=lambda d_in: d_in* sensetivity,
    )



def make_filter_rows(column_name, value):
    """Create a transformation that filters the rows based on the value of a column `column_name`.

    """

    def filter_rows(df):
        df = df.copy()

        # Filter the rows
        return df[df[column_name] == value]

    return dp.t.make_user_transformation(
        input_domain=dataframe_domain(),
        input_metric=dp.symmetric_distance(),
        output_domain=dataframe_domain(),
        output_metric=dp.symmetric_distance(),
        function=filter_rows,
        stability_map=lambda d_in: d_in,
    )

def make_filter_rows_with_country(column_name, country_code_prefix):
    """Create a transformation that filters the rows based on the value of a column `column_name`.
    """
    def filter_rows(df):
        df = df.copy()

        # Filter the rows
        return df[df["merch_postal_code"].astype(str).str.startswith(country_code_prefix)]

    return dp.t.make_user_transformation(
        input_domain=dataframe_domain(),
        input_metric=dp.symmetric_distance(),
        output_domain=dataframe_domain(),
        output_metric=dp.symmetric_distance(),
        function=filter_rows,
        stability_map=lambda d_in: d_in,
    )

def make_private_nb_transactions_avg_count(merch_category, upper_bound , dp_dataset_size, zip_code_list, scale = 1.0):
    """Create a measurement that computes the grouped bounded sum"""

    def private_count(df):
        df = df.copy()
        data = df[df["merch_category"]==merch_category]["merch_postal_code"].unique()
        # (where TIA stands for Atomic Input Type)
        input_space = dp.vector_domain(dp.atom_domain(T=float)), dp.symmetric_distance()
        # (where TIA stands for Atomic Input Type)
        # TODO: what should be the sensitivity here? Many merchant records can contribute to the same zip code
        # So, scale = 1, is a good enough choice.
        count_meas = input_space >> dp.t.then_count() >> dp.m.then_laplace(1.)
        dp_count = count_meas(zip_code_list)
        return dp_count

    def compute_private_sum(df):
        df = df.copy()
        sum = df[df["merch_category"]==merch_category]["nb_transactions"].clip(lower=0, upper=upper_bound).sum()
        dp_sum = np.random.laplace(loc=sum, scale=scale)
        dp_count = private_count(df)
        return dp_sum/dp_count

    return dp.m.make_user_measurement(
        input_domain=dataframe_domain(),
        input_metric=dp.symmetric_distance(),
        output_measure=dp.max_divergence(T=float),
        function=compute_private_sum,
        privacy_map=lambda d_in: d_in*upper_bound,
    )
