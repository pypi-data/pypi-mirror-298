"""
This module contains the implementation of the likelihood calculation, and various functions to manipulate test statistics.

Abstracted from the underlying ``YODA`` objects, this module defines
two ways to construct likelihood functions from numerical types:

    * :class:`~contur.factories.likelihood.Likelihood` -- The base likelihood building blocks, representing the information extracted from an underlying histogram of potentially correlated observables.

    * :class:`~contur.factories.likelihood.CombinedLikelihood` -- A shell to combine :class:`~contur.factories.likelihood.Likelihood` blocks into a full likelihood, automatically encodes assumption that the included blocks are uncorrelated.
"""
import sys
import logging
import numpy as np
import scipy.stats as spstat
from numpy import linalg as la
from scipy.optimize import minimize

import contur
import contur.config.config as cfg
import contur.data.static_db as cdb

try:
    import spey
    from spey.math import value_and_grad
except ImportError:
    spey = None

class Likelihood(object):
    """Fundamental likelihood-block class and confidence-interval calculator

    This class defines the structure of a series of observables to be constructed into a hypothesis test

    :Keyword Arguments:
        * **calculate** (``bool``) -- Perform the statistics calculation (otherwise the input variables are just set up)
        * **ratio** (``bool``) -- Flag if data is derived from a ratio measurement (not general! caveat emptor!)
        * **profile** (``bool``) -- Flag if data is derived from a profile histogram measurement
        * **lumi** (``float``) -- the integrated luminosity in the units of the measurement. used to calculate expected stat uncertainty on signal
        * **lumi_fb** (``float``) -- the integrated luminosity for the measurement in fb. used to scale for HL-LHC
        * **sxsec** (``float``) -- Signal cross-section in picobarns, if non-null
        * **tags** (``string``) -- names of the histograms this is associated with  
        * **sm_values** (:class:`Observable_Values`) -- All the numbers for the SM prediction
        * **measured_values** (:class:`Observable_Values`) -- All the numbers for the measurement
        * **bsm_values** (:class:`Observable_Values`) -- All the numbers for the signal
        * **expected_values** (:class:`Observable_Values`) -- The SM prediction with data uncertainties.
        

    """

    def __init__(self, calculate=False,
                 ratio=False, profile=False, 
                 lumi=1.0, lumi_fb=1.0, sxsec=None, bxsec=None,
                 tags='',sm_values=None, measured_values=None, bsm_values=None, expected_values=None):

        self._covariances    = {}
        self._inverses       = {}
        self._ndof = {}

        
        self.measured_values = measured_values
        self.expected_values = expected_values
        self.sm_values       = sm_values
        self.bsm_values      = bsm_values
        
        if measured_values is not None:
            self._bw = measured_values.bin_widths
            self._nbins = len(measured_values.central_values)                
        elif expected_values is not None:
            self._bw = expected_values.bin_widths
            self._nbins = len(expected_values.central_values)

        self._lumi = lumi
        self._lumi_fb = lumi_fb
        self._sxsec = sxsec
        self._bxsec = bxsec

        self.ratio = ratio
        self.profile = profile

        # various statistics etc. 
        self._pval = {}
        self._sm_pval = None
        self._CLs = {}
        self._index  = {}
        self._ts_s_b = {}
        self._ts_b = {}        
        # attribute to hold chi-square test stats for cases where we have no covariance matrix
        self._test_stats = {}

        # A bool to work out whether the correlations should be used or not
        self._singleBin = False

        # the histogram names
        self._tags = tags
        # these are set later.
        self._pools = ''
        self._subpools = ''
        
        # do this if asked and if there is no BSM (doing SM test) or there are non-zero BSM entries
        #if (self.bsm_values is None or self.bsm_values.central_values.any()) and calculate:
        if calculate:
            # build the inverse covariance matrices.
            self.__buildCovinv()

            try:
                self.__build_stats()
            except Exception as ex:
                cfg.contur_log.error("Error calculating pval for {}: {}".format(self._tags),ex)
                raise

    def __spey_test_stats(self,stat_type):
        """
        Replicate the contur test stats calculation using spey.
        Because of the difference in the likelihood normalisation between spey and contur, some conversion is required to get the same value
        """

        try:
            if stat_type==cfg.expected:
                meas = self.expected_values.central_values
                bg = self.expected_values.central_values
                cov = self._covariances["C1"]
                cov_bg_only = self._covariances["C2"]
            elif stat_type==cfg.hlexpected:
                if (cdb.get_pool(path=self._tags).beamid)=='13TeV':
                    sf = cfg.hllhc_intl_fb/self._lumi_fb
                else:
                    sf=1.0
                meas = self.expected_values.central_values
                bg = self.expected_values.central_values
                cov = self._covariances["C1"]/sf
                cov_bg_only = self._covariances["C2"]/sf
            elif stat_type==cfg.smbg:
                meas = self.measured_values.central_values
                bg = self.sm_values.central_values
                cov = self._covariances["B1"]
                cov_bg_only = self._covariances["B2"]
            elif stat_type==cfg.databg:
                meas = self.measured_values.central_values
                bg = self.measured_values.central_values
                cov = self._covariances["A1"]
                cov_bg_only = self._covariances["A2"]
                # spey needs 2D matrices
                if cov.ndim ==1:
                    cov = np.diag(cov)
                    cov_bg_only = np.diag(cov_bg_only)

            else:
                cfg.contur_log.warn("Unknown stat type {}".format(stat_type))
                return None, None

        except (KeyError, AttributeError):
            cfg.contur_log.debug('Data missing for stat type {}. Test stats will be None'.format(stat_type))
            return None, None     

        if self.bsm_values is not None:
            signal = self.bsm_values.central_values
        else:
            # this is when we're doing SM test.
            signal = np.zeros(len(meas))
        
        # Load the pdf wrapper
        pdf_wrapper = spey.get_backend('default_pdf.multivariate_normal')

        if self.ratio:
            # To match the contur calc, set the background to zero for the mu=1 case, and the signal to zero for the mu=0 case
            s_b_model = pdf_wrapper(
            signal_yields=signal,
            background_yields=np.zeros(len(meas)),
            data=meas,
            covariance_matrix=cov,
            )
            # need a model for the null hypothesis (uses the bg only covariance matrix)
            b_only_model = pdf_wrapper(
            signal_yields=np.zeros(len(meas)),
            background_yields=bg,
            data=meas,
            covariance_matrix=cov_bg_only,
            )

        elif self._singleBin:
            raise NotImplementedError('Single bin spey calculation not yet implemented.')
        elif cfg.sig_plus_bg:
            raise NotImplementedError('Spey calculation for --signal-plus-background mode currently implemented')
        elif self.profile:
            raise NotImplementedError('Spey profiling calculation not currently implemented')

        # 'Normal' histogram calculation
        else:
            s_b_model = pdf_wrapper(
            signal_yields=signal,
            background_yields=bg,
            data=meas,
            covariance_matrix=cov,
            )
            # need a model for the null hypothesis (uses the bg only covariance matrix)
            b_only_model = pdf_wrapper(
            signal_yields=signal,
            background_yields=bg,
            data=meas,
            covariance_matrix=cov_bg_only,
            )

        # build negative log-likelihood function
        neg_log_lh_s_b = value_and_grad(s_b_model)
        neg_log_lh_b = value_and_grad(b_only_model)

        try:
            s_b_det_cov = np.linalg.det(cov)
            b_det_cov = np.linalg.det(cov_bg_only)
            if s_b_det_cov < 0.0 or b_det_cov < 0.0:
                cfg.contur_log.warning("Covariance matrix for {} has negative determinant (s_b {}, b {}) Covariance matrix considered pathological, test stats will be None.".format(self._tags,s_b_det_cov,b_det_cov))
                return None, None
        except FloatingPointError as ex:
            cfg.contur_log.warning("FloatingPointError: {} for {}, test stats will be None.".format(ex,self._tags))
            return None, None

        # evaluate NLL for mu=1 and mu=0 hypotheses, and convert to match the contur test statistic
        ts_s_b = 2*neg_log_lh_s_b([1.0])[0]-len(meas)*np.log(2*np.pi)-np.log(s_b_det_cov)
        ts_b = 2*neg_log_lh_b([0.0])[0]-len(meas)*np.log(2*np.pi)-np.log(b_det_cov)

        return ts_s_b, ts_b
            
    def __build_stats(self):
        """Internal function to trigger the calculation of the various statistical metrics on initialisation.
        """
        mu_null = 0.0
        # this is the master flag that says whether we will use a covariance matrix (diagonal or not) or the single-bin method.
        cfg.contur_log.debug("USING SINGLE BIN METHOD={}".format(self._singleBin))
        
        for stat_type in cfg.stat_types:

            # if there's no signal object, we're doing SM comparison so only do the SMBG version
            if self.bsm_values is None and stat_type != cfg.smbg:
                continue

            
            if self.bsm_values is not None:
                # the first part checks for histograms with all zero entries. The second checks for counters with nan (which is
                # what they are if never filled).
                if (not self.bsm_values.central_values.any()) or (len(self.bsm_values.central_values==1) and np.isnan(self.bsm_values.central_values[0])):     
                    # No signal in this plot.
                    # Do we treat this as "no information" or as "allowed". Choice based on cfg.look_elsewhere
                    if cfg.look_elsewhere:
                        if self._singleBin:
                            self._test_stats[stat_type] = 0.0, 0.0
                        else:   
                            self._ts_s_b[stat_type] = 0.0
                            self._ts_b[stat_type] = 0.0
                        continue
                    else:
                        # tests stats will be None
                        return

            # We keep all test stats when we don't have the covariance matrix, the
            # test stats we keep are then used by likelihood_blocks_find_dominant_ts method                    
            if self._singleBin:
                if cfg.use_spey:
                    self._test_stats[stat_type] = self.__spey_test_stats(stat_type)
                else:
                    self._test_stats[stat_type] = self.__chisq(stat_type, mu_test=1.0, mu_null=mu_null)
                
            else:
                if cfg.use_spey:
                    self._ts_s_b[stat_type], self._ts_b[stat_type] = self.__spey_test_stats(stat_type)
                else:
                    self._ts_s_b[stat_type], self._ts_b[stat_type] = self.__chisq(stat_type, mu_test=1.0, mu_null=mu_null)
                
                cfg.contur_log.debug("Test stats are {}, {} for {} stat type {}".format(self._ts_s_b[stat_type], self._ts_b[stat_type], self._tags, stat_type))
                if self._ts_s_b[stat_type] is not None and self._ts_b[stat_type] is not None:
                    if self._ts_s_b[stat_type] < self._ts_b[stat_type]:
                        cfg.contur_log.debug("BSM+SM is in better agreement with data for {}. Setting pvalues equal.".format(self._tags))
                        self._ts_s_b[stat_type] = 0.0
                        self._ts_b[stat_type] = 0.0
       
                    elif self._ts_s_b[stat_type] < 0.0 or self._ts_b[stat_type] < 0.0:
                        # some cases where the spey calc gives a very small but negative test stat due to numerical precision when converting to contur test stat definition.
                        if cfg.use_spey:
                            contur_ts_s_b, contur_ts_b = self.__chisq(stat_type,mu_test=1.0,mu_null=mu_null)
                            if self._ts_s_b[stat_type] < 0.0 and not contur_ts_s_b < 0.0:
                                cfg.contur_log.debug("Negative test stat for {} from Spey (sb {}). The default contur calculation returned a non negative test stat: {}, using the default result.".format(self._tags,self._ts_s_b[stat_type],contur_ts_s_b))
                                self._ts_s_b[stat_type] = contur_ts_s_b
                            if self._ts_b[stat_type] < 0.0 and not contur_ts_b < 0.0:
                                cfg.contur_log.debug("Negative test stat for {} from Spey (b {}). The default contur calculation returned a non negative test stat: {}, using the default result.".format(self._tags,self._ts_b[stat_type],contur_ts_b))
                                self._ts_b[stat_type] = contur_ts_b
                        else:
                            cfg.contur_log.warning("Negative test stat for {} (sb {}, b {}). This is probably a numerical precision issue. Setting both to zero, no exclusion from this plot.".format(self._tags,self._ts_s_b[stat_type],self._ts_b[stat_type]))
                            self._ts_s_b[stat_type] = 0.0
                            self._ts_b[stat_type] = 0.0

            # fill in the ndof too
            self.get_ndof(stat_type)
            
        # if this is a measurement where we always use the sm theory as background, copy the test stats over.
        if cdb.theoryComp(self.tags):
            if self._singleBin:
                self._test_stats[cfg.databg] = self._test_stats[cfg.smbg]
            else:
                self._ts_s_b[cfg.databg] = self._ts_s_b[cfg.smbg]
                self._ts_b[cfg.databg] = self._ts_b[cfg.smbg]
                
    def __buildBGCov(self):
        """
        Internal function to build theory background covariance matrices.

        """

        if self.sm_values is None:
            return

