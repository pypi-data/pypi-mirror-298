#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0302
"""
LISA Orbits

This module implements orbit classes.

Authors:
    Jean-Baptiste Bayle <j2b.bayle@gmail.com>
    Marc Lilley <marc.lilley@gmail.com>
    Aurelien Hees <aurelien.hees@obspm.fr>
"""

import abc
import logging
import h5py
import numpy as np
import scipy.interpolate
import importlib_metadata
import matplotlib.pyplot as plt
import pooch

from oem import OrbitEphemerisMessage
from packaging.version import Version

from lisaconstants import (
    c,
    GM_SUN,
    ASTRONOMICAL_UNIT,
    SUN_SCHWARZSCHILD_RADIUS,
)

from astropy.coordinates import SkyCoord
from astropy import units as u

from .utils import dot, norm, receiver, emitter
from .utils import arrayindex, atleast_2d


logger = logging.getLogger(__name__)


esa_repository = pooch.create(
    path=pooch.os_cache('lisaorbits'),
    base_url='https://github.com/esa/lisa-orbit-files/raw/v1.0/',
    registry={
        'crema_1p0/mida-20deg/trajectory_out_mida-20deg_cw_sg-2nmss.oem1':
            'sha256:56452a2eb84aaf6c328e0931063cb6e62a3c2d01bbdb3dd25e2d6a063225b5e4',
        'crema_1p0/mida-20deg/trajectory_out_mida-20deg_cw_sg-2nmss.oem2':
            'sha256:9a43bed2239625786001c046c3dc49affff23891bf3fcfd58864390eb5399639',
        'crema_1p0/mida-20deg/trajectory_out_mida-20deg_cw_sg-2nmss.oem3':
            'sha256:f8166f2d7050782525634f1e7dd9e9155563ec485bf7bb0c9890e8d8433be46a',
        'crema_1p0/mida+20deg/trajectory_out_mida+20deg_cw_sg-2nmss.oem1':
            'sha256:eec0de47d4b6791aeb1b3caf2a3db3e89cb77e2011e0fed9d6622f3258ee8d78',
        'crema_1p0/mida+20deg/trajectory_out_mida+20deg_cw_sg-2nmss.oem2':
            'sha256:ac120521d8c9cefd3a943a8a0bedd0d56507ba1dcef881f8f88f5d360e068f53',
        'crema_1p0/mida+20deg/trajectory_out_mida+20deg_cw_sg-2nmss.oem3':
            'sha256:b36f2c95db5b524ef50b7ca7750f025b700dee8e4f2ee595c0b9c7d1cea2824c',
    },
)


#: ((3,) ndarray) Spacecraft indices.
SC = np.array([1, 2, 3])


#: ((6,) ndarray) Link (or MOSA) indices.
LINKS = np.array([12, 23, 31, 13, 32, 21])


