from dayabay_model import model_dayabay


model = model_dayabay(
    # We provide information that dm31 should be used for the survival
    # probability calculations
    leading_mass_splitting_3l_name="DeltaMSq31",
    # Providing remapping dictionary. Keys are internal parameters model,
    # they could be checked in the model code, values are our custom configurations
    override_cfg_files={
        "parameters.survival_probability": "custom-configurations/configurations/dm31/survival_probability.yaml",
        "parameters.survival_probability_solar": "custom-configurations/configurations/dm31/survival_probability_solar.yaml",
    }
)

print("Let's check which survival probability parameters are used", model.storage["parameters.all.survival_probability"], sep="\n")
print("Free parameters are", model.storage["parameters.free.survival_probability"], sep="\n")
print("Constrained parameters are", model.storage["parameters.constrained.survival_probability"], sep="\n")
