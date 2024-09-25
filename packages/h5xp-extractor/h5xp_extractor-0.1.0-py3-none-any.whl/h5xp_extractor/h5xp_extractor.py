#!/usr/bin/env python3

import h5py
import os
import logging
import time
import argparse
import numpy as np
import tifffile as tiff


def export_h5xp(hdf5_file, output_dir, root, meta):
    if meta:
        # Create README file in the root directory
        open(os.path.join(output_dir, 'README.txt'), 'w').close()

    # Open the HDF5 file
    with h5py.File(hdf5_file, 'r') as hdf:
        start = time.time()
        logging.info('Operation started on: %s', time.ctime())
        logging.info(f'Opened HDF5 {hdf5_file}')
        logging.info(f'Root directory is "{root}"')
        # Callable
        def process_group(name, obj):
            if name.split("/")[0] == 'Packages':
                pass
            else:
                if isinstance(obj, h5py.Dataset):
                    # Read dataset into numpy array
                    try:
                        data = obj[()]
                    except TypeError:
                        pass
                    # Filter string and variable objects (shape = ())
                    try:
                        shape = data.shape
                    except Exception:
                        logging.debug(f'Failed to get .shape of {obj.name}')
                        shape = ()

                    # Get dataset data type
                    try:
                        nbytes = data.dtype.itemsize
                    except Exception:
                        logging.debug(f'Failed to get .dtype of {obj.name}')
                        shape = ()
                        nbytes = 0
                    
                    bps = nbytes * 8  # Bits per sample

                    # Get IGORWaveScaling, if available
                    try:
                        bWaveScale = obj.attrs['IGORWaveScaling'][1:,]  # Discard first row, always [[0 0]]
                    except Exception:
                        bWaveScale = np.array([[1, 0]])  # Default scaling
                    
                    try:
                        bWaveNote = obj.attrs['IGORWaveNote']
                    except Exception:
                        bWaveNote = b""                    

                    try:
                        bWaveUnits = str(obj.attrs['IGORWaveUnits'])
                    except Exception:
                        bWaveUnits = "None"
                    
                    save_name = obj.name.replace(root, output_dir)

                    # Save metadata to README.txt for waves only
                    if meta and len(shape):
                        readme_path = os.path.join(obj.parent.name.replace(root, output_dir), 'README.txt')
                        with open(readme_path, 'a') as fp:
                            metadata = b"\n".join([
                                bytes(obj.name.replace("/Packed Data", "root").replace("/", ":"), 'utf-8'),
                                b'Wave note:', bWaveNote,
                                b'Wave scaling [dx x0]', bytes(np.array2string(bWaveScale), 'utf-8'),
                                b'Wave units ', bytes(bWaveUnits, 'utf-8'),
                            ])
                            fp.write(metadata.decode("utf-8") + "\n" + "-" * 32 + "\n")
                    
                    # Check dimensionality of the dataset.
                    # First test catches strings and variables.
                    # Second gets waves with zero elements
                    # The third test catches textwaves, until you find a better way.
                    # data.flat is a very fast operation.
                    if len(shape) == 0 or not data.size or (type(data.flat[0]) in (bytes, str)):
                        pass
                    elif len(shape) == 1:
                        # 1D Dataset - Export as .txt
                        txt_path = f"{save_name}.txt"
                        nvals, = shape
                        step, offset = bWaveScale[0]
                        xvals = offset + np.arange(0, nvals) * step
                        np.savetxt(txt_path, np.transpose([xvals, data]))
                        logging.info(f'Exported 1D dataset to {txt_path} [{bps}-bit]')

                    elif len(shape) == 2:
                        # 2D Dataset - Export as TIFF image
                        img_path = f"{save_name}.tif"
                        tiff.imwrite(img_path, data)
                        logging.info(f'Exported 2D dataset to {img_path} [{bps}-bit]')

                    elif len(shape) == 3:
                        # 3D Dataset - Export as TIFF stack
                        tiff_path = f"{save_name}.tif"
                        # Swap axes, so data is written as (x, y, z)
                        data = np.swapaxes(data, 0, 2)
                        tiff.imwrite(tiff_path, data, shaped=True)
                        logging.info(f'Exported 3D dataset to {tiff_path} [{bps}-bit]')
                    else:
                        logging.info(f'Skipping dataset {obj.name}')

                elif isinstance(obj, h5py.Group):
                    # Create folder in output directory if not exists
                    logging.info(f'<Entering folder>: {obj.name}')
                    target_path = os.path.join(obj.name.replace(root, output_dir))
                    if not os.path.exists(target_path):
                        os.makedirs(target_path)
                        if meta:
                            open(os.path.join(target_path, 'README.txt'), 'a').close()

                else:
                    logging.debug('This was not supposed to happen')

        # Export all data
        try:
            dfr = hdf[root]
        except KeyError:
            logging.ERROR(f'Folder {root} not an HDF5 group.')
        try:
            dfr.visititems(process_group)
        except Exception:
            logging.ERROR('Error in visititems(process_group) callback.')

        # Done
        end = time.time()
        logging.info("Export finished")
        logging.info(f'Processing time: {end - start:.2f} sec.')


def mainF(hdf5_file, output_dir, root, meta):
    # Ensure output directory exists
    output_dir = os.path.abspath(output_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Set up logging
    logging.basicConfig(
        filename=os.path.join(output_dir, 'IgorExport.log'),
        filemode='w',
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    export_h5xp(hdf5_file, output_dir, root, meta)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Extract data from an Igor Pro .h5xp file."
            " Directory structure mirrors the structure of the Igor Pro file."
            " By default, all datasets are exported (base folder: root (Igor Pro) or 'Packed Data')."
            " You can set the optional argument -r RootFolder (--root) to set another export root folder."
            " Use single quotes for literal names (names with special characters and spaces) and a semicolon (:)"
            " as a directory separator. For example, to export only the subfolder 'Dataset after heating'"
            " of the parent folder Sample123, use the optional argument -r Sample123:'Dataset after heating'."
        )
    )
    parser.add_argument('h5xp', type=str, help='Igor Pro .h5xp file partial or full path')
    parser.add_argument('outdir', type=str, help='Output folder (create/overwrite)')
    parser.add_argument("-r", "--root", help="Root folder", type=str, default="root", required=False)
    parser.add_argument("-m", "--meta", help="Export metadata (0 = No, 1 = Yes [default])", type=int, default=1, required=False)
    
    args = parser.parse_args()
    
    if args.root == "root":
        root = "/Packed Data"
    else:
        # We don't use os.path here it is OS dependent
        root = "/".join(('/Packed Data', args.root)).replace(":", "/").replace("//", "/")
    # Check if we have the right file
    filename, extention = os.path.splitext(args.h5xp)
    if extention == '.h5xp':
        # Call main        
        mainF(args.h5xp, args.outdir, root, args.meta)
    else:
        print(args.h5xp + " is not an .h5xp file, sorry ... ")
    
