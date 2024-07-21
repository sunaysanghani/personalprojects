import snowflake.snowpark as snowpark
from snowflake.snowpark.functions import col
import pandas as pd
import datetime
import sklearn
import numpy as np
import matplotlib.pyplot as plt


def main(session: snowpark.Session):
    table1 = session.table("user_info")
    table2 = session.table("marketing_campaigns")
    df_users = table1.to_pandas()
    df_marketing = table2.to_pandas()
    df_marketing['START_DATE'] = pd.to_datetime(df_marketing['START_DATE'])
    df_marketing['END_DATE'] = pd.to_datetime(df_marketing['END_DATE'])

    df_marketing['start_month'] = df_marketing['START_DATE'].dt.to_period('M')
    monthly_campaigns = df_marketing.groupby('start_month').agg({
        'BUDGET': 'sum',
        'CLICKS': 'sum',
        'IMPRESSIONS': 'sum',
        'CONVERSIONS': 'sum'
    }).reset_index()
    

    monthly_campaigns['start_month'] = monthly_campaigns['start_month'].dt.to_timestamp()
    print(monthly_campaigns['start_month'].head())

    monthly_campaigns['budget_lag1'] = monthly_campaigns['BUDGET'].shift(1)
    monthly_campaigns['clicks_lag1'] = monthly_campaigns['CLICKS'].shift(1)
    monthly_campaigns['impressions_lag1'] = monthly_campaigns['IMPRESSIONS'].shift(1)
    monthly_campaigns['conversions_lag1'] = monthly_campaigns['CONVERSIONS'].shift(1)

    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import mean_squared_error
    
    # Select features and target variable
    features = ['BUDGET', 'CLICKS', 'IMPRESSIONS', 'budget_lag1', 'clicks_lag1', 'impressions_lag1', 'conversions_lag1']
    target = 'CONVERSIONS'
    
    X = monthly_campaigns[features]
    y = monthly_campaigns[target]
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Initialize and train the Random Forest Regressor
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Predict on the test set
    y_pred = model.predict(X_test)

    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    print(f'Mean Squared Error: {mse}')


    import numpy as np
    import matplotlib.pyplot as plt
    
    # Predict future values
    future_dates = pd.date_range(start=monthly_campaigns.index[-1], periods=12, freq='M')
    future_features = monthly_campaigns[features].iloc[-12:]
    future_predictions = model.predict(future_features)
    
    # Create a DataFrame for future predictions
    future_df = pd.DataFrame({'ds': future_dates, 'y': future_predictions})
    future_df.set_index('ds', inplace=True)
    
    # Plot the predictions
    plt.figure(figsize=(10, 6))
    plt.plot(monthly_campaigns.index, monthly_campaigns['CONVERSIONS'], label='Actual Conversions')
    plt.plot(future_df.index, future_df['y'], label='Predicted Conversions', linestyle='--')
    plt.legend()
    plt.title('Predicted Campaign Conversions')
    plt.xlabel('Date')
    plt.ylabel('Conversions')
    plt.show()
    
    #table.show()
    return table1
    