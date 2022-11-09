from locale import setlocale, LC_ALL, format_string
from textwrap import wrap

from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QWidget, QLabel, QGroupBox, QGridLayout, QLineEdit, QPushButton
from pyperclip import copy

from utilities.PopupWindow import PopupWindow
from utilities.Validator import is_empty, is_correct_prefix, is_correct_mask, is_correct_ip_with_prefix

class IpInformation(QWidget):
    def __init__(self):
        super(IpInformation, self).__init__()


        main_layout = QGridLayout()
        self.setLayout(main_layout)

        # Prefix-mask-conversion group box
        self.prefix_mask_box = QGroupBox("Conversión de prefijo a máscara")
        self.prefix_mask_box.setMaximumHeight(90)
        main_layout.addWidget(self.prefix_mask_box, 0, 0)
        prefix_mask_box_layout = QGridLayout()
        prefix_mask_box_layout.setContentsMargins(200, 20, 200, 20)
        prefix_mask_box_layout.setHorizontalSpacing(30)
        self.prefix_mask_box.setLayout(prefix_mask_box_layout)

        self.prefix_input = QLineEdit()
        self.prefix_input.setMaxLength(3)
        self.prefix_input.setAlignment(Qt.AlignCenter)
        self.prefix_input.setPlaceholderText("Prefijo")
        prefix_mask_box_layout.addWidget(self.prefix_input, 0, 0)
        self.mask_input = QLineEdit()
        self.mask_input.setMaxLength(15)
        self.mask_input.setAlignment(Qt.AlignCenter)
        self.mask_input.setPlaceholderText("Máscara")
        prefix_mask_box_layout.addWidget(self.mask_input, 0, 1)

        self.convert_btn = QPushButton("Convertir")
        self.convert_btn.setIcon(QIcon("static/images/exchange.png"))
        self.convert_btn.clicked.connect(self.convert_action)
        self.prefix_input.returnPressed.connect(self.convert_action)
        self.mask_input.returnPressed.connect(self.convert_action)
        prefix_mask_box_layout.addWidget(self.convert_btn, 0, 2, alignment=Qt.AlignLeft)

        # IP information group box
        self.ip_information_box = QGroupBox("Información IP")
        main_layout.addWidget(self.ip_information_box, 1, 0)
        ip_information_box_layout = QGridLayout()
        ip_information_box_layout.setContentsMargins(80, 80, 80, 80)
        ip_information_box_layout.setHorizontalSpacing(30)
        ip_information_box_layout.setVerticalSpacing(15)
        self.ip_information_box.setLayout(ip_information_box_layout)

        self.ip_address_label = QLabel("Dirección IP con prefijo:")
        ip_information_box_layout.addWidget(self.ip_address_label, 0, 0, alignment=Qt.AlignCenter)
        self.ip_address_textfield = QLineEdit()
        self.ip_address_textfield.setPlaceholderText("192.168.1.100/24")
        self.ip_address_textfield.setAlignment(Qt.AlignCenter)
        self.ip_address_textfield.setMaxLength(18)
        ip_information_box_layout.addWidget(self.ip_address_textfield, 0, 1)

        self.get_info_btn = QPushButton("Obtener información")
        self.get_info_btn.setIcon(QIcon("static/images/get_info.png"))
        self.get_info_btn.clicked.connect(self.get_info_action)
        self.ip_address_textfield.returnPressed.connect(self.get_info_action)
        ip_information_box_layout.addWidget(self.get_info_btn, 0, 2)

        self.ip_class_label = QLabel("Clase IP:")
        ip_information_box_layout.addWidget(self.ip_class_label, 1, 0, alignment=Qt.AlignCenter)
        self.ip_class_textfield = QLineEdit()
        self.ip_class_textfield.setReadOnly(True)
        self.ip_class_textfield.setAlignment(Qt.AlignCenter)
        ip_information_box_layout.addWidget(self.ip_class_textfield, 1, 1)
        self.ip_class_copy_btn = QPushButton("Copiar")
        self.ip_class_copy_btn.setIcon(QIcon("static/images/copy_clipboard.png"))
        self.ip_class_copy_btn.clicked.connect(lambda: copy_action(self.ip_class_textfield.text()))
        ip_information_box_layout.addWidget(self.ip_class_copy_btn, 1, 2)

        self.ip_type_label = QLabel("Tipo de IP:")
        ip_information_box_layout.addWidget(self.ip_type_label, 2, 0, alignment=Qt.AlignCenter)
        self.ip_type_textfield = QLineEdit()
        self.ip_type_textfield.setReadOnly(True)
        self.ip_type_textfield.setAlignment(Qt.AlignCenter)
        ip_information_box_layout.addWidget(self.ip_type_textfield, 2, 1)
        self.ip_type_copy_btn = QPushButton("Copiar")
        self.ip_type_copy_btn.setIcon(QIcon("static/images/copy_clipboard.png"))
        self.ip_type_copy_btn.clicked.connect(lambda: copy_action(self.ip_type_textfield.text()))
        ip_information_box_layout.addWidget(self.ip_type_copy_btn, 2, 2)

        self.network_address_label = QLabel("Dirección de red:")
        ip_information_box_layout.addWidget(self.network_address_label, 3, 0, alignment=Qt.AlignCenter)
        self.network_address_textfield = QLineEdit()
        self.network_address_textfield.setReadOnly(True)
        self.network_address_textfield.setAlignment(Qt.AlignCenter)
        ip_information_box_layout.addWidget(self.network_address_textfield, 3, 1)
        self.network_address_copy_btn = QPushButton("Copiar")
        self.network_address_copy_btn.setIcon(QIcon("static/images/copy_clipboard.png"))
        self.network_address_copy_btn.clicked.connect(lambda: copy_action(self.network_address_textfield.text()))
        ip_information_box_layout.addWidget(self.network_address_copy_btn, 3, 2)

        self.subnet_mask_label = QLabel("Máscara de subred:")
        ip_information_box_layout.addWidget(self.subnet_mask_label, 4, 0, alignment=Qt.AlignCenter)
        self.subnet_mask_textfield = QLineEdit()
        self.subnet_mask_textfield.setReadOnly(True)
        self.subnet_mask_textfield.setAlignment(Qt.AlignCenter)
        ip_information_box_layout.addWidget(self.subnet_mask_textfield, 4, 1)
        self.subnet_mask_copy_btn = QPushButton("Copiar")
        self.subnet_mask_copy_btn.setIcon(QIcon("static/images/copy_clipboard.png"))
        self.subnet_mask_copy_btn.clicked.connect(lambda: copy_action(self.subnet_mask_textfield.text()))
        ip_information_box_layout.addWidget(self.subnet_mask_copy_btn, 4, 2)

        self.first_addressable_ip_label = QLabel("Primera IP utilizable:")
        ip_information_box_layout.addWidget(self.first_addressable_ip_label, 5, 0, alignment=Qt.AlignCenter)
        self.first_addressable_ip_textfield = QLineEdit()
        self.first_addressable_ip_textfield.setReadOnly(True)
        self.first_addressable_ip_textfield.setAlignment(Qt.AlignCenter)
        ip_information_box_layout.addWidget(self.first_addressable_ip_textfield, 5, 1)
        self.first_addressable_ip_copy_btn = QPushButton("Copiar")
        self.first_addressable_ip_copy_btn.setIcon(QIcon("static/images/copy_clipboard.png"))
        self.first_addressable_ip_copy_btn.clicked.connect(lambda: copy_action(self.first_addressable_ip_textfield.text()))
        ip_information_box_layout.addWidget(self.first_addressable_ip_copy_btn, 5, 2)

        self.last_addressable_ip_label = QLabel("Última IP utilizable:")
        ip_information_box_layout.addWidget(self.last_addressable_ip_label, 6, 0, alignment=Qt.AlignCenter)
        self.last_addressable_ip_textfield = QLineEdit()
        self.last_addressable_ip_textfield.setReadOnly(True)
        self.last_addressable_ip_textfield.setAlignment(Qt.AlignCenter)
        ip_information_box_layout.addWidget(self.last_addressable_ip_textfield, 6, 1)
        self.last_addressable_ip_copy_btn = QPushButton("Copiar")
        self.last_addressable_ip_copy_btn.setIcon(QIcon("static/images/copy_clipboard.png"))
        self.last_addressable_ip_copy_btn.clicked.connect(lambda: copy_action(self.last_addressable_ip_textfield.text()))
        ip_information_box_layout.addWidget(self.last_addressable_ip_copy_btn, 6, 2)

        self.broadcast_address_label = QLabel("IP de broadcast:")
        ip_information_box_layout.addWidget(self.broadcast_address_label, 7, 0, alignment=Qt.AlignCenter)
        self.broadcast_address_textfield = QLineEdit()
        self.broadcast_address_textfield.setReadOnly(True)
        self.broadcast_address_textfield.setAlignment(Qt.AlignCenter)
        ip_information_box_layout.addWidget(self.broadcast_address_textfield, 7, 1)
        self.broadcast_address_copy_btn = QPushButton("Copiar")
        self.broadcast_address_copy_btn.setIcon(QIcon("static/images/copy_clipboard.png"))
        self.broadcast_address_copy_btn.clicked.connect(lambda: copy_action(self.broadcast_address_textfield.text()))
        ip_information_box_layout.addWidget(self.broadcast_address_copy_btn, 7, 2)

        self.next_network_address_label = QLabel("Siguiente dirección de red:")
        ip_information_box_layout.addWidget(self.next_network_address_label, 8, 0, alignment=Qt.AlignCenter)
        self.next_network_address_textfield = QLineEdit()
        self.next_network_address_textfield.setReadOnly(True)
        self.next_network_address_textfield.setAlignment(Qt.AlignCenter)
        ip_information_box_layout.addWidget(self.next_network_address_textfield, 8, 1)
        self.next_network_address_copy_btn = QPushButton("Copiar")
        self.next_network_address_copy_btn.setIcon(QIcon("static/images/copy_clipboard.png"))
        self.next_network_address_copy_btn.clicked.connect(lambda: copy_action(self.next_network_address_textfield.text()))
        ip_information_box_layout.addWidget(self.next_network_address_copy_btn, 8, 2)

        self.max_endpoint_label = QLabel("Máxima cantidad de hosts:")
        ip_information_box_layout.addWidget(self.max_endpoint_label, 9, 0, alignment=Qt.AlignCenter)
        self.max_endpoint_textfield = QLineEdit()
        self.max_endpoint_textfield.setReadOnly(True)
        self.max_endpoint_textfield.setAlignment(Qt.AlignCenter)
        ip_information_box_layout.addWidget(self.max_endpoint_textfield, 9, 1)
        self.max_endpoint_copy_btn = QPushButton("Copiar")
        self.max_endpoint_copy_btn.setIcon(QIcon("static/images/copy_clipboard.png"))
        self.max_endpoint_copy_btn.clicked.connect(lambda: copy_action(self.max_endpoint_textfield.text()))
        ip_information_box_layout.addWidget(self.max_endpoint_copy_btn, 9, 2)

    def convert_action(self):
        if is_empty(self.prefix_input.text()) and \
                is_empty(self.mask_input.text()):
            PopupWindow("warning",
                        "El pefijo y la máscara no pueden estar vacíos (ambos)",
                        self.prefix_input)
        elif not is_empty(self.prefix_input.text()) and \
                not is_empty(self.mask_input.text()):
            if is_correct_prefix(self.prefix_input.text()):
                prefix_corrected = self.prefix_input.text().replace("/", "").replace("\\", "")
                self.mask_input.setText(get_mask_from_prefix(prefix_corrected))
            else:
                PopupWindow("warning",
                            "Prefijo inválido",
                            self.prefix_input)
        else:
            if self.prefix_input.text():
                if is_correct_prefix(self.prefix_input.text()):
                    prefix_corrected = self.prefix_input.text().replace("/", "").replace("\\", "")
                    self.mask_input.setText(get_mask_from_prefix(prefix_corrected))
                else:
                    PopupWindow("warning",
                                "Prefijo inválido",
                                self.prefix_input)
            else:
                if is_correct_mask(self.mask_input.text()):
                    self.prefix_input.setText(f"/{get_prefix_from_mask(self.mask_input.text())}")
                else:
                    PopupWindow("warning",
                                "Máscara inválida",
                                self.mask_input)

    def get_info_action(self):
        if is_empty(self.ip_address_textfield.text()):
            PopupWindow("warning",
                        "La dirección IP/prefijo no puede estar vació ",
                        self.ip_address_textfield)
        elif is_correct_ip_with_prefix(self.ip_address_textfield.text()):
            ip = self.ip_address_textfield.text().split("/")[0]
            ip_first_octet = int(str(ip).split(".")[0])
            prefix = self.ip_address_textfield.text().split("/")[1]

            if ip_first_octet == 127:
                PopupWindow("warning",
                            "La dirección IP que ingresaste es de loopback",
                            self.ip_address_textfield)
            elif 224 <= ip_first_octet <= 239:
                PopupWindow("warning",
                            "La dirección IP que ingresaste es de multicast",
                            self.ip_address_textfield)
            elif 240 <= ip_first_octet <= 254:
                PopupWindow("warning",
                            "La dirección IP que ingresaste es de investigación",
                            self.ip_address_textfield)
            elif ip_first_octet == 255:
                PopupWindow("warning",
                            "La dirección IP que ingresaste está reservada para máscaras de subred",
                            self.ip_address_textfield)
            else:
                self.ip_class_textfield.setText(get_ip_class(ip))
                self.ip_type_textfield.setText(get_ip_type(ip, prefix))
                self.network_address_textfield.setText(get_network_address(ip, prefix))
                self.subnet_mask_textfield.setText(get_mask_from_prefix(prefix))
                self.first_addressable_ip_textfield.setText(get_first_addressable_ip(ip, prefix))
                self.last_addressable_ip_textfield.setText(get_last_addressable_ip(ip, prefix))
                self.broadcast_address_textfield.setText(get_broadcast_ip(ip, prefix))
                self.next_network_address_textfield.setText(get_next_network_ip(ip, prefix))
                self.max_endpoint_textfield.setText(get_max_endpoint_formatted(prefix))
        else:
            PopupWindow("warning",
                        "Dirección IP/Prefijo inválido",
                        self.ip_address_textfield)