#        cfg.contur_log.debug("MEAS uncertainty: {}".format(np.sqrt(np.diag(self.measured_values.covariance_matrix))))
#        cfg.contur_log.debug("SM uncertainty: {}".format(np.sqrt(np.diag(self.sm_values.diagonal_matrix))))

        
        if cfg.useTheoryCorr and self.sm_values.covariance_matrix is not None and len(self.sm_values.err_breakdown) >= cfg.min_num_sys_sm:
            if self.measured_values.covariance_matrix is not None and len(self.measured_values.err_breakdown) >= cfg.min_num_sys:
                self._covariances["B1"] = self.measured_values.covariance_matrix+self.sm_values.covariance_matrix+self._statCov
                self._covariances["B2"] = self.measured_values.covariance_matrix+self.sm_values.covariance_matrix
                cfg.contur_log.debug("using theory correlations")
            else:
                try:
                    # we don't have valid data correlations, so add uncorrelated theory uncertainties.
                    self._covariances["B1"] = self.measured_values.diagonal_matrix+self.sm_values.diagonal_matrix+self._statCov
                    self._covariances["B2"] = self.measured_values.diagonal_matrix+self.sm_values.diagonal_matrix
                    cfg.contur_log.debug("not using theory correlations")
                except:
                    raise cfg.ConturError("Could not figure out how to combine theory and refdata uncertainties for {}".format(self._tags))

        elif self.sm_values.diagonal_matrix is not None:
            cfg.contur_log.debug("not using theory correlations")
            if self.measured_values.covariance_matrix is not None and len(self.measured_values.err_breakdown) >= cfg.min_num_sys:
                # we aren't using theory correlations, but we do have data correlations.
                self._covariances["B1"] = self.measured_values.covariance_matrix+self.sm_values.diagonal_matrix+self._statCov
                self._covariances["B2"] = self.measured_values.covariance_matrix+self.sm_values.diagonal_matrix
            else:
                # we don't have data correlations or theory correlations, use diagonal matrices.
                try:
                    self._covariances["B1"] = self.measured_values.diagonal_matrix+self.sm_values.diagonal_matrix+self._statCov
                    self._covariances["B2"] = self.measured_values.diagonal_matrix+self.sm_values.diagonal_matrix
                except:
                    raise cfg.ConturError("Could not figure out how to combine theory and refdata uncertainties for {}".format(self._tags))


        self._inverses["B1"] = la.inv(self._covariances["B1"])
        self._inverses["B2"] = la.inv(self._covariances["B2"])

        self._covariances["C1"] = self._covariances["B1"]
        self._inverses["C1"]    = self._inverses["B1"]
        self._covariances["C2"] = self._covariances["B2"]
        self._inverses["C2"]    = self._inverses["B2"]


        
    def __buildCovinv(self):
        """Internal function to take the covariance matrix and invert it for the chi square test

        In building the Cov matrix we note three cases
            * The matrix is built, and has det!=0, the variables have been built with a covariance that makes sense 
              and the nusiances can be correlated accordingly

            * The matrix has det==0, so we use the diagonal version of it, ignoring correlations
              
            * The diagonalised matrix also has det==0, this means one of the diagonals has 0 uncertainty, this bin should be 
              removed from HEPData. It is considered pathological so the whole entry is discarded

        We build several separate inverse matrices. 
        A- the "data=background" mode, where the non-signal uncertainties are those of the measurement
        B- the "SM=background" mode, where the SM background uncertainties and measurement uncertainties are both included
        C- the "expected limits" mode, where the matrix is identical to B.

        In each case we build two matrices, with the signal+background (1) and background only (2) covariance matrices for each case. 
        The former contains the uncertainties on the signal (MC stats and expected stats given the integrated lumi), the latter do not.
        
        So... six matrices built in total, but only four distinct ones since B1=C1 and B2=C2.

        """

        # Calculate the  covariance matrix for the signal. This is assumed uncorrelated
        # and so is diagonal (the signal errors are the stat errors from the MC generation
        # and the expected signal stat uncertainty from integrated lumi and cross section.
        # (If there are no BSM values, this means we are doing a SM-only test.)
        if self.bsm_values is not None:
            self._statCov = np.diag(self.bsm_values.err_breakdown**2)
        else:
            self._statCov = np.diag(np.zeros(self._nbins))

            
        # If we have a covariance matrix, it has enough error sources, and the user has not turned off correlations, then use it.
        if self.measured_values.covariance_matrix is not None and len(self.measured_values.err_breakdown) >= cfg.min_num_sys and not cfg.diag :
            try:                
                self._covariances["A1"] = self.measured_values.covariance_matrix + self._statCov
                self._covariances["A2"] = self.measured_values.covariance_matrix                
                self._inverses["A1"] = la.inv(self._covariances["A1"])
                self._inverses["A2"] = la.inv(self._covariances["A2"])
                #cfg.contur_log.debug("A1 {}".format(self._covariances["A1"]))

            except:
                cfg.contur_log.warning("Could not invert covariance matrices for: {}. Will diagonalise.".format(self._tags))
                # TODO: according to the logic described above, we should try the diagonal version
                self._covariances["A1"] = self.measured_values.diagonal_matrix + self._statCov
                self._covariances["A2"] = self.measured_values.diagonal_matrix                
                self._inverses["A1"] = la.inv(self._covariances["A1"])
                self._inverses["A2"] = la.inv(self._covariances["A2"])
                
        elif self.measured_values.diagonal_matrix is not None:

            cfg.contur_log.debug("Not using off-diagonal correlations. Flag is {}.".format(cfg.diag))

            self._covariances["A1"] = np.diag(self.measured_values.diagonal_matrix + self._statCov)
            self._covariances["A2"] = np.diag(self.measured_values.diagonal_matrix)

            # this is diagonal anyway so do quicker & more reliably
            if np.count_nonzero(self._covariances["A1"]) == len(self._covariances["A1"]):
                self._inverses["A1"] = np.diag(1.0 / (self._covariances["A1"]))
            else:
                cfg.contur_log.warning(
                    self._tags + " has at least one element with zero uncertainty. Can't invert. Data discarded.")
            
            if np.count_nonzero(self._covariances["A2"]) == len(self._covariances["A2"]):
                self._inverses["A2"] = np.diag(1.0 / (self._covariances["A2"]))
            else:
                cfg.contur_log.warning(
                    self._tags + " has at least one element with zero uncertainty. Can't invert. Data discarded.")

            # if errors are requested uncorrelated and the other criteria fail, use single bin method
            # otherwise, will use the diagonal matrix.
            if cfg.diag and not (self.measured_values.covariance_matrix is not
                                 None and len(self.measured_values.err_breakdown) >= cfg.min_num_sys):
                cfg.contur_log.debug("Using single bin method.")
                self._singleBin = True
            else:
                cfg.contur_log.debug("Using diagonal correlation matrix.")
                #cfg.contur_log.debug("A1 {}".format(self._covariances["A1"]))
                self._singleBin = False
        else:
            cfg.contur_log.warning(
                "Couldn't invert covariance matrix for " + self._tags + ". Data discarded.")

        # build the SM background/expected limit cases
        self.__buildBGCov()

            
    def __chisq(self, stat_type, mu_test, mu_null):
        """Internal function to calculate a pair of chi square test statistics corresponding to two input hypothesis values.

        :arg mu_test:
            The signal strength to test
        :type mu_test: ``float``
        :arg mu_null:
            The signal strength in the null hypothesis. If this is None, is is the same as being zero, unless
            we are minimising nuisance parameters, in which case None just saves some time.
        :type mu_null: ``float``
        
        :Requirements:
            * :func:`self.__buildCovinv` runs and populated `_covinv` and `_covBuilt` exist

        :return: (ts_tested,ts_null) ``float`` -- Returns a tuple of the test statistics corresponding to the requested signal strength parameters

        """


        # load the correct matrices.
        try:
            if stat_type==cfg.expected:
                covinv = self._inverses["C1"]
                covinv_bg_only = self._inverses["C2"]
                meas = self.expected_values.central_values
                bg = self.expected_values.central_values
            elif stat_type==cfg.hlexpected:
                if (cdb.get_pool(path=self._tags).beamid)=='13TeV':
                    sf = cfg.hllhc_intl_fb/self._lumi_fb
                else:
                    sf=1.0
                covinv = self._inverses["C1"]*sf
                covinv_bg_only = self._inverses["C2"]*sf
                meas = self.expected_values.central_values
                bg = self.expected_values.central_values
            elif stat_type==cfg.smbg:
                covinv = self._inverses["B1"]
                covinv_bg_only = self._inverses["B2"]
                bg = self.sm_values.central_values
                meas = self.measured_values.central_values
            elif stat_type==cfg.databg:
                covinv = self._inverses["A1"]
                covinv_bg_only = self._inverses["A2"]
                bg = self.measured_values.central_values
                meas = self.measured_values.central_values
            else:
                cfg.contur_log.warn("Unknown stat type {}".format(stat_type))
                return None, None

        except (KeyError, AttributeError):
            # This just means there wasn't info supplied for the requested stat type.
            return None, None

        if covinv is None:
            return None, None
            
        sb_offset = np.zeros(self._nbins)
        b_offset = np.zeros(self._nbins)
        b_nuisance = None

        if self.bsm_values is not None:
            signal = self.bsm_values.central_values
        else:
            # this is when we're doing SM test.
            signal = np.zeros(len(meas))


        ## Handle different data types in addition to "normal" stacked histograms
