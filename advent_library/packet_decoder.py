nibble_to_bits = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111',
}


def prod(args):
    result = 1
    for x in args:
        result *= x
    return result


class PacketDecoder:

    # ------------------------------
    # Parsing
    # ------------------------------

    @staticmethod
    def __hex_to_bin(packet):
        packet_bin = ''
        for c in packet:
            packet_bin += nibble_to_bits[c]
        return packet_bin

    @staticmethod
    def __read_int(bits, count):
        return int(bits[:count], 2), bits[count:]

    @staticmethod
    def __read_bool(bits):
        return bool(int(bits[0])), bits[1:]

    @staticmethod
    def __read_literal(bits):
        int_bits = ''
        while True:
            more, bits = PacketDecoder.__read_bool(bits)
            int_bits += bits[:4]
            bits = bits[4:]
            if not more:
                break

        return PacketDecoder.__read_int(int_bits, len(int_bits))[0], bits

    @staticmethod
    def __parse_bin(bits, parse_tree=None):
        if parse_tree is None:
            parse_tree = []
        version, bits = PacketDecoder.__read_int(bits, 3)
        type_id, bits = PacketDecoder.__read_int(bits, 3)
        if type_id == 4:  # Literal
            literal_value, bits = PacketDecoder.__read_literal(bits)
            parse_tree.append({
                'version': version,
                'type_id': type_id,
                'literal_value': literal_value,
            })
            return parse_tree, bits
        else:  # Operator
            mode, bits = PacketDecoder.__read_bool(bits)
            if not mode:
                length, bits = PacketDecoder.__read_int(bits, 15)
                original_length = len(bits)
                sub_parse_tree = []
                while original_length - len(bits) < length:
                    sub_parse_tree, bits = PacketDecoder.__parse_bin(bits, sub_parse_tree)
                parse_tree.append({
                    'version': version,
                    'type_id': type_id,
                    'sub-packets': sub_parse_tree,
                })
                return parse_tree, bits
            else:
                packet_count, bits = PacketDecoder.__read_int(bits, 11)
                sub_parse_tree = []
                for _ in range(packet_count):
                    sub_parse_tree, bits = PacketDecoder.__parse_bin(bits, sub_parse_tree)
                parse_tree.append({
                    'version': version,
                    'type_id': type_id,
                    'sub-packets': sub_parse_tree,
                })
                return parse_tree, bits

    @staticmethod
    def parse(packet):
        packet_bin = PacketDecoder.__hex_to_bin(packet)
        return PacketDecoder.__parse_bin(packet_bin)

    @staticmethod
    def parse_file(file_name):
        with open(file_name) as f:
            return PacketDecoder.parse(f.read().strip())

    # -------------------------
    # Evaluation
    # -------------------------

    __operators = {
        0: lambda args: sum(args),
        1: lambda args: prod(args),
        2: lambda args: min(args),
        3: lambda args: max(args),
        5: lambda args: int(args[0] > args[1]),
        6: lambda args: int(args[0] < args[1]),
        7: lambda args: int(args[0] == args[1]),
    }

    @staticmethod
    def eval(tree):
        if 'literal_value' in tree:
            return tree['literal_value']
        args = []
        for x in tree['sub-packets']:
            args.append(PacketDecoder.eval(x))
        return PacketDecoder.__operators[tree['type_id']](args)

    @staticmethod
    def decode(packet):
        parse_tree, _ = PacketDecoder.parse(packet)
        return PacketDecoder.eval(parse_tree[0])

    @staticmethod
    def decode_file(file_name):
        parse_tree, _ = PacketDecoder.parse_file(file_name)
        return PacketDecoder.eval(parse_tree[0])
