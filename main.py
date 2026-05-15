import subprocess


COMMANDS = [
    "python -m src.test_source_manager",
    "python -m src.select_best_multisource_scene",
    "python -m src.download_best_scene_assets",
    "python -m src.inspect_downloaded_rasters",
    "python -m src.calculate_ndwi",
    "python -m src.generate_water_mask",
    "python -m src.vectorize_water_mask",
    "python -m src.create_water_map",
]


def run_command(command):
    print("\n===================================")
    print("RUN:", command)
    print("===================================")

    result = subprocess.run(command, shell=True)

    if result.returncode != 0:
        raise RuntimeError(f"Eroare la comanda: {command}")


if __name__ == "__main__":
    for command in COMMANDS:
        run_command(command)

    print("\nPipeline GEOINT finalizat cu succes.")