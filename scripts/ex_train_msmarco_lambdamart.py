import lightgbm as lgb

from codecarbon import track_emissions


def setup():
    train_data = lgb.Dataset("data/letor_c14b/dataset/ltrc_yahoo/yahoo.train")
    validation_data = lgb.Dataset("data/letor_c14b/dataset/ltrc_yahoo/yahoo.valid", reference=train_data)
    return {"train_data": train_data, "validation_data": validation_data}


@track_emissions(offline=True, country_iso_code="AUS", project_name="LambdaMART Training")
def run(train_data, validation_data):
    bst = lgb.train({"objective": "lambdarank", "metric": "ndcg"}, train_data, 500, valid_sets=validation_data)  # , callbacks=[lgb.early_stopping(stopping_rounds=100)])
    bst.save_model("data/letor_c14b/model.txt")


if __name__ == '__main__':
    run(**setup())
