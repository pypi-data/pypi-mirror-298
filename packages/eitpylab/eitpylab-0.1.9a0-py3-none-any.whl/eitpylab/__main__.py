import multiprocessing

if __name__ == "__main__":
    # Pyinstaller fix - run pip install pywin32 if error in ImportError: DLL load failed while importing _matfuncs_sqrtm_triu
    multiprocessing.freeze_support()
