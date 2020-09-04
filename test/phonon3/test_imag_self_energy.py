import numpy as np

gammas = [
    0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000,
    0.0005412, 0.0005412, 0.0008843, 0.0191694, 0.0206316, 0.0206316,
    0.0019424, 0.0019424, 0.0067566, 0.0548967, 0.0506115, 0.0506115,
    0.0062204, 0.0062204, 0.0088148, 0.0426150, 0.0417223, 0.0417223,
    0.0016263, 0.0016263, 0.0017293, 0.0279509, 0.0289259, 0.0289259,
    0.0097926, 0.0097926, 0.0170092, 0.0438828, 0.0523105, 0.0523105,
    0.0035542, 0.0035542, 0.0135109, 0.0623533, 0.0343746, 0.0343746,
    0.0073140, 0.0073140, 0.0289659, 0.5006760, 0.5077932, 0.5077932,
    0.0016144, 0.0016144, 0.0126326, 0.2731933, 0.2791702, 0.2791702,
    0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000,
    0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000,
    0.0023304, 0.0026469, 0.0052513, 0.0209641, 0.0220092, 0.0234752,
    0.0035532, 0.0038158, 0.0087882, 0.0276654, 0.0315055, 0.0286975,
    0.0345193, 0.0277533, 0.0495734, 0.0511798, 0.0465938, 0.0436605,
    0.0071705, 0.0081615, 0.0139063, 0.0204058, 0.0307320, 0.0237855,
    0.0202095, 0.0197716, 0.0316074, 0.0402461, 0.0438103, 0.0394924,
    0.0171448, 0.0176446, 0.0567310, 0.0930479, 0.0570520, 0.0622142,
    0.0292639, 0.0328821, 0.0667957, 0.2541887, 0.4592188, 0.4234131,
    0.0104887, 0.0179753, 0.0827533, 0.2659557, 0.3242633, 0.3189804,
    0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000]
gammas_class1 = [
    0.00000000, 0.00000000, 0.00000000, -0.00000000, 0.00000000, 0.00000000,
    0.00053387, 0.00053387, 0.00086230, 0.01894313, 0.02034210, 0.02034210,
    0.00155506, 0.00155506, 0.00260125, 0.01821681, 0.01820381, 0.01820381,
    0.00571765, 0.00571765, 0.00544460, 0.01325570, 0.01118428, 0.01118428,
    0.00016153, 0.00016153, 0.00032679, 0.00020002, 0.00020927, 0.00020927,
    0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000,
    0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000,
    0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000,
    0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000,
    0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000,
    0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000,
    0.00233036, 0.00264690, 0.00525130, 0.02096414, 0.02200915, 0.02347515,
    0.00297698, 0.00348529, 0.00638118, 0.01776255, 0.02740917, 0.02217207,
    0.03234423, 0.02580162, 0.03682891, 0.03904463, 0.01942315, 0.02072384,
    0.00004097, 0.00005101, 0.00007457, 0.00003508, 0.00004210, 0.00003803,
    0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000,
    0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000,
    0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000,
    0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000,
    0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000]
gammas_class2 = [
    0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000,
    0.00000728, 0.00000728, 0.00002201, 0.00022624, 0.00028946, 0.00028946,
    0.00038736, 0.00038736, 0.00415534, 0.03667993, 0.03240766, 0.03240766,
    0.00050274, 0.00050274, 0.00337024, 0.02935928, 0.03053801, 0.03053801,
    0.00146473, 0.00146473, 0.00140248, 0.02775086, 0.02871662, 0.02871662,
    0.00979262, 0.00979262, 0.01700920, 0.04388280, 0.05231049, 0.05231049,
    0.00355424, 0.00355424, 0.01351094, 0.06235333, 0.03437465, 0.03437465,
    0.00731397, 0.00731397, 0.02896588, 0.50067605, 0.50779324, 0.50779324,
    0.00161440, 0.00161440, 0.01263256, 0.27319333, 0.27917018, 0.27917018,
    0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000,
    0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000,
    0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000,
    0.00057618, 0.00033051, 0.00240702, 0.00990280, 0.00409632, 0.00652547,
    0.00217505, 0.00195163, 0.01274449, 0.01213516, 0.02717067, 0.02293662,
    0.00712953, 0.00811051, 0.01383178, 0.02037067, 0.03068992, 0.02374747,
    0.02020952, 0.01977157, 0.03160744, 0.04024612, 0.04381027, 0.03949241,
    0.01714475, 0.01764459, 0.05673104, 0.09304789, 0.05705200, 0.06221421,
    0.02926385, 0.03288210, 0.06679574, 0.25418868, 0.45921877, 0.42341309,
    0.01048868, 0.01797532, 0.08275328, 0.26595568, 0.32426329, 0.31898043,
    0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000]