class Orbits(abc.ABC):
    r"""Abstract base class for concrete orbit classes.

    Note that :attr:`t_init` is used to define all initial conditions, including
    the synchronization of the TPSs w.r.t. the TCB,

    .. math::

        \delta \tau(t_\text{init}) = 0.

    Args:
        t_init (float): TCB time for initial conditions [s]
        tt_method (str): light travel time computation method, one of 'analytic' or 'iterative'
        tt_order (int): light travel time series expansion order (0, 1 or 2)
        tt_niter (int): number of iterations for light travel times iterative procedure
        ignore_shapiro (bool): whether Shapiro delay are in light travel times
    """

    #: ((3,) ndarray) Spacecraft indices.
    SC = SC

    #: ((6,) ndarray) Link (or MOSA) indices.
    LINKS = LINKS

    def __init__(
        self,
        t_init=0.0,
        tt_method='analytic',
        tt_order=2,
        tt_niter=4,
        ignore_shapiro=False,
    ) -> None:

        self.git_url = 'https://gitlab.in2p3.fr/lisa-simulation/orbits'
        self.version = importlib_metadata.version('lisaorbits')
        self.generator = self.__class__.__name__
        logger.info("Initializing orbits (lisaorbit verion %s)", self.version)

        #: str: Light travel time computation method.
        self.tt_method = str(tt_method)
        #: int: Maximum relativistic order for light travel time analytical
        #: expansion (use twice the half-integer order to make it an integer).
        self.tt_order = int(tt_order)
        #: int: Number of iterations for the light travel time iterative method.
        self.tt_niter = int(tt_niter)
        #: bool: Whether Shapiro delay is included in the computation
        #: of light travel times.
        self.ignore_shapiro = bool(ignore_shapiro)
        #: float: TCB time for initial conditions [s].
        self.t_init = float(t_init)

    def _since_init(self, t):
        """Compute time since :attr:`t_init`.

        Args:
            t ((...) array-like): TCB times [s]

        Returns:
            (...) ndarray: Time since :attr:`t_init` [s]
        """
        return np.asarray(t) - self.t_init

    @abc.abstractmethod
    def compute_position(self, t, sc=SC):
        r"""Compute the spacecraft position vector :math:`(\vb{x}, \vb{y}, \vb{z})`.

        The vector coordinates are given in the BCRS frame.

        Args:
            t ((N,) or (N, M) array-like): TCB times [s]
            sc ((M,) array-like): spacecraft indices

        Returns:
            (N, M, 3) ndarray: Spacecraft positions [m].
        """
        raise NotImplementedError

    @abc.abstractmethod
    def compute_velocity(self, t, sc=SC):
        r"""Compute the spacecraft velocity vector :math:`(\vb{v}_x, \vb{v}_y, \vb{v}_z)`.

        The vector coordinates are given in the BCRS frame.

        Args:
            t ((N,) or (N, M) array-like): TCB times [s]
            sc ((M,) array-like): spacecraft indices

        Returns:
            (N, M, 3) ndarray: Spacecraft velocities [m/s].
        """
        raise NotImplementedError

    @abc.abstractmethod
    def compute_acceleration(self, t, sc=SC):
        r"""Compute the spacecraft acceleration vector :math:`(\vb{a}_x, \vb{a}_y, \vb{a}_z)`.

        The vector coordinates are given in the BCRS frame.

        Args:
            t ((N,) or (N, M) array-like): TCB times [s]
            sc ((M,) array-like): spacecraft indices

        Returns:
            (N, M, 3) ndarray: Spacecraft accelerations [m/s2].
        """
        raise NotImplementedError

    @abc.abstractmethod
    def compute_tps_deviation(self, t, sc=SC):
        r"""Compute spacecraft proper time (TPS) deviation as function of TCB.

        We compute the spacecraft proper time deviations, defined by

        .. math::
            \delta\tau(t) = \tau(t) - t \qc

        where :math:`\tau` is the spacecraft TPS and :math:`t` the associated TCB,
        with the initial conditions :math:`\delta\tau(t_\text{init}) = 0`.

        Args:
            t ((N,) or (N, M) array-like): TCB times [s]
            sc ((M,) array-like): spacecraft indices

        Returns:
            (N, M) ndarray: Spacecraft proper time deviations [s].
        """
        raise NotImplementedError

    @abc.abstractmethod
    def compute_tps_deviation_derivative(self, t, sc=SC):
        r"""Compute spacecraft proper time (TPS) deviation derivatives as function of TCB.

        We compute the time derivatives of the spacecraft proper time (TPS) deviations,
        defined by

        .. math::
            \dv{(\delta\tau)}{t} = \dv{(\tau - t)}{t} = \dv{\tau}{t} - 1 \qc

        where :math:`\tau` is the spacecraft TPS and :math:`t` the associated TCB.

        Args:
            t ((N,) or (N, M) array-like): TCB times [s]
            sc ((M,) array-like): spacecraft indices

        Returns:
            (N, M) ndarray: Spacecraft proper time deviation derivatives [s/s].
        """
        raise NotImplementedError

    def compute_tcb_deviation(self, tau, sc=SC, order=1):
        r"""Compute coordinate time (TCB) deviation as function of TPS.

        We compute to a given order the coordinate time,

        .. math::
            \delta t(\tau) = t(\tau) - \tau \qc

        where :math:`\tau` is the spacecraft TPS and :math:`t` the associated
        TCB, with the initial conditions :math:`\delta t(\tau = t_\text{init}) =
        0`.

        Args:
            tau ((N,) or (N, M) array-like): TPS times [s]
            sc ((M,) array-like): spacecraft indices
            order (int): number of iterations

        Returns:
            (N, M) ndarray: Spacecraft coordinate time deviations [s].
        """
        # At zeroth order, there is no deviations
        tcb_deviation = 0
        for _ in range(order):
            tcb_deviation = -self.compute_tps_deviation(tcb_deviation + tau, sc) # (N, M)
        return tcb_deviation

    def compute_unit_vector(self, t, link=LINKS):
        r"""Compute link unit vector.

        The unit vector points from the emitter spacecraft to the receiver spacecraft.

        The vector coordinates are given in the BCRS frame.

        We compute

        .. math::
           \vu{n}(t_\text{rec}) = \frac{\vb{x}_\text{rec}(t_\text{rec}) - \vb{x}_\text{emit}(t_\text{emit})}
           {\abs{\vb{x}_\text{rec}(t_\text{rec}) - \vb{x}_\text{emit}(t_\text{emit})}} \qs

        Args:
            t ((N,) or (N, M) array-like): TCB times [s]
            link ((M,) array-like): link indices

        Returns:
            (N, M, 3) ndarray: Link unit vectors.
        """
        tt = self.compute_ltt(t, link) # (N, M)
        pos_rec = self.compute_position(t, receiver(link)) # (N, M, 3)
        t_em = atleast_2d(t) - tt # (N, M)
        pos_em = self.compute_position(t_em, emitter(link)) # (N, M, 3)
        return (pos_rec - pos_em) / norm(pos_rec - pos_em)[:, :, np.newaxis] # (N, M, 3)

    def compute_ltt(self, t, link=LINKS):
        """Compute light travel times (LTTs).

        Light travel times are the differences between the TCB time of reception
        of a photon at one spacecraft, and the TCB time of emission of the same photon
        by another spacecraft.

        The default implementation calls :meth:`lisaorbits.Orbits._compute_ltt_analytic`
        or :meth:`lisaorbits.Orbits._compute_ltt_iterative` depending on the value
        of :attr:`lisaorbits.Orbits.tt_method`.

        Subclasses can override this method with custom implementations.

        Args:
            t ((N,) or (N, M) array-like): TCB times [s]
            link ((M,) array-like): link indices

        Returns:
            (N, M) ndarray: Light travel times [s].

        Raises:
            ValueError: if the computation method is invalid
        """
        if self.tt_method == 'analytic':
            return self._compute_ltt_analytic(t, link) # (N, M)
        if self.tt_method == 'iterative':
            return self._compute_ltt_iterative(t, link) # (N, M)
        raise ValueError(f"Invalid light travel time computation method '{self.tt_method}', "
                         "must be 'analytic' or 'iterative'.")

    def _compute_ltt_analytic(self, t, link):
        """Compute light travel times from a series expansion of the emitter trajectory.

        Refer to the model for more information.

        Args:
            t ((N,) or (N, M) array-like): TCB times [s]
            link ((M,) array-like): link indices

        Returns:
            (N, M) ndarray: Light travel times [s].

        Raises:
            ValueError: if expansion order is invalid
            ValueError: if Shapiro delay is on but expansion order is less than 2
        """
        if self.tt_order < 0 or self.tt_order > 2:
            raise ValueError(f"Invalid light travel time computation order '{self.tt_order}', "
                             "should be one of 0, 1, or 2 when computed with analytical expansion.")

        if self.tt_order < 2 and not self.ignore_shapiro:
            raise ValueError("Cannot include Shapiro delay for light travel times using an analytic "
                             f"expansion of order '{self.tt_order}' (must be greater than 2)")

        pos_em = self.compute_position(t, emitter(link)) # (N, M, 3)
        pos_rec = self.compute_position(t, receiver(link)) # (N, M, 3)

        # Order 0
        d_er = norm(pos_rec - pos_em) # (N, M)
        tt = d_er # (N, M)

        # Order 1
        if self.tt_order >= 1:
            vel_em = self.compute_velocity(t, emitter(link)) # (N, M, 3)
            r_er = pos_rec - pos_em # from emitter to receiver (N, M, 3)
            velem_rer = dot(vel_em, r_er) # (N, M)
            tt += velem_rer / c # (N, M)

        # Order 2
        if self.tt_order == 2:
            acc_em = self.compute_acceleration(t, emitter(link)) # (N, M, 3)
            # This part is a correction arising from emitter motion
            tt += 0.5 * (dot(vel_em, vel_em) + (velem_rer / d_er)**2 - dot(acc_em, r_er)) * d_er / c**2 # (N, M)
            # The following part is the Shapiro delay
            if not self.ignore_shapiro:
                r_em, r_rec = norm(pos_em), norm(pos_rec) # (N, M)
                tt += SUN_SCHWARZSCHILD_RADIUS * np.log((r_em + r_rec + d_er) / (r_em + r_rec - d_er)) # (N, M)

        return tt / c # (N, M)

    def _compute_ltt_iterative(self, t, link):
        """Compute light travel times using an iterative procedure.

        Refer to the model for more information.

        Args:
            t ((N,) or (N, M) array-like): TCB times [s]
            link ((M,) array-like): link indices

        Returns:
            (N, M) ndarray: Light travel times [s].

        Raises:
            ValueError: if the number of iterations is invalid
            ValueError: if Shapiro delay is on but the number of iterations is less than 2
        """
        if self.tt_niter < 0:
            raise ValueError(f"Invalid number of iterations '{self.tt_niter}' for iterative procedure when "
                             "computing the light travel times.")

        if self.tt_niter < 2 and not self.ignore_shapiro:
            raise ValueError("Cannot include Shapiro delay for light travel times using an iterative"
                             f"procedure with number of iterations '{self.tt_niter}' (must be greater than 2)")

        pos_em = self.compute_position(t, emitter(link)) # (N, M, 3)
        pos_rec = self.compute_position(t, receiver(link)) # (N, M, 3)

        # First the iteration to find the flat spacetime travel time
        tt = norm(pos_rec - pos_em) / c # (N, M)
        for _ in range(self.tt_niter):
            t_em = atleast_2d(t) - tt # (N, M)
            pos_em = self.compute_position(t_em, emitter(link)) # (N, M, 3)
            tt = norm(pos_rec - pos_em) / c # (N, M)

        # And the Shapiro time delay
        if not self.ignore_shapiro:
            r_em, r_rec = norm(pos_em), norm(pos_rec) # (N, M)
            d_er = c * tt # (N, M)
            tt += SUN_SCHWARZSCHILD_RADIUS * np.log((r_em + r_rec + d_er) / (r_em + r_rec - d_er)) / c # (N, M)

        return tt # (N, M)

    def compute_ltt_derivative(self, t, link=LINKS):
        """Compute light travel time derivatives (LTTs).

        The default implementation uses an series expansion of the emitting spacecraft
        trajectory. Subclasses can override this method with custom implementations.

        Args:
            t ((N,) or (N, M) array-like): TCB times [s]
            link ((M,) array-like): link indices

        Returns:
            (N, M) ndarray: Light travel time derivatives [s/s].
        """
        pos_rec = self.compute_position(t, receiver(link)) # (N, M, 3)
        vel_rec = self.compute_velocity(t, receiver(link)) # (N, M, 3)
        ltt = self.compute_ltt(t, link) # (N, M)

        # Note that the position and velocity of the emitter are evaluated
        # at receiver time for order 0 and 1, but at emitter time for order 2
        if self.tt_order < 2 and self.tt_method == 'analytic':
            pos_em = self.compute_position(t, emitter(link)) # (N, M, 3)
            vel_em = self.compute_velocity(t, emitter(link)) # (N, M, 3)
        else:
            t_em = atleast_2d(t) - ltt # (N, M)
            pos_em = self.compute_position(t_em, emitter(link)) # (N, M, 3)
            vel_em = self.compute_velocity(t_em, emitter(link)) # (N, M, 3)

        r_er = pos_rec - pos_em # from emitter to receiver (N, M, 3)
        d_er = norm(pos_rec - pos_em) # (N, M)
        n_er = r_er / d_er[:, :, np.newaxis] # unit vector from emitter to receiver (N, M, 3)
        ner_vr = dot(n_er, vel_rec) # (N, M)
        ner_ve = dot(n_er, vel_em) # (N, M)

        if self.tt_order < 2 and self.tt_method == 'analytic':
            # This is the zeroth order term which contributes only
            # for order 0 or order 1
            # all quantities being evaluated at the receiver time
            d_tt = (ner_vr - ner_ve) / c # (N, M)
        else:
            # The derivation is different if one goes to 2nd order.
            # See Eq. 27 in Hees et al CQG 29(23):235027 (2012).
            r_em = norm(pos_em) # (N, M)
            r_rec = norm(pos_rec) # (N, M)
            den = (r_em + r_rec)**2 - d_er**2 # (N, M)
            dq_rec = ner_vr + 2 * SUN_SCHWARZSCHILD_RADIUS * \
                ((r_em + r_rec) * ner_vr - d_er * dot(pos_rec, vel_rec) / r_rec) / den # (N, M)
            dq_em = ner_ve + 2 * SUN_SCHWARZSCHILD_RADIUS * \
                ((r_em + r_rec) * ner_ve + d_er * dot(pos_em, vel_em) / r_em) / den # (N, M)
            d_tt = (dq_rec - dq_em) / (c - dq_em) # (N, M)

        if self.tt_order == 1 and self.tt_method == 'analytic':
            # This is the first order contribution, to be included only if
            # the order is strictly less than 2
            acc_em = self.compute_acceleration(t, emitter(link)) # (N, M, 3)
            d_tt += (dot(vel_rec - vel_em, vel_em) + dot(pos_rec - pos_em, acc_em)) / c**2 # (N, M)

        return d_tt # (N, M)

    def compute_ppr(self, t, link=LINKS):
        """Compute proper pseudoranges (PPRs).

        Proper pseudoranges are the differences between the time of reception of a photon
        expressed in the TPS of the receiving spacecraft and the time of emission of the
        same photon expressed in the TPS of the emitting spacecraft.

        Note that they include information about the light travel times, as well as
        the conversion between TPSs and TCB.

        Args:
            t ((N,) or (N, M) array-like): TCB times [s]
            link ((M,) array-like): link indices

        Returns:
            (N, M) ndarray: Proper pseudoranges [s].
        """
        tau_receiver = self.compute_tps_deviation(t, receiver(link)) # (N, M)
        ltt = self.compute_ltt(t, link) # (N, M)
        t_em = atleast_2d(t) - ltt # (N, M)
        tau_emitter = self.compute_tps_deviation(t_em, emitter(link)) # (N, M)
        return ltt + tau_receiver - tau_emitter # (N, M)

    def compute_ppr_derivative(self, t, link=LINKS):
        """Compute proper pseudorange (PPR) derivatives.

        Args:
            t ((N,) or (N, M) array-like): TCB times [s]
            link ((M,) array-like): link indices

        Returns:
            (N, M) ndarray: Proper pseudorange derivatives [s/s].
        """
        dtau_receiver = self.compute_tps_deviation_derivative(t, receiver(link)) # (N, M)
        d_tt = self.compute_ltt_derivative(t, link) # (N, M)
        ltt = self.compute_ltt(t, link) # (N, M)
        t_em = atleast_2d(t) - ltt # (N, M)
        dtau_emitter = self.compute_tps_deviation_derivative(t_em, emitter(link)) # (N, M)
        return (dtau_receiver - dtau_emitter + d_tt * (1 + dtau_emitter)) / (1 + dtau_receiver) # (N, M)

    def plot_spacecraft(self, t, sc, output=None):
        """Plot quantities associated with one spacecraft.

        Args:
            t ((N,) array-like): TCB times [s]
            sc (int): spacecraft index, one of 1, 2, 3
            output (str): output filename, or ``None`` to show the plots
        """
        # Initialize the plot
        _, axes = plt.subplots(5, 1, figsize=(12, 20))
        axes[0].set_title(f"Spacecraft {sc}")
        axes[4].set_xlabel("Barycentric time (TCB) [s]")
        # Plot positions
        logger.info("Plotting positions for spacecraft %d", sc)
        axes[0].set_ylabel("Position [m]")
        positions = self.compute_position(t, [sc])[:, 0] # (N, 3)
        axes[0].plot(t, positions[:, 0], label=r'$x$')
        axes[0].plot(t, positions[:, 1], label=r'$y$')
        axes[0].plot(t, positions[:, 2], label=r'$z$')
        # Plot velocities
        logger.info("Plotting velocities for spacecraft %d", sc)
        axes[1].set_ylabel("Velocity [m/s]")
        velocities = self.compute_velocity(t, [sc])[:, 0] # (N, 3)
        axes[1].plot(t, velocities[:, 0], label=r'$v_x$')
        axes[1].plot(t, velocities[:, 1], label=r'$v_y$')
        axes[1].plot(t, velocities[:, 2], label=r'$v_z$')
        # Plot accelerations
        logger.info("Plotting accelerations for spacecraft %d", sc)
        axes[2].set_ylabel("Acceleration [m/s^2]")
        accelerations = self.compute_acceleration(t, [sc])[:, 0] # (N, 3)
        axes[2].plot(t, accelerations[:, 0], label=r'$a_x$')
        axes[2].plot(t, accelerations[:, 1], label=r'$a_y$')
        axes[2].plot(t, accelerations[:, 2], label=r'$a_z$')
        # Plot proper times
        logger.info("Plotting proper times for spacecraft %d", sc)
        axes[3].set_ylabel("Proper time deviation [s]")
        tps_deviations = self.compute_tps_deviation(t, [sc])[:, 0] # (N,)
        axes[3].plot(t, tps_deviations, label=r'$\delta \tau$')
        # Plot proper time derivatives
        logger.info("Plotting proper time derivatives for spacecraft %d", sc)
        axes[4].set_ylabel("Proper time deviation derivative [s/s]")
        tps_deviations_derivatives = self.compute_tps_deviation_derivative(t, [sc])[:, 0] # (N,)
        axes[4].plot(t, tps_deviations_derivatives, label=r'$\dot \delta \tau$')
        # Add legend and grid
        for axis in axes:
            axis.legend()
            axis.grid()
        # Show or save figure
        if output is not None:
            logger.info("Saving plots to %s", output)
            plt.savefig(output, bbox_inches='tight')
        else:
            logger.info("Showing plots")
            plt.show()

    def plot_links(self, t, output=None):
        """Plot quantities associated with the 6 links.

        Args:
            t ((N,) array-like): TCB times [s]
            output: output filename, or ``None`` to show the plots
        """
        # Initialize the plot
        _, axes = plt.subplots(4, 1, figsize=(12, 16))
        axes[0].set_title("Light travel times, proper pseudorange and derivatives")
        axes[3].set_xlabel("Barycentric time (TCB) [s]")
        # Plot light travel times
        logger.info("Plotting light travel times")
        axes[0].set_ylabel("Light travel time [s]")
        ltts = self.compute_ltt(t, self.LINKS) # (N, M)
        for index, link in enumerate(self.LINKS):
            axes[0].plot(t, ltts[:, index], label=link)
        # Plot proper pseudoranges
        logger.info("Plotting proper pseudoranges")
        axes[1].set_ylabel("Proper pseudorange [s]")
        pprs = self.compute_ppr(t, self.LINKS) # (N, M)
        for index, link in enumerate(self.LINKS):
            axes[1].plot(t, pprs[:, index], label=link)
        # Plot light travel time derivatives
        logger.info("Plotting light travel time derivatives")
        axes[2].set_ylabel("Light travel time derivative [s/s]")
        ltt_derivatives = self.compute_ltt_derivative(t, self.LINKS) # (N, M)
        for index, link in enumerate(self.LINKS):
            axes[2].plot(t[:], ltt_derivatives[:, index], label=link)
        # Plot proper pseudorange derivatives
        logger.info("Plotting proper pseudorange derivatives")
        axes[3].set_ylabel("Proper pseudorange derivative [s/s]")
        ppr_derivatives = self.compute_ppr_derivative(t, self.LINKS) # (N, M)
        for index, link in enumerate(self.LINKS):
            axes[3].plot(t[:], ppr_derivatives[:, index], label=link)
        # Add legend and grid
        for axis in axes:
            axis.legend()
            axis.grid()
        # Show or save figure
        if output is not None:
            logger.info("Saving plots to %s", output)
            plt.savefig(output, bbox_inches='tight')
        else:
            logger.info("Showing plots")
            plt.show()

    def _write_attr(self, hdf5, *names):
        """Write a single object attribute as metadata on ``hdf5``.

        This method is used in :meth:`lisaorbits.Orbits._write_metadata`
        to write Python self's attributes as HDF5 attributes.

        >>> my_orbits = ConcreteOrbits()
        >>> my_orbits.parameter = 42
        >>> my_orbits._write_attr('parameter')

        Args:
            hdf5 (:obj:`h5py.Group`): an HDF5 file, or a dataset
            names* (str): attribute names
        """
        for name in names:
            hdf5.attrs[name] = getattr(self, name)

    def _write_metadata(self, hdf5):
        """Write relevant object's attributes as metadata on ``hdf5``.

        This is for tracability and reproducibility. All parameters
        necessary to re-instantiate the orbits object and reproduce the
        exact same simulation should be written to file.

        Use the :meth:`lisaorbits.Orbits._write_attr` method.

        .. admonition:: Suclassing notes
            This class is intended to be overloaded by subclasses to write
            additional attributes.

        .. important::
            You MUST call super implementation in subclasses.

        Args:
            hdf5 (:obj:`h5py.Group`): an HDF5 file, or a dataset
        """
        self._write_attr(hdf5,
            'git_url', 'version', 'generator',
            't_init', 'tt_method', 'tt_order', 'tt_niter', 'ignore_shapiro',
        )

    def write(self, path, dt=100000.0, size=316, t0="init", mode="x"):
        """Generate an orbit file.

        Args:
            dt (float): time step [s]
            size (int): number of samples
            t0 (float or str): start time [s], or ``"init"`` to use :attr:`t_init`
            path (str): path to the generated orbit file
            mode (str): open mode, default ``'x'`` (create file, fail if exists)
        """
        if t0 == "init":
            t0 = self.t_init

        # Open orbit file
        logger.info("Creating orbit file %s", path)
        with h5py.File(path, mode) as hdf5:

            logger.debug("Writing metadata")
            self._write_metadata(hdf5)
            hdf5.attrs["dt"] = dt
            hdf5.attrs["size"] = size
            hdf5.attrs["t0"] = t0

            logger.debug("Writing TCB spacecraft quantities")
            t = t0 + np.arange(size) * dt
            hdf5['tcb/x'] = self.compute_position(t, self.SC)
            hdf5['tcb/v'] = self.compute_velocity(t, self.SC)
            hdf5['tcb/a'] = self.compute_acceleration(t, self.SC)
            hdf5['tcb/delta_tau'] = self.compute_tps_deviation(t, self.SC)

            logger.debug("Writing TCB link quantities")
            hdf5['tcb/n'] = self.compute_unit_vector(t, self.LINKS)
            hdf5['tcb/ltt'] = self.compute_ltt(t, self.LINKS)
            hdf5['tcb/ppr'] = self.compute_ppr(t, self.LINKS)
            hdf5['tcb/d_ltt'] = self.compute_ltt_derivative(t, self.LINKS)
            hdf5['tcb/d_ppr'] = self.compute_ppr_derivative(t, self.LINKS)

            logger.debug("writing TPS spacecraft quantities")
            delta_t = self.compute_tcb_deviation(t, self.SC)
            hdf5['tps/delta_t'] = delta_t

            logger.debug("writing TPS link quantities")
            t = t[:, np.newaxis] + delta_t[:, arrayindex(self.SC, receiver(self.LINKS))]
            hdf5['tps/ppr'] = self.compute_ppr(t, self.LINKS)
            hdf5['tps/d_ppr'] = self.compute_ppr_derivative(t, self.LINKS)

            logger.info("Closing orbit file %s", path)


