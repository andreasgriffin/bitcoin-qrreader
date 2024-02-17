from bitcoin_qrreader.bitcoin_qr import *
from bitcoin_qrreader.multipath_descriptor import *


def test_xpub():

    # test xpub
    s = "tpubDDnGNapGEY6AZAdQbfRJgMg9fvz8pUBrLwvyvUqEgcUfgzM6zc2eVK4vY9x9L5FJWdX8WumXuLEDV5zDZnTfbn87vLe9XceCFwTu9so9Kks"
    data = Data.from_str(s, network=bdk.Network.REGTEST)
    assert data.data_type == DataType.Xpub
    assert data.data == s


def test_txid():

    # test txid
    s = "14cd7d7ec4ab969afcb1609a6638b89895ae023446fd523875b0e930fdcd1b67"
    data = Data.from_str(s, network=bdk.Network.REGTEST)
    assert data.data_type == DataType.Txid
    assert data.data == s


def test_tx():

    # test tx
    s = "020000000001010000000000000000000000000000000000000000000000000000000000000000ffffffff0502ad000101ffffffff0200f9029500000000160014b947c0de955cd2ccdfcd5b33198d2656834d0cd50000000000000000266a24aa21a9ede2f61c3f71d1defd3fa999dfa36953755c690689799962b48bebd836974e8cf90120000000000000000000000000000000000000000000000000000000000000000000000000"
    data = Data.from_str(s, network=bdk.Network.REGTEST)
    assert data.data_type == DataType.Tx
    assert serialized_to_hex(data.data.serialize()) == s

    # tx  in base43  (electrum)
    s = "M2/VL:YG123EZA4VZ36QF7E*AJAOI/7XORPC8X8S69504C2ZZX493.ZQRA.UJ88O5YI7E$3JA.6OEVKFQW4V0+X4192T0+1Y5K3YUHZ.6Z*LXNN:GAB/BBU7T+H9SA2A7ALE8UJBLYVV6$$ZN1I.TY1M+8MOIOW/BWS/$KP1$0.FVDU/HUTTYT2PO5R0*3XWOF:LY4L0JQ3TPOAJ1QDE8A/0H+1O+D0TX+UE4KU44VE6QIAO:W0VG830-VQ+BF:.OANNB2GLOYXUU*4V2VCJS*RS2TC5JO2JLDEL.92F5PS3Y1EDY-G9-4C30S3F*-7V0BXB6R"
    data = Data.from_str(s, network=bdk.Network.REGTEST)
    assert data.data_type == DataType.Tx
    assert (
        bytes(data.data.serialize()).hex()
        == "01000000000101324ffaac81edf89c4b318f42028116c6d19fc547884327e9fc8dce0c2e34a7650000000000fdffffff02dbad3d25000000001600140277d89eda5f5c3152595828c5239eda1cc045dc400d03000000000016001488aca5ab3813f3e09512487e30be0fa293ce2bf602473044022054634107fa26af77735d2eefa48618de2500cc0e852fd804a1816b85e58de671022010170c91c3423f324f7487456dfa0c485220bc7bc66f3e65ec90abe88731ad640121026c192a98c1fb5f84870e6833b4bc7a06f8d37f58ffa940428d3a3dca8809e4cca4020000"
    )

    # raw transaction splitted with UR  (like sparrow)
    parts = [
        "UR:BYTES/162-3/LPCSOEAXCSVTCYHKMSLGOLHDGRVOVLHLGRHDCEFLTBCXCFMUAEAEAEAECMAEBBBGSOVTSOGTTBSTCEZESTRFZMCMZEWDBKBSRORFHLAOFLDYFYAOCXHHLOTYTSVLAHNECMSWYLGTWMRHKPGLZERDLDYTDRCNKGKIASTAJKDMHKROOSTBBAOLCXKP",
        "UR:BYTES/164-3/LPCSOXAXCSVTCYHKMSLGOLHDGRRDFSHHGRHDCEFLTSCLJTJZJEGTVEHHRHISMNLTZMNLMEPRRYHFDYUTFWISDEFZSSVLPFGLJKRPJSEYPRBGFYAOCXHHLODTDECEZSNTRPAYCKGSWMRHKPGLVSRDNTBDAAISIOWSDNWFGRNSURFEJYFDBSCMFHVA",
        "UR:BYTES/165-3/LPCSONAXCSVTCYHKMSLGOLHDGRFNVYKIIOROWFJYHHTSIODMLKBBPLLOVYVSDAAADTHTWYVWGSDTIETSDESFDMWDJKJKONASRHNTHELFINDLNNATMTKTMSTESGTBRHGLFHFTYATTCSVSASDKASASEYYKSNGLBTRDTSURZEDMHKROOSTBETOLNBMD",
    ]
    meta_data_handler = MetaDataHandler(bdk.Network.REGTEST)
    for part in parts:
        meta_data_handler.add(part)
    assert meta_data_handler.is_complete()
    data = meta_data_handler.get_complete_data()
    assert data.data_type == DataType.Tx
    assert (
        serialized_to_hex(data.data.serialize())
        == "0100000000010177ff6b4de45caf689a95367958ff6b912c2385d4d7563a09ba41cb0a2c30f5220000000000fdffffff02a0cee90100000000160014f22e4b1c92222a38b286fdd39ee2e35d4b581c47d62019930000000016001412c9e0c94dd6c71cfec7bcff16feea0a0fb8bc5d0247304402205c88d4d7e3059f16c6f74debb9754efeba89f92a237b7d09d9732e59b8a7d6de02202ce0ef338af77ebd8c14ae88f7e83116e0ba27a89aee7829ef70d1fc8d99af06012102802e1fda05b62b1f071d35bcd129fc0f9cf3517c6af7b3bb0ce76d76c7de068d00000000"
    )


