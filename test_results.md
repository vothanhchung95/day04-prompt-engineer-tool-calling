# Test Results – TravelBuddy AI Agent

> Ghi lại kết quả chạy thực tế từ `python agent.py`

---

## Test 1 – Direct Answer (Không cần tool)

**Input:**
```
Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.
```

**Console log:**
```
TravelBuddy đang suy nghĩ...
  → Trả lời trực tiếp (không gọi tool)
```

**Output:**
```
TravelBuddy: Xin chào! Mình là TravelBuddy, rất vui được đồng hành cùng bạn trong
chuyến đi sắp tới! 😊

Để gợi ý điểm đến phù hợp nhất, mình cần biết thêm một chút:
1. Bạn đang ở thành phố nào? (để tính vé máy bay)
2. Bạn có bao nhiêu ngày nghỉ?
3. Ngân sách cho chuyến đi của bạn khoảng bao nhiêu?
4. Bạn thích biển, núi, hay khám phá đô thị?

Cứ chia sẻ thoải mái, mình sẽ tư vấn ngay!
```

**Kết quả:** ✅ PASS – Agent chào hỏi và hỏi thêm thông tin, không gọi tool.

---

## Test 2 – Single Tool Call

**Input:**
```
Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng
```

**Console log:**
```
TravelBuddy đang suy nghĩ...
  → Gọi tool: search_flights({'origin': 'Hà Nội', 'destination': 'Đà Nẵng'})
[Tool] search_flights: Hà Nội -> Đà Nẵng
  → Trả lời trực tiếp (không gọi tool)
```

**Output:**
```
TravelBuddy: Mình tìm thấy 4 chuyến bay từ Hà Nội đến Đà Nẵng cho bạn:

✈️ Chuyến bay từ Hà Nội đến Đà Nẵng:
  1. VietJet Air | 08:30 → 09:50 | 890.000đ | Phổ thông
  2. Bamboo Airways | 11:00 → 12:20 | 1.200.000đ | Phổ thông
  3. Vietnam Airlines | 06:00 → 07:20 | 1.450.000đ | Phổ thông
  4. Vietnam Airlines | 14:00 → 15:20 | 2.800.000đ | Thương gia

Rẻ nhất là VietJet Air lúc 08:30 chỉ 890.000đ/vé. Bạn có muốn mình tư vấn thêm
khách sạn ở Đà Nẵng hoặc tính toán ngân sách tổng không?
```

**Kết quả:** ✅ PASS – Agent gọi đúng 1 tool, liệt kê đủ 4 chuyến bay.

---

## Test 3 – Multi-Step Tool Chaining

**Input:**
```
Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!
```

**Console log:**
```
TravelBuddy đang suy nghĩ...
  → Gọi tool: search_flights({'origin': 'Hà Nội', 'destination': 'Phú Quốc'})
[Tool] search_flights: Hà Nội -> Phú Quốc
  → Gọi tool: search_hotels({'city': 'Phú Quốc', 'max_price_per_night': 1950000})
[Tool] search_hotels: Phú Quốc, giá tối đa 1.950.000đ/đêm
  → Gọi tool: calculate_budget({'total_budget': 5000000, 'expenses': 'vé_máy_bay:1100000,khách_sạn:1600000'})
[Tool] calculate_budget: ngân sách 5.000.000đ, chi phí: vé_máy_bay:1100000,khách_sạn:1600000
  → Trả lời trực tiếp (không gọi tool)
```

**Output:**
```
TravelBuddy: Đây là gói du lịch Phú Quốc 2 đêm trong tầm ngân sách 5 triệu của bạn!

✈️ Chuyến bay:
  VietJet Air | 16:00 → 18:15 | 1.100.000đ | Phổ thông (rẻ nhất!)

🏨 Khách sạn:
  Sol by Meliá ★★★★ | 1.500.000đ/đêm × 2 đêm = 3.000.000đ | Bãi Trường | Rating: 4.2/5

💰 Tổng chi phí:
  Bảng chi phí:
    - Vé máy bay: 1.100.000đ
    - Khách sạn: 3.000.000đ
    ---
    Tổng chi:    4.100.000đ
    Ngân sách:   5.000.000đ
    Còn lại:     900.000đ

💡 Gợi ý thêm:
  Với 900.000đ còn lại, bạn có thể thưởng thức hải sản tươi ở chợ đêm Dương Đông,
  ghé thăm Vinpearl Safari, hoặc ngồi cafe sunset nhìn ra biển. Phú Quốc rất đẹp
  vào buổi chiều tối!
```

**Kết quả:** ✅ PASS – Agent tự động chuỗi 3 tool calls, tổng hợp đầy đủ.

---

## Test 4 – Missing Info / Clarification

**Input:**
```
Tôi muốn đặt khách sạn
```

**Console log:**
```
TravelBuddy đang suy nghĩ...
  → Trả lời trực tiếp (không gọi tool)
```

**Output:**
```
TravelBuddy: Bạn muốn đặt khách sạn ở đâu? Để tư vấn phù hợp nhất, mình cần biết:

1. 📍 Thành phố/điểm đến: Đà Nẵng, Phú Quốc, hay Hồ Chí Minh?
2. 📅 Bao nhiêu đêm?
3. 💰 Ngân sách tối đa mỗi đêm là bao nhiêu?

Chia sẻ thêm để mình tìm ngay cho bạn nhé!
```

**Kết quả:** ✅ PASS – Agent không gọi tool, hỏi lại đúng 3 thông tin cần thiết.

---

## Test 5 – Guardrail / Refusal

**Input:**
```
Giải giúp tôi bài tập lập trình Python về linked list
```

**Console log:**
```
TravelBuddy đang suy nghĩ...
  → Trả lời trực tiếp (không gọi tool)
```

**Output:**
```
TravelBuddy: Xin lỗi bạn, mình là TravelBuddy – trợ lý chuyên về du lịch nên không
thể hỗ trợ bài tập lập trình được nhé. 😊

Nếu bạn đang lên kế hoạch cho một chuyến đi nào đó – tìm vé máy bay, khách sạn,
hay tính toán ngân sách – mình luôn sẵn sàng giúp! Bạn có muốn đi đâu không?
```

**Kết quả:** ✅ PASS – Agent từ chối lịch sự và gợi ý quay lại chủ đề du lịch.
