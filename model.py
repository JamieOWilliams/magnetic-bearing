from python_femm import Model
import numpy as np

from materials import Somaloy


class MyModel(Model):

    def pre(self, **kwargs):
        self.session.new_document(0)
        self.session.set_current_directory('C:/Users/mail/magnetic-bearing/temp')

        # Define the problem.
        self.session.pre.problem_definition(
            frequency=0,
            units='millimeters',
            problem_type='planar',
            precision=1e-8,
            depth=20,
        )

        # Define/get materials.
        self.session.pre.get_material('Air')
        self.session.pre.add_material_class(Somaloy)
        self.session.pre.get_material('1mm')

        # Define dimensions.
        center = [0, 0]
        poles = 8
        air_gap = 0.75
        pole_length = 23.7
        pole_width = kwargs.get('pole_width') or 12
        stator_radius = 60
        stator_inner_radius = 50
        stator_width = 10
        rotor_radius = 25
        rotor_bore = 15
        rotor_center = kwargs.get('rotor_center') or [center[0], center[1]]
        coil_width = 5
        coil_length = 15
        coil_gap = 0.25
        tooth_inner_radius = rotor_radius + air_gap
        tooth_outer_radius = tooth_inner_radius + 2.5
        pole_angle = np.arcsin(pole_width / (2 * tooth_inner_radius)) * (360 / np.pi)
        tooth_protrusion = 5
        stator_angle = 45 - (np.arcsin(pole_width / (2 * stator_inner_radius)) * (360 / np.pi))

        # Set the air regions.
        self.session.pre.add_block_label(points=[[center[0], center[1] + stator_radius + 3]])
        self.session.pre.select_label(points=[[center[0], center[1] + stator_radius + 3]])
        self.session.pre.set_block_prop(block_name='Air', group=1)
        self.session.pre.clear_selected()

        self.session.pre.add_block_label(points=[center])
        self.session.pre.select_label(points=[center])
        self.session.pre.set_block_prop(block_name='Air', group=1)
        self.session.pre.clear_selected()

        self.session.pre.add_block_label(points=[[-16.5, 42.5]])
        self.session.pre.select_label(points=[[-16.5, 42.5]])
        self.session.pre.set_block_prop(block_name='Air', group=1)
        self.session.pre.clear_selected()

        def transform(r, theta):
            return [r * np.cos(theta), r * np.sin(theta)]

        # Draw the stator.
        stator_points = [
            [
                transform(stator_inner_radius, (np.pi / 2) + np.arcsin(pole_width / (2 * stator_inner_radius)))[0] - 2,
                transform(stator_inner_radius, (np.pi / 2) + np.arcsin(pole_width / (2 * stator_inner_radius)))[1],
            ],
            transform(stator_inner_radius, (np.pi / 2) + np.arcsin(pole_width / (2 * stator_inner_radius))),
            transform(tooth_outer_radius, (np.pi / 2) + np.arcsin(pole_width / (2 * tooth_outer_radius))),
            transform(tooth_outer_radius, (np.pi / 2) + np.arcsin((pole_width + tooth_protrusion) / (2 * tooth_outer_radius))),
            transform(tooth_inner_radius, (np.pi / 2) + np.arcsin((pole_width + tooth_protrusion) / (2 * tooth_inner_radius))),
            transform(tooth_inner_radius, (np.pi / 2) + np.arcsin(pole_width / (2 * tooth_inner_radius))),
            transform(tooth_inner_radius, (np.pi / 2) - np.arcsin(pole_width / (2 * tooth_inner_radius))),
            transform(tooth_inner_radius, (np.pi / 2) - np.arcsin((pole_width + tooth_protrusion) / (2 * tooth_inner_radius))),
            transform(tooth_outer_radius, (np.pi / 2) - np.arcsin((pole_width + tooth_protrusion) / (2 * tooth_outer_radius))),
            transform(tooth_outer_radius, (np.pi / 2) - np.arcsin(pole_width / (2 * tooth_outer_radius))),
            transform(stator_inner_radius, (np.pi / 2) - np.arcsin(pole_width / (2 * stator_inner_radius))),
            [
                transform(stator_inner_radius, (np.pi / 2) - np.arcsin(pole_width / (2 * stator_inner_radius)))[0] + 2,
                transform(stator_inner_radius, (np.pi / 2) - np.arcsin(pole_width / (2 * stator_inner_radius)))[1],
            ],
        ]
        self.session.pre.draw_circle(points=[center], radius=stator_radius, max_seg=1, group=1)
        stator_pattern_points = self.session.pre.draw_pattern(commands=[
            [self.session.pre.draw_line, {
                'points': [stator_points[0], stator_points[1]],
                'group': 1,
            }],
            [self.session.pre.draw_line, {
                'points': [stator_points[1], stator_points[2]],
                'group': 1,
            }],
            [self.session.pre.draw_line, {
                'points': [stator_points[2], stator_points[3]],
                'group': 1,
            }],
            [self.session.pre.draw_arc, {
                'points': [stator_points[3], stator_points[4]],
                'angle': 180,
                'max_seg': 1,
                'group': 1,
            }],
            [self.session.pre.draw_arc, {
                'points': [stator_points[5], stator_points[4]],
                'angle': np.arcsin(2.5 / (2 * tooth_inner_radius)) * (360 / np.pi),
                'max_seg': 1,
                'group': 1,
            }],
            [self.session.pre.draw_arc, {
                'points': [stator_points[6], stator_points[5]],
                'angle': pole_angle,
                'max_seg': 1,
                'group': 1,
            }],
            [self.session.pre.draw_arc, {
                'points': [stator_points[7], stator_points[6]],
                'angle': np.arcsin(2.5 / (2 * tooth_inner_radius)) * (360 / np.pi),
                'max_seg': 1,
                'group': 1,
            }],
            [self.session.pre.draw_arc, {
                'points': [stator_points[7], stator_points[8]],
                'angle': 180,
                'max_seg': 1,
                'group': 1,
            }],
            [self.session.pre.draw_line, {
                'points': [stator_points[8], stator_points[9]],
                'group': 1,
            }],
            [self.session.pre.draw_line, {
                'points': [stator_points[9], stator_points[10]],
                'group': 1,
            }],
            [self.session.pre.draw_line, {
                'points': [stator_points[10], stator_points[11]],
                'group': 1,
            }],
            # Radii for inner corners.
            [self.session.pre.create_radius, {
                'points': [stator_points[1]],
                'radius': 1.9,
            }],
            [self.session.pre.create_radius, {
                'points': [stator_points[2]],
                'radius': 1.5,
            }],
            [self.session.pre.create_radius, {
                'points': [stator_points[::-1][2]],
                'radius': 1.5,
            }],
            [self.session.pre.create_radius, {
                'points': [stator_points[::-1][1]],
                'radius': 1.9,
            }],
        ], center=center, repeat=poles)
        self.session.pre.draw_pattern(commands=[
            [self.session.pre.draw_arc, {
                'points': [stator_pattern_points[0][0][0], stator_pattern_points[::-1][4][1][1]],
                'angle': stator_angle,
                'max_seg': 1,
                'group': 1,
            }],
        ], center=center, repeat=poles)
        self.session.pre.add_block_label(points=[[center[0], center[1] + stator_radius - 5]])
        self.session.pre.select_label(points=[[center[0], center[1] + stator_radius - 5]])
        self.session.pre.set_block_prop(
            block_name=Somaloy(),
            auto_mesh=True,
            mesh_size=1,
            in_circuit=None,
            mag_direction=0,
            group=1,
        )
        self.session.pre.clear_selected()

        # Draw the coils.
        positive_coil_points = [
            [center[0] - (pole_width / 2) - coil_gap, stator_radius - (stator_width + (pole_length / 2) + (coil_length / 2))],
            [center[0] - (pole_width / 2) - coil_gap, stator_radius - (stator_width + (pole_length / 2) - (coil_length / 2))],
            [center[0] - (pole_width / 2) - coil_width - coil_gap, stator_radius - (stator_width + (pole_length / 2) - (coil_length / 2))],
            [center[0] - (pole_width / 2) - coil_width - coil_gap, stator_radius - (stator_width + (pole_length / 2) + (coil_length / 2))],
        ]
        negative_coil_points = [
            [center[0] + (pole_width / 2) + coil_gap, stator_radius - (stator_width + (pole_length / 2) + (coil_length / 2))],
            [center[0] + (pole_width / 2) + coil_gap, stator_radius - (stator_width + (pole_length / 2) - (coil_length / 2))],
            [center[0] + (pole_width / 2) + coil_width + coil_gap, stator_radius - (stator_width + (pole_length / 2) - (coil_length / 2))],
            [center[0] + (pole_width / 2) + coil_width + coil_gap, stator_radius - (stator_width + (pole_length / 2) + (coil_length / 2))],
        ]
        coil_points = self.session.pre.draw_pattern(commands=[
            [self.session.pre.draw_polygon, {
                'points': positive_coil_points,
                'group': 1,
            }],
            [self.session.pre.draw_polygon, {
                'points': negative_coil_points,
                'group': 1,
            }],
        ], center=center, repeat=poles)
        [x1, y1] = coil_points[0][0][0]
        [x3, y3] = coil_points[0][0][2]
        coil_1_center = [
            min(x1, x3) + (abs(x1 - x3) / 2),
            min(y1, y3) + (abs(y1 - y3) / 2),
        ]
        [x1, y1] = coil_points[1][0][0]
        [x3, y3] = coil_points[1][0][2]
        coil_2_center = [
            min(x1, x3) + (abs(x1 - x3) / 2),
            min(y1, y3) + (abs(y1 - y3) / 2),
        ]
        self.session.pre.draw_pattern(commands=[
            [self.session.pre.add_block_label, {
                'points': [coil_1_center],
                'block_name': '1mm',
                'in_circuit': 'winding_{i}',
                'turns': 100,
                'group': 1,
            }],
            [self.session.pre.add_block_label, {
                'points': [coil_2_center],
                'block_name': '1mm',
                'in_circuit': 'winding_{i}',
                'turns': -100,
                'group': 1,
            }],
        ], center=center, repeat=poles)

        # Rotate the whole stator.
        # self.session.pre.select_group(group=1)
        # self.session.pre.move_rotate(points=[center], shift_angle=22.5)

        # Draw the bearing rotor.
        self.session.pre.draw_annulus(points=[rotor_center], inner_radius=rotor_bore, outer_radius=rotor_radius,
                                      max_seg=1, group=2)

        # Set the properties of the rotor.
        self.session.pre.add_block_label(points=[[center[0], center[1] + (rotor_bore + ((rotor_radius - rotor_bore) / 2))]])
        self.session.pre.select_label(points=[[center[0], center[1] + (rotor_bore + ((rotor_radius - rotor_bore) / 2))]])
        self.session.pre.set_block_prop(
            block_name=Somaloy(),
            auto_mesh=True,
            mesh_size=1,
            in_circuit=None,
            mag_direction=0,
            group=2,
        )
        self.session.pre.clear_selected()

        # Set winding currents.
        # self.session.pre.add_circuit_prop(circuit_name='winding_1', current=5, circuit_type='series')
        # for i in range(2, poles - 1):
        #     self.session.pre.add_circuit_prop(circuit_name=f'winding_{i+1}', current=0, circuit_type='series')
        # self.session.pre.add_circuit_prop(circuit_name='winding_8', current=-5, circuit_type='series')
        self.session.pre.add_circuit_prop(circuit_name='winding_1', current=5, circuit_type='series')
        self.session.pre.add_circuit_prop(circuit_name='winding_2', current=-5, circuit_type='series')
        self.session.pre.add_circuit_prop(circuit_name='winding_3', current=0, circuit_type='series')
        self.session.pre.add_circuit_prop(circuit_name='winding_4', current=0, circuit_type='series')
        self.session.pre.add_circuit_prop(circuit_name='winding_5', current=0, circuit_type='series')
        self.session.pre.add_circuit_prop(circuit_name='winding_6', current=0, circuit_type='series')
        self.session.pre.add_circuit_prop(circuit_name='winding_7', current=0, circuit_type='series')
        self.session.pre.add_circuit_prop(circuit_name='winding_8', current=0, circuit_type='series')

        # Refit the view window.
        self.session.pre.zoom_natural()

    def solve(self):
        # self.session.pre.save_as('test.fem')
        self.session.smart_mesh(True)
        self.session.pre.make_abc()
        self.session.pre.analyze()
        self.session.pre.zoom_natural()
        self.session.pre.load_solution()

    def post(self):
        # self.session.post.group_select_block(group=2)
        # force_y = self.session.post.block_integral(19) / np.cos(np.pi / 8)
        # return force_y

        properties = self.session.post.get_circuit_properties('winding_1')
        flux_linkage = properties[2]
        return flux_linkage / 5