#        if signal is None:
#            # Typically comparing SM only to measurement. e.g in SM testing
#            delta_mu_test = (bg + sb_offset) - meas
#            delta_mu_null = np.zeros(len(meas))
#            cfg.contur_log.debug("SM eval: {}".format(delta_mu_test))
#        elif self.ratio or cfg.sig_plus_bg:
        if self.ratio or cfg.sig_plus_bg:
            # First case: ratio plot.
            #   In general, a histogram ratio will be like (A_bkg + A_sig) / (B_bkg + B_sig), and can't be combined without RAW info
            #   This implementation is specific to ratios where the BSM enters the numerator only, and assumes
            #   the "signal" to actually correspond to s+b  (AB: is this implicit in the MET+jet/ll+jet ratio Rivet analysis?)
            # Second case sig_plus_bg is set. This means the input histograms are SM plus BSM, not just the BSM.

            # The covariances use will already be fine, as long as the signal uncertainties only include
            # the uncertainties on the BSM part. Otherwise the SM uncertainties will be double-counted

            delta_mu_test = (signal + sb_offset) - meas  #< assumed mu_test = 1
            delta_mu_null = (bg + b_offset) - meas  #< assumed mu_null = 0
        elif self.profile:
            # We use the SM cross-section from the database, the signal cross-section
            # read from YODA, and compute the new weighted mean
            assert self._bxsec is not None
            # Weighting fractions, assuming signal contribution with mu = 1
            # TODO: generalise to weightings with mu_test/null != {0,1}
            f_bkg = self._bxsec / (self._sxsec + self._bxsec)
            f_sig = self._sxsec / (self._sxsec + self._bxsec)
            # Deltas (note that sb_offset is not broken into weighted s and b parts)
            # TODO: also update the covariance and sb_offset for the weighting?
            delta_mu_null = (bg + b_offset) - meas
            delta_mu_test = (f_sig*signal + f_bkg*bg + sb_offset) - meas
            #print("***", self._bxsec, self._sxsec, f_bkg, f_sig, delta_mu_null, delta_mu_test)
        else:
            # The 'normal' situation where the delta is the sum of (mu*s + b + Delta) - data
            delta_mu_test = (mu_test * signal + bg + sb_offset) - meas
            if mu_null is not None:
                delta_mu_null = (mu_null * signal + bg +  b_offset) - meas
            else:
                delta_mu_null = np.zeros(len(meas))

        #cfg.contur_log.debug("delta for {} signal: {}".format(self._tags,delta_mu_test))
        #cfg.contur_log.debug("uncertainty: {}".format(1.0/np.sqrt(np.diag(covinv))))
        cfg.contur_log.debug("sig, bg, meas for {},{} signal: {} bg: {} meas:{}".format(self._tags,stat_type,signal,bg,meas))
        
        if self._singleBin:
            # do some magic to find the max single, and removing those where the BSM agrees better than SM
            ts_ts = zip([(x ** 2) * y for x, y in zip(delta_mu_test, np.diag(covinv))],
                        [(x ** 2) * y for x, y in zip(delta_mu_null, np.diag(covinv_bg_only))])
            cls_input = []
            for x, y in ts_ts:
                if y>x:
                    cls_input.append([0,0])
                else:
                    cls_input.append([x,y])
            return cls_input

        else:
            return (np.dot(delta_mu_test, np.dot(covinv, delta_mu_test)),
                    np.dot(delta_mu_null, np.dot(covinv_bg_only, delta_mu_null)))





    def __minimise_LL(self, meas, signal, nuisances, sig_errs, mu_test):
        """ 
        Function to find the nuisance parameters which minimise the log likilood for (mu_test*s + b)
        Use nuisances, which is dictionary of the syst uncertainties(bin) keyed by the [errorSource].
        Will also need signal and self_.bg
        Returns zeros if the minimization fails to converge in time
        Returns None if the minimization crashes
        """

        def evalNLL(v, mu, s, b, serr, n, sigma, poissonOnly=False):
            LL = 0
            gaussianFactorL = 0

            
            for val in v:
                gaussianFactorL += spstat.norm.logpdf(val, 0., 1.)

            for i in range(len(n)):

                source = 0
                offset = 0
                for errorVal in sigma[i]:
                    offset = offset + v[source] * errorVal
                    source = source + 1

                if not (s[i]==0 and n[i]==b[i]):
                    poissonFactorL = spstat.poisson.logpmf(n[i], mu * s[i] + b[i] + offset)
                    if np.isnan(poissonFactorL):
                        # will happen for empty bins, but seems harmless.
                        cfg.contur_log.warning(
                            "Poisson returned nan for n=%f,mu=%f,s=%f,b=%f" % (n[i], mu, s[i], b[i]))
                    else:
                        LL += poissonFactorL

            if not poissonOnly:
                LL += gaussianFactorL

            return -1 * LL
        # end of evalNLL

        if nuisances is not None:
            nuisance = {}
            mu = mu_test  # signal strength

            s = []
            b = []
            n = []
            serr = []
            sigma = []

            for i in range(len(meas)):
                # Poisson expects the observed to be an integer...
                n.append(int(round(self._lumi * meas[i] * self._bw[i])))
                #print(int(round(self._lumi * meas[i] * self._bw[i])),self._lumi,meas[i],self._bw[i])
                # Round the others too but keep them floats
                b.append(round(self._lumi * bg[i] * self._bw[i]))
                # JMB I am worried that we don't seem to take the MC statistical uncertainty into account here,
                #    and to do so seems from the literature to be prohibitively complex and slow. See
                #    R. Barlow and C. Beeston, Comp. Phys. Comm. 77 (1993) 219.
                #    J. S. Conway in Proceedings of PHYSTAT 2011, https://cds.cern.ch/record/1306523
                #    So for now we will not include bins with very low numbers of MC events (<4) in the
                #    nuisance parameter fitting, otherwise they can move the nuisance parameters
                #    too far from nominal, leading to unrealistically strong exclusion in the final
                #    result (even though MC stats are taken into account in the error matrix).
                try:
                    tmp_s = round(self._lumi * signal[i] * self._bw[i])
                    tmp_serr = self._lumi * sig_errs[i]
                    if tmp_s > 0:
                        nmc = tmp_s * tmp_s / (tmp_serr * tmp_serr)
                        if nmc < 4:
                            tmp_s = 0
                # This avoid low-stats fitting to rounding errors...
                    s.append(tmp_s)
                    serr.append(tmp_serr)

                except (ValueError, OverflowError, TypeError):
                    s.append(0)
                    serr.append(0)


            for errorSource in nuisances:
                sigma.append(self._lumi * nuisances[errorSource]* self._bw[i])

            v0 = np.zeros(len(nuisances))

            s = np.array(s)
            n = np.array(n)
            b = np.array(b)
            serr = np.array(serr)
            sigma = np.transpose(np.array(sigma))
            
            cfg.contur_log.debug("{}, Using minimization method to find best-fit nuisances".format(self._tags))
            try:
                res = minimize(evalNLL, v0, args=(mu, s, b, serr, n, sigma), method='Nelder-Mead',
                               options={'disp': False, 'fatol': cfg.ll_prec, 'xatol': cfg.err_prec,
                                        'maxiter': cfg.n_iter * len(v0)}, )  # minimize quietly.
                nuisance_values = res.x
                if not res.success:
                    cfg.contur_log.warning("Minimization did not converge {}, mu = {} ".format(self._tags,mu))
                    nuisance_values = v0
                cfg.contur_log.debug("initial  LL = {}".format(evalNLL(v0, mu, s, b, serr, n, sigma)))
                cfg.contur_log.debug("ended on LL = {}".format(evalNLL(res.x, mu, s, b, serr, n, sigma)))

                i = 0
                for source in nuisances:
                    nuisance[source] = nuisance_values[i]
                    i += 1

                return nuisance
                    
            except Exception as e:
                cfg.contur_log.warning(
                    "Minimization crashed " + self._tags, exc_info=e)
                cfg.contur_log.warning("v0 {}, nuisances {}, len {}").format(v0, nuisances,len(nuisances))
                return None

        else:
            return None

    @property
    def tags(self):
        """Name(s) of source histograms for this block

        *settable parameter*

        **type** (``string``)
        """
        return self._tags

    @tags.setter
    def tags(self, value):
        self._tags = value

    @property
    def pools(self):
        """Pool that the test belongs to

        *settable parameter*

        **type** (``string``)
        """
        return self._pools

    @pools.setter
    def pools(self, value):
        self._pools = value

    @property
    def subpools(self):
        """Subpool the test belongs to

        *settable parameter*

        **type** (``string``)
        """
        return self._subpools

    @subpools.setter
    def subpools(self, value):
        self._subpools = value


    def getCLs(self,type):
        """
        CLs hypothesis test value (ratio of `p_s_b` and `p_b`)

        **type** (``float``)

        """
        try:
            CLs = self._CLs[type] 
        except KeyError:
            CLs = None
        return CLs

    def get_ts_s_b(self,type):
        """Test statistic of the s+b hypothesis

        **type** (``float``)
        """
        try:
            ts_s_b = self._ts_s_b[type] 
        except KeyError:
            #raise cfg.ConturError("Asked for test statistic of type {} but it does not exist.".format(type))
            ts_s_b = None
        except:
            ts_s_b = self._ts_s_b

        return ts_s_b

    def get_ts_b(self,type):
        """Test statistic of b only hypothesis

        **type** (``float``)
        """
        try:
            ts_b = self._ts_b[type] 
        except KeyError:
            ts_b = None
            #            raise cfg.ConturError("Asked for test statistic of type {} but it does not exist.".format(type))
        except:
            ts_b = self._ts_b

        return ts_b

    def set_ts_b(self,type,value):
        self._ts_b[type]=value

    def set_ts_s_b(self,type,value):
        self._ts_s_b[type]=value

    def get_ndof(self,type):
        """
        estimate numbers of degree of freedom for this plot
        """
        
        try:
            return self._ndof[type]
        except KeyError:
            # calculate it            
            ndof = 0
            i = 0
            if type==cfg.smbg:
                try:
                    matrix = self._covariances["B1"]
                except KeyError:
                    self._ndof[type] = None
                    return None
            elif type==cfg.databg:
                try:
                    matrix = self._covariances["A1"]
                except KeyError:
                    self._ndof[type] = None
                    return None
            elif type==cfg.expected or type==cfg.hlexpected:
                try:
                    matrix = self._covariances["C1"]
                except KeyError:
                    self._ndof[type] = None
                    return None
            else:
                raise cfg.ConturError("unknown type in ndof request {}".format(type))
                               
