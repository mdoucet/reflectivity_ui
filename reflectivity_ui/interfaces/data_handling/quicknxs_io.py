"""
    Read and write quicknxs reduced files
    #TODO: replace this by a mantid algorithm
"""
from __future__ import absolute_import, division, print_function
import sys
import time
import math

# Import mantid according to the application configuration
from . import ApplicationConfiguration
application_conf = ApplicationConfiguration()
sys.path.insert(0, application_conf.mantid_path)
import mantid

from ... import __version__

class Exporter(object):
    """
        Reflectivity exporter
    """
    def __init__(self, ws_list):
        """
            :param list ws_list: list of workspaces used to create a file header
        """
        self.ws_list = ws_list

    def write_reflectivity_header(self, output_path, pol_states):
        """
            Write out reflectivity header in a format readable by QuickNXS
            :param str output_path: output file path
            :param str pol_state: descriptor for the polarization state
        """
        # Sanity check
        if len(self.ws_list) == 0:
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
        run_list = [str(ws.getRunNumber()) for ws in self.ws_list]
        fd.write("# Input file indices: %s\n" % ','.join(run_list))
        fd.write("# Extracted states: %s\n" % pol_states)
        fd.write("#\n")
        fd.write("# [Direct Beam Runs]\n")
        toks = ['%8s' % item for item in direct_beam_options]
        fd.write("# %s\n" % '  '.join(toks))

        # Direct beam section
        i_direct_beam = 0
        for ws in self.ws_list:
            i_direct_beam += 1
            run_object = ws.getRun()
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

        for ws in self.ws_list:
            i_direct_beam += 1

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
            try:
                scaling_factor = run_object.getProperty("scaling_factor").value
            except:
                scaling_factor = 1

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

            item = dict(scale=scaling_factor, DB_ID=i_direct_beam, P0=0, PN=0, tth=tth,
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

    def write_reflectivity_data(self, output_path, pol_state, as_multi=False):
        """
            Write out reflectivity header in a format readable by QuickNXS
            :param list ws_list: list of mantid workspaces
            :param str output_path: output file path
            :param str pol_state: descriptor for the polarization state
            :param bool as_multi: it True, the data will be appended with extra comments
        """
        fd = open(output_path, 'a')

        data_block = ''
        for ws in self.ws_list:
            x = ws.readX(0)
            y = ws.readY(0)
            dy = ws.readE(0)
            dx = ws.readDx(0)
            tth = ws.getRun().getProperty("SANGLE").getStatistics().mean * math.pi / 180.0

            for i in range(len(x)):
                #data_block += "%12.6g  %12.6g  %12.6g  %12.6g  %12.6g\n" % (x[i], y[i], dy[i], dx[i], tth)
                data_block += "%12.6g\t%12.6g\t%12.6g\t%12.6g\t%12.6g\n" % (x[i], y[i], dy[i], dx[i], tth)

        if as_multi:
            fd.write("# Start of channel %s\n" % pol_state)

        fd.write("# [Data]\n") 
        toks = [u'%12s' % item for item in [u'Qz [1/A]', u'R [a.u.]', u'dR [a.u.]', u'dQz [1/A]', u'theta [rad]']]
        #fd.write(u"# %s\n" % '   '.join(toks))
        fd.write(u"# %s\n" % '\t'.join(toks))
        fd.write(u"%s\n" % data_block)

        if as_multi:
            fd.write("# End of channel %s\n\n\n" % pol_state)
        fd.close()
