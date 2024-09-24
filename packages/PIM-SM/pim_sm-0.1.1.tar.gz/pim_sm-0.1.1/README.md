# PIM-SM Packet Sender

## 项目简介

这是一个用于处理 PIM-SM（Protocol Independent Multicast - Sparse Mode）协议报文发送的 Python 项目，使用了 Scapy 和 PyShark 库。该项目旨在提供一种简单的方法来生成、发送和分析 PIM-SM 数据包。

## 主要功能

- 生成 PIM-SM 协议的报文
- 发送 IGMP 数据包
- 使用 Scapy 和 PyShark 进行数据包捕获和分析

## 调用方法
from pim_sm import *

hello_packet('router_ip', 'router_mac', 'your_iface')

