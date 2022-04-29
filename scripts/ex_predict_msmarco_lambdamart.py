import lightgbm as lgb

from codecarbon import track_emissions


def setup():
    model = lgb.Booster(model_file="data/letor_c14b/model.txt")
    return {"model": model}


@track_emissions(offline=True, country_iso_code="AUS", project_name="LambdaMART Searching")
def run(model):
    model.predict("data/letor_c14b/dataset/ltrc_yahoo/yahoo.synthetic.test")


if __name__ == '__main__':
    run(**setup())