def copy_action(input_field_text):
    if input_field_text:
        copy(input_field_text)


def get_32bit_format(ip_address):
    format_32bit = ""
    for octet in ip_address.split("."):
        format_32bit += f'{bin(int(octet)).replace("0b", "").rjust(8, "0")}'
    return format_32bit


def get_ip_from_32bit_format(format_32bit):
    ip_dec = ""
    for octet in wrap(format_32bit, 8):
        ip_dec += f"{int(octet, 2)}."
    return ip_dec[:-1]


def get_mask_from_prefix(prefix):
    mask_decimal = ""
    for octet in wrap((int(prefix) * "1").ljust(32, "0"), 8):
        mask_decimal += f"{int(octet, 2)}."
    return mask_decimal[:-1]


def get_prefix_from_mask(mask):
    mask_bin_32bit = ""
    for octet in mask.split("."):
        mask_bin_32bit += bin(int(octet)).replace("0b", "").rjust(8, "0")
    return mask_bin_32bit.count("1")


def get_ip_class(ip_address):
    first_octet = int(str(ip_address).split(".")[0])
    second_octet = int(str(ip_address).split(".")[1])

    if 0 <= first_octet <= 127:
        if first_octet == 10:
            return "Clase A, privada"
        else:
            return "Clase A, pública"
    elif 128 <= first_octet <= 191:
        if (first_octet == 172 and 16 <= second_octet <= 31) or (first_octet == 169 and second_octet == 254):
            return "Clase B, privada"
        else:
            return "Clase B, pública"
    elif 192 <= first_octet <= 223:
        if first_octet == 192 and second_octet == 168:
            return "Clase C, privada"
        else:
            return "Clase C, pública"


