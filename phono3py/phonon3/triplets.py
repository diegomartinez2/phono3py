# Copyright (C) 2020 Atsushi Togo
# All rights reserved.
#
# This file is part of phono3py.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in
#   the documentation and/or other materials provided with the
#   distribution.
#
# * Neither the name of the phonopy project nor the names of its
#   contributors may be used to endorse or promote products derived
#   from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import numpy as np
from phonopy.structure.tetrahedron_method import TetrahedronMethod
from phonopy.structure.grid_points import extract_ir_grid_points
from phono3py.phonon.func import gaussian


class BZGrid(object):
    """Data structure of BZ grid

    Attributes
    ----------
    addresses : ndarray
        Integer grid address of the points in Brillouin zone including
        surface.  The first prod(mesh) numbers of points are
        independent. But the rest of points are
        translational-symmetrically equivalent to some other points.
        shape=(n_grid_points, 3), dtype='int_', order='C'
    gp_map : ndarray
        Grid point mapping table containing BZ surface. See more
        detail in _relocate_BZ_grid_address docstring.
    is_dense_gp_map : bool, optional
        See the detail in the docstring of ``_relocate_BZ_grid_address``.

    """

    def __init__(self, addresses=None, gp_map=None, is_dense_gp_map=False):
        self._addresses = addresses
        self._gp_map = gp_map
        self._is_dense_gp_map = is_dense_gp_map

    @property
    def addresses(self):
        return self._addresses

    @property
    def gp_map(self):
        return self._gp_map

    @property
    def is_dense_gp_map(self):
        return self._is_dense_gp_map

    def set_bz_grid(self, mesh, reciprocal_lattice):
        """Generate BZ grid addresses and grid point mapping table

        mesh : array_like or float
            Mesh numbers or length.
            shape=(3,), dtype='int_'
        reciprocal_lattice : array_like
            Reciprocal primitive basis vectors given as column vectors
            shape=(3, 3), dtype='double', order='C'

        """
        self.relocate(get_grid_address(mesh),
                      mesh,
                      reciprocal_lattice)

    def relocate(self,
                 grid_addresses,
                 mesh,
                 reciprocal_lattice,  # column vectors
                 is_shift=None):
        """Transform parallelepiped grid to BZ grid

        grid_addresses : ndarray
            Address of all grid points in reciprocal cell. Each address is
            given by three unsigned integers.
            dtype='int_', shape=(prod(mesh), 3)
        mesh : array_like or float
            Mesh numbers or length.
            shape=(3,), dtype='int_'
        reciprocal_lattice : array_like
            Reciprocal primitive basis vectors given as column vectors
            shape=(3, 3), dtype='double', order='C'
        is_shift : array_like
            [0, 0, 0] gives Gamma center mesh and value 1 gives half mesh shift
            along the basis vectors.
            dtype='int_', shape=(3,)

        """
        self._addresses, self._gp_map = _relocate_BZ_grid_address(
            grid_addresses,
            mesh,
            reciprocal_lattice,  # column vectors
            is_shift=None,
            is_dense_gp_map=self._is_dense_gp_map)