class StaticConstellation(Orbits):
    """Static constellation (fixed positions and constant armlengths).

    You can either initialize the orbits from a set of spacecraft positions,
    another instance of :class:`lisaorbits.Orbits`, or a set of armlengths.

    We assume that TPS deviations and derivatives thereof are vanishing.
    Similarly, velocities and accelerations are set to zero.

    Args:
        r_1 ((3,) array-like): position vector of spacecraft 1 in BCRS [m]
        r_2 ((3,) array-like): position vector of spacecraft 2 in BCRS [m]
        r_3 ((3,) array-like): position vector of spacecraft 3 in BCRS [m]
        **kwargs: all other args from :class:`lisaorbits.orbits.Orbits`
    """

    def __init__(self, r_1, r_2, r_3, tt_order=0, tt_niter=0, ignore_shapiro=True, **kwargs):

        # Update default args because we have a static constellation
        # and therefore do not need higher-order LTT computation
        super().__init__(
            tt_order=tt_order,
            tt_niter=tt_niter,
            ignore_shapiro=ignore_shapiro,
            **kwargs)

        #: (3, 3) ndarray: Spacecraft position vectors in BCRS [m].
        self.sc_positions = np.stack([r_1, r_2, r_3], axis=0) # (3 SC, 3 COORDS)
        if self.sc_positions.shape != (3, 3):
            raise TypeError("invalid shape '{self.sc_positions.shape}' for spacecraft positions")

    @classmethod
    def from_orbits(cls, orbits, t_freeze, **kwargs):
        """Initialize a static constellation from other orbits.

        We compute spacecraft positions from ``orbits`` at ``t_freeze`` and
        use them as constant spacecraft positions for our static constellation.

        Args:
            orbits (:class:`lisaorbits.Orbits`): orbit instance
            t_freeze (float): time at which spacecraft positions are computed [s]
            **kwargs: all other args from :class:`lisaorbits.orbits.StaticConstellation`
        """
        if not isinstance(orbits, Orbits):
            raise TypeError(f"orbits should be of type 'Orbits', got '{type(orbits)}'")

        sc_positions = orbits.compute_position([t_freeze], [1, 2, 3])[0]
        return cls(sc_positions[0], sc_positions[1], sc_positions[2], **kwargs)

    @classmethod
    def from_armlengths(cls,
                        l_12=8.33242295*c,
                        l_23=8.30282196*c,
                        l_31=8.33242298*c,
                        barycenter=(0, 0, 0),
                        **kwargs):
        r"""Initialize a static constellation from armlengths.

        The default armlength values are based on the PPRs values for the first
        samples generated with :class:`lisaorbits.orbits.KeplerianOrbits`.

        The spacecraft are positioned such that spacecraft 1 lies on the x-axis,
        and the constellation is contained in the xy-plane.

        Args:
            l_12 (float): armlength between spacecraft 1 and 2 [m]
            l_23 (float): armlength between spacecraft 2 and 3 [m]
            l_31 (float): armlength between spacecraft 3 and 1 [m]
            barycenter ((3,) array-like): constellation's barycenter BCRS position [m]
            **kwargs: all other args from :class:`lisaorbits.orbits.StaticConstellation`
        """
        x_1 = np.sqrt(2 * l_12**2 - l_23**2 + 2 * l_31**2) / 3
        x_2 = (l_23**2 + l_31**2 - 5 * l_12**2) / (18 * x_1)
        x_3 = (l_12**2 + l_23**2 - 5 * l_31**2) / (18 * x_1)

        y_2 = -np.sqrt(-(l_12 - l_23 - l_31) * (l_12 + l_23 - l_31) \
            * (l_12 - l_23 + l_31) * (l_12 + l_23 + l_31)) / (6 * x_1)

        return cls(
            r_1=[x_1 + barycenter[0], barycenter[1], barycenter[2]],
            r_2=[x_2 + barycenter[0], y_2 + barycenter[1], barycenter[2]],
            r_3=[x_3 + barycenter[0], -y_2 + barycenter[1], barycenter[2]],
            **kwargs)

    def _write_metadata(self, hdf5):
        super()._write_metadata(hdf5)
        self._write_attr(hdf5, 'sc_positions')

    def compute_position(self, t, sc=SC):
        sc_indices = arrayindex(self.SC, sc) # (M,)
        positions = self.sc_positions[sc_indices][np.newaxis]  # (1, M, 3)
        return np.repeat(positions, len(t), axis=0) # (N, M, 3)

    def compute_velocity(self, t, sc=SC):
        return np.zeros((len(t), len(sc), 3)) # (N, M, 3)

    def compute_acceleration(self, t, sc=SC):
        return np.zeros((len(t), len(sc), 3)) # (N, M, 3)

    def compute_tps_deviation(self, t, sc=SC):
        return np.zeros((len(t), len(sc))) # (N, M)

    def compute_tps_deviation_derivative(self, t, sc=SC):
        return np.zeros((len(t), len(sc))) # (N, M)