#            for i in range(0,len(matrix)):
#                rsum = sum(matrix[i])
#                ndof = ndof + matrix[i][i]/rsum
            
#            self._ndof[type]=ndof
            self._ndof[type]=len(matrix)
            ndof = len(matrix)
            #print(self._ndof[type])
            return ndof

    def get_sm_pval(self):
        """
        Calculate the pvalue compatibility (using chi2 survival) for the SM prediction and this
        measurement
        """        
        try:
            ts = self.get_ts_b(cfg.smbg)
            ndof = self.get_ndof(cfg.smbg)
            #print(ts,ndof)
            self._sm_pval = np.exp(spstat.chi2.logsf(ts,ndof))
            #print("PVAL:",self._sm_pval)
            return self._sm_pval
        except:
            return None
        
    def __repr__(self):
        if not self.tags:
            tag = "Combined blocks"
        else:
            tag = self.pools + self.tags

        ts_vals = "Test stat values:"
        for stat_type in cfg.stat_types:
            ts_vals = ts_vals + "{} ({}); ".format(self.get_ts_s_b(stat_type),stat_type)
            
        return "{} from {}, {}".format(self.__class__.__name__, tag, ts_vals)


class CombinedLikelihood(Likelihood):
    """
    Shell to combine :class:`~contur.factories.likelihood.Likelihood` blocks

    Must specify a statistic type which selects which statistics will be combined.

    This class is used to extract the relevant test statistic from each individual :class:`~contur.factories.likelihood.Likelihood` and combine them
    This is initialised with no arguments as it is just a shell to combine the individual components, and automatically encodes the fact that
    each block is uncorrelated with each other

    .. note:: Technically this could be constructed by building a :class:`~contur.factories.likelihood.Likelihood` with a master covariance matrix made forming block diagonals with each individual component. Avoiding this is faster but less rigourous

    """

    def __init__(self,stat_type="all"):
        super(self.__class__, self).__init__()
        self.stat_type=stat_type

        
    def calc_cls(self):
        """Call the calculation of the CLs confidence interval

        Triggers the parent class calculation of the CLs interval based on the sum of test statistics added with the :func:`add_likelihood` method

        """

        if self.stat_type == "all":
            for stat_type in cfg.stat_types:
                try:
                    self._CLs[stat_type] = ts_to_cls([(self._ts_s_b[stat_type], self._ts_b[stat_type])],self._tags)[0]
                except (TypeError, KeyError):
                    self._CLs[stat_type] = None

        else:
            try:
                self._CLs[self.stat_type] = ts_to_cls([(self._ts_s_b[self.stat_type], self._ts_b[self.stat_type])],self._tags)[0]
            except (TypeError, KeyError):
                self._CLs[self.stat_type] = None

    def add_likelihood(self, likelihood):
        """Add a :class:`~contur.factories.likelihood.Likelihood` block to this combination likelihood

        :arg likelihood: Instance of computed Likelihood
        :type likelihood: :class:`~contur.factories.likelihood.Likelihood`
        """

        if self.stat_type != "all":
            # combining specific stat type for a full likelihood.

            try:
                if likelihood._ts_b[self.stat_type] is not None and likelihood._ts_s_b[self.stat_type] is not None:
                    try:
                        self._ts_s_b[self.stat_type] += likelihood._ts_s_b[self.stat_type]
                        self._ts_b[self.stat_type] += likelihood._ts_b[self.stat_type]
                        self._ndof[self.stat_type] += likelihood._ndof[self.stat_type]

                    except (KeyError, TypeError):
                        self._ts_s_b[self.stat_type] = likelihood._ts_s_b[self.stat_type]
                        self._ts_b[self.stat_type] = likelihood._ts_b[self.stat_type]
                        self._ndof[self.stat_type] = likelihood._ndof[self.stat_type]

            except:
                    # this is ok, just means there was no signal for this histo for this test stat.
                    # TODO: handle the combinations here when we mix SM and Data, for example.
                    pass

            cfg.contur_log.debug("Adding {} to {}, using {}.".format(likelihood,self,self.stat_type))

        else:
            # combining all stat types for a subpool
            for stat_type in cfg.stat_types:
                try:
                    if likelihood._ts_b[stat_type] is not None and likelihood._ts_s_b[stat_type] is not None:
                        try:
                            self._ts_s_b[stat_type] += likelihood._ts_s_b[stat_type]
                            self._ts_b[stat_type] += likelihood._ts_b[stat_type]
                            self._ndof[stat_type] += likelihood._ndof[stat_type]

                        except (KeyError, TypeError):
                            self._ts_s_b[stat_type] = likelihood._ts_s_b[stat_type]
                            self._ts_b[stat_type] = likelihood._ts_b[stat_type]
                            self._ndof[stat_type] = likelihood._ndof[stat_type]

                except:
                        # this is ok, just means there was no signal for this histo for this test stat.
                        # TODO: handle the combinations here when we mix SM and Data, for example.
                        pass

                cfg.contur_log.debug("Adding subpool likelihood {} to {}, using {}.".format(likelihood,self,stat_type))

    def getCLs(self,type="internal"):
        """
        CLs hypothesis test value (ratio of `p_s_b` and `p_b`)
        For the CombinedLikelihood version, the input type is ignored and the internal value is always used.
        The "all" option is for when it is being used for a subpool.

        **type** (``float``)

        """
        try:
            if self.stat_type == "all":
                CLs = self._CLs[type] 
            else:
                CLs = self._CLs[self.stat_type] 
        except KeyError:
            CLs = None
    
        return CLs
    
    def get_spey_CLs(self,type="internal"):
        """
        CLs hypothesis test value (ratio of `p_s_b` and `p_b`)
        For the CombinedLikelihood version, the input type is ignored and the internal value is always used.
        The "all" option is for when it is being used for a subpool.

        **type** (``float``)

        """
        try:
            if self.stat_type == "all":
                CLs = self._spey_CLs[type] 
            else:
                CLs = self._spey_CLs[self.stat_type] 
        except KeyError:
            CLs = None
    
        return CLs


    def get_ts_s_b(self, type="internal"):
        """Test statistic of the s+b hypothesis
        For the CombinedLikelihood version, the input type is ignored and the internal value is always used.

        **type** (``float``)
        """
        try:
            if self.stat_type == "all":
                ts_s_b = self._ts_s_b[type] 
            else:
                ts_s_b = self._ts_s_b[self.stat_type] 
        except KeyError:
            #raise cfg.ConturError("Asked for test statistic of type {} but it does not exist.".format(type))
            ts_s_b = None
        except:
            ts_s_b = self._ts_s_b

        return ts_s_b

    def get_ts_b(self, type="internal"):
        """Test statistic of b only hypothesis
        For the CombinedLikelihood version, the input type is ignored and the internal value is always used.

        **type** (``float``)
        """
        try:
            if self.stat_type == "all":
                ts_b = self._ts_b[type] 
            else:
                ts_b   = self._ts_b[self.stat_type] 
        except KeyError:
            ts_b = None
            #            raise cfg.ConturError("Asked for test statistic of type {} but it does not exist.".format(type))
        except:
            ts_b = self._ts_b

        return ts_b

    def set_ts_b(self,value):
        self._ts_b[self.stat_type]=value

    def set_ts_s_b(self,value):
        self._ts_s_b[self.stat_type]=value

    def __repr__(self):
        if not self.tags:
            tag = "Combined blocks"
        else:
            tag = self.pools + self.tags
        return "{} from {}, ts={} with stat type {} ".format(self.__class__.__name__, tag, self.get_ts_s_b(), self.stat_type)

