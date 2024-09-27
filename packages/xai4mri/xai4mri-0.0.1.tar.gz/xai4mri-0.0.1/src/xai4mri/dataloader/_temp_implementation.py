#!/usr/bin/python3
"""
Running the _temp_implementation.py script.

Author: Simon M. Hofmann
Years: 2024
"""

# %% Import
from __future__ import annotations

import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from time import perf_counter

import numpy as np
from tqdm import tqdm

from xai4mri.dataloader import PruneConfig
from xai4mri.dataloader.datasets import (
    BaseDataSet,
    _DataSetGenerator,
    _DataSetGeneratorFactory,
    _DataSetGeneratorFromFilePaths,
    _DataSetGeneratorFromFullArray,
)
from xai4mri.utils import ask_true_false, bytes_to_rep_string, check_storage_size, compute_array_size, cprint

# %% Set global vars & paths >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o
# TODO: move / copy this to .../tests/test_datasets.py  # noqa: FIX002
PROJECT_ROOT = "/Users/zimon/Work/Doktor/ResearchProjects/xai4mri"
CACHE_DIR = Path(PROJECT_ROOT, "data", "cache")
TEST_NUMERIC_SIDS: bool = False
PROJECT_ID = "TestImplementationNr" if TEST_NUMERIC_SIDS else "TestImplementation"
SID_TABLE_NAME = "sid_tab_nr.tsv" if TEST_NUMERIC_SIDS else "sid_tab.csv"
CACHE_FILES: bool = False
REGISTER_MNI = None  # 1, 2, or None
PruneConfig.largest_brain_max_axes = np.array([160, 170, 198])

PRUNE_MODE = "max"  # "cube", "max", or None
N_TESTS: int = 10  # for "TEST_LOAD_MODE_SPEED"

# What to test
TEST_GENERATORS: bool = False
TEST_DATASET_CLASS: bool = False
TEST_MEM_MAPS: bool = False
TEST_LOAD_MODE_SPEED: bool = False

# %% Functions >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o