class EqualArmlengthOrbits(Orbits):
    r"""Keplerian orbits that minimize flexing to leading order in eccentricity.

    These orbits are the solution to the two-body problem in Newtonian gravity,
    optimized to leave inter-spacecraft distances constant to leading order in
    eccentricity.

    Args:
        L (float): mean inter-spacecraft distance [m]
        a (float): semi-major axis for an orbital period of 1 yr [m]
        lambda1 (float): spacecraft 1's longitude of periastron [rad]
        m_init1 (float): spacecraft 1's mean anomaly at initial time :math:`t_init` [rad]
        **kwargs: all other args from :class:`lisaorbits.orbits.Orbits`
    """

    def __init__(self, L=2.5E9, a=ASTRONOMICAL_UNIT, lambda1=0, m_init1=0, **kwargs):

        super().__init__(**kwargs)

        #: float: Semi-major axis for an orbital period of 1 yr [m].
        self.a = float(a)
        #: float: Mean inter-spacecraft distance [m].
        self.L = float(L)
        #: float: Spacecraft 1's mean anomaly at :attr:`t_init` [rad].
        self.m_init1 = float(m_init1)
        #: float: Spacecraft 1's longitude of periastron [rad].
        self.lambda1 = float(lambda1)
        #: float: Orbits eccentricity.
        self.e = self.L / (2 * self.a) / np.sqrt(3)

        self.n = np.sqrt(GM_SUN / self.a**3)
        self.theta = (self.SC - 1) * 2 * np.pi / 3 # (M,)
        self.beta = self.theta + self.lambda1 # (M,)
        self.cos_beta = np.cos(self.beta) # (M,)
        self.sin_beta = np.sin(self.beta) # (M,)

        self.gr_const = (self.n * self.a / c)**2

    def _write_metadata(self, hdf5):
        super()._write_metadata(hdf5)
        self._write_attr(hdf5, 'a', 'L', 'm_init1', 'lambda1')

    def _compute_mbar(self, t):
        """Computes the angle of the constellation center of mass.

        Args:
            t ((N,) or (N, M) array-like): TCB times [s]

        Returns:
            tuple: The 3-tuple ``(m_bar, cos(mbar), sin(mbar))`` of ndarrays,
            each with shape (N, 1) or (N, M) for each element.
        """
        t = atleast_2d(t) # (N, 1) or (N, M)
        mbar = self.n * self._since_init(t) + self.m_init1 + self.lambda1 # (N, 1) or (N, M)
        return (mbar, np.cos(mbar), np.sin(mbar)) # each (N, 1) or (N, M)

    def compute_position(self, t, sc=SC):
        sc_indices = arrayindex(self.SC, sc) # (M,)
        # Compute constellation angle
        mbar, cos_mbar, sin_mbar = self._compute_mbar(t) # (N, 1) or (N, M)
        # Compute positions
        sc_x = self.a * cos_mbar + self.a * self.e * (sin_mbar * cos_mbar * self.sin_beta[np.newaxis, sc_indices] \
                - (1 + sin_mbar**2) * self.cos_beta[np.newaxis, sc_indices]) # (N, M)
        sc_y = self.a * sin_mbar + self.a * self.e * (sin_mbar * cos_mbar * self.cos_beta[np.newaxis, sc_indices] \
                - (1 + cos_mbar**2) * self.sin_beta[np.newaxis, sc_indices]) # (N, M)
        sc_z = -self.a * self.e * np.sqrt(3) * np.cos(mbar - self.beta[np.newaxis, sc_indices]) # (N, M)
        # Stack coordinates
        return np.stack([sc_x, sc_y, sc_z], axis=-1) # (N, M, 3)

    def compute_velocity(self, t, sc=SC):
        sc_indices = arrayindex(self.SC, sc) # (M,)
        # Compute constellation angle
        mbar, cos_mbar, sin_mbar = self._compute_mbar(t) # (N, 1) or (N, M)
        # Compute velocities
        sc_vx = -self.a * self.n * sin_mbar \
            + self.a * self.e * self.n * ((cos_mbar**2 - sin_mbar**2) * self.sin_beta[np.newaxis, sc_indices] \
            - 2 * sin_mbar * cos_mbar * self.cos_beta[np.newaxis, sc_indices]) # (N, M)
        sc_vy = self.a * self.n * cos_mbar \
            + self.a * self.e * self.n * ((cos_mbar**2 - sin_mbar**2) * self.cos_beta[np.newaxis, sc_indices] \
            + 2 * sin_mbar * cos_mbar * self.sin_beta[np.newaxis, sc_indices]) # (N, M)
        sc_vz = self.a * self.e * self.n * np.sqrt(3) * np.sin(mbar - self.beta[np.newaxis, sc_indices]) # (N, M)
        # Stack coordinates
        return np.stack([sc_vx, sc_vy, sc_vz], axis=-1) # (N, M, 3)

    def compute_acceleration(self, t, sc=SC):
        sc_indices = arrayindex(self.SC, sc) # (M,)
        # Compute constellation angle
        mbar, cos_mbar, sin_mbar = self._compute_mbar(t) # (N, 1) or (N, M)
        # Compute velocities
        sc_ax = -self.a * self.n**2 * cos_mbar - 4 * self.a * self.e * self.n**2 \
            * (sin_mbar * cos_mbar * self.sin_beta[np.newaxis, sc_indices] \
            + (0.5 - sin_mbar**2) * self.cos_beta[np.newaxis, sc_indices]) # (N, M)
        sc_ay = -self.a * self.n**2 * sin_mbar - 4 * self.a * self.e * self.n**2 \
            * (sin_mbar * cos_mbar * self.cos_beta[np.newaxis, sc_indices] \
            + (0.5 - cos_mbar**2) * self.sin_beta[np.newaxis, sc_indices]) # (N, M)
        sc_az = self.a * self.e * self.n**2 * np.sqrt(3) \
            * np.cos(mbar - self.beta[np.newaxis, sc_indices]) # (N, M)
        # Stack coordinates
        return np.stack([sc_ax, sc_ay, sc_az], axis=-1) # (N, M, 3)

    def compute_tps_deviation(self, t, sc=SC):
        sc_indices = arrayindex(self.SC, sc) # (M,)
        # Compute constellation angle
        t = atleast_2d(t) # (N, 1) or (N, M)
        mbar, _, _ = self._compute_mbar(t) # (N, 1) or (N, M)
        # Compute proper time deviation
        return -self.gr_const * (
            1.5 * self._since_init(t)
            + 2
            * self.e
            / self.n
            * (
                np.sin(mbar - self.beta[np.newaxis, sc_indices])
                - np.sin(self.m_init1 - self.theta[np.newaxis, sc_indices])
            )
        )  # (N, M)

    def compute_tps_deviation_derivative(self, t, sc=SC):
        sc_indices = arrayindex(self.SC, sc) # (M,)
        # Compute constellation angle
        mbar, _, _ = self._compute_mbar(t) # (N, 1) or (N, M)
        # Compute proper time deviation
        return -self.gr_const * (
            1.5 + 2 * self.e * np.cos(mbar - self.beta[np.newaxis, sc_indices])
        )  # (N, M)


