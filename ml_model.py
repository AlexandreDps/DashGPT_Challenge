import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,mean_squared_error
from catboost import CatBoostClassifier, CatBoostRegressor
import plotly.express as px

def train(df,target,**kwargs):
    multi = kwargs.get('multi',False)
    reg = kwargs.get('reg', False)
    nbiter = 100
    y = df[target]
    X = df.drop(target, axis=1)
    result = ''

    # Processing of categorical features
    categorical_features = X.select_dtypes(include=['object']).columns
    X[categorical_features] = X[categorical_features].astype(str)

    X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=.2)
    if multi:
        model = CatBoostClassifier(iterations=nbiter, early_stopping_rounds=20,verbose=False,loss_function='MultiClass')
    elif reg:
        model = CatBoostRegressor(iterations=nbiter, early_stopping_rounds=20,verbose=False,loss_function='RMSE')
    else:
        model = CatBoostClassifier(iterations=nbiter, early_stopping_rounds=20,verbose=False)
    model.fit(X_train, y_train,cat_features=list(categorical_features))
    # Make the prediction using the resulting model
    preds_class = model.predict(X_test)
    model.save_model('catboost_model.cmb')
    feature_importance = model.get_feature_importance()
    feature_names = X.columns

    feature_importance_df = pd.DataFrame(zip(feature_names, feature_importance),
                                         columns=['names', 'importance'])
    feature_importance_df['importance'] = (feature_importance_df['importance'] / feature_importance_df['importance'].sum()) * 100
    feature_importance_df = feature_importance_df[feature_importance_df['importance'] > 1]
    fig = px.pie(feature_importance_df, values='importance', names='names')
    fig.update_layout(
        title={
            'text': 'Features Importance',
            'x': 0.5,
        }
    )
    prompt = f"Here are my features importances {zip(feature_names, feature_importance)}. And here was the dataset I'm using : {df.describe()}"
    if reg:
        score = mean_squared_error(y_test, preds_class, squared=False)
        result+=f'Model successfully trained, RMSE = {score}'
        prompt+=("I was trying to predict {target} with regression and obtained a RMSE of {score}")
    else :
        score = accuracy_score(y_test, preds_class)
        result+=f'Model successfully trained, accuracy = {score}'
        prompt+=("I was trying to predict {target} with classification and obtained an accuracy of {score}")
    prompt+=("Give me a list of advices for the dataset only to improve this model")
    return result,prompt,fig
    