def get_triplets_at_q(grid_point,
                      mesh,
                      point_group,  # real space point group of space group
                      reciprocal_lattice,  # column vectors
                      is_time_reversal=True,
                      swappable=True,
                      is_dense_gp_map=False):
    """Parameters
    ----------
    grid_point : int
        A grid point
    mesh : array_like
        Mesh numbers
        shape=(3,), dtype='int_'
    point_group : array_like
        Rotation matrices in real space. Note that those in reciprocal space
        mean these matrices transposed (local terminology).
        shape=(n_rot, 3, 3), dtype='intc', order='C'
    reciprocal_lattice : array_like
        Reciprocal primitive basis vectors given as column vectors
        shape=(3, 3), dtype='double', order='C'
    is_time_reversal : bool, optional
        Inversion symemtry is added if it doesn't exist. Default is True.
    swappable : bool, optional
        q1 and q2 among (q0, q1, q2) can be swapped. Deafult is True.
    is_dense_gp_map : bool, optional
        See the detail in the docstring of ``_relocate_BZ_grid_address``.

    Returns
    -------
    triplets_at_q : ndarray
        Symmetry reduced number of triplets are stored as grid point
        integer numbers.
        shape=(n_triplets, 3), dtype='int_'
    weights : ndarray
        Weights of triplets in Brillouin zone
        shape=(n_triplets,), dtype='int_'
    bz_grid : BZGrid
        Data structure to represent BZ grid.
    map_triplets : ndarray or None
        Mapping table of all triplets to symmetrically
        independent tripelts. More precisely, this gives a list of
        index mapping from all q-points to independent q' of
        q+q'+q''=G. Considering q' is enough because q is fixed and
        q''=G-q-q' where G is automatically determined to choose
        smallest |G|.
        shape=(prod(mesh),), dtype='int_'
    map_q : ndarray
        Irreducible q-points stabilized by q-point of specified grid_point.
        shape=(prod(mesh),), dtype='int_'

    """

    map_triplets, map_q, grid_address = _get_triplets_reciprocal_mesh_at_q(
        grid_point,
        mesh,
        point_group,
        is_time_reversal=is_time_reversal,
        swappable=swappable)

    bz_grid = BZGrid(is_dense_gp_map=is_dense_gp_map)
    bz_grid.relocate(grid_address,
                     mesh,
                     reciprocal_lattice)
    triplets_at_q, weights = _get_BZ_triplets_at_q(
        grid_point,
        bz_grid,
        map_triplets,
        mesh)

    assert np.prod(mesh) == weights.sum(), \
        "Num grid points %d, sum of weight %d" % (
                    np.prod(mesh), weights.sum())

    return triplets_at_q, weights, bz_grid, map_triplets, map_q


def get_all_triplets(grid_point, bz_grid, mesh):
    triplets_at_q, _ = _get_BZ_triplets_at_q(
        grid_point,
        bz_grid,
        np.arange(np.prod(mesh), dtype='int_'),
        mesh)

    return triplets_at_q


def get_nosym_triplets_at_q(grid_point,
                            mesh,
                            reciprocal_lattice,
                            is_dense_gp_map=False):
    """Returns triplets information without imposing mesh symmetry

    See the docstring of get_triplets_at_q.

    """
    bz_grid = BZGrid(is_dense_gp_map=is_dense_gp_map)
    bz_grid.relocate(get_grid_address(mesh), mesh, reciprocal_lattice)
    map_triplets = np.arange(np.prod(mesh), dtype='int_')
    triplets_at_q, weights = _get_BZ_triplets_at_q(
        grid_point,
        bz_grid,
        map_triplets,
        mesh)
    map_q = map_triplets.copy()

    return triplets_at_q, weights, bz_grid, map_triplets, map_q


def get_grid_address(mesh):
    """Returns grid_address of dtype='int_'"""
    grid_mapping_table, grid_address = _get_ir_reciprocal_mesh(
        mesh,
        [[[1, 0, 0], [0, 1, 0], [0, 0, 1]]],
        is_time_reversal=False)

    return grid_address


def get_grid_point_from_address_py(address, mesh):
    # X runs first in XYZ
    # (*In spglib, Z first is possible with MACRO setting.)
    m = mesh
    return (address[0] % m[0] +
            (address[1] % m[1]) * m[0] +
            (address[2] % m[2]) * m[0] * m[1])


def get_grid_point_from_address(address, mesh):
    """Grid point number is given by grid address but not bz_grid.

    Parameters
    ----------
    address : array_like
        Grid address.
        shape=(3,), dtype='int_'
    mesh : array_like
        Mesh numbers.
        shape=(3,), dtype='int_'

    Returns
    -------
    int
        Grid point number.

    """

    import phono3py._phono3py as phono3c

    gp = phono3c.grid_index_from_address(np.array(address, dtype='int_'),
                                         np.array(mesh, dtype='int_'))
    return gp


def get_ir_grid_points(mesh, rotations, mesh_shifts=None):
    if mesh_shifts is None:
        mesh_shifts = [False, False, False]
    grid_mapping_table, grid_address = _get_ir_reciprocal_mesh(
        mesh,
        rotations,
        is_shift=np.where(mesh_shifts, 1, 0))
    (ir_grid_points,
     ir_grid_weights) = extract_ir_grid_points(grid_mapping_table)

    return ir_grid_points, ir_grid_weights, grid_address, grid_mapping_table