def get_ip_type(ip_address, prefix):
    if ip_address == get_network_address(ip_address, prefix):
        return "Dirección de red"
    elif ip_address == get_broadcast_ip(ip_address, prefix):
        return "Dirección de broadcast"
    return "Dirección de host"


def get_network_address(ip_address, prefix):
    mask_32bit = get_32bit_format(get_mask_from_prefix(prefix))
    ip_address_32bit = get_32bit_format(ip_address)
    network_address_32bit = f"{ip_address_32bit[:-mask_32bit.count('0')]}{'0' * mask_32bit.count('0')}"
    return get_ip_from_32bit_format(network_address_32bit)


def get_first_addressable_ip(ip_address, prefix):
    network_address_32bit = get_32bit_format(get_network_address(ip_address, prefix))
    network_address_increased = bin(int(network_address_32bit, 2) + int("1", 2)).replace("0b", "").rjust(32, "0")
    return get_ip_from_32bit_format(network_address_increased)


def get_last_addressable_ip(ip_address, prefix):
    network_address_32bit = get_32bit_format(get_network_address(ip_address, prefix))
    max_endpoint_bin = int(bin(int(get_max_endpoint(prefix))).replace("0b", ""), 2)
    last_addressable_ip_32bit = bin(int(network_address_32bit, 2) + max_endpoint_bin).replace("0b", "").rjust(32, "0")
    return get_ip_from_32bit_format(last_addressable_ip_32bit)


