#pylint: disable=bare-except
"""
    Read and write quicknxs reduced files
"""
from __future__ import absolute_import, division, print_function
import sys
import time
import math
import logging

# Import mantid according to the application configuration
from . import ApplicationConfiguration
application_conf = ApplicationConfiguration()
sys.path.insert(0, application_conf.mantid_path)
import mantid

from ... import __version__
from ..configuration import Configuration


def write_reflectivity_header(reduction_list, output_path, pol_states):
    """
        Write out reflectivity header in a format readable by QuickNXS
        :param str output_path: output file path
        :param str pol_state: descriptor for the polarization state
    """
    # Sanity check
    if len(reduction_list) == 0:
        return

    direct_beam_options=['DB_ID', 'P0', 'PN', 'x_pos', 'x_width', 'y_pos', 'y_width',
                         'bg_pos', 'bg_width', 'dpix', 'tth', 'number', 'File']
    dataset_options=['scale', 'P0', 'PN', 'x_pos', 'x_width', 'y_pos', 'y_width',
                     'bg_pos', 'bg_width', 'fan', 'dpix', 'tth', 'number', 'DB_ID', 'File']

    fd = open(output_path, 'w')
    fd.write("# Datafile created by QuickNXS %s\n" % __version__)
    fd.write("# Datafile created using Mantid %s\n" % mantid.__version__)
    fd.write("# Date: %s\n" % time.strftime(u"%Y-%m-%d %H:%M:%S"))
    fd.write("# Type: Specular\n")
    run_list = [str(item.number) for item in reduction_list]
    fd.write("# Input file indices: %s\n" % ','.join(run_list))
    fd.write("# Extracted states: %s\n" % pol_states)
    fd.write("#\n")
    fd.write("# [Direct Beam Runs]\n")
    toks = ['%8s' % item for item in direct_beam_options]
    fd.write("# %s\n" % '  '.join(toks))

    # Get the 
    pol_list = reduction_list[0].cross_sections.keys()
    if len(pol_list) == 0:
        logging.error("No data found in run %s", reduction_list[0].number)
        return

    # Direct beam section
    i_direct_beam = 0
    for data_set in reduction_list:
        i_direct_beam += 1
        run_object = data_set.cross_sections[pol_list[0]].reflectivity_workspace.getRun()
        normalization_run = run_object.getProperty("normalization_run").value
        if normalization_run == "None":
            continue
        peak_min = run_object.getProperty("norm_peak_min").value
        peak_max = run_object.getProperty("norm_peak_max").value
        bg_min = run_object.getProperty("norm_bg_min").value
        bg_max = run_object.getProperty("norm_bg_max").value
        low_res_min = run_object.getProperty("norm_low_res_min").value
        low_res_max = run_object.getProperty("norm_low_res_max").value
        dpix = run_object.getProperty("normalization_dirpix").value
        filename = run_object.getProperty("normalization_file_path").value

        item = dict(DB_ID=i_direct_beam, tth=0, P0=0, PN=0,
                    x_pos=(peak_min+peak_max)/2.0,
                    x_width=peak_max-peak_min+1,
                    y_pos=(low_res_max+low_res_min)/2.0,
                    y_width=low_res_max-low_res_min+1,
                    bg_pos=(bg_min+bg_max)/2.0,
                    bg_width=bg_max-bg_min+1,
                    dpix=dpix,
                    number=normalization_run,
                    File=filename)

        par_list = ['{%s}' % p for p in direct_beam_options]
        template = "# %s\n" % '  '.join(par_list)
        _clean_dict = {}
        for key in item:
            if isinstance(item[key], (bool, str)):
                _clean_dict[key] = "%8s" % item[key]
            else:
                _clean_dict[key] = "%8g" % item[key]
        fd.write(template.format(**_clean_dict))

    # Scattering data
    fd.write("#\n") 
    fd.write("# [Data Runs]\n") 
    toks = ['%8s' % item for item in dataset_options]
    fd.write("# %s\n" % '  '.join(toks))
    i_direct_beam = 0

    for data_set in reduction_list:
        i_direct_beam += 1
        conf = data_set.cross_sections[pol_list[0]].configuration
        ws = data_set.cross_sections[pol_list[0]].reflectivity_workspace
        run_object = ws.getRun()
        peak_min = run_object.getProperty("scatt_peak_min").value
        peak_max = run_object.getProperty("scatt_peak_max").value
        bg_min = run_object.getProperty("scatt_bg_min").value
        bg_max = run_object.getProperty("scatt_bg_max").value
        low_res_min = run_object.getProperty("scatt_low_res_min").value
        low_res_max = run_object.getProperty("scatt_low_res_max").value
        dpix = run_object.getProperty("DIRPIX").getStatistics().mean
        filename = run_object.getProperty("Filename").value
        constant_q_binning = run_object.getProperty("constant_q_binning").value
        scatt_pos = run_object.getProperty("specular_pixel").value
        scaling_factor = conf.scaling_factor

        # For some reason, the tth value that QuickNXS expects is offset.
        # It seems to be because that same offset is applied later in the QuickNXS calculation.
        # Correct tth here so that it can load properly in QuickNXS and produce the same result.
        tth = run_object.getProperty("two_theta").value
        det_distance = run_object['SampleDetDis'].getStatistics().mean / 1000.0
        direct_beam_pix = run_object['DIRPIX'].getStatistics().mean

        # Get pixel size from instrument properties
        if ws.getInstrument().hasParameter("pixel_width"):
            pixel_width = float(ws.getInstrument().getNumberParameter("pixel_width")[0]) / 1000.0
        else:
            pixel_width = 0.0007
        tth -= ((direct_beam_pix - scatt_pos) * pixel_width) / det_distance * 180.0 / math.pi

        item = dict(scale=scaling_factor, DB_ID=i_direct_beam,
                    P0=conf.cut_first_n_points, PN=conf.cut_last_n_points, tth=tth,
                    fan=constant_q_binning,
                    x_pos=scatt_pos,
                    x_width=peak_max-peak_min+1,
                    y_pos=(low_res_max+low_res_min)/2.0,
                    y_width=low_res_max-low_res_min+1,
                    bg_pos=(bg_min+bg_max)/2.0,
                    bg_width=bg_max-bg_min+1,
                    dpix=dpix,
                    number=str(ws.getRunNumber()),
                    File=filename)

        par_list = ['{%s}' % p for p in dataset_options]
        template = "# %s\n" % '  '.join(par_list)
        _clean_dict = {}
        for key in item:
            if isinstance(item[key], str):
                _clean_dict[key] = "%8s" % item[key]
            else:
                _clean_dict[key] = "%8g" % item[key]
        fd.write(template.format(**_clean_dict))

    fd.write("#\n")
    fd.write("# [Global Options]\n")
    fd.write("# name           value\n")
    fd.write("# sample_length  10\n")
    fd.write("#\n")
    fd.close()