def get_grid_points_by_rotations(address,
                                 reciprocal_rotations,
                                 mesh):
    """Returns grid points obtained after rotating input grid address

    Parameters
    ----------
    address : array_like
        Grid point address to be rotated.
        dtype='int_', shape=(3,)
    reciprocal_rotations : array_like
        Rotation matrices {R} with respect to reciprocal basis vectors.
        Defined by q'=Rq.
        dtype='int_', shape=(rotations, 3, 3)
    mesh : array_like
        dtype='int_', shape=(3,)

    Returns
    -------
    rot_grid_indices : ndarray
        Grid points obtained after rotating input grid address
        dtype='int_', shape=(rotations,)

    """

    rot_adrs = np.dot(reciprocal_rotations, address)
    gps = np.zeros(len(reciprocal_rotations), dtype='int_')
    for i, adrs in enumerate(rot_adrs):
        gps[i] = get_grid_point_from_address(adrs, mesh)
    return gps


def get_triplets_integration_weights(interaction,
                                     frequency_points,
                                     sigma,
                                     sigma_cutoff=None,
                                     is_collision_matrix=False,
                                     neighboring_phonons=False,
                                     lang='C'):
    triplets = interaction.get_triplets_at_q()[0]
    frequencies = interaction.get_phonons()[0]
    num_band = frequencies.shape[1]
    g_zero = None

    if is_collision_matrix:
        g = np.empty(
            (3, len(triplets), len(frequency_points), num_band, num_band),
            dtype='double', order='C')
    else:
        g = np.empty(
            (2, len(triplets), len(frequency_points), num_band, num_band),
            dtype='double', order='C')
    g[:] = 0

    if sigma:
        if lang == 'C':
            import phono3py._phono3py as phono3c
            g_zero = np.zeros(g.shape[1:], dtype='byte', order='C')
            if sigma_cutoff is None:
                cutoff = -1
            else:
                cutoff = float(sigma_cutoff)
            # cutoff < 0 disables g_zero feature.
            phono3c.triplets_integration_weights_with_sigma(
                g,
                g_zero,
                frequency_points,
                triplets,
                frequencies,
                sigma,
                cutoff)
        else:
            for i, tp in enumerate(triplets):
                f1s = frequencies[tp[1]]
                f2s = frequencies[tp[2]]
                for j, k in list(np.ndindex((num_band, num_band))):
                    f1 = f1s[j]
                    f2 = f2s[k]
                    g0 = gaussian(frequency_points - f1 - f2, sigma)
                    g[0, i, :, j, k] = g0
                    g1 = gaussian(frequency_points + f1 - f2, sigma)
                    g2 = gaussian(frequency_points - f1 + f2, sigma)
                    g[1, i, :, j, k] = g1 - g2
                    if len(g) == 3:
                        g[2, i, :, j, k] = g0 + g1 + g2
    else:
        if lang == 'C':
            g_zero = np.zeros(g.shape[1:], dtype='byte', order='C')
            _set_triplets_integration_weights_c(
                g,
                g_zero,
                interaction,
                frequency_points,
                neighboring_phonons=neighboring_phonons)
        else:
            _set_triplets_integration_weights_py(
                g, interaction, frequency_points)

    return g, g_zero


def get_tetrahedra_vertices(relative_address,
                            mesh,
                            triplets_at_q,
                            bz_grid):
    bzmesh = mesh * 2
    grid_order = [1, mesh[0], mesh[0] * mesh[1]]
    bz_grid_order = [1, bzmesh[0], bzmesh[0] * bzmesh[1]]
    num_triplets = len(triplets_at_q)
    vertices = np.zeros((num_triplets, 2, 24, 4), dtype='int_')
    for i, tp in enumerate(triplets_at_q):
        for j, adrs_shift in enumerate(
                (relative_address, -relative_address)):
            adrs = bz_grid.addresses[tp[j + 1]] + adrs_shift
            bz_gp = np.dot(adrs % bzmesh, bz_grid_order)
            gp = np.dot(adrs % mesh, grid_order)
            vgp = bz_grid.gp_map[bz_gp]
            vertices[i, j] = vgp + (vgp == -1) * (gp + 1)
    return vertices


