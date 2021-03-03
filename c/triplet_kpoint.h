/* Copyright (C) 2015 Atsushi Togo */
/* All rights reserved. */

/* These codes were originally parts of spglib, but only develped */
/* and used for phono3py. Therefore these were moved from spglib to */
/* phono3py. This file is part of phonopy. */

/* Redistribution and use in source and binary forms, with or without */
/* modification, are permitted provided that the following conditions */
/* are met: */

/* * Redistributions of source code must retain the above copyright */
/*   notice, this list of conditions and the following disclaimer. */

/* * Redistributions in binary form must reproduce the above copyright */
/*   notice, this list of conditions and the following disclaimer in */
/*   the documentation and/or other materials provided with the */
/*   distribution. */

/* * Neither the name of the phonopy project nor the names of its */
/*   contributors may be used to endorse or promote products derived */
/*   from this software without specific prior written permission. */

/* THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS */
/* "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT */
/* LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS */
/* FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE */
/* COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, */
/* INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, */
/* BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; */
/* LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER */
/* CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT */
/* LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN */
/* ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE */
/* POSSIBILITY OF SUCH DAMAGE. */

#ifndef __triplet_kpoint_H__
#define __triplet_kpoint_H__

#include "kpoint.h"
#include "triplet.h"

long tpk_get_ir_triplets_at_q(long *map_triplets,
                              long *map_q,
                              long (*grid_address)[3],
                              const long grid_point,
                              const long mesh[3],
                              const long is_time_reversal,
                              const MatLONG * rotations,
                              const long swappable);
long tpk_get_BZ_triplets_at_q(long (*triplets)[3],
                              const long grid_point,
                              TPLCONST long (*bz_grid_address)[3],
                              const long *bz_map,
                              const long *map_triplets,
                              const long num_map_triplets,
                              const long mesh[3]);

#endif
