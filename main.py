import dearpygui.dearpygui as dpg
import librosa
from timetools import allpeakonsets, tdiffer, statsvel

y1, sr1, y2, sr2, totalp = 0, 0, 0, 0, 0

dpg.create_context()

def a1call(sender, app_data):
    global y1
    global sr1

    dpg.set_value(title1, 'Archivo actual: cargando...')
    y1, sr1 = librosa.load(app_data['file_path_name'], sr=None, mono=True)
    dpg.set_value(title1, f'Archivo actual: {app_data["file_name"]}')


with dpg.file_dialog(directory_selector=False, show=False, callback=a1call, tag='a1sel', width=700 ,height=400):
    dpg.add_file_extension(".wav")

def a2call(sender, app_data):
    global y2
    global sr2

    dpg.set_value(title2, 'Archivo actual: cargando...')
    y2, sr2 = librosa.load(app_data['file_path_name'], sr=None, mono=True)
    dpg.set_value(title2, f'Archivo actual: {app_data["file_name"]}')


with dpg.file_dialog(directory_selector=False, show=False, callback=a2call, id='a2sel', width=700 ,height=400):
    dpg.add_file_extension(".wav")

def mainf():
    d = dpg.get_value(inp)
    if sr1 == sr2:
        if d > 0:
            dpg.hide_item(errtext)
            dpg.set_value(errtext, '')
            twosec = librosa.time_to_samples(2, sr=sr1)
            totalp = int(len(y1)/twosec + len(y2)/twosec)
            pinc = 1/totalp

            peaks1 = allpeakonsets(y1, pinc, progress, sr1)
            peaks2 = allpeakonsets(y2, pinc, progress, sr2)

            dpg.set_value(result, f'Resultado: {statsvel(tdiffer(peaks1, peaks2, srd=sr1), d)}')
            dpg.set_value(progress, 0)
        else:
            dpg.show_item(errtext)
            dpg.set_value(errtext, 'Error: la distancia ingresada no es válida.')
    else:
        dpg.show_item(errtext)
        dpg.set_value(errtext, f'Error: las frecuencias de muestreo de los dos archivos son distintas.\n  -Archivo 1: {sr1}Hz\n  -Archivo 2: {sr2}Hz')


with dpg.font_registry():
    default_font = dpg.add_font('./assets/Gabarito-VariableFont_wght.ttf', 20)
    big_font = dpg.add_font('./assets/Gabarito-VariableFont_wght.ttf', 25)

with dpg.window(tag='vsonido'):
    dpg.add_spacer(height=5)
    
    with dpg.group(horizontal=True, horizontal_spacing=10):
        title1s = dpg.add_text('Cargar primer archivo.')
        a1selbtn = dpg.add_button(label='Explorar', callback=lambda: dpg.show_item('a1sel'))
    title1 = dpg.add_text('Archivo actual:')
    dpg.add_spacer(height=20)

    with dpg.group(horizontal=True, horizontal_spacing=10):
        title2s = dpg.add_text('Cargar segundo archivo.')
        a2selbtn = dpg.add_button(label='Explorar', callback=lambda: dpg.show_item('a2sel'))
    title2 = dpg.add_text('Archivo actual:')
    dpg.add_spacer(height=20)

    title3s = dpg.add_text('Cargar distancia entre micrófonos (en metros):')
    inp = dpg.add_input_float()
    dpg.add_spacer(height=20)

    with dpg.group(horizontal=True, horizontal_spacing=10):
        calcbtn = dpg.add_button(label='Calcular velocidad', callback=mainf)
        errtext = dpg.add_text('', show=False)
    dpg.add_spacer(height=40)

    prog = dpg.add_text('Progreso:')
    progress = dpg.add_progress_bar()
    dpg.add_spacer(height=20)

    result = dpg.add_text('Resultado:')

    dpg.bind_font(default_font)
    dpg.bind_item_font(title1s, big_font)
    dpg.bind_item_font(title2s, big_font)
    dpg.bind_item_font(title3s, big_font)
    dpg.bind_item_font(calcbtn, big_font)
    dpg.bind_item_font(prog, big_font)
    dpg.bind_item_font(result, big_font)

with dpg.theme() as item_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 5, category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Button, (29,151,236,103), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (120,160,255,200), category=dpg.mvThemeCat_Core)

dpg.bind_item_theme(calcbtn, item_theme)

with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 5, category=dpg.mvThemeCat_Core)

dpg.bind_theme(global_theme)

dpg.create_viewport(title='Calcular velocidad del sonido', width=800, height=650)
dpg.set_viewport_small_icon('./assets/vsonido.ico')
dpg.set_viewport_large_icon('./assets/vsonido.ico')
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window('vsonido', True)
dpg.start_dearpygui()
dpg.destroy_context()