def pval_to_cls(pval_tuple):
    """
    Function to calculate a cls when passed background and signal p values.

    notes: we are not actually varying a parameter of interest (mu), just checking mu=0 vs mu=1

           the tail we integrate to get a p-value depends on whether you're looking for signal-like or background-like tails. 
           For the signal-like p-value we integrate over all the probability density less signal-like than was observed, i.e. to the right of the observed 
           test stat.

           For the background-like p-value we should integrate over the less background-like stuff, i.e. from -infty to t_obs... which is 1 - the t-obs...infty 
           integral.

           So CLs is the ratio of the two right-going integrals, which is nice and simple and symmetric, but looks asymmetric when written in terms of the 
           p-values because they contain complementary definitions of the integral limits 

           The code has implemented them both as right-going integrals, so does look symmetric, hence this comment to hopefully avoid future confusion.

    :arg pval_tuple: Tuple, first element p-value of signal hypothesis, second p-value of background
    :type pval_tuple: ``Tuple of floats``

    :return: CLs ``float`` -- Confidence Interval in CLs formalism

    """

    # convert to log for numerical stability.
    # this ignore error state means -inf will be passed for log of zero, which can be handled later
    with np.errstate(divide='ignore'):
        log_p_vals = np.log(pval_tuple)
        
    #list to hold computed confidence levels
    cls = []

    for ts_index in range(len(log_p_vals)):
        log_pval_b = log_p_vals[ts_index][1]
        log_pval_sb = log_p_vals[ts_index][0]

        cls_ts_index = 1 - np.exp(log_pval_sb - log_pval_b) #computed confidence level

        cfg.contur_log.debug("pval sb = {}, pval b = {}".format(pval_tuple[ts_index][0],pval_tuple[ts_index][1]))
            

        cfg.contur_log.debug(
                "CLs %e, log pval sb %e, log pval b %e:" % (cls_ts_index, log_pval_sb, log_pval_b))

        if (cls_ts_index is not None and cls_ts_index < 0):
            cfg.contur_log.debug("Negative CLs %f, setting to zero. BSM+SM is in better agreement with data." % (cls_ts_index))
            cls_ts_index = 0

        cls.append(cls_ts_index)

    return cls