def iter_through_data_generator(data_generator: _DataSetGenerator, stop_at: int = 2) -> None:
    """Iterate through a data generator to test functioning."""
    for _i, (x_batch, y_batch) in enumerate(data_generator):
        print(f"Batch {_i}:")
        print("x_batch.shape:", x_batch.shape, x_batch.dtype)
        print("y_batch.shape:", y_batch.shape, y_batch.dtype)
        print("element in x_batch:", x_batch[tuple(np.array(x_batch.shape) // 2)])
        print("y_batch[0] :", y_batch[0])
        if _i == stop_at:
            break


class MyImplementationTestData(BaseDataSet):
    """FA dataset class."""

    def __init__(self):
        """Init FA dataset."""
        super().__init__(
            study_table_or_path=Path(PROJECT_ROOT, "data/demo/LIFE", SID_TABLE_NAME),
            project_id=PROJECT_ID,
            mri_sequence="t1",
            register_to_mni=REGISTER_MNI,
            cache_dir=CACHE_DIR,
            cache_files=CACHE_FILES,
            # MRI processing kwargs
            prune_mode=PRUNE_MODE,
            load_mode="file_paths",
        )

    @staticmethod
    def mri_path_constructor(sid: str) -> Path:
        """
        Construct the MRI path for LIFE t1 demo data.

        :param sid: subject ID
        :return: absolute file path
        """
        return Path(PROJECT_ROOT, "data/demo/LIFE", sid, "mri", "brain.finalsurfs.mgz")


# %% __main__  >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o

if __name__ == "__main__":
    # o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o
    # Test dataset generator
    # o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o
    if TEST_GENERATORS:
        # Test _DataSetGeneratorFromFullArray
        N_samples, x, y, z = 30, 192, 192, 192  # Example dimensions
        dtype_of_array = np.uint8  # np.float32
        data_gen = _DataSetGeneratorFromFullArray(
            name="test_gen_from_full_array",
            x_data=np.random.randint(0, 256, size=(N_samples, x, y, z), dtype=dtype_of_array),  # noqa: NPY002
            y_data=np.random.randint(0, 10, size=(N_samples,), dtype=int),  # e.g., classes 0-9  # noqa: NPY002
            batch_size=2,
            data_indices=np.random.choice(range(N_samples * 5), size=N_samples, replace=False),  # noqa: NPY002
        )
        print()
        print(data_gen)
        print("len(data_gen.data_indices):", len(data_gen.data_indices))
        print("len(data_gen):", len(data_gen))
        print("data_gen.x.shape:", data_gen.x.shape)

        iter_through_data_generator(data_gen)

        # Test _DataSetGeneratorFromFilePaths
        import os

        os.chdir(PROJECT_ROOT)  # for debugging
        paths_to_x_data = list(Path("data/demo/LIFE").glob("0[A-D]*/mri/brain.finalsurfs.mgz"))
        N_samples = len(paths_to_x_data)
        data_gen = _DataSetGeneratorFromFilePaths(
            name="test_gen_from_file_paths",
            x_data=paths_to_x_data,
            y_data=np.random.randint(18, 83, size=(N_samples,), dtype=int),  # e.g., age 18-82  # noqa: NPY002
            batch_size=2,
            data_indices=np.random.choice(range(N_samples * 5), size=N_samples, replace=False),  # noqa: NPY002
        )
        print()
        print(data_gen)
        print("len(data_gen.data_indices):", len(data_gen.data_indices))
        print("len(data_gen):", len(data_gen))
        print("data_gen.x.shape:", data_gen.x.shape)

        iter_through_data_generator(data_gen)

        # Test _DataSetGeneratorFactory
        for x_data in [
            paths_to_x_data,  # file paths
            np.random.randint(0, 256, size=(N_samples, x, y, z), dtype=dtype_of_array),  # full array # noqa: NPY002
        ]:
            data_gen = _DataSetGeneratorFactory.create_generator(
                name="test_gen_from_factory",
                x_data=x_data,
                y_data=np.random.randint(18, 83, size=(N_samples,), dtype=int),  # noqa: NPY002
                batch_size=2,
                data_indices=np.random.choice(range(N_samples * 5), size=N_samples, replace=False),  # noqa: NPY002
                preprocess=lambda _x: _x * 2,
            )
            print()
            print(data_gen)
            print("len(data_gen.data_indices):", len(data_gen.data_indices))
            print("len(data_gen):", len(data_gen))
            print("data_gen.x.shape:", data_gen.x.shape)

            iter_through_data_generator(data_gen, stop_at=1)

    # o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o
    # Test dataset class
    # o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o
    if TEST_DATASET_CLASS:
        mydata = MyImplementationTestData()

        print(mydata.sid_list)
        mydata.get_size_of_prospective_mri_set(estimate_processing_time=False)

        start_time = perf_counter()
        sid_list, train_gen, val_gen, test_gen = mydata.create_data_split(
            target="fake_age",
            force=True,
            save_after_processing=True,
        )
        print(f"Time to process: {perf_counter() - start_time:.2f} sec")
        print(sid_list)

        iter_through_data_generator(train_gen)

        if CACHE_DIR.exists() and ask_true_false(f"Delete cache directory: '{CACHE_DIR}'?"):
            import shutil

            shutil.rmtree(CACHE_DIR)

    # o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o
    # Test loading speeds of the two `load_mode`'s in BaseDataSet
    # o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o

    if TEST_LOAD_MODE_SPEED:
        dict_times = {}  # init
        for load_mode in ("file_paths", "full_array"):
            list_times = []  # init
            general_start_time = perf_counter()
            for _ in tqdm(range(N_TESTS), desc=f"Speed test load_mode: '{load_mode}'"):
                start_time_round_i = perf_counter()
                with TemporaryDirectory(dir=Path(PROJECT_ROOT, "data")) as temp_cache_dir:
                    print("temp_cache_dir:", temp_cache_dir)
                    mydata = MyImplementationTestData()
                    mydata.load_mode = load_mode
                    mydata.cache_files = True
                    mydata.cache_dir = temp_cache_dir

                    sid_list, train_gen, val_gen, test_gen = mydata.create_data_split(
                        target="fake_age",
                        force=True,
                    )

                    for data_split in (train_gen, val_gen, test_gen):
                        iter_through_data_generator(data_split, stop_at=5)
                list_times.append(perf_counter() - start_time_round_i)

            print(f"Total time to process load_mode '{load_mode}': {perf_counter() - general_start_time:.2f} sec")
            dict_times[load_mode] = list_times

        # Print timings of speed
        print()
        for load_mode, time_ls in dict_times.items():
            cprint(
                string=f"load_mode '{load_mode}' mean processing time: "
                f"{np.mean(time_ls):.3f}+/-{np.std(time_ls):.2f} SD seconds.",
                col="b",
            )
        print()
        cprint(
            string=f"Loading 'file_paths' takes "
            f"{np.mean(dict_times['file_paths']) / np.mean(dict_times['full_array']):.1f} "
            f"times the time of loading 'full_array'.",
            col="y",
        )
        print()

    # o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o
    # Explore memmaps
    # o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o
    if TEST_MEM_MAPS:
        # Define the shape and data type of the array
        N_samples, x, y, z = 100, 192, 192, 192  # Example dimensions
        dtype_of_array = np.float32
        _ = compute_array_size(shape=(N_samples, x, y, z), dtype=dtype_of_array, verbose=True)

        # Create a memory-mapped file
        # See: https://numpy.org/doc/stable/reference/generated/numpy.memmap.html
        filename = "data/temp_large_array.dat"
        large_array = np.memmap(filename, dtype=dtype_of_array, mode="w+", shape=(N_samples, x, y, z))
        print("In RAM:", bytes_to_rep_string(sys.getsizeof(large_array)))
        # > Compare:
        # -> print("In RAM:", bytes_to_rep_string(sys.getsizeof(np.random.rand(N_samples, x, y, z).astype(dtype))))
        print("On disk:")
        _ = check_storage_size(obj=large_array, verbose=True)

        # Fill every second row with random data using slicing
        for i in tqdm(range(N_samples // 2)):
            sample_data = np.random.rand(x, y, z).astype(dtype_of_array)  # noqa: NPY002
            large_array[i * 2] = sample_data

        print("In RAM:", bytes_to_rep_string(sys.getsizeof(large_array)))
        print("On disk:")
        _ = check_storage_size(obj=large_array, verbose=True)

        # Flush changes to disk
        large_array.flush()
        print("In RAM:", bytes_to_rep_string(sys.getsizeof(large_array)))
        print("On disk:")
        _ = check_storage_size(obj=large_array, verbose=True)

        # Access the data using slicing
        sample_array = large_array[0:5, :]  # Access the first sample
        print(sample_array.shape)  # Output: (5, x, y, z)
        print(type(sample_array))
        print("In RAM:", bytes_to_rep_string(sys.getsizeof(sample_array)))
        _ = check_storage_size(obj=sample_array, verbose=True)
        sample_array += sample_array.var(axis=0)
        print(type(sample_array))

        large_array = np.memmap(filename, mode="r+", shape=(N_samples, x, y, z))
        print(large_array.shape)
        _ = check_storage_size(obj=large_array, verbose=True)
        try:
            large_array += 1
        except ValueError as e:
            print(e)
            print("Use 'r+' instead")
        large_array.flush()

        # Example usage
        N_samples = 5_500  # NAKO n = 10_663
        shape_of_array = (N_samples, x, y, z)  # (10_000, 192, 192, 192)
        dtype_of_array = np.uint8  # np.float32
        _ = compute_array_size(shape_of_array, dtype_of_array, verbose=True)

        Path(filename).unlink(missing_ok=True)
        large_array = np.memmap(filename, dtype=dtype_of_array, mode="w+", shape=shape_of_array)
        for i in tqdm(range(N_samples // 10)):
            sample_data = np.random.randint(0, 256, size=(x, y, z), dtype=dtype_of_array)  # noqa: NPY002
            large_array[i * 2] = sample_data

        print(large_array[15 * 2, :])

        large_array2 = np.memmap(filename, mode="r", shape=shape_of_array)
        print(large_array2[15 * 2, :])


# o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o >><< o END
