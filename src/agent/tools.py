from langchain_core.tools import tool

# ============================================================
# MOCK DATA – Dữ liệu giả lập hệ thống du lịch
# Lưu ý: Giá cả có logic (VD: cuối tuần đắt hơn, hạng cao hơn đắt hơn)
# ============================================================

FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1_450_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2_800_000, "class": "business"},
        {"airline": "VietJet Air", "departure": "08:30", "arrival": "09:50", "price": 890_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "11:00", "arrival": "12:20", "price": 1_200_000, "class": "economy"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "10:00", "arrival": "12:15", "price": 1_350_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "16:00", "arrival": "18:15", "price": 1_100_000, "class": "economy"},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1_600_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "07:30", "arrival": "09:40", "price": 950_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "12:00", "arrival": "14:10", "price": 1_300_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3_200_000, "class": "business"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1_300_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "14:20", "price": 780_000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "15:00", "arrival": "16:00", "price": 650_000, "class": "economy"},
    ],
}

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury", "stars": 5, "price_per_night": 1_800_000, "area": "Mỹ Khê", "rating": 4.5},
        {"name": "Sala Danang Beach", "stars": 4, "price_per_night": 1_200_000, "area": "Mỹ Khê", "rating": 4.3},
        {"name": "Fivitel Danang", "stars": 3, "price_per_night": 650_000, "area": "Sơn Trà", "rating": 4.1},
        {"name": "Memory Hostel", "stars": 2, "price_per_night": 250_000, "area": "Hải Châu", "rating": 4.6},
        {"name": "Christina's Homestay", "stars": 2, "price_per_night": 350_000, "area": "An Thượng", "rating": 4.7},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort", "stars": 5, "price_per_night": 3_500_000, "area": "Bãi Dài", "rating": 4.4},
        {"name": "Sol by Meliá", "stars": 4, "price_per_night": 1_500_000, "area": "Bãi Trường", "rating": 4.2},
        {"name": "Lahana Resort", "stars": 3, "price_per_night": 800_000, "area": "Dương Đông", "rating": 4.0},
        {"name": "9Station Hostel", "stars": 2, "price_per_night": 200_000, "area": "Dương Đông", "rating": 4.5},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel", "stars": 5, "price_per_night": 2_800_000, "area": "Quận 1", "rating": 4.3},
        {"name": "Liberty Central", "stars": 4, "price_per_night": 1_400_000, "area": "Quận 1", "rating": 4.1},
        {"name": "Cochin Zen Hotel", "stars": 3, "price_per_night": 550_000, "area": "Quận 3", "rating": 4.4},
        {"name": "The Common Room", "stars": 2, "price_per_night": 180_000, "area": "Quận 1", "rating": 4.6},
    ],
}


def _format_price(amount: int) -> str:
    """Format số tiền với dấu chấm phân cách hàng nghìn."""
    return f"{amount:,}đ".replace(",", ".")


@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm các chuyến bay giữa hai thành phố.
    Tham số:
    - origin: thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh')
    - destination: thành phố đến (VD: 'Đà Nẵng', 'Phú Quốc')
    Trả về danh sách chuyến bay với hãng, giờ bay, giá vé.
    Nếu không tìm thấy tuyến bay, trả về thông báo không có chuyến.
    """
    print(f"[Tool] search_flights: {origin} -> {destination}")

    flights = FLIGHTS_DB.get((origin, destination))

    # Thử tra ngược chiều nếu không tìm thấy
    if not flights:
        flights = FLIGHTS_DB.get((destination, origin))
        if flights:
            origin, destination = destination, origin

    if not flights:
        return f"Không tìm thấy chuyến bay từ {origin} đến {destination}."

    lines = [f"Chuyến bay từ {origin} đến {destination} ({len(flights)} chuyến):"]
    for i, f in enumerate(flights, 1):
        class_label = "Phổ thông" if f["class"] == "economy" else "Thương gia"
        lines.append(
            f"  {i}. {f['airline']} | {f['departure']} → {f['arrival']} | "
            f"{_format_price(f['price'])} | {class_label}"
        )
    return "\n".join(lines)


@tool
def search_hotels(city: str, max_price_per_night: int = 99_999_999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm.
    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
    - max_price_per_night: giá tối đa mỗi đêm (VNĐ), mặc định không giới hạn
    Trả về danh sách khách sạn phù hợp với tên, số sao, giá, khu vực, rating.
    """
    print(f"[Tool] search_hotels: {city}, giá tối đa {_format_price(max_price_per_night)}/đêm")

    all_hotels = HOTELS_DB.get(city)
    if not all_hotels:
        return f"Không tìm thấy thông tin khách sạn tại {city}."

    filtered = [h for h in all_hotels if h["price_per_night"] <= max_price_per_night]

    if not filtered:
        return (
            f"Không tìm thấy khách sạn tại {city} với giá dưới "
            f"{_format_price(max_price_per_night)}/đêm. Hãy thử tăng ngân sách."
        )

    # Sắp xếp theo rating giảm dần
    filtered.sort(key=lambda h: h["rating"], reverse=True)

    lines = [f"Khách sạn tại {city} (giá ≤ {_format_price(max_price_per_night)}/đêm):"]
    for i, h in enumerate(filtered, 1):
        stars = "★" * h["stars"]
        lines.append(
            f"  {i}. {h['name']} {stars} | {_format_price(h['price_per_night'])}/đêm | "
            f"Khu vực: {h['area']} | Rating: {h['rating']}/5"
        )
    return "\n".join(lines)


@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.
    Tham số:
    - total_budget: tổng ngân sách ban đầu (VNĐ)
    - expenses: chuỗi mô tả các khoản chi, mỗi khoản cách nhau bởi dấu phẩy,
      định dạng 'tên_khoản:số_tiền' (VD: 'vé_máy_bay:890000,khách_sạn:650000')
    Trả về bảng chi tiết các khoản chi và số tiền còn lại.
    Nếu vượt ngân sách, cảnh báo rõ ràng số tiền thiếu.
    """
    print(f"[Tool] calculate_budget: ngân sách {_format_price(total_budget)}, chi phí: {expenses}")

    try:
        expense_dict: dict[str, int] = {}
        for item in expenses.split(","):
            item = item.strip()
            if not item:
                continue
            parts = item.split(":")
            if len(parts) != 2:
                return f"Lỗi định dạng: '{item}' không đúng cú pháp 'tên_khoản:số_tiền'."
            name = parts[0].strip().replace("_", " ").capitalize()
            amount = int(parts[1].strip())
            expense_dict[name] = amount
    except ValueError as e:
        return f"Lỗi khi đọc số tiền: {e}. Vui lòng dùng số nguyên (VD: 890000)."

    total_spent = sum(expense_dict.values())
    remaining = total_budget - total_spent

    lines = ["Bảng chi phí:"]
    for name, amount in expense_dict.items():
        lines.append(f"  - {name}: {_format_price(amount)}")
    lines.append("  ---")
    lines.append(f"  Tổng chi:    {_format_price(total_spent)}")
    lines.append(f"  Ngân sách:   {_format_price(total_budget)}")

    if remaining >= 0:
        lines.append(f"  Còn lại:     {_format_price(remaining)}")
    else:
        lines.append(f"  Còn lại:     -{_format_price(abs(remaining))}")
        lines.append(f"  ⚠️ Vượt ngân sách {_format_price(abs(remaining))}! Cần điều chỉnh kế hoạch.")

    return "\n".join(lines)
