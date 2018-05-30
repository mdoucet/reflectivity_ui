"""
    Class to execute and hold the off-specular reflectivity calculation.
"""
import logging
import numpy as np
import scipy.stats
from reflectivity_ui.interfaces.configuration import Configuration

H_OVER_M_NEUTRON = 3.956034e-7 # h/m_n [m^2/s]


class OffSpecular(object):
    """
        Compute off-specular reflectivity
    """
    d_wavelength = 0
    Qx = None
    Qz = None
    ki_z = None
    kf_z = None
    S = None
    dS = None

    def __init__(self, cross_section_data):
        """
            :param CrossSectionData cross_section_data: processed data object
        """
        self.data_set = cross_section_data

    def __call__(self, direct_beam=None):
        """
            Extract off-specular scattering from 4D dataset (x,y,ToF,I).
            Uses a window in y to filter the 4D data
            and than sums all I values for each ToF and x channel.
            Qz,Qx,kiz,kfz is calculated using the x and ToF positions
            together with the tth-bank and direct pixel values.

            :param CrossSectionData direct_beam: if given, this data will be used to normalize the output
        """
        #TODO: correct for detector sensitivity

        x_pos = self.data_set.configuration.peak_position
        scale = 1./self.data_set.proton_charge * self.data_set.configuration.scaling_factor

        # Range in low-res direction
        y_min, y_max = self.data_set.configuration.low_res_roi

        rad_per_pixel = self.data_set.det_size_x / self.data_set.dist_sam_det / self.data_set.xydata.shape[1]

        xtth = self.data_set.direct_pixel - np.arange(self.data_set.data.shape[0])[self.data_set.active_area_x[0]:
                                                                                   self.data_set.active_area_x[1]]
        pix_offset_spec = self.data_set.direct_pixel - x_pos
        delta_dangle = self.data_set.dangle - self.data_set.dangle0
        tth_spec = delta_dangle * np.pi/180. + pix_offset_spec * rad_per_pixel
        af = delta_dangle * np.pi/180. + xtth * rad_per_pixel - tth_spec/2.
        ai = np.ones_like(af) * tth_spec / 2.

        # Background
        bck = self.data_set.get_background_vs_TOF() * scale

        v_edges = self.data_set.dist_mod_det/self.data_set.tof_edges * 1e6 #m/s
        lambda_edges = H_OVER_M_NEUTRON / v_edges * 1e10 #A

        wl = (lambda_edges[:-1] + lambda_edges[1:]) / 2.
        # The resolution for lambda is digital range with equal probability
        # therefore it is the bin size divided by sqrt(12)
        self.d_wavelength = np.abs(lambda_edges[:-1] - lambda_edges[1:]) / np.sqrt(12)
        k = 2. * np.pi / wl

        # calculate reciprocal space, incident and outgoing perpendicular wave vectors
        self.Qz=k[np.newaxis, :]*(np.sin(af)+np.sin(ai))[:, np.newaxis]
        self.Qx=k[np.newaxis, :]*(np.cos(af)-np.cos(ai))[:, np.newaxis]
        self.ki_z=k[np.newaxis, :]*np.sin(ai)[:, np.newaxis]
        self.kf_z=k[np.newaxis, :]*np.sin(af)[:, np.newaxis]

        # calculate ROI intensities and normalize by number of points
        raw_multi_dim=self.data_set.data[self.data_set.active_area_x[0]:self.data_set.active_area_x[1], y_min:y_max, :]
        raw = raw_multi_dim.sum(axis=1)
        d_raw = np.sqrt(raw)

        # normalize data by width in y and multiply scaling factor
        intensity = raw/(y_max-y_min) * scale
        d_intensity = d_raw/(y_max-y_min) * scale
        self.S = intensity - bck[np.newaxis, :]
        self.dS = np.sqrt(d_intensity**2+(bck**2)[np.newaxis, :])

        if direct_beam is not None:
            if not direct_beam.configuration.tof_bins == self.data_set.configuration.tof_bins:
                logging.error("Trying to normalize with a direct beam data set with different binning")

            norm_y_min, norm_y_max = direct_beam.configuration.low_res_roi
            norm_x_min, norm_x_max = direct_beam.configuration.peak_roi
            norm_raw_multi_dim=direct_beam.data[norm_x_min:norm_x_max,
                                                norm_y_min:norm_y_max, :]

            norm_raw = norm_raw_multi_dim.sum(axis=0).sum(axis=0)
            norm_d_raw = np.sqrt(norm_raw)
            norm_scale = (float(norm_x_max)-float(norm_x_min)) * (float(norm_y_max)-float(norm_y_min))
            norm_raw /= norm_scale * direct_beam.proton_charge
            norm_d_raw /= norm_scale * direct_beam.proton_charge

            idxs=norm_raw>0.
            self.dS[:, idxs]=np.sqrt(
                         (self.dS[:, idxs]/norm_raw[idxs][np.newaxis, :])**2+
                         (self.S[:, idxs]/norm_raw[idxs][np.newaxis, :]**2*norm_d_raw[idxs][np.newaxis, :])**2
                         )
            self.S[:, idxs]/=norm_raw[idxs][np.newaxis, :]
            self.S[:, np.logical_not(idxs)]=0.
            self.dS[:, np.logical_not(idxs)]=0.