class KeplerianOrbits(Orbits):
    """Keplerian orbits that minimize flexing to next-to leading order in eccentricity.

    These orbits are the solution to the two-body problem in Newtonian gravity,
    optimized to leave inter-spacecraft distances constant to second order in
    eccentricity.

    Args:
        L (float): mean inter-spacecraft distance [m]
        a (float): semi-major axis for an orbital period of 1 yr [m]
        lambda1 (float): spacecraft 1's longitude of periastron [rad]
        m_init1 (float): spacecraft 1's mean anomaly at :attr:`t_init` [rad]
        kepler_order (int): number of iterations in the Newton-Raphson procedure
        **kwargs: all other args from :class:`lisaorbits.Orbits`
    """

    def __init__(self, L=2.5E9, a=ASTRONOMICAL_UNIT, lambda1=0, m_init1=0, kepler_order=2, **kwargs):
        super().__init__(**kwargs)

        #: float: Semi-major axis for an orbital period of 1 yr [m].
        self.a = float(a)
        #: float: Mean inter-spacecraft distance [m].
        self.L = float(L)
        #: int: Number of iterations in the Newton-Raphson procedure.
        self.kepler_order = int(kepler_order)
        #: float: Spacecraft 1's mean anomaly at initial time [rad].
        self.m_init1 = float(m_init1)
        #: float: Spacecraft 1's longitude of periastron [rad].
        self.lambda1 = float(lambda1)

        #: float: Perturbation :math:`\delta` to tilt angle :math:`\nu`.
        self.delta = 5.0 / 8.0
        #: float: Orbital parameter (used for series expansions).
        self.alpha = self.L / (2 * self.a)
        #: float: Orbits tilt angle [rad].
        self.nu = np.pi / 3 + self.delta * self.alpha
        #: float: Orbits eccentricity.
        self.e = np.sqrt(1 + 4 * self.alpha * np.cos(self.nu) / np.sqrt(3) + 4 * self.alpha**2 / 3) - 1

        self.tan_i = self.alpha * np.sin(self.nu) / ((np.sqrt(3) / 2) + self.alpha * np.cos(self.nu))
        self.cos_i = 1 / np.sqrt(1 + self.tan_i**2)
        self.sin_i = self.tan_i * self.cos_i

        self.n = np.sqrt(GM_SUN / self.a**3)
        self.theta = (self.SC - 1) * 2 * np.pi / 3 # (3,)
        self.m_init = self.m_init1 - self.theta # (3,)
        self.lambda_k = self.lambda1 + self.theta # (3,)
        self.sin_lambda = np.sin(self.lambda_k) # (3,)
        self.cos_lambda = np.cos(self.lambda_k) # (3,)

        self.gr_const = (self.n * self.a / c)**2

    def _write_metadata(self, hdf5):
        super()._write_metadata(hdf5)
        self._write_attr(hdf5, 'a', 'L', 'kepler_order', 'm_init1', 'lambda1')

    def compute_eccentric_anomaly(self, t, sc):
        r"""Estimate the eccentric anomaly.

        This uses an iterative Newton-Raphson method to solve the Kepler equation,
        starting from a low eccentricity expansion of the solution.

        .. math::
            \psi_k - e \sin \psi_k = m_k(t) \qc

        with :math:`m_k(t)` the mean anomaly.

        We use ``kepler_order`` iterations. For low eccentricity, the convergence rate
        of this iterative scheme is of the order of :math:`e^2`. Typically for LISA
        spacecraft (characterized by a small eccentricity 0.005), the iterative
        procedure converges in one iteration using double precision.

        Args:
            t ((N,) or (N, M) array-like): TCB times [s]
            sc ((M,) array-like): spacecraft indices

        Returns:
            (N, M) ndarray: Eccentric anomalies [rad].
        """
        # Compute the mean anomaly
        logger.debug("Computing eccentric anomaly for spacecraft %s at time %s s", sc, t)
        sc_index = arrayindex(self.SC, sc) # (M,)
        m_init = self.m_init[sc_index] # (M,)
        m = m_init[np.newaxis] + self.n * atleast_2d(self._since_init(t)) # (N, M)
        # The following expression is valid up to e**4
        ecc_anomaly = m + (self.e - self.e**3/8) * np.sin(m) + 0.5 * self.e**2 * np.sin(2 * m) \
            + 3/8 * self.e**3 * np.sin(3 * m) # (N, M)
        # Standard Newton-Raphson iterative procedure
        for _ in range(self.kepler_order):
            error = ecc_anomaly - self.e * np.sin(ecc_anomaly) - m # (N, M)
            ecc_anomaly -= error / (1 - self.e * np.cos(ecc_anomaly)) # (N, M)
        return ecc_anomaly # (N, M)

    def compute_position(self, t, sc=SC):
        sc_index = arrayindex(self.SC, sc)
        # Compute eccentric anomaly
        psi = self.compute_eccentric_anomaly(t, sc) # (N, M)
        cos_psi = np.cos(psi) # (N, M)
        sin_psi = np.sin(psi) # (N, M)
        # Reference position
        ref_x = self.a * self.cos_i * (cos_psi - self.e) # (N, M)
        ref_y = self.a * np.sqrt(1 - self.e**2) * sin_psi # (N, M)
        ref_z = -self.a * self.sin_i * (cos_psi - self.e) # (N, M)
        # Spacecraft position
        sc_x = self.cos_lambda[np.newaxis, sc_index] * ref_x \
            - self.sin_lambda[np.newaxis, sc_index] * ref_y # (N, M)
        sc_y = self.sin_lambda[np.newaxis, sc_index] * ref_x \
            + self.cos_lambda[np.newaxis, sc_index] * ref_y # (N, M)
        sc_z = ref_z # (N, M)
        # Stack coordinates
        return np.stack([sc_x, sc_y, sc_z], axis=-1) # (N, M, 3)

    def compute_velocity(self, t, sc=SC):
        sc_index = arrayindex(self.SC, sc)
        # Compute eccentric anomaly
        psi = self.compute_eccentric_anomaly(t, sc) # (N, M)
        cos_psi = np.cos(psi) # (N, M)
        sin_psi = np.sin(psi) # (N, M)
        dpsi = self.n / (1 - self.e * cos_psi) # (N, M)
        # Reference velocity
        ref_vx = -self.a * dpsi * self.cos_i * sin_psi # (N, M)
        ref_vy = self.a * dpsi * np.sqrt(1 - self.e**2) * cos_psi # (N, M)
        ref_vz = self.a * self.sin_i * dpsi * sin_psi # (N, M)
        # Spacecraft velocity
        sc_vx = self.cos_lambda[np.newaxis, sc_index] * ref_vx \
            - self.sin_lambda[np.newaxis, sc_index] * ref_vy # (N, M)
        sc_vy = self.sin_lambda[np.newaxis, sc_index] * ref_vx \
            + self.cos_lambda[np.newaxis, sc_index] * ref_vy # (N, M)
        sc_vz = ref_vz # (N, M)
        # Stack coordinates
        return np.stack([sc_vx, sc_vy, sc_vz], axis=-1) # (N, M, 3)

    def compute_acceleration(self, t, sc=SC):
        pos = self.compute_position(t, sc) # (N, M, 3)
        # Spacecraft acceleration
        a3_dist3 = float(self.a**3) / norm(pos)**3 # (N, M)
        return -self.n**2 * pos * a3_dist3[:, :, np.newaxis] # (N, M, 3)

    def compute_tps_deviation(self, t, sc=SC):
        # Compute eccentric anomaly
        t = atleast_2d(t) # (N, 1) or (N, M)
        sin_psi = np.sin(self.compute_eccentric_anomaly(t, sc)) # (N, M)
        sin_psi_init = np.sin(self.compute_eccentric_anomaly(self.t_init, sc)) # (1, M)
        # Proper time deviation
        return -1.5 * self.gr_const * self._since_init(t) - 2 * self.gr_const * (
            self.e / self.n
        ) * (
            sin_psi - sin_psi_init
        )  # (N, M)

    def compute_tps_deviation_derivative(self, t, sc=SC):
        # Compute eccentric anomaly
        psi = self.compute_eccentric_anomaly(t, sc) # (N, M)
        cos_psi = np.cos(psi) # (N, M)
        dpsi = self.n / (1 - self.e * cos_psi) # (N, M)
        # Compute proper time deviation
        return -(3 + self.e * cos_psi) / (2 * self.n) * self.gr_const * dpsi # (N, M)


