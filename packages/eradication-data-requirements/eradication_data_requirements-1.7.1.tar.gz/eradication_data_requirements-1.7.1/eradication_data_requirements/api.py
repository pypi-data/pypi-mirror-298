from fastapi import FastAPI
import pandas as pd
import json


from eradication_data_requirements.cli import (
    plot_cumulative_series_cpue_by_flight,
    write_effort_and_captures_with_probability,
    write_progress_probability_figure,
)
from eradication_data_requirements.data_requirements_plot import (
    traps_data_requirements_plot,
    plot_comparative_catch_curves,
    plot_data_requirements_from_config_file,
)
from eradication_data_requirements.calculate_intersect import get_population_status_dict
from eradication_data_requirements.set_data import filter_data_by_method
from eradication_data_requirements.resample_aerial_monitoring import get_monitoring_dict


api = FastAPI()


@api.get("/write_aerial_monitoring")
async def api_write_aerial_monitoring(input_path: str, bootstrapping_number: int, output_path: str):
    raw_data = pd.read_csv(input_path)
    json_content = get_monitoring_dict(raw_data, bootstrapping_number)
    write_json(output_path, json_content)


@api.get("/filter_by_method")
async def api_filter_by_method(input_path: str, method: str, output_path: str):
    raw_data = pd.read_csv(input_path)
    filtered_data = filter_data_by_method(raw_data, method)
    filtered_data.to_csv(output_path, index=False)


@api.get("/write_population_status")
async def api_write_population_status(input_path: str, bootstrapping_number: int, output_path: str):
    raw_data = pd.read_csv(input_path)
    seed = 42
    json_content = get_population_status_dict(raw_data, bootstrapping_number, seed)
    write_json(output_path, json_content)


def write_json(output_path, json_content):
    with open(output_path, "w") as jsonfile:
        json.dump(json_content, jsonfile)


@api.get("/write_effort_and_captures_with_probability")
async def api_write_effort_and_captures_with_probability(
    input_path: str, bootstrapping_number: int, output_path: str, window_length: int
):
    resample_method = "cumulative"
    write_effort_and_captures_with_probability(
        input_path, bootstrapping_number, output_path, window_length, resample_method
    )


@api.get("/write_probability_figure")
async def api_write_probability_figure(input_path: str, output_path: str):
    write_progress_probability_figure(input_path, output_path)


@api.get("/plot_custom_cpue_vs_cum_captures")
async def api_plot_custom_cpue_vs_cum_captures(input_path: str, config_path: str, output_path: str):
    plot_data_requirements_from_config_file(input_path, output_path, config_path)


@api.get("/plot_cpue_vs_cum_captures")
async def api_plot_cpue_vs_cum_captures(input_path: str, output_path: str):
    traps_data_requirements_plot(input_path, output_path)


@api.get("/plot_cumulative_series_cpue_by_flight")
async def api_plot_cumulative_series_cpue_by_flight(input_path: str, output_path: str):
    font_size = 27
    plot_cumulative_series_cpue_by_flight(input_path, output_path, font_size)


@api.get("/plot_comparative_catch_curves")
async def api_plot_comparative_catch_curves(
    socorro_path: str, guadalupe_path: str, output_path: str
):
    plot_comparative_catch_curves(socorro_path, guadalupe_path, output_path)