def merge(reduction_list, pol_state):
    """
        Merge the off-specular data from a reduction list.
        :param list reduction_list: list of NexusData objects
        :param string pol_state: polarization state to consider

        The scaling factors should have been determined at this point. Just use them
        to merge the different runs in a set.
    """
    _Qx = np.empty(0)
    _Qz = np.empty(0)
    _ki_z = np.empty(0)
    _kf_z = np.empty(0)
    _S = np.empty(0)
    _dS = np.empty(0)

    for item in reduction_list:
        offspec = item.cross_sections[pol_state].off_spec
        Qx, Qz, ki_z, kf_z, S, dS = (offspec.Qx, offspec.Qz, offspec.ki_z, offspec.kf_z,
                                    offspec.S, offspec.dS)

        n_total = len(S[0])
        p_0 = item.cross_sections[pol_state].configuration.cut_first_n_points
        p_n = n_total-item.cross_sections[pol_state].configuration.cut_last_n_points

        #NOTE: need to unravel the arrays from [TOF][pixel] to [q_points]
        Qx = np.ravel(Qx[:, p_0:p_n])
        Qz = np.ravel(Qz[:, p_0:p_n])
        ki_z = np.ravel(ki_z[:, p_0:p_n])
        kf_z = np.ravel(kf_z[:, p_0:p_n])
        S = np.ravel(S[:, p_0:p_n])
        dS = np.ravel(dS[:, p_0:p_n])

        _Qx = np.concatenate((_Qx, Qx))
        _Qz = np.concatenate((_Qz, Qz))
        _ki_z = np.concatenate((_ki_z, ki_z))
        _kf_z = np.concatenate((_kf_z, kf_z))
        _S = np.concatenate((_S, S))
        _dS = np.concatenate((_dS, dS))

    return _Qx, _Qz, _ki_z, _kf_z, _ki_z-_kf_z, _S, _dS

def closest_bin(q, bin_edges):
    for i in range(len(bin_edges)):
        if q > bin_edges[i] and q < bin_edges[i+1]:
            return i
    return None