class InterpolatedOrbits(Orbits):
    """Interpolate an array of spacecraft positions.

    Splines are used to interpolate the spacecraft positions and velocities. The
    analytic derivatives of the splines are used to compute spacecraft velocities
    and accelerations if they are not provided.

    TPS deviations are numerically integrated.

    Args:
        t_interp ((N,) array-like): interpolating TCB times (needs to be ordered) [s]
        spacecraft_positions ((N, 3, 3) array-like):
            array of spacecraft positions with dimension ``(t, sc, coordinate)`` [m]
        spacecraft_velocities ((N, 3, 3) array-like or None):
            array of spacecraft velocities with dimension ``(t, sc, coordinate)``
            [m/s], or None to compute velocities as the derivatives of the
            interpolated positions
        interp_order (int): interpolation order to be used, 3 to 5
        ext (str): extrapolation mode for elements not in the interval defined by the knot sequence
        check_input (bool):
            whether to check that input contains only finite numbers -- disabling may give
            a performance gain, but may result in problems (crashes, non-termination or invalid results)
            if input file contains infinities or ``NaNs``
        **kwargs: all other args from :class:`lisaorbits.Orbits`

    Raises:
        ValueError: if interp_order is not valid
    """

    def __init__(self,
                 t_interp,
                 spacecraft_positions,
                 spacecraft_velocities=None,
                 interp_order=5,
                 ext='raise',
                 check_input=True,
                 **kwargs):

        super().__init__(**kwargs)

        #: array: Interpolating TCB times [s].
        self.t_interp = np.asarray(t_interp)
        #: array: Spacecraft positions [m].
        self.spacecraft_positions = np.asarray(spacecraft_positions)
        #: array: Spacecraft velocities [m/s].
        self.spacecraft_velocities = np.asarray(spacecraft_velocities) \
            if spacecraft_velocities is not None \
            else None
        #: int: Spline interpolation order.
        self.interp_order = int(interp_order)
        if self.interp_order < 3 or self.interp_order > 5:
            raise ValueError(f"Invalid value for '{self.interp_order}', must be 3, 4 or 5.")
        #: str: Extrapolation mode for elements not in the interval defined by the knot sequence.
        self.ext = str(ext)
        #: bool: Whether to check that input contains only finite numbers.
        self.check_input = bool(check_input)

        # Check t_interp, spacecraft_positions and spacecraft_velocities' shapes
        self._check_shapes()

        # pylint: disable=unnecessary-lambda-assignment
        interpolate = lambda x: scipy.interpolate.InterpolatedUnivariateSpline(
            self.t_interp, x,
            k=self.interp_order,
            ext=self.ext,
            check_finite=self.check_input
        )

        # Compute spline interpolation for positions
        logger.debug("Computing spline interpolation for spacecraft positions")
        self.interp_x = {sc: interpolate(self.spacecraft_positions[:, sc - 1, 0]) for sc in self.SC}
        self.interp_y = {sc: interpolate(self.spacecraft_positions[:, sc - 1, 1]) for sc in self.SC}
        self.interp_z = {sc: interpolate(self.spacecraft_positions[:, sc - 1, 2]) for sc in self.SC}

        if spacecraft_velocities is None:
            logger.debug("Computing spline derivatives for spacecraft velocities")
            # Compute derivatives of spline objects for spacecraft velocities
            self.interp_vx = {sc: self.interp_x[sc].derivative() for sc in self.SC}
            self.interp_vy = {sc: self.interp_y[sc].derivative() for sc in self.SC}
            self.interp_vz = {sc: self.interp_z[sc].derivative() for sc in self.SC}
        else:
            # Compute spline interpolation for velocities
            logger.debug("Computing spline interpolation for spacecraft velocities")
            self.interp_vx = {sc: interpolate(spacecraft_velocities[:, sc - 1, 0]) for sc in self.SC}
            self.interp_vy = {sc: interpolate(spacecraft_velocities[:, sc - 1, 1]) for sc in self.SC}
            self.interp_vz = {sc: interpolate(spacecraft_velocities[:, sc - 1, 2]) for sc in self.SC}

        # Compute derivatives of spline objects for spacecraft accelerations
        logger.debug("Computing spline derivatives for spacecraft accelerations")
        self.interp_ax = {sc: self.interp_vx[sc].derivative() for sc in self.SC}
        self.interp_ay = {sc: self.interp_vy[sc].derivative() for sc in self.SC}
        self.interp_az = {sc: self.interp_vz[sc].derivative() for sc in self.SC}

        logger.debug("Computing spline interpolation for spacecraft proper times")
        self.interp_dtau = {}
        self.interp_tau = {}
        self.tau_init = {}
        self.tau_t = {}
        for sc in self.SC:
            pos_norm = norm(self.spacecraft_positions[:, sc - 1])
            v_squared = self.interp_vx[sc](self.t_interp)**2 \
                + self.interp_vy[sc](self.t_interp)**2 \
                + self.interp_vz[sc](self.t_interp)**2
            dtau = -0.5 * (SUN_SCHWARZSCHILD_RADIUS / pos_norm + v_squared / c**2)
            self.interp_dtau[sc] = interpolate(dtau)
            # Antiderivative of dtau is integral from t_interp_0 to t, so tau(t) - tau(t_interp_0)
            # To use initial condition, we compute integral from t_init to t, which
            # is tau(t) - tau(t_init) = tau(t), but also int_{t_init}^{t_interp_0} + int_{t_interp_0}^t
            self.tau_t[sc] = self.interp_dtau[sc].antiderivative() # int_{t_interp_0}^t dtau
            self.tau_init[sc] = self.tau_t[sc](self.t_init)  # int_{t_interp_0}^{t_init} dtau
            self.interp_tau[sc] = lambda t, sc=sc: self.tau_t[sc](t) - self.tau_init[sc]

    def _write_metadata(self, hdf5):
        super()._write_metadata(hdf5)
        self._write_attr(hdf5, 'interp_order', 'ext', 'check_input')

    def _check_shapes(self):
        """Check array shapes.

        We check that ``t_interp`` is of shape (N,), and ``spacecraft_positions`` and
        ``spacecraft_velocities`` (if not None) are of shape (N, 3, 3).

        Raises:
            ValueError: if the shapes are invalid.
        """
        if len(self.t_interp.shape) != 1:
            raise ValueError(f"time array has shape {self.t_interp.shape}, must be (N).")

        size = self.t_interp.shape[0]
        if len(self.spacecraft_positions.shape) != 3 or \
           self.spacecraft_positions.shape[0] != size or \
           self.spacecraft_positions.shape[1] != 3 or \
           self.spacecraft_positions.shape[2] != 3:
            raise ValueError(
                f"spacecraft position array has shape "
                f"{self.spacecraft_positions.shape}, expected ({size}, 3, 3).")
        if self.spacecraft_velocities is not None and (
                len(self.spacecraft_velocities.shape) != 3 or \
                self.spacecraft_velocities.shape[0] != size or \
                self.spacecraft_velocities.shape[1] != 3 or \
                self.spacecraft_velocities.shape[2] != 3
            ):
            raise ValueError(
                f"spacecraft velocity array has shape "
                f"{self.spacecraft_velocities.shape}, expected ({size}, 3, 3).")

    @staticmethod
    def _broadcast(t, sc):
        """Broadcast t to have compatible shape with sc.

        Add a second axis to t if necessary, and broadcast to sc's shape.

        Args:
            t ((N,) or (N, M) array-like): TCB times [s]
            sc ((M,) array-like): spacecraft indices

        Returns:
            tuple: The broadcasted time array and length of second axis ``(t, n)``.
        """
        t = atleast_2d(t)
        broad_t, _ = np.broadcast_arrays(t, sc)
        return broad_t, broad_t.shape[1]

    def compute_position(self, t, sc=SC):
        t, n = self._broadcast(t, sc)
        sc_x = np.stack([self.interp_x[sc[i]](t[:, i]) for i in range(n)], axis=-1) # (N, M)
        sc_y = np.stack([self.interp_y[sc[i]](t[:, i]) for i in range(n)], axis=-1) # (N, M)
        sc_z = np.stack([self.interp_z[sc[i]](t[:, i]) for i in range(n)], axis=-1) # (N, M)

        return np.stack([sc_x, sc_y, sc_z], axis=-1) # (N, M, 3)

    def compute_velocity(self, t, sc=SC):
        t, n = self._broadcast(t, sc)
        sc_vx = np.stack([self.interp_vx[sc[i]](t[:, i]) for i in range(n)], axis=-1) # (N, M)
        sc_vy = np.stack([self.interp_vy[sc[i]](t[:, i]) for i in range(n)], axis=-1) # (N, M)
        sc_vz = np.stack([self.interp_vz[sc[i]](t[:, i]) for i in range(n)], axis=-1) # (N, M)

        return np.stack([sc_vx, sc_vy, sc_vz], axis=-1) # (N, M, 3)

    def compute_acceleration(self, t, sc=SC):
        t, n = self._broadcast(t, sc)
        sc_ax = np.stack([self.interp_ax[sc[i]](t[:, i]) for i in range(n)], axis=-1) # (N, M)
        sc_ay = np.stack([self.interp_ay[sc[i]](t[:, i]) for i in range(n)], axis=-1) # (N, M)
        sc_az = np.stack([self.interp_az[sc[i]](t[:, i]) for i in range(n)], axis=-1) # (N, M)

        return np.stack([sc_ax, sc_ay, sc_az], axis=-1) # (N, M, 3)

    def compute_tps_deviation(self, t, sc=SC):
        t, n = self._broadcast(t, sc)
        return np.stack([self.interp_tau[sc[i]](t[:, i]) for i in range(n)], axis=-1) # (N, M)

    def compute_tps_deviation_derivative(self, t, sc=SC):
        t, n = self._broadcast(t, sc)
        return np.stack([self.interp_dtau[sc[i]](t[:, i]) for i in range(n)], axis=-1)  # (N, M)


