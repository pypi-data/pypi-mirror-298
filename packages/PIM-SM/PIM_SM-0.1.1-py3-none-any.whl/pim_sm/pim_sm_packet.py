import asyncio

import pyshark
from scapy.all import *
from scapy.contrib.igmp import IGMP
from scapy.layers.inet import *
from scapy.layers.l2 import ARP


def hello_packet(sender_ip, sender_mac, iface):
    def compute_checksum(data):
        """
        计算校验和
        """
        if len(data) % 2 != 0:
            data += b'\x00'
        total = sum(struct.unpack('!%dH' % (len(data) // 2), data))
        total = (total & 0xFFFF) + (total >> 16)
        total = ~total & 0xFFFF
        return total

    class PIM(Packet):
        """
        PIM 数据包类
        """
        name = "PIM"
        fields_desc = [
            BitField("version", 2, 4),  # PIM Version，4 比特，值为 2
            BitField("type", 0, 4),  # Type，4 比特，消息类型，值为 0
            ByteField("reserved", 0),  # Reserved，8 比特
            XShortField("checksum", 0x0000)  # Checksum，16 比特
        ]

    class PIMHelloOption(Packet):
        """
        PIM Hello 选项数据包类
        """
        name = "PIM Hello Option"
        fields_desc = [
            ShortField("option_type", 0),  # OptionType
            ShortField("option_length", 0),  # OptionLength
            StrLenField("value", "", length_from=lambda pkt: pkt.option_length)  # OptionValue
        ]

    class PIMHello(Packet):
        """
        PIM Hello 数据包类
        """
        name = "PIM-Hello"
        fields_desc = [
            PacketListField("options", None, PIMHelloOption, length_from=lambda pkt: pkt.underlayer.len - 4)
        ]

    # 绑定各层
    bind_layers(IP, PIM, proto=103)
    bind_layers(PIM, PIMHello, type=0)

    # 构建 PIM Hello 选项
    holdtime = PIMHelloOption(option_type=1, option_length=2, value=struct.pack('!H', 105))
    lan_prune_delay = PIMHelloOption(option_type=2, option_length=4,
                                     value=struct.pack('!H H', (500 >> 1) & 0x7FFF, 2500))
    dr_priority = PIMHelloOption(option_type=19, option_length=4, value=struct.pack('!I', 1))
    generation_id = PIMHelloOption(option_type=20, option_length=4, value=struct.pack('!I', 994602213))

    options = [holdtime, dr_priority, generation_id, lan_prune_delay]

    # 创建报文
    pim_hello_packet = (
            Ether(dst="01:00:5e:00:00:0d", src=sender_mac, type=0x0800) /
            IP(src=sender_ip, dst="224.0.0.13", ttl=1, proto=103) /
            PIM() /
            PIMHello(options=options)
    )

    # 计算 PIM 报文的校验和
    pim_hello_packet[PIM].checksum = 0  # 校验和初始值设置为 0
    pim_data = bytes(pim_hello_packet[PIM])
    pim_hello_packet[PIM].checksum = compute_checksum(pim_data)
    # 发送报文
    sendp(pim_hello_packet, iface=iface)


def bootstrap_packet(rp_ip, bsr_ip, sender_ip, multicast_group, iface):
    def compute_checksum(data):
        """
        计算校验和
        """
        if len(data) % 2 != 0:
            data += b'\x00'
        total = sum(struct.unpack('!%dH' % (len(data) // 2), data))
        total = (total & 0xFFFF) + (total >> 16)
        total = ~total & 0xFFFF
        return total

    class PIM(Packet):
        """
        PIM 数据包类
        """
        name = "PIM"
        fields_desc = [
            BitField("version", 2, 4),  # PIM Version，4 比特，值为 2
            BitField("type", 4, 4),  # Type，4 比特，消息类型，值为 4 (Bootstrap)
            ByteField("reserved", 0),  # Reserved，8 比特
            XShortField("checksum", 0x0000)  # Checksum，16 比特
        ]

    class EncodedUnicast(Packet):
        """
        Encoded Unicast 数据包类
        """
        name = "Encoded-Unicast"
        fields_desc = [
            ByteField("addr_family", 1),  # Address Family，8 比特，值为 1 (IPv4)
            ByteField("enc_type", 0),  # Encoding Type，8 比特，值为 0 (Native)
            IPField("address", "0.0.0.0")  # Address，32 比特
        ]

    class EncodedGroup(Packet):
        """
        Encoded Group 数据包类
        """
        name = "Encoded-Group"
        fields_desc = [
            ByteField("addr_family", 1),  # Address Family，8 比特，值为 1 (IPv4)
            ByteField("enc_type", 0),  # Encoding Type，8 比特，值为 0 (Native)
            ByteField("reserved", 0),  # Reserved，8 比特
            ByteField("masklen", 4),  # Mask Length，8 比特
            IPField("group_address", "0.0.0.0")  # Group Address，32 比特
        ]

    class RPInfo(Packet):
        """
        RP 信息数据包类
        """
        name = "RP-Info"
        fields_desc = [
            PacketField("rp_address", None, EncodedUnicast),  # RP Address
            ShortField("rp_holdtime", 0),  # RP Holdtime，16 比特
            ByteField("rp_priority", 0),  # RP Priority，8 比特
            ByteField("reserved", 0)  # Reserved，8 比特
        ]

    class PIMBootstrap(Packet):
        """
        PIM Bootstrap 数据包类
        """
        name = "PIM-Bootstrap"
        fields_desc = [
            ShortField("fragment_tag", 0),  # Fragment Tag，16 比特
            ByteField("hash_mask_len", 0),  # Hash Mask Length，8 比特
            ByteField("bsr_priority", 0),  # BSR Priority，8 比特
            PacketField("bsr_address", None, EncodedUnicast),  # BSR Address
            PacketListField("group_addresses", [], EncodedGroup),  # Group Addresses
            ByteField("rp_count", 0),  # RP Count，8 比特
            ByteField("frag_rp_count", 0),  # Frag RP Count，8 比特
            ShortField("reserved2", 0),  # Reserved，16 比特
            PacketListField("rp_info", [], RPInfo)  # RP Info
        ]

    # 绑定各层
    bind_layers(IP, PIM, proto=103)
    bind_layers(PIM, PIMBootstrap, type=4)

    # 构建 BSR 地址和组播地址
    bsr_address = EncodedUnicast(address=bsr_ip)
    group_address = EncodedGroup(masklen=32, group_address=multicast_group)

    # 构建 RP 信息
    rp_info = RPInfo(rp_address=EncodedUnicast(address=rp_ip), rp_holdtime=150, rp_priority=10)

    # 构建 PIM Bootstrap 数据包
    pim_bootstrap_packet = (
            Ether(dst="01:00:5e:00:00:0d", src="00:e0:fc:e2:7a:76", type=0x0800) /
            IP(src=sender_ip, dst='224.0.0.13', ttl=1, proto=103) /
            PIM() /
            PIMBootstrap(fragment_tag=0x1234, hash_mask_len=30, bsr_priority=0, bsr_address=bsr_address,
                         group_addresses=[group_address], rp_count=1, frag_rp_count=1, rp_info=[rp_info])
    )

    # 计算 PIM 报文的校验和
    pim_bootstrap_packet[PIM].checksum = 0  # 校验和初始值设置为 0
    pim_data = bytes(pim_bootstrap_packet[PIM])
    pim_bootstrap_packet[PIM].checksum = compute_checksum(pim_data)

    # 发送报文
    sendp(pim_bootstrap_packet, iface=iface)


def crp_packet(rp_ip, sender_ip, receive_ip, multicast_group, iface, sender_mac, receive_mac):
    def compute_checksum(data):
        """
        计算校验和
        """
        if len(data) % 2 != 0:
            data += b'\x00'
        total = sum(struct.unpack('!%dH' % (len(data) // 2), data))
        total = (total & 0xFFFF) + (total >> 16)
        total = ~total & 0xFFFF
        return total

    class PIM(Packet):
        """
        PIM 数据包类
        """
        name = "PIM"
        fields_desc = [
            BitField("version", 2, 4),  # PIM Version，4 比特，值为 2
            BitField("type", 8, 4),  # Type，4 比特，消息类型，值为 8 (Candidate-RP-Advertisement)
            ByteField("reserved", 0),  # Reserved，8 比特
            XShortField("checksum", 0x0000)  # Checksum，16 比特
        ]

    class EncodedUnicast(Packet):
        """
        Encoded Unicast 数据包类
        """
        name = "Encoded-Unicast"
        fields_desc = [
            ByteField("addr_family", 1),  # Address Family，8 比特，值为 1 (IPv4)
            ByteField("enc_type", 0),  # Encoding Type，8 比特，值为 0 (Native)
            IPField("rp_address", "0.0.0.0")  # RP Address，32 比特
        ]

    class EncodedGroup(Packet):
        """
        Encoded Group 数据包类
        """
        name = "Encoded-Group"
        fields_desc = [
            ByteField("addr_family", 1),  # Address Family，8 比特，值为 1 (IPv4)
            ByteField("enc_type", 0),  # Encoding Type，8 比特，值为 0 (Native)
            ByteField("reserved", 0),  # Reserved，8 比特
            ByteField("masklen", 4),  # Mask Length，8 比特
            IPField("group_address", "0.0.0.0")  # Group Address，32 比特
        ]

    class PIMCRPAdv(Packet):
        """
        PIM C-RP Advertisement 数据包类
        """
        name = "PIM-CRP-Adv"
        fields_desc = [
            ByteField("prefix_cnt", 0),  # Prefix-cnt，8 比特
            ByteField("priority", 0),  # Priority，8 比特
            ShortField("holdtime", 0),  # Holdtime，16 比特
            PacketField("rp_address", None, EncodedUnicast),  # RP Address
            PacketListField("group_addresses", [], EncodedGroup)  # Group Addresses
        ]

    # 绑定各层
    bind_layers(IP, PIM, proto=103)
    bind_layers(PIM, PIMCRPAdv, type=8)

    # 构建 RP 地址和组播地址
    rp_address = EncodedUnicast(rp_address=rp_ip)
    group_address = EncodedGroup(masklen=32, group_address=multicast_group)

    # 构建 PIM C-RP Advertisement 数据包
    pim_crp_adv_packet = (
            Ether(dst=receive_mac, src=sender_mac, type=0x0800) /
            IP(src=sender_ip, dst=receive_ip, ttl=255, proto=103) /
            PIM() /
            PIMCRPAdv(prefix_cnt=1, priority=10, holdtime=150, rp_address=rp_address, group_addresses=[group_address])
    )

    # 计算 PIM 报文的校验和
    pim_crp_adv_packet[PIM].checksum = 0  # 校验和初始值设置为 0
    pim_data = bytes(pim_crp_adv_packet[PIM])
    pim_crp_adv_packet[PIM].checksum = compute_checksum(pim_data)

    # 发送报文
    sendp(pim_crp_adv_packet, iface=iface)


def returnMac(router_ip, iface):
    # 创建事件循环
    asyncio.set_event_loop(asyncio.new_event_loop())

    # 加载数据包
    capture = pyshark.LiveCapture(interface=iface)

    for packet in capture.sniff_continuously():
        if 'PIM' in packet and packet.ip.src == router_ip:
            capture.close()
            return packet.eth.src


def igmp_join(igmp_ip, multicast_group, iface):
    """
    创建并发送 IGMP 加入组播组的报文。示例使用：
    源 IP 地址: 192.168.10.3
    组播组地址: 225.1.1.1
    网络接口名称: igmpv2
    """

    def create_igmp_join(igmp_ip, multicast_group):
        """
        创建 IGMP 加入组播组的报文。
        """
        packet = (
                IP(src=igmp_ip, dst=multicast_group, options=IPOption_Router_Alert()) /
                IGMP(type=0x16, gaddr=multicast_group)
        )
        return packet

    def send_igmp_packet(packet, iface):
        """
        发送 IGMP 报文。
        """
        send(packet, iface=iface)

    # 创建 IGMP 加入组播组的报文
    igmp_join_packet = create_igmp_join(igmp_ip, multicast_group)

    send_igmp_packet(igmp_join_packet, iface)


def igmp_leave(igmp_ip, multicast_group, iface):
    """
    创建并发送 IGMP 离开组播组的报文。
    """

    def create_igmp_leave(igmp_ip, multicast_group):
        """
        创建 IGMP 离开组播组的报文。
        """
        packet = (
                IP(src=igmp_ip, dst="224.0.0.2", options=IPOption_Router_Alert()) /
                IGMP(type=0x17, gaddr=multicast_group)
        )
        return packet

    def send_igmp_packet(packet, iface):
        """
        发送 IGMP 报文。
        """
        send(packet, iface=iface)

    # 创建 IGMP 离开组播组的报文
    igmp_leave_packet = create_igmp_leave(igmp_ip, multicast_group)

    # 发送 IGMP 报文
    send_igmp_packet(igmp_leave_packet, iface)


def send_arp(src_mac, src, dst_mac, dst, iface):
    # 构建以太网层
    ether_layer = Ether(dst="ff:ff:ff:ff:ff:ff", src=src_mac, type=0x0806)

    # 构建ARP请求层
    arp_layer = ARP(hwtype=1, ptype=0x0800, hwlen=6, plen=4, op=1,
                    hwsrc=src_mac, psrc=src,
                    hwdst=dst_mac, pdst=dst)

    # 构建整个数据包
    arp_request_packet = ether_layer / arp_layer

    # 发送数据包
    sendp(arp_request_packet, iface=iface)


def register_packet(src_mac, dst_mac, src_ip, dst_ip, ip2_src, ip2_dst, iface):
    """
    发送注册PIM数据包的函数

    参数:
    - src_mac: Ether层的源MAC地址
    - dst_mac: Ether层的目标MAC地址
    - src_ip: 第一个IP层的源IP地址
    - dst_ip: 第一个IP层的目标IP地址
    - ip2_src: 第二个IP层的源IP地址
    - ip2_dst: 第二个IP层的目标IP地址
    - iface: 网络接口
    """

    # 定义PIM类
    class PIM(Packet):
        name = "PIM"
        fields_desc = [
            BitField("version", 2, 4),
            BitField("type", 1, 4),
            ByteField("reserved", 0),
            XShortField("checksum", 0xDEFF)
        ]

    # 定义PIMOptions类
    class PIMOptions(Packet):
        name = "PIM Options"
        fields_desc = [
            BitField("border", 0, 1),
            BitField("null_register", 0, 1),
            BitField("reserved2", 0, 30)
        ]

    # 绑定各层
    bind_layers(Ether, IP, type=0x0800)
    bind_layers(IP, PIM, proto=103)
    bind_layers(PIM, PIMOptions)

    # 构建数据包
    packet = (
            Ether(src=src_mac, dst=dst_mac) /
            IP(src=src_ip, dst=dst_ip, ttl=255, proto=103) /
            PIM(version=2, type=1, reserved=0, checksum=0xDEFF) /
            PIMOptions(border=0, null_register=0, reserved2=0) /
            IP(src=ip2_src, dst=ip2_dst, ttl=254, proto=17) /
            UDP(sport=0, dport=0, len=8, chksum=0xFFF7) /
            Raw(load=bytes.fromhex('80a3b662'))
    )

    # 发送数据包
    sendp(packet, iface=iface)


def register_stop(ip_src, ip_dst, src_mac, dst_mac, source_addr, group_addr, iface):
    class PIM(Packet):
        name = "PIM"
        fields_desc = [
            BitField("version", 2, 4),
            BitField("type", 2, 4),
            ByteField("reserved", 0),
            XShortField("checksum", 0xf9f9),
        ]

    class EncodedUnicast(Packet):
        """
        Encoded Unicast 数据包类
        """
        name = "Encoded-Unicast"
        fields_desc = [
            ByteField("addr_family", 1),  # Address Family，8 比特，值为 1 (IPv4)
            ByteField("enc_type", 0),  # Encoding Type，8 比特，值为 0 (Native)
            IPField("address", "0.0.0.0")  # Address，32 比特
        ]

    class EncodedGroup(Packet):
        """
        Encoded Group 数据包类
        """
        name = "Encoded-Group"
        fields_desc = [
            ByteField("addr_family", 1),  # Address Family，8 比特，值为 1 (IPv4)
            ByteField("enc_type", 0),  # Encoding Type，8 比特，值为 0 (Native)
            ByteField("reserved", 0),  # Reserved，8 比特
            ByteField("masklen", 4),  # Mask Length，8 比特
            IPField("group_address", "0.0.0.0")  # Group Address，32 比特
        ]

    class PIM_Register_Stop(Packet):
        name = "PIM Register-Stop"
        fields_desc = [
            PacketListField("group_addresses", [], EncodedGroup),  # Group Addresses
            PacketField("source_address", None, EncodedUnicast),  # Source Address
        ]

    source_address = EncodedUnicast(address=source_addr)
    group_address = EncodedGroup(masklen=32, group_address=group_addr)

    bind_layers(IP, PIM, proto=103)
    bind_layers(PIM, PIM_Register_Stop)

    eth_layer = Ether(src=src_mac, dst=dst_mac, type=0x0800)
    ip_layer = IP(src=ip_src, dst=ip_dst, proto=103)
    pim_layer = PIM()
    pim_register_stop_layer = PIM_Register_Stop(group_addresses=[group_address], source_address=[source_address])

    packet = eth_layer / ip_layer / pim_layer / pim_register_stop_layer

    packet[PIM].checksum = 0x2584

    sendp(packet, iface=iface)


def send_udp_packet(source_ip, multicast_group, iface):
    # 构建以太网层
    eth = Ether()

    # 构建IP层
    ip = IP(src=source_ip, dst=multicast_group)

    # 构建UDP层
    udp = UDP(sport=12345, dport=54321)  # 可以自定义源端口和目的端口

    # 构建数据负载
    data = b"Test UDP packet"

    # 构建完整的数据包
    pkt = eth / ip / udp / Raw(load=data)

    time.sleep(2)

    # 通过指定的接口发送数据包
    sendp(pkt, iface=iface)