def ts_to_pval(ts):
    """
    Method to convert test statistic to log pval

    :arg ts: Single or numpy array of test statistics to convert to a p-values with a Gaussian
    :type ts: ``float`` assuming n DoF=1

    :return: p-value ``float``

    """

    return spstat.norm.logsf(np.sqrt(ts))


def ts_to_cls(ts_tuple_list,tags):
    """
    Method to directly cast a list of tuples of test statistics (tuple 
    contains background and signal test stats) into a list of CLs values

    notes: we are not actually varying a parameter of interest (mu), just checking mu=0 vs mu=1

           the tail we integrate to get a p-value depends on whether you're looking for signal-like or background-like tails. 
           For the signal-like p-value we integrate over all the probability density less signal-like than was observed, i.e. to the right of the observed 
           test stat.

           For the background-like p-value we should integrate over the less background-like stuff, i.e. from -infty to t_obs... which is 1 - the t-obs...infty 
           integral.

           So CLs is the ratio of the two right-going integrals, which is nice and simple and symmetric, but looks asymmetric when written in terms of the 
           p-values because they contain complementary definitions of the integral limits 

           The code has implemented them both as right-going integrals, so does look symmetric, hence this comment to hopefully avoid future confusion.

    :arg ts_tuple_list: list of tuples of tests statistics (tuples of the form (test stat background, test stat background))
    :type ts_tuple_list: ``list``

    :return: CLs ``list`` -- List of Confidence Intervals in CLs formalism

    """
    if type(ts_tuple_list) == tuple:
        ts_tuple_list = [ts_tuple_list] #place in list

    log_p_vals = ts_to_pval(np.array(ts_tuple_list))
    cls = []

    for ts_index in range(len(log_p_vals)):
        log_pval_b = log_p_vals[ts_index][1]
        log_pval_sb = log_p_vals[ts_index][0]

        try:
            # have stayed with logs for as long as possible for numerical stability
            cls_ts_index = 1 - np.exp(log_pval_sb - log_pval_b)
        except FloatingPointError:
            cls_ts_index = 1
        cfg.contur_log.debug(
            "CLs %e, log pval sb %e, log pval b %e:" % (cls_ts_index, log_pval_sb, log_pval_b))

        if (cls_ts_index is not None and cls_ts_index < 0):
            cfg.contur_log.debug(
                "Negative CLs %f, setting to zero for %s. BSM+SM is in better agreement with data." % (cls_ts_index, tags))
            cls_ts_index = 0

        cls.append(cls_ts_index)


    return cls