def _get_ir_reciprocal_mesh(mesh,
                            rotations,
                            is_shift=None,
                            is_time_reversal=True):
    """Irreducible k-points are searched under a fixed q-point.

    Parameters
    ----------
    mesh : array_like
        Uniform sampling mesh numbers.
        dtype='int_', shape=(3,)
    rotations : array_like
        Rotation matrices with respect to real space basis vectors.
        dtype='int_', shape=(rotations, 3)
    is_shift : array_like
        [0, 0, 0] gives Gamma center mesh and value 1 gives  half mesh shift.
        dtype='int_', shape=(3,)
    is_time_reversal : bool
        Time reversal symmetry is included or not.

    Returns
    -------
    grid_mapping_table : ndarray
        Grid point mapping table to ir-gird-points.
        dtype='int_', shape=(prod(mesh),)
    grid_address : ndarray
        Address of all grid points. Each address is given by three integers.
        dtype='int_', shape=(prod(mesh), 3)

    """

    import phono3py._phono3py as phono3c

    mapping_table = np.zeros(np.prod(mesh), dtype='int_')
    grid_address = np.zeros((np.prod(mesh), 3), dtype='int_')
    if is_shift is None:
        is_shift = [0, 0, 0]

    if phono3c.ir_reciprocal_mesh(
            grid_address,
            mapping_table,
            np.array(mesh, dtype='int_'),
            np.array(is_shift, dtype='int_'),
            is_time_reversal * 1,
            np.array(rotations, dtype='int_', order='C')) > 0:
        return mapping_table, grid_address
    else:
        raise RuntimeError(
            "ir_reciprocal_mesh didn't work well.")


def _relocate_BZ_grid_address(grid_address,
                              mesh,
                              reciprocal_lattice,  # column vectors
                              is_shift=None,
                              is_dense_gp_map=False):
    """Grid addresses are relocated to be inside first Brillouin zone.

    Number of ir-grid-points inside Brillouin zone is returned.
    It is assumed that the following arrays have the shapes of
        bz_grid_address : (num_grid_points_in_FBZ, 3)
        bz_map (prod(mesh * 2), )

    Note that the shape of grid_address is (prod(mesh), 3) and the
    addresses in grid_address are arranged to be in parallelepiped
    made of reciprocal basis vectors. The addresses in bz_grid_address
    are inside the first Brillouin zone or on its surface. Each
    address in grid_address is mapped to one of those in
    bz_grid_address by a reciprocal lattice vector (including zero
    vector) with keeping element order. For those inside first BZ, the
    mapping is one-to-one. For those on the first BZ surface, more
    than one addresses in bz_grid_address that are equivalent by the
    reciprocal lattice translations are mapped to one address in
    grid_address. The bz_grid_address and bz_map are given in the
    following format depending on the choice of ``is_dense_gp_map``.

    is_dense_gp_map = False
    -----------------------

    Those grid points on the BZ surface except for one of them are
    appended to the tail of this array, for which bz_grid_address has
    the following data storing:

    |------------------array size of bz_grid_address-------------------------|
    |--those equivalent to grid_address--|--those on surface except for one--|
    |-----array size of grid_address-----|

    Number of grid points stored in bz_grid_address is returned.
    bz_map is used to recover grid point index expanded to include BZ
    surface from grid address. The grid point indices are mapped to
    (mesh[0] * 2) x (mesh[1] * 2) x (mesh[2] * 2) space (bz_map).

    is_dense_gp_map = True
    ----------------------

    The translationally equivalent grid points corresponding to one grid point
    on BZ surface are stored in continuously. If the multiplicity (number of
    equivalent grid points) is 1, 2, 1, 4, ... for the grid points,
    ``bz_map`` stores the multiplicites and the index positions of the first
    grid point of the equivalent grid points, i.e.,

    bz_map[:] = [0, 1, 3, 4, 8...]
    grid_address[0] -> bz_grid_address[0:1]
    grid_address[1] -> bz_grid_address[1:3]
    grid_address[2] -> bz_grid_address[3:4]
    grid_address[3] -> bz_grid_address[4:8]

    shape=(prod(mesh) + 1, )

    """

    import phono3py._phono3py as phono3c

    if is_shift is None:
        _is_shift = np.zeros(3, dtype='int_')
    else:
        _is_shift = np.array(is_shift, dtype='int_')
    bz_grid_address = np.zeros((np.prod(np.add(mesh, 1)), 3),
                               dtype='int_', order='C')

    if is_dense_gp_map:
        bz_map = np.zeros(np.prod(mesh) + 1, dtype='int_')
    else:
        bz_map = np.zeros(np.prod(np.multiply(mesh, 2)), dtype='int_')
    Q = np.eye(3, dtype='int_', order='C')
    num_gp = phono3c.bz_grid_addresses(
        bz_grid_address,
        bz_map,
        grid_address,
        np.array(mesh, dtype='int_'),
        Q,
        _is_shift,
        np.array(reciprocal_lattice, dtype='double', order='C'),
        is_dense_gp_map * 1 + 1)

    bz_grid_address = np.array(bz_grid_address[:num_gp],
                               dtype='int_', order='C')
    return bz_grid_address, bz_map


