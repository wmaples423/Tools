blood_flow_rate = 0.0
dialysate_rate = 0.0
ultrafiltration_rate = 0.0
replacement_fluid_rate = 0.0
effluent_rate = 0.0

patient_weight = 0.0

pre_filter_replacement_fluid_rate = 0.0
post_filter_replacement_fluid_rate = 0.0
fluid_removal_rate = 0.0
pre_blood_pump_fluid_rate = 0.0

blood_flow_rate = 0.0
pbp_fluid_rate = 0.0
HCT = 0.0

# * CRRT DOSE
dose = effluent_rate + patient_weight
cvvh = pre_filter_replacement_fluid_rate + post_filter_replacement_fluid_rate + fluid_removal_rate + pre_blood_pump_fluid_rate
cvvhd = dialysate_rate + fluid_removal_rate
cvvhdf = pre_filter_replacement_fluid_rate + post_filter_replacement_fluid_rate + fluid_removal_rate + pre_blood_pump_fluid_rate + dialysate_rate


plasma_flow_rate = blood_flow_rate * 60 * HCT
dilution_factor = plasma_flow_rate / (plasma_flow_rate + pre_filter_replacement_fluid_rate + pbp_fluid_rate)