def sort_blocks(likelihood_blocks, stat_type, omitted_pools=""):
    """Function that sorts the list of likelihood blocks extracted from the ``YODA`` file

    This function implements the sorting algorithm to sort the list of all extracted :class:`~contur.factories.likelihood.Likelihood`
    blocks in the :attr:`likelihood_blocks` list, storing the reduced list in the :attr:`sorted_likelihood_blocks[stat_type]` list

    :Keyword Arguments:
        * *omittedPools* (``string``) --
          String of analysis pools to omit
        * *stat_type* (``string``) --
          Which statisic (default, smbg, expected, hlexpected) to sort on.
    """
    if likelihood_blocks is None or len(likelihood_blocks) == 0:
        raise ValueError('List of likelihood blocks passed is empty, the likelihood blocks list must contain at least one likelihood object')

    sorted_likelihood_blocks = {}
    
    pool_list = []
    cls_list = []
    for x in likelihood_blocks:
        CLs = x.getCLs(stat_type)    
        if CLs is not None:
            pool_list.append(x.pools)
            cfg.contur_log.debug("block CLs: {}, getCLs({})= {}, ".format(x._CLs,stat_type,CLs))
            cls_list.append(CLs)

    if len(cls_list)==0:
        return None
            
    # Create dictionary of empty lists
    combine_pool_cls_group = {}
    for i in set(pool_list):
        combine_pool_cls_group[i] = []

    combine_pool_cls = list(zip(pool_list,cls_list))

    
    #Key is the pool pointing to list of CLs for pool
    for pair in combine_pool_cls:
        combine_pool_cls_group[pair[0]].append(pair[1])

    #Take the maximum CLS in each list
    for i in combine_pool_cls_group:
        try:
            combine_pool_cls_group[i] = max(combine_pool_cls_group[i])
        except:
            combine_pool_cls_group[i] = None
              

    # find the likelihood block matching this for each pool and append it to the sorted blocks list        
    sorted_likelihood_blocks[stat_type] = []
    # build the list of analysis pool which are represented in these likelihood blocks
    pools = []
    [pools.append(x) for x in [
        item.pools for item in likelihood_blocks] if x not in pools]

    
    for p in pools:  #TODO reinstate above to get order the same
    #for p in combine_pool_cls_group.keys():
        if (not p == omitted_pools) and (p in combine_pool_cls_group.keys()):
            for item in likelihood_blocks:
                CLs = item.getCLs(stat_type)
                if CLs == combine_pool_cls_group[p] \
                        and item.pools == p \
                        and item.pools not in [x.pools for x in sorted_likelihood_blocks[stat_type]]:
                    sorted_likelihood_blocks[stat_type].append(item)

    return sorted_likelihood_blocks[stat_type]


def combine_subpool_likelihoods(likelihood_blocks, omitted_pools=""):
    """
    build combined likelihoods for any active subpools, and add them to the list of likelihood blocks.

    """

    # build the list of analysis pool which are represented in these likelihood blocks
    pools = []
    subpool_lh = []
    [pools.append(x) for x in [
        item.pools for item in likelihood_blocks] if x not in pools]

    #now loop over these pools
    for p in pools:
        if omitted_pools == p:
            continue

        # build the list of analyses associated with this pool
        anas = []
        [anas.append(x) for x in
         [cfg.ANALYSIS.search(item.tags).group() for item in likelihood_blocks if
          item.tags and item.pools == p] if
         x not in anas]

        for a in anas:
            subpools = []
            for item in likelihood_blocks:
                if item.pools == p and a in item.tags:
                    if item.subpools not in subpools and item.subpools is not None:
                        subpools.append(item.subpools)

            if len(subpools) > 0:
                result = {}
                for sp in subpools:
                    result[sp] = CombinedLikelihood()

                for k, v in result.items():
                    # Remove the point if it ends up in a group
                    # Tags need to store which histo contribute to this point.
                    for y in likelihood_blocks:
                        if y.subpools == k and a in y.tags:
                            result[k].add_likelihood(y)
                            if len(result[k].tags) > 0:
                                result[k].tags += ","
                            result[k].tags += y.tags
                
                    v.calc_cls()
                    v.pools = p
                    v.tags = result[k].tags

                # add the max subpool back into the list of points with the pool tag set but no subpool
                [subpool_lh.append(v) for k, v in result.items()]  
#                [likelihood_blocks.append(v) for k, v in result.items()]  

    return subpool_lh

def build_full_likelihood(sorted_blocks, stat_type, omittedPool=""):
    """
    Function to build the full likelihood representing an entire ``YODA`` file

    This function takes the :attr:`sorted_likelihood_blocks` and combines them as statistically uncorrelated
    diagonal contributions to a :class:`~contur.factories.likelihood.CombinedLikelihood` instance which is stored
    as an attribute to this class as :attr:`likelihood`

    :Keyword Arguments:
        * *omittedPools* (``string``) --
          String of analysis pools to omit

    """

    if sorted_blocks is None:
        return None
    
    if len(sorted_blocks) == 0:
        raise ValueError('List of sorted blocks passed is empty, the sorted blocks list must contain at least one likelihood object')

    full_likelihood = CombinedLikelihood(stat_type)
    for x in sorted_blocks:
        if x.pools != omittedPool:
            full_likelihood.add_likelihood(x)
    full_likelihood.calc_cls()
    return full_likelihood