def rebin_extract(reduction_list, pol_state, y_list=None, output_dir=None, use_weights=True,
            n_bins_x=350, n_bins_y=350):
    """
        Rebin off-specular data and extract cut at given Qz values.
        Note: the analysis computers with RHEL7 have Scipy 0.12 installed, which makes
        this code uglier. Refactor once we get a more recent version.
    """
    # Sanity check
    if len(reduction_list) == 0:
        return
    if not isinstance(y_list, list):
        y_list = []

    run_numbers = [item.number for item in reduction_list]

    Qx, Qz, ki_z, kf_z, delta_k, S, dS = merge(reduction_list, pol_state)

    # Specify how many bins we want in each direction.
    _bins = [n_bins_x, n_bins_y]

    # Specify the axes
    x_label = 'ki_z-kf_z'
    y_label = 'Qz'
    x_values = delta_k
    y_values = Qz
    if reduction_list[0].cross_sections[pol_state].configuration.off_spec_x_axis == Configuration.QX_VS_QZ:
        x_label = 'Qx'
        x_values = Qx
    elif reduction_list[0].cross_sections[pol_state].configuration.off_spec_x_axis == Configuration.KZI_VS_KZF:
        x_label = 'ki_z'
        y_label = 'kf_z'
        x_values = ki_z
        y_values = kf_z

    # Find the indices of S[TOF][main_axis_pixel] where we have non-zero data.
    indices = S > 0
    if use_weights:
        # Compute the weighted average
        # - Weighted sum
        _r = S/dS**2
        statistic, x_edge, y_edge, _ = scipy.stats.binned_statistic_2d(x_values[indices],
                                                                       y_values[indices],
                                                                       _r[indices], 
                                                                       statistic='sum',
                                                                       bins=_bins)
        # - Sum of weights
        _w = 1/dS**2
        w_statistic, _, _, _  = scipy.stats.binned_statistic_2d(x_values[indices], y_values[indices], _w[indices], 
                                                  statistic='sum',
                                                  bins=[x_edge, y_edge])

        result = statistic / w_statistic
        result = result.T
        error = np.sqrt(1.0/w_statistic).T
    else:
        # Compute the simple average, with errors
        statistic, x_edge, y_edge, _ = scipy.stats.binned_statistic_2d(x_values[indices],
                                                                       y_values[indices],
                                                                       S[indices], 
                                                                       statistic='mean',
                                                                       bins=_bins)
        # Compute the errors
        _w = dS**2
        w_statistic, _, _, _ = scipy.stats.binned_statistic_2d(x_values[indices],
                                                               y_values[indices],
                                                               _w[indices], 
                                                               statistic='sum',
                                                               bins=[x_edge, y_edge])

        _c = np.ones(len(x_values))
        counts, _, _, _ = scipy.stats.binned_statistic_2d(x_values[indices],
                                                          y_values[indices],
                                                          _c[indices], 
                                                          statistic='sum',
                                                          bins=[x_edge, y_edge])

        result = statistic.T
        error = (np.sqrt(w_statistic) / counts).T

    x_middle = x_edge[:-1] + (x_edge[1] - x_edge[0]) / 2.0
    y_middle = y_edge[:-1] + (y_edge[1] - y_edge[0]) / 2.0

    _q_data = []

    #TODO: Checkpoint note: the following is incomplete.
    for q in y_list:
        i_q = closest_bin(q, y_edge)
        indices = abs(x_middle)<0.01
        if error is not None:
            _r = result[i_q][indices]
            _dr = error[i_q][indices]
            _q_data.append( [[x_middle[indices], _r, _dr],
                           '%s %s=%s' % (str(run_numbers), y_label, q)] )
        else:
            _r = result[i_q][indices]
            _q_data.append( [[x_middle[indices], _r],
                           '%s %s=%s' % (str(run_numbers), y_label, q)] )
        
        if output_dir is not None:
            _file_path = get_output_path(f, str(q).replace('.', '_'), output_dir)
            if error is not None:
                _to_save = np.asarray([x_middle, result[i_q], error[i_q]]).T
            else:
                _to_save = np.asarray([x_middle, result[i_q]]).T
            np.savetxt(_file_path, _to_save, delimiter=' ')

    return result, error, x_middle, y_middle, _q_data, [x_label, y_label]