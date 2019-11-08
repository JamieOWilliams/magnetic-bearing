class Material:

    def __str__(self):
        return self.__class__.__name__

    mu_x = None
    mu_y = None
    h_c = None
    j = None
    c_duct = None
    lam_d = None
    phi_hmax = None
    lam_fill = None
    lam_type = None
    phi_hx = None
    phi_hy = None
    wire_diameter = None
    number_of_strands = None,
    bh_curve_data = None


class Somaloy(Material):

    mu_x = 430
    h_c = 210
    number_of_strands = 1
    c_duct = (1 / 300e-6)
    bh_curve_data = [
        [0, 0],
        [0.03, 93],
        [0.06, 165],
        [0.12, 284],
        [0.19, 399],
        [0.23, 457],
        [0.58, 1104],
        [0.77, 1594],
        [0.95, 2306],
        [1.13, 3606],
        [1.31, 6468],
        [1.49, 12904],
        [1.68, 26799],
        [1.83, 49770],
        [1.92, 74770],
        [1.98, 99770],
        [2.03, 124770],
        [2.08, 149770],
        [2.15, 189770],
        [2.21, 229770],
        [2.29, 279770],
        [2.33, 304770],
    ]