def write_reflectivity_data(output_path, data, pol_state, as_multi=False):
    """
        Write out reflectivity header in a format readable by QuickNXS
        :param list ws_list: list of mantid workspaces
        :param str output_path: output file path
        :param str pol_state: descriptor for the polarization state
        :param bool as_multi: it True, the data will be appended with extra comments
    """
    with open(output_path, 'a') as fd:
        data_block = ''
        for p in data:
            #data_block += "%12.6g  %12.6g  %12.6g  %12.6g  %12.6g\n" % (x[i], y[i], dy[i], dx[i], tth)
            data_block += "%12.6g\t%12.6g\t%12.6g\t%12.6g\t%12.6g\n" % (p[0], p[1], p[2], p[3], p[4])

        if as_multi:
            fd.write("# Start of channel %s\n" % pol_state)

        fd.write("# [Data]\n") 
        toks = [u'%12s' % item for item in [u'Qz [1/A]', u'R [a.u.]', u'dR [a.u.]', u'dQz [1/A]', u'theta [rad]']]
        #fd.write(u"# %s\n" % '   '.join(toks))
        fd.write(u"# %s\n" % '\t'.join(toks))
        fd.write(u"%s\n" % data_block)

        if as_multi:
            fd.write("# End of channel %s\n\n\n" % pol_state)

def read_reduced_file(file_path):
    """
        Read in configurations from a reduced data file.
        :param str file_path: reduced data file
    """
    direct_beam_runs = []
    data_runs = []

    with open(file_path, 'r') as file_content:
        # Section identifier
        #   0: None
        #   1: direct beams
        #   2: data runs
        _in_section = 0
        for line in file_content.readlines():
            if "[Direct Beam Runs]" in line:
                _in_section = 1
            elif "[Data Runs]" in line:
                _in_section = 2
            elif "[Global Options]" in line:
                _in_section = 0

            # Process direct beam runs
            if _in_section == 1:
                toks = line.split()
                if len(toks)<14 or 'DB_ID' in line:
                    continue
                try:
                    db_id = int(toks[1])
                    conf = Configuration()
                    conf.cut_first_n_points = int(toks[2])
                    conf.cut_last_n_points = int(toks[3])
                    conf.peak_position = float(toks[4])
                    conf.peak_width = float(toks[5])
                    conf.low_res_position = float(toks[6])
                    conf.low_res_width = float(toks[7])
                    conf.bck_position = float(toks[8])
                    conf.bck_width = float(toks[9])
                    conf.direct_pixel_overwrite = int(toks[10])
                    run_number = int(toks[12])
                    run_file = toks[13]
                    direct_beam_runs.append([db_id, run_number, run_file, conf])
                except:
                    logging.error("Could not parse reduced data file:\n %s", sys.exc_info()[1])
                    logging.error(line)

            # Process data runs
            if _in_section == 2:
                toks = line.split()
                if len(toks)<16 or 'DB_ID' in line:
                    continue
                try:
                    conf = Configuration()
                    conf.scaling_factor = float(toks[1])
                    conf.cut_first_n_points = int(toks[2])
                    conf.cut_last_n_points = int(toks[3])
                    conf.peak_position = float(toks[4])
                    conf.peak_width = float(toks[5])
                    conf.low_res_position = float(toks[6])
                    conf.low_res_width = float(toks[7])
                    conf.bck_position = float(toks[8])
                    conf.bck_width = float(toks[9])
                    conf.direct_pixel_overwrite = int(toks[11])
                    conf.normalization = int(toks[14])
                    run_number = int(toks[13])
                    run_file = toks[15]
                    data_runs.append([run_number, run_file, conf])
                except:
                    logging.error("Could not parse reduced data file:\n %s", sys.exc_info()[1])
                    logging.error(line)

    return direct_beam_runs, data_runs