def get_broadcast_ip(ip_address, prefix):
    last_addressable_ip_32bit = get_32bit_format(get_last_addressable_ip(ip_address, prefix))
    broadcast_ip_32bit = bin(int(last_addressable_ip_32bit, 2) + int("1", 2)).replace("0b", "").rjust(32, "0")
    return get_ip_from_32bit_format(broadcast_ip_32bit)


def get_next_network_ip(ip_address, prefix):
    broadcast_ip_32bit = get_32bit_format(get_broadcast_ip(ip_address, prefix))
    if broadcast_ip_32bit == "11011111111111111111111111111111" or \
            broadcast_ip_32bit == "01111110111111111111111111111111":
        return "-"
    else:
        next_network_ip_32bit = bin(int(broadcast_ip_32bit, 2) + int("1", 2)).replace("0b", "").rjust(32, "0")
        return get_ip_from_32bit_format(next_network_ip_32bit)


def get_max_endpoint(prefix):
    hostbits = 32 - int(prefix)
    hosts_bin = ("1" * hostbits).rjust(32, "0")
    return str(int(hosts_bin, 2) - 1)


def get_max_endpoint_formatted(prefix):
    max_endpoint = str(get_max_endpoint(prefix)).format("{0:n}", get_max_endpoint(prefix))
    setlocale(LC_ALL, "")
    return format_string("%d", int(max_endpoint), grouping=True)