def likelihood_blocks_ts_to_cls(likelihood_blocks,stat_type):
    """Function that calculates the confidence level for each
       likelihood block extracted from the ``YODA`` file using the signal
       and background test statistic for the block
    """
    if len(likelihood_blocks) == 0:
        raise ValueError('List of likelihood blocks passed is empty, the likelihood blocks list must contain at least one likelihood object')

    #Collect test statistics for each likelihood where the background
    test_stats = {}

    for number, likehood_object in enumerate(likelihood_blocks):
        try:
            if likehood_object._ts_s_b[stat_type] is not None:
                tssb = likehood_object._ts_s_b[stat_type]
                tsb = likehood_object._ts_b[stat_type]
                if tssb < 0.0:
                    cfg.contur_log.warning("ts_s_b = {} for {}. Setting to zero.".format(tssb,likehood_object._tags))
                    tssb = 0.0
                if tsb < 0.0:
                    cfg.contur_log.warning("ts_b = {} for {}. Setting to zero.".format(tsb,likehood_object._tags))
                    tsb = 0.0
                test_stats[number] = (likehood_object._ts_s_b[stat_type], likehood_object._ts_b[stat_type])
                test_stats[number] = (tssb,tsb)
                
        except KeyError:
            # this is ok, just means this stat wasn't used for this object
            pass
                
    #Convert test statistics into p values
    test_stat_list = list(test_stats.values())

    try:
        p_values = np.exp(spstat.norm.logsf(np.sqrt(test_stat_list)))
    except FloatingPointError:
        try:
            p_values = np.exp( np.clip(  spstat.norm.logsf(np.sqrt(test_stat_list)) ,-3.0e+02,3.0e-2))
        except FloatingPointError:
            cfg.contur_log.error("Problem getting CLs from ts. min test_stat_list is {}".format(min(test_stat_list)))
            raise
            
    #Loop over each likelihood block, where p value exists evaluate confidence level
    # and update value of the ._CLs attribute for the likelihood block
    count = 0
    for ts_index, like_ob in enumerate(likelihood_blocks):
        if like_ob.bsm_values is None or like_ob.bsm_values.central_values.any():
            #only do the below when we have signal events or are doing SM test

            if ts_index in test_stats.keys():
                p_s_b, p_b = p_values[count]
                count +=1
                like_ob._CLs[stat_type] = pval_to_cls([(p_s_b, p_b)])[0]
                if like_ob._CLs[stat_type] is not None:
                    like_ob._pval[stat_type] = 1.0-like_ob._CLs[stat_type]
            else:
                like_ob._pval[stat_type] = None
                like_ob._CLs[stat_type] = None

            if like_ob._CLs[stat_type] is not None:
                if cfg.contur_log.isEnabledFor(logging.DEBUG):
                    cfg.contur_log.debug("Reporting CLs {}, pval {}, p_sb {}, p_b {}, ts_s_b {}, ts_b {} for {}:".format(
                                           like_ob._CLs[stat_type], like_ob._pval[stat_type], p_s_b, p_b, like_ob._ts_s_b[stat_type], like_ob._ts_b[stat_type], like_ob._tags))

                if np.isnan(like_ob._CLs[stat_type]):
                    like_ob._CLs[stat_type] = None
                    cfg.contur_log.warning(
                        "CLs {} evaluated to nan, set to None. {} ".format(stat_type,like_ob._tags))
            else:
                if stat_type == cfg.databg and like_ob.sm_values is None:
                    # warn, unless this is a measurement without SM theory and and that was required, in which
                    # case it's normal.
                    cfg.contur_log.warning(
                        "Could not evaluate CLs for {}, type {}".format(like_ob._tags, stat_type))


        elif  (((stat_type == cfg.smbg or stat_type == cfg.expected or stat_type == cfg.hlexpected) and like_ob.sm_values is not None) or (stat_type == cfg.databg)):
            # this should be zero if
            # (i) there was a theory projection we would use, but there were no signal events or
            # (ii) we were using data as background and there were no signal events.            
            like_ob._pval[stat_type] = 0.0
            like_ob._CLs[stat_type] = 0.0



            
def likelihood_blocks_find_dominant_ts(likelihood_blocks,stat_type):
    """Function that finds the chi-square test statistic that gives the
       maximum confidence level for each likelihood block for which we
       don't have a valid covariance matrix (either the matrix has no
       invserse or has not been succesfully built)
    """
    if len(likelihood_blocks) == 0:
        raise ValueError('List of likelihood blocks passed is empty, the likelihood blocks list must contain at least one likelihood object')

    #Collect chi-square test statistics for all likelihood for blocks for
    # which ._test_stats is not none, in addition collect index for each
    # block (given by ._tags attribute) and the liklihood object block
    # itself
    chi_test = []
    likelihood_index = []
    like_blocks = {}

    for num, like_ob in enumerate(likelihood_blocks):
        try:
            #        if like_ob._test_stats[stat_type] is not None:
            chi_test = chi_test + like_ob._test_stats[stat_type]
            likelihood_index = likelihood_index + [num]*len(like_ob._test_stats[stat_type])
            like_blocks[num] = like_ob
        except:
            pass
            
    #Convert test stats first to p-value and then confidence level
    try:
        p_values = np.exp(spstat.norm.logsf(np.sqrt(chi_test)))
    except:
        cfg.contur_log.warning("Floating point error in when calculating p_values for {}. Clipping.".format(like_ob._tags))
        p_values = np.exp(np.clip(spstat.norm.logsf(np.sqrt(chi_test)),-3.0e+02,3.0e-2))


    cls_list = pval_to_cls(p_values)


    # For each likelihood block we want to find the test stats which give
    # the largest cls, we create a dictionary for both test stats and cls
    # where the keys are given by the likelihood block and each value is an
    # empty list
    test_stats = {}
    cls = {}
    for tag in set(likelihood_index):
        test_stats[tag] = []
        cls[tag] = []

    #Now populate each list with the test stats and cls for the block
    for num, tag in enumerate(likelihood_index):
        test_stats[tag].append(chi_test[num])
        cls[tag].append(cls_list[num])

    #Loop over the blocks, for each block we find the index of the maximum
    # cls, we then update ._ts_s_sb and .ts_b with the test stat value using
    # the cls index
    for tag in set(likelihood_index):
        like_ob = like_blocks[tag]
        like_ob._index[stat_type] = max(range(len(cls[tag])), key=cls[tag].__getitem__) + 1

#        if cfg.contur_log.isEnabledFor(logging.DEBUG):
#            cfg.contur_log.debug(
#                "n data?, {} signal, {} background {}, bin {} ".format(like_ob._n, like_ob._s, like_ob._bg, like_ob._index))
                                                                
        like_ob._ts_s_b[stat_type], like_ob._ts_b[stat_type] = test_stats[tag][like_ob._index[stat_type] - 1]

def filter_nuisances(central_values,error_breakdown):
    """
    This function should take a dict of error sources, apply a filter to remove those that are either
    uncorrelated or neglible, and return the filtered dict for use in NP fitting.
    Untested, since we don't really do the fitting at present, so probably has issues.
    """
    filtered_breakdown={}

    for source, values in error_breakdown:
        if len(source)>0 and not "stat" in source.lower() and not "uncor" in source.lower():

            systErrs = np.zeros(self.nbins)
            fracErrs = np.zeros(self.nbins)
            ibin=0
            for values in values:
                nomVal = central_values[ibin]
                #symmetrize the errors (be conservative - use the largest!)
                systErrs[ibin]=max(abs(errMap_single_value[source][0]),abs(errMap_single_value[source][1]))
                if not nomVal==0.0:
                    fracErrs[ibin] = systErrs[ibin]/nomVal
                else:                            
                    fracErrs[ibin] = 0.0
                ibin=ibin+1
                
            if max(fracErrs)> cfg.min_syst:
                filtered_breakdown[source] = systErrs

    return filtered_breakdown

    