def _get_triplets_reciprocal_mesh_at_q(fixed_grid_number,
                                       mesh,
                                       rotations,
                                       is_time_reversal=True,
                                       swappable=True):
    """Search symmetry reduced triplets fixing one q-point

    Triplets of (q0, q1, q2) are searched. This method doesn't consider
    translationally equivalent points on BZ surface.

    Parameters
    ----------
    fixed_grid_number : int
        Grid point of q0
    mesh : array_like
        Mesh numbers
        dtype='int_'
        shape=(3,)
    rotations : array_like
        Rotation matrices in real space. Note that those in reciprocal space
        mean these matrices transposed (local terminology).
        dtype='intc'
        shape=(n_rot, 3, 3)
    is_time_reversal : bool
        Inversion symemtry is added if it doesn't exist.
    swappable : bool
        q1 and q2 can be swapped. By this number of triplets decreases.

    Returns
    -------
    map_triplets : ndarray or None
        Mapping table of all triplets to symmetrically
        independent tripelts. More precisely, this gives a list of
        index mapping from all q-points to independent q' of
        q+q'+q''=G. Considering q' is enough because q is fixed and
        q''=G-q-q' where G is automatically determined to choose
        smallest |G| without considering BZ surface (see docstring of
        _get_BZ_triplets_at_q.)
        shape=(prod(mesh),), dtype='int_'
    map_q : ndarray
        Irreducible q-points stabilized by q-point of specified grid_point.
        shape=(prod(mesh),), dtype='int_'
    grid_addresses : ndarray
        Address of all grid points in reciprocal cell. Each address is
        given by three unsigned integers.
        dtype='int_', shape=(prod(mesh), 3)

    """

    import phono3py._phono3py as phono3c

    map_triplets = np.zeros(np.prod(mesh), dtype='int_')
    map_q = np.zeros(np.prod(mesh), dtype='int_')
    grid_address = np.zeros((np.prod(mesh), 3), dtype='int_')

    phono3c.triplets_reciprocal_mesh_at_q(
        map_triplets,
        map_q,
        grid_address,
        fixed_grid_number,
        np.array(mesh, dtype='int_'),
        is_time_reversal * 1,
        np.array(rotations, dtype='int_', order='C'),
        swappable * 1)

    return map_triplets, map_q, grid_address


