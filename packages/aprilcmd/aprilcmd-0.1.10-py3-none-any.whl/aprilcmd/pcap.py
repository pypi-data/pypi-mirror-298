from scapy.all import *  
  
# 加载pcap文件  
packets = rdpcap('/home/ygh/tmp/usbmon1.cap')  
  
# 遍历数据包  
for packet in packets:  
    # 处理数据包，例如打印  
    print(packet.show())  
  
# 你也可以进一步分析数据包内容，如解析USB请求等