def test_checksum():
    # checksum test
    descriptor = "raw(deadbeef)"
    assert add_checksum_to_descriptor(descriptor).split("#")[1] == "89f8spxm"

    # checksum test
    descriptor = "wpkh([189cf85e/84'/1'/0']tpubDDkYCWGii5pUuqqqvh9vRqyChQ88aEGZ7z7xpwDzAQ87SpNrii9MumksW8WSqv2aYEBssKYF5KVeY9kmoreJrvQSB2dgCz11TXu81YhyaqP/0/*)"
    assert add_checksum_to_descriptor(descriptor).split("#")[1] == "arpc0qa2"

    # checksum test
    parts = [
        "wsh(sortedmulti(2,tprv8ZgxMBicQKsPeXkN69E47nqEZhrdWZkRBrzsZjzYQGjbr85QApCLuRCgKHTnfaiB9BZCDHrewdC8cTsyd54yGHZJxsvVvuB719VqYVu8eSz/84'/1'/0'/0/*,tprv8ZgxMBicQKsPeVD8mgZXgNgqTgGUhsv9qtHiRjhrvHL2ecXWhiCd4okHeC6sdFvs1rNYmwWf5Sa3B2PvhrZ1MHcCK8qPJqTSnZ9nLnywUGA/84'/1'/0'/0/*,tprv8ZgxMBicQKsPe3ca8xqj6BNa3Lb9pfyNyYaUy1y4AUCqTSAYwmhAMNnEHnBYtLgggRGrYt8BxcBwedNMnXFbWSxrtEzcJGu9L3k1BBVTNzD/84'/1'/0'/0/*))"
    ]
    meta_data_handler = MetaDataHandler(bdk.Network.REGTEST)
    for part in parts:
        meta_data_handler.add(part)
    assert meta_data_handler.is_complete()
    data = meta_data_handler.get_complete_data()
    assert data.data_type == DataType.Descriptor, "Wrong type"
    assert (
        data.data_as_string()
        == "wsh(sortedmulti(2,tprv8ZgxMBicQKsPeXkN69E47nqEZhrdWZkRBrzsZjzYQGjbr85QApCLuRCgKHTnfaiB9BZCDHrewdC8cTsyd54yGHZJxsvVvuB719VqYVu8eSz/84'/1'/0'/0/*,tprv8ZgxMBicQKsPeVD8mgZXgNgqTgGUhsv9qtHiRjhrvHL2ecXWhiCd4okHeC6sdFvs1rNYmwWf5Sa3B2PvhrZ1MHcCK8qPJqTSnZ9nLnywUGA/84'/1'/0'/0/*,tprv8ZgxMBicQKsPe3ca8xqj6BNa3Lb9pfyNyYaUy1y4AUCqTSAYwmhAMNnEHnBYtLgggRGrYt8BxcBwedNMnXFbWSxrtEzcJGu9L3k1BBVTNzD/84'/1'/0'/0/*))#5j8fff0h"
    )

    # checksum test (sparrow)
    descriptor = "wpkh([7d315cd9/84h/1h/0h]tpubDCUCSorYswSAurXv7ZcwfkPR8ms2fmxkEW7LFHuLs85wsCngaNAEVFkAvZSabsnz2VH6NvH4uFd4tZ8J3PSaVaxchE8QCd9wxak5Sugnd9p/<0;1>/*)"
    assert add_checksum_to_descriptor(descriptor).split("#")[1] == "3gahv2xk"

    # checksum test multipath_descriptor (created with sparrow pdf)
    parts = [
        "wpkh([7d315cd9/84h/1h/0h]tpubDCUCSorYswSAurXv7ZcwfkPR8ms2fmxkEW7LFHuLs85wsCngaNAEVFkAvZSabsnz2VH6NvH4uFd4tZ8J3PSaVaxchE8QCd9wxak5Sugnd9p/<0;1>/*)"
    ]
    meta_data_handler = MetaDataHandler(bdk.Network.REGTEST)
    for part in parts:
        meta_data_handler.add(part)
    assert meta_data_handler.is_complete()
    data = meta_data_handler.get_complete_data()
    assert data.data_type == DataType.MultiPathDescriptor, "Wrong type"
    # bdk returns '  instead of h  (which sparrrow does), so the checksum is different
    assert (
        data.data_as_string()
        == "wpkh([7d315cd9/84'/1'/0']tpubDCUCSorYswSAurXv7ZcwfkPR8ms2fmxkEW7LFHuLs85wsCngaNAEVFkAvZSabsnz2VH6NvH4uFd4tZ8J3PSaVaxchE8QCd9wxak5Sugnd9p/<0;1>/*)#xqqeqtvt"
    )
    # however if one replaces again the h by ', one gets the sparrow checksum
    assert (
        replace_in_descriptor(data.data_as_string(), "'", "h")
        == "wpkh([7d315cd9/84h/1h/0h]tpubDCUCSorYswSAurXv7ZcwfkPR8ms2fmxkEW7LFHuLs85wsCngaNAEVFkAvZSabsnz2VH6NvH4uFd4tZ8J3PSaVaxchE8QCd9wxak5Sugnd9p/<0;1>/*)#3gahv2xk"
    )