import sys, os
from PyQt5 import QtWidgets, QtCore
from core_files.ImageEditor import *
from ui_functions.supportWindows import *


# Menu Functions
def export_ow_image(ui):
    image = make_image_from_rom(ui.selected_ow, ui.selected_table)

    # For the Palette
    palette_id = get_ow_palette_id(root.tables_list[ui.selected_table].ow_data_ptrs[ui.selected_ow].ow_data_addr)
    palette_addr = ui.sprite_manager.get_palette_addr(palette_id)
    sprite_palette = create_palette_from_gba(ptr_to_addr(palette_addr))
    image.putpalette(sprite_palette)

    name = '/' + str(ui.selected_table) + '_' + str(ui.selected_ow)
    fn, ext = QtWidgets.QFileDialog.getSaveFileName(ui, 'Export Frames Sheet',
                                                  ui.paths['EXP_FRMS_PATH'] + name,
                                                  "PNG File (*.png);;"
                                                  "BMP File (*.bmp);;"
                                                  "JPEG File (*.jpg)")

    if not fn:
        return
    ui.paths['EXP_FRMS_PATH'] = os.path.dirname(os.path.realpath(fn))

    try:
        image.save(fn)
    except ValueError:
        fn += ext.replace(")","").split("*")[-1]
        image.save(fn)
    SHOW("Saved "+fn)

def import_frames_sheet(ui):
    dlg = QtWidgets.QFileDialog()
    image_loc, _ = dlg.getOpenFileName(dlg, 'Open Image file', ui.paths['IMP_FRMS_PATH'], "PNG Files (*.png);;"
                                                                                       "BMP Files (*.bmp)")
    if not image_loc:
        return
    ui.paths['IMP_FRMS_PATH'] = os.path.dirname(os.path.realpath(image_loc))

    sprite = Image.open(image_loc)

    # Safety measures
    ow_type = root.tables_list[ui.selected_table].ow_data_ptrs[ui.selected_ow].frames.get_type()
    width, height = get_frame_dimensions(ow_type)
    frames_num = root.tables_list[ui.selected_table].ow_data_ptrs[ui.selected_ow].frames.get_num()

    recom_width = width * frames_num

    if height != sprite.height:
        message = "The height should be " + str(height) + ", yours is " + str(sprite.height)
        message += "\nThis means that your image is of different OW Type."
        QtWidgets.QMessageBox.critical(QtWidgets.QMessageBox(), "File has wrong size", message)
    elif recom_width != sprite.width:
        message = "Your image has a different number of  frames than the OW\n"
        message += "1) Check if the type of the OW is correct.\n2) Check how many frames are in your image"
        QtWidgets.QMessageBox.critical(QtWidgets.QMessageBox(), "Different number of Frames detected", message)
    else:
        ui.tree_model.importOWFrames(sprite, ui.selected_ow, ui.selected_table, ui)
        SHOW("Imported {} for Table[{}] : OW[{}]".format(image_loc, ui.selected_table, ui.selected_ow))

def import_ow_sprsrc(ui):
    dlg = QtWidgets.QFileDialog()
    image_loc, _ = dlg.getOpenFileName(dlg, 'Open Image file', ui.paths['OW_PATH'], "PNG Files (*.png);;"
                                                                                       "BMP Files (*.bmp)")
    if not image_loc:
        return
    ui.paths['OW_PATH'] = os.path.dirname(os.path.realpath(image_loc))

    sprite = Image.open(image_loc)

    # Safety measures
    if (sprite.width != 96) or (sprite.height != 128):
        message = "The size should be 96x128, yours is " + str(sprite.width) + "x" + str(sprite.height)
        QtWidgets.QMessageBox.critical(QtWidgets.QMessageBox(), "File has wrong size", message)
    else:
        ui.tree_model.importOWSpr(sprite, ui.selected_ow, ui.selected_table, ui)
        SHOW("Imported {} for Table[{}] : OW[{}]".format(image_loc, ui.selected_table, ui.selected_ow))

def import_pokemon_sprsrc(ui):
    dlg = QtWidgets.QFileDialog()
    image_loc, _ = dlg.getOpenFileName(dlg, 'Open Image file', ui.paths['PKMN_PATH'], "PNG Files (*.png);;"
                                                                                       "BMP Files (*.bmp)")
    if not image_loc:
        return
    ui.paths['PKMN_PATH'] = os.path.dirname(os.path.realpath(image_loc))

    sprite = Image.open(image_loc)

    # Safety measures
    if (sprite.width != 64) or (sprite.height != 128):
        message = "The size should be 64x128, yours is " + str(sprite.width) + "x" + str(sprite.height)
        QtWidgets.QMessageBox.critical(QtWidgets.QMessageBox(), "File has wrong size", message)
    else:
        ui.tree_model.importPokeSpr(sprite, ui.selected_ow, ui.selected_table, ui)
        SHOW("Imported {} for Table[{}] : OW[{}]".format(image_loc, ui.selected_table, ui.selected_ow))

def palette_cleanup(ui):
    ui.tree_model.paletteCleanup(ui)

def remove_table(ui):
    ui.tree_model.removeTable(ui.selected_table, ui)

# Buttons Functions
def addOWButtonFunction(ui):

    owWindow = addOWWindow(ui)
    owWindow.exec()

def insertOWButtonFunction(ui):
    owWindow = insertOWWindow(ui)
    owWindow.exec()

def resizeOWButtonFunction(ui):
    owWindow = resizeOWWindow(ui)
    owWindow.exec()

def removeOWButtonFunction(ui):
    selectedOWs = ui.OWTreeView.selectionModel().selectedRows(0);
    for selected_ow in sorted(selectedOWs, reverse=True):
        selected_table = selected_ow.parent().row()
        if selected_table != -1:
            ui.tree_model.removeOWs(selected_ow.row(), selected_table, 1, ui)
        #ui.tree_model.removeOWs(index.selected_ow, index.selected_table, 1, ui)

def addTableButtonFunction(ui):
    addTable = addTableWindow(ui)
    addTable.exec()
