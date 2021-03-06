import gstools as gs

from pykrige.rk import Krige
from spatial_interpolation.utils.experiments import conf
from spatial_interpolation.interpolators import kriging as kr

from dataclasses import dataclass

BaseConfig = conf.Config.from_yaml("conf/kriging/parameters.yaml", as_base_cls=True)
config = conf.config_dict.ConfigDict()

class ordinary_kriging_config(BaseConfig):
    """
    This experiments trains a ordinary kriging model on the 
    entire training dataset since 2011 to predict the wave height.
    Uses the locations at each evaluation area to evaluate the model.
    """
    eval_set:str = "set1" # placeholder
    interpolator:object = kr.GsKrige
    dimensions:list = ["latitude","longitude"]
    interpolator_params = dict(
        model="gaussian", # placeholder for now
        latlon=True,
        krige_params = dict(exact=True),
        model_params = dict(rescale=gs.EARTH_RADIUS)
    )
    search_parameters:dict = {
        "model": list(kr.GsKrige.gs_models.values()),
        "num_bins": [8, 10, 20, 30, 40, 50, 60],
    }

class ok_time_config(BaseConfig):
    """
    This experiments trains a ordinary kriging model on the 
    entire training dataset since 2011 to predict the wave height.
    Uses the locations at each evaluation area to evaluate the model.
    """
    eval_set:str = "set1" # placeholder
    interpolator:object = kr.GsKrige
    dimensions:list = ["longitude", "latitude", "time_step"]
    interpolator_params = dict(
        model="gaussian", # placeholder for now
    )
    krige_params = {}
    search_parameters:dict = {
        "model": list(kr.GsKrige.gs_models.values()),
        "num_bins": [8, 10, 20, 30, 40, 50, 60],
    }


for model_name in list(kr.GsKrige.gs_models.keys()):
    for eval_set in ["set1","set2","set3"]:
        # experiment with ordinary kriging on this eval area and this model
        ok_exp_config = conf.as_config_dict(ordinary_kriging_config)
        ok_exp_config.interpolator_params["model"] = model_name
        ok_exp_config.eval_set = eval_set
        config[f"ok_{model_name.lower()}_{eval_set}"] = ok_exp_config
        # experiment with regression kriging on this eval area and this model
        #TODO: implement regression kriging


def get_config():
    return config