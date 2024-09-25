import os
import json
from base import Base  # Giả sử file base.py nằm cùng thư mục với main.py

def main():
    base_instance = Base()

    # Kiểm tra cấu hình
    config_file = base_instance.file_path("config.json")  # Giả sử có tệp config.json
    if not os.path.exists(config_file):
        base_instance.log("Config file does not exist.")
        return  # Kết thúc nếu tệp cấu hình không tồn tại

    is_enabled = base_instance.get_config(config_file, "auto_claim")
    
    if is_enabled:
        base_instance.log("Auto claim is enabled.")
    else:
        base_instance.log("Auto claim is disabled.")
        return  # Kết thúc nếu không bật auto claim

    # Xóa màn hình
    base_instance.clear_terminal()

    # Kiểm tra địa chỉ IP
    proxy_info = "http://user:pass@ip:port"  # Thay thế bằng thông tin proxy của bạn
    actual_ip = base_instance.check_ip(proxy_info)
    if actual_ip:
        base_instance.log(f"Current IP is: {actual_ip}")

    # Ghi nhật ký
    base_instance.log("Starting the auto-claimer process...")
    # Thực hiện các tác vụ tự động khác ở đây...
    # Ví dụ:
    # base_instance.perform_auto_claim()  # Gọi hàm thực hiện auto-claim nếu có

if __name__ == "__main__":
    main()