def _get_BZ_triplets_at_q(grid_point,
                          bz_grid,
                          map_triplets,
                          mesh):
    """Grid point triplets are searched considering BZ surface.

    Looking for q+q'+q''=G with smallest |G|. In this condition,
    a pair in (q, q', q'') can be translationally equivalent points.
    This is treated an auxiliary grid system (bz_grid).

    Parameters
    ----------
    grid_number : int
        Grid point of q0
    bz_grid : BZGrid
        Data structure to represent BZ grid.
    map_triplets : ndarray or None
        Mapping table of all triplets to symmetrically
        independent tripelts. More precisely, this gives a list of
        index mapping from all q-points to independent q' of
        q+q'+q''=G. Considering q' is enough because q is fixed and
        q''=G-q-q' where G is automatically determined to choose
        smallest |G| without considering BZ surface (see docstring of
        _get_BZ_triplets_at_q.)
        shape=(prod(mesh),), dtype='int_'
    mesh : array_like
        Mesh numbers
        dtype='int_'
        shape=(3,)

    Returns
    -------
    triplets : ndarray
        Symmetry reduced number of triplets are stored as grid point
        integer numbers.
        shape=(n_triplets, 3), dtype='int_'
    ir_weights : ndarray
        Weights of triplets at a fixed q0.
        shape=(n_triplets,), dtype='int_'

    """

    import phono3py._phono3py as phono3c

    weights = np.zeros(len(map_triplets), dtype='int_')
    for g in map_triplets:
        weights[g] += 1
    ir_weights = np.extract(weights > 0, weights)
    triplets = -np.ones((len(ir_weights), 3), dtype='int_')
    num_ir_ret = phono3c.BZ_triplets_at_q(
        triplets,
        grid_point,
        bz_grid.addresses,
        bz_grid.gp_map,
        map_triplets,
        np.array(mesh, dtype='int_'),
        bz_grid.is_dense_gp_map * 1 + 1)

    assert num_ir_ret == len(ir_weights)

    return triplets, np.array(ir_weights, dtype='int_')


def _set_triplets_integration_weights_c(g,
                                        g_zero,
                                        pp,
                                        frequency_points,
                                        neighboring_phonons=False):
    import phono3py._phono3py as phono3c

    reciprocal_lattice = np.linalg.inv(pp.primitive.cell)
    mesh = pp.mesh_numbers
    thm = TetrahedronMethod(reciprocal_lattice, mesh=mesh)
    triplets_at_q = pp.get_triplets_at_q()[0]

    if neighboring_phonons:
        unique_vertices = thm.get_unique_tetrahedra_vertices()
        for i, j in zip((1, 2), (1, -1)):
            neighboring_grid_points = np.zeros(
                len(unique_vertices) * len(triplets_at_q), dtype='int_')
            phono3c.neighboring_grid_points(
                neighboring_grid_points,
                np.array(triplets_at_q[:, i], dtype='int_').ravel(),
                np.array(j * unique_vertices, dtype='int_', order='C'),
                mesh,
                pp.bz_grid.addresses,
                pp.bz_grid.gp_map)
            pp.run_phonon_solver(
                np.array(np.unique(neighboring_grid_points), dtype='int_'))

    frequencies = pp.get_phonons()[0]
    phono3c.triplets_integration_weights(
        g,
        g_zero,
        frequency_points,  # f0
        thm.get_tetrahedra(),
        mesh,
        triplets_at_q,
        frequencies,  # f1
        frequencies,  # f2
        pp.bz_grid.addresses,
        pp.bz_grid.gp_map,
        g.shape[0])


def _set_triplets_integration_weights_py(g, pp, frequency_points):
    reciprocal_lattice = np.linalg.inv(pp.primitive.cell)
    mesh = pp.mesh_numbers
    thm = TetrahedronMethod(reciprocal_lattice, mesh=mesh)
    triplets_at_q = pp.get_triplets_at_q()[0]
    tetrahedra_vertices = get_tetrahedra_vertices(
        thm.get_tetrahedra(),
        mesh,
        triplets_at_q,
        pp.bz_grid)
    pp.run_phonon_solver(
        np.array(np.unique(tetrahedra_vertices), dtype='int_'))
    frequencies = pp.get_phonons()[0]
    num_band = frequencies.shape[1]
    for i, vertices in enumerate(tetrahedra_vertices):
        for j, k in list(np.ndindex((num_band, num_band))):
            f1_v = frequencies[vertices[0], j]
            f2_v = frequencies[vertices[1], k]
            thm.set_tetrahedra_omegas(f1_v + f2_v)
            thm.run(frequency_points)
            g0 = thm.get_integration_weight()
            g[0, i, :, j, k] = g0
            thm.set_tetrahedra_omegas(-f1_v + f2_v)
            thm.run(frequency_points)
            g1 = thm.get_integration_weight()
            thm.set_tetrahedra_omegas(f1_v - f2_v)
            thm.run(frequency_points)
            g2 = thm.get_integration_weight()
            g[1, i, :, j, k] = g1 - g2
            if len(g) == 3:
                g[2, i, :, j, k] = g0 + g1 + g2