class OEMValueError(Exception):
    """Unexpected value in OEM file."""


class OEMOrbits(InterpolatedOrbits):
    """Reads orbits from three Orbit Ephemeris Message (OEM) files.

    Each OEM file describes the orbit of one spacecraft.

    The package includes some standard OEM files. Use {meth}`lisaorbits.OEMOrbits.
    from_included` to initialize an instance from those easily.

    Args:
        oem_1 (str): path to OEM file for spacecraft 1
        oem_2 (str): path to OEM file for spacecraft 2
        oem_3 (str): path to OEM file for spacecraft 3
        t_init (float or str): TCB time for initial conditions [s], or 'start'
            to use the start time of the orbits :attr:`t_start`
        **kwargs: all other args from :class:`lisaorbits.InterpolatedOrbits`
    """

    def __init__(self, oem_1, oem_2, oem_3, ext="raise", t_init="start", **kwargs):

        # Save file paths
        #: str: Path to OEM file for spacecraft 1.
        self.filename_1 = str(oem_1)
        #: str: Path to OEM file for spacecraft 2.
        self.filename_2 = str(oem_2)
        #: str: Path to OEM file for spacecraft 3.
        self.filename_3 = str(oem_3)

        # Read files
        epochs_1, positions_1 = self._read_oem(oem_1, 1)
        epochs_2, positions_2 = self._read_oem(oem_2, 2)
        epochs_3, positions_3 = self._read_oem(oem_3, 3)

        # Check time scales are identical
        if not np.all(epochs_1 == epochs_2) or not np.all(epochs_2 == epochs_3):
            raise ValueError("input files have different sampling")
        epochs = epochs_1
        oem_positions = np.stack([positions_1, positions_2, positions_3], axis=1) # (t, sc, coord)

        # Save first and last time
        #: float: Start time of the orbits [s].
        self.t_start = epochs[0]
        #: float: End time of the orbits [s].
        self.t_end = epochs[-1]

        # Adjust t_init to start time if requested
        if t_init == "start":
            t_init = self.t_start

        # Assume positions are in km and in EME2000 frame
        # In astropy, the EME2000 frame is referred to as ICRS (International
        # Celestial Reference System), which is very close to EME2000, with
        # differences typically below a few milliarcseconds.
        eme_positions = SkyCoord(
            x=oem_positions[:, :, 0],
            y=oem_positions[:, :, 1],
            z=oem_positions[:, :, 2],
            representation_type="cartesian",
            frame="icrs",
            unit=u.km,
        )  # each (t, sc)
        # Convert to heliocentric mean ecliptic coordinates, J2000 equinox
        hme_positions = eme_positions.heliocentricmeanecliptic.cartesian
        positions = np.stack(
            [
                hme_positions.x.to(u.m).value,
                hme_positions.y.to(u.m).value,
                hme_positions.z.to(u.m).value,
            ],
            axis=-1,
        )  # (t, sc, coord)

        logger.warning(
            "OEM preferred interpolation method ignored, using spline "
            "interpolation (see InterpolatedOrbits for details)"
        )
        super().__init__(epochs, positions, ext=ext, t_init=t_init, **kwargs)

    @classmethod
    def from_included(cls, name, **kwargs):
        """Initialize an instance from OEM files included in the package.

        Args:
            name (str): 'esa-leading' or 'esa-trailing'
            **kwargs: all other args from :class:`lisaorbits.OEMOrbits`
        """
        def fetch(path: str) -> str:
            """Fetch a file from the Github ESA repository.

            If the file is already present in the local cache, it is not
            downloaded again.

            Args:
                path (str): path to file in Github ESA repository

            Returns:
                str: path to local copy of file
            """
            return esa_repository.fetch(path, progressbar=True)

        logger.info("Fetching OEM files from ESA repository")
        if name == 'esa-trailing':
            oem_1 = fetch('crema_1p0/mida-20deg/trajectory_out_mida-20deg_cw_sg-2nmss.oem1')
            oem_2 = fetch('crema_1p0/mida-20deg/trajectory_out_mida-20deg_cw_sg-2nmss.oem2')
            oem_3 = fetch('crema_1p0/mida-20deg/trajectory_out_mida-20deg_cw_sg-2nmss.oem3')
        elif name == 'esa-leading':
            oem_1 = fetch('crema_1p0/mida+20deg/trajectory_out_mida+20deg_cw_sg-2nmss.oem1')
            oem_2 = fetch('crema_1p0/mida+20deg/trajectory_out_mida+20deg_cw_sg-2nmss.oem2')
            oem_3 = fetch('crema_1p0/mida+20deg/trajectory_out_mida+20deg_cw_sg-2nmss.oem3')
        else:
            raise ValueError(f"unsupported included OEM files '{name}'")

        # Print file hashes of files fetched from ESA repository
        logger.debug("SHA256 hash for '%s' is '%s'", oem_1, pooch.file_hash(oem_1))
        logger.debug("SHA256 hash for '%s' is '%s'", oem_2, pooch.file_hash(oem_2))
        logger.debug("SHA256 hash for '%s' is '%s'", oem_3, pooch.file_hash(oem_3))

        return cls(oem_1, oem_2, oem_3, **kwargs)

    def _write_metadata(self, hdf5):
        super()._write_metadata(hdf5)
        self._write_attr(
            hdf5, "filename_1", "filename_2", "filename_3", "t_start", "t_end"
        )

    def _read_oem(self, path, index):
        """Parse OEM file.

        We check structure and metadata, and return epochs and positions.

        Args:
            path (str): path to OEM file
            index (int): spacecraft index

        Returns:
            tuple: 2-tuple ``(epochs, positions)`` where `epochs` is a list of N UNIX timestamps,
            and ``positions`` is an array of shape (N, 3).
        """
        # pylint: disable=protected-access
        logger.info("Reading OEM file '%s'", path)
        ephemeris = OrbitEphemerisMessage.open(path)

        if ephemeris.version.strip() != '2.0':
            raise OEMValueError("unsupported OEM version")
        if len(ephemeris._segments) != 1:
            logger.warning("OEM file contains more than one segment, using the first one")

        header = {key: ephemeris.header[key] for key in ephemeris.header}
        setattr(self, f'header_{index}', header)

        segment = ephemeris._segments[0]
        metadata = segment.metadata
        if metadata['REF_FRAME'] != 'EME2000':
            # Support Earth Mean Equator and Equinox of J2000 (EME2000) frame only
            raise OEMValueError("unsupported reference frame in OEM '{metadata['REF_FRAME']}'")

        metadata_dict = {key: metadata[key] for key in metadata}
        setattr(self, f'metadata_{index}', metadata_dict)

        epochs = np.array([state.epoch.unix for state in segment])
        positions = np.stack([state.position for state in segment], axis=0)
        return (epochs, positions)


