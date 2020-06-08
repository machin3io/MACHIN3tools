axis_items = [('X', 'X', ''),
              ('Y', 'Y', ''),
              ('Z', 'Z', '')]

uv_axis_items = [('U', 'U', ''),
                 ('V', 'V', '')]


# OPERATORS

focus_method_items = [('VIEW_SELECTED', 'View Selected', ''),
                      ('LOCAL_VIEW', 'Local View', '')]

focus_levels_items = [('SINGLE', 'Single', ''),
                      ('MULTIPLE', 'Multiple', '')]

align_mode_items = [('VIEW', 'View', ''),
                    ('AXES', 'Axes', '')]

align_type_items = [('MIN', 'Min', ''),
                    ('MAX', 'Max', ''),
                    ('MINMAX', 'Min/Max', ''),
                    ('ZERO', 'Zero', ''),
                    ('AVERAGE', 'Average', ''),
                    ('CURSOR', 'Cursor', '')]

align_direction_items = [('LEFT', 'Left', ''),
                         ('RIGHT', 'Right', ''),
                         ('TOP', 'Top', ''),
                         ('BOTTOM', 'Bottom', ''),
                         ('HORIZONTAL', 'Horizontal', ''),
                         ('VERTICAL', 'Vertical', '')]

align_axis_mapping_dict = {'X': 0, 'Y': 1, 'Z': 2}

uv_align_axis_mapping_dict = {'U': 0, 'V': 1}


# PIES

eevee_preset_items = [('NONE', 'None', ''),
                      ('LOW', 'Low', 'Use Scene Lights, Ambient Occlusion and Screen Space Reflections'),
                      ('HIGH', 'High', 'Use Bloom and Screen Space Refractions'),
                      ('ULTRA', 'Ultra', 'Use Scene World and Volumetrics.\nCreate Principled Volume node if necessary')]

render_engine_items = [('BLENDER_EEVEE', 'Eevee', ''),
                       ('CYCLES', 'Cycles', '')]

cycles_device_items = [('CPU', 'CPU', ''),
                       ('GPU', 'GPU', '')]