freq_points = [0., 3.41024688, 6.82049376, 10.23074063, 13.64098751,
               17.05123439, 20.46148127, 23.87172814, 27.28197502, 30.6922219]
detailed_gamma = [0.00000000, 0.00653193, 0.02492913, 0.01682092, 0.01001680,
                  0.02181888, 0.01858641, 0.16208762, 0.09598706, 0.00000000]


def test_imag_self_energy_npoints(si_pbesol):
    si_pbesol.mesh_numbers = [9, 9, 9]
    si_pbesol.init_phph_interaction()
    si_pbesol.run_imag_self_energy(
        [1, 103],
        temperatures=[300, ],
        num_frequency_points=10)
    print(np.array(si_pbesol.gammas).shape)
    np.testing.assert_allclose(
        gammas, si_pbesol.gammas.ravel(), atol=1e-2)
    np.testing.assert_allclose(
        freq_points, si_pbesol.frequency_points.ravel(),
        atol=1e-5)


def test_imag_self_energy_freq_points(si_pbesol):
    si_pbesol.mesh_numbers = [9, 9, 9]
    si_pbesol.init_phph_interaction()
    si_pbesol.run_imag_self_energy(
        [1, 103],
        temperatures=[300, ],
        frequency_points=freq_points)
    np.testing.assert_allclose(
        gammas, si_pbesol.gammas.ravel(), atol=1e-2)
    np.testing.assert_allclose(
        freq_points, si_pbesol.frequency_points.ravel(), atol=1e-5)


def test_imag_self_energy_detailed(si_pbesol):
    si_pbesol.mesh_numbers = [9, 9, 9]
    si_pbesol.init_phph_interaction()
    si_pbesol.run_imag_self_energy(
        [1, ],
        temperatures=[300, ],
        frequency_points=freq_points,
        keep_gamma_detail=True)
    np.testing.assert_allclose(
        detailed_gamma,
        si_pbesol.detailed_gammas[0][0, 0].sum(axis=(1, 2, 3, 4)),
        atol=1e-2)


def test_imag_self_energy_scat_class1(si_pbesol):
    si_pbesol.mesh_numbers = [9, 9, 9]
    si_pbesol.init_phph_interaction()
    si_pbesol.run_imag_self_energy(
        [1, 103],
        temperatures=[300, ],
        frequency_points=freq_points,
        scattering_event_class=1)
    # for line in si_pbesol.gammas.reshape(-1, 6):
    #     print(("%10.8f, " * 6) % tuple(line))
    np.testing.assert_allclose(
        gammas_class1, np.array(si_pbesol.gammas).ravel(), atol=1e-2)


def test_imag_self_energy_scat_class2(si_pbesol):
    si_pbesol.mesh_numbers = [9, 9, 9]
    si_pbesol.init_phph_interaction()
    si_pbesol.run_imag_self_energy(
        [1, 103],
        temperatures=[300, ],
        frequency_points=freq_points,
        scattering_event_class=2)
    # for line in si_pbesol.gammas.reshape(-1, 6):
    #     print(("%10.8f, " * 6) % tuple(line))
    np.testing.assert_allclose(
        gammas_class2, np.array(si_pbesol.gammas).ravel(), atol=1e-2)