class ResampledOrbits(InterpolatedOrbits):
    """Resamples an orbit file (HDF5 created using LISAOrbits) to a new time grid.

    Splines are used to resample the spacecraft positions. All other quantities
    are deduced, as described in :class:`lisaorbits.InterpolatedOrbits`.

    Args:
        orbits (str): path to an existing orbit file
        **kwargs: all other args from :class:`lisaorbits.InterpolatedOrbits`
    """

    def __init__(self, orbits, **kwargs):

        #: str: Path to the original orbit file.
        self.orbits_path = str(orbits)

        # Load orbit file
        logger.info("Reading orbit file '%s'", self.orbits_path)
        t, spacecraft_positions = self._read_orbit_file()

        with h5py.File(self.orbits_path, 'r') as orbitf:
            self.original_attrs = dict(orbitf.attrs)

        super().__init__(t, spacecraft_positions, **kwargs)

    def _write_metadata(self, hdf5):
        super()._write_metadata(hdf5)
        self._write_attr(hdf5, 'original_attrs')

    def _read_orbit_file(self):
        """Read the original orbit file.

        Returns:
            tuple: Tuple ``(t, spacecraft_positions)`` of arrays of times [s] and
            spacecraft positions [m] with dimension (t, sc, coordinate).

        Raises:
            ValueError: if the orbit file's version is not supported.
        """
        with h5py.File(self.orbits_path, 'r') as orbitf:

            version = Version(orbitf.attrs['version'])
            logger.debug("Using orbit file version %s", version)
            if version.is_devrelease or version.local is not None:
                logger.warning("You are using an orbit file in a development version")
            if version > Version('2.3'):
                logger.warning(
                    "You are using an orbit file in a version that might not be fully supported")

            if version >= Version('2.0.dev'):
                t = orbitf.attrs['t0'] + np.arange(orbitf.attrs['size']) * orbitf.attrs['dt']
                return t, orbitf['tcb/x'][:]

            sc_1 = np.stack((orbitf['tcb/sc_1'][coord] for coord in ['x', 'y', 'z']), axis=-1)
            sc_2 = np.stack((orbitf['tcb/sc_2'][coord] for coord in ['x', 'y', 'z']), axis=-1)
            sc_3 = np.stack((orbitf['tcb/sc_3'][coord] for coord in ['x', 'y', 'z']), axis=-1)
            spacecraft_positions = np.stack((sc_1, sc_2, sc_3), axis=1)
            return orbitf['tcb/t'], spacecraft_positions